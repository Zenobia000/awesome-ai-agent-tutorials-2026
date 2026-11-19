"""可選整合測試：真正的模型、MCP、Dense 檢索與 PostgreSQL。"""

import os
import secrets

import pytest
from oncall_agent.models import Decision, IncidentRequest, Settings
from oncall_agent.runtime import Runtime


@pytest.mark.skipif(
    os.getenv("ONCALL_TEST_LIVE") != "1"
    or not os.getenv("ONCALL_TEST_POSTGRES"),
    reason="需 Ollama 模型及隔離 PostgreSQL；設定 ONCALL_TEST_LIVE=1",
)
def test_real_model_mcp_and_persistent_approval(tmp_path):
    settings = Settings(
        mode="live",
        checkpoint="postgres",
        data_dir=str(tmp_path),
        api_token=secrets.token_hex(24),
        database_url=os.environ["ONCALL_TEST_POSTGRES"],
    )
    first = Runtime(settings)
    try:
        state = first.start(IncidentRequest())
        assert state["status"] == "awaiting_approval"
        assert (
            state["evidence"]["runbooks"]["method"] == "ollama-chroma+bm25+rrf"
        )
        assert first.operations.status("order-db-proxy")["restart_count"] == 0
    finally:
        first.close()
    second = Runtime(settings)
    try:
        restored = second.snapshot(state["incident_id"])
        assert restored["pending"]
        result = second.decide(
            state["incident_id"],
            Decision(
                action_id=state["incident_id"],
                approved=True,
                reviewer="live-test",
            ),
        )
        assert result["status"] == "verified"
    finally:
        second.close()
