"""Neo4j 使用隔離資料庫；一般測試只驗證離線備援。"""

import json
import os

import pytest
from neo4j import GraphDatabase
from oncall_agent.models import Settings
from oncall_agent.retrieval import ROOT, Topology


@pytest.mark.skipif(
    not os.getenv("ONCALL_TEST_NEO4J_URI"), reason="需要隔離 Neo4j 測試資料庫"
)
def test_real_neo4j_dependencies():
    settings = Settings(
        neo4j_uri=os.environ["ONCALL_TEST_NEO4J_URI"],
        neo4j_password=os.environ["ONCALL_TEST_NEO4J_PASSWORD"],
    )
    with GraphDatabase.driver(
        settings.neo4j_uri, auth=("neo4j", settings.neo4j_password)
    ) as driver:
        driver.execute_query(
            "UNWIND $edges AS edge "
            "MERGE (a:Service {name:edge[0]}) "
            "MERGE (b:Service {name:edge[1]}) "
            "MERGE (a)-[:DEPENDS_ON]->(b)",
            edges=json.loads((ROOT / "data/topology.json").read_text()),
        )
    result = Topology(settings).lookup("order-db-proxy")
    assert result["source"] == "neo4j"
    assert {"source": "order-api", "target": "order-db-proxy"} in result[
        "edges"
    ]
