import sqlite3

import pytest
from oncall_agent.models import Settings
from oncall_agent.retrieval import Runbooks, Topology
from sqlglot.errors import ParseError


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM orders",
        "SELECT * FROM orders; DELETE FROM orders",
        "PRAGMA table_info(orders)",
        "SELECT * FROM services",
        "SELECT * FROM sqlite_master",
        "SELECT load_extension('/tmp/unsafe')",
        "WITH x AS (SELECT * FROM services) SELECT * FROM x",
    ],
)
def test_sql_rejects_writes_and_private_tables(runtime, sql):
    with pytest.raises((ValueError, sqlite3.DatabaseError, ParseError)):
        runtime.tools.query(sql)
    assert len(runtime.tools.query("SELECT * FROM orders")) == 3


def test_readonly_sql_counts_orders(runtime):
    rows = runtime.tools.query(
        "SELECT status, COUNT(*) AS count FROM orders GROUP BY status"
    )
    assert {row["status"]: row["count"] for row in rows} == {
        "failed": 2,
        "paid": 1,
    }


def test_hybrid_retrieval_and_dense_fallback(monkeypatch):
    runbooks = Runbooks(Settings())
    result = runbooks.search("order-db-proxy DB_POOL_TIMEOUT pool exhausted")
    assert result["method"] == "offline-lsa+bm25+rrf"
    assert result["hits"][0]["source"] == "db-pool.md"
    runbooks.settings.mode = "live"

    def unavailable(query):
        raise ConnectionError("offline")

    monkeypatch.setattr(runbooks, "_ollama_chroma", unavailable)
    fallback = runbooks.search("DB_POOL_TIMEOUT")
    assert fallback["method"] == "bm25-fallback"
    assert fallback["hits"][0]["source"] == "db-pool.md"


def test_local_topology_fallback():
    result = Topology(Settings()).lookup("order-db-proxy")
    assert result["source"] == "local-topology-fallback"
    assert {"source": "order-api", "target": "order-db-proxy"} in result[
        "edges"
    ]


def test_all_agent_tools_have_validated_arguments(runtime):
    from pydantic import BaseModel

    definitions = runtime.tools.definitions()
    assert len(definitions) == 5
    assert all(issubclass(tool.args_schema, BaseModel) for tool in definitions)
    assert not any("restart" in tool.name for tool in definitions)


def test_real_stdio_mcp_round_trip(runtime):
    runtime.tools.use_mcp = True
    assert runtime.tools.metrics("order-db-proxy")["state"] == "degraded"
    assert runtime.tools.logs("order-db-proxy")
    assert runtime.tools.query("SELECT COUNT(*) AS count FROM orders") == [
        {"count": 3}
    ]
