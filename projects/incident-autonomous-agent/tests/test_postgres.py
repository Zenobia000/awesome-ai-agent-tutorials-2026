"""設定 ONCALL_TEST_POSTGRES 才會執行實際跨連線恢復測試。"""

import os

import pytest
from oncall_agent.models import Decision, IncidentRequest, Settings
from oncall_agent.runtime import Runtime


@pytest.mark.skipif(
    not os.getenv("ONCALL_TEST_POSTGRES"),
    reason="需要隔離 PostgreSQL 測試資料庫",
)
def test_postgres_survives_closed_runtime(tmp_path):
    settings = Settings(
        data_dir=str(tmp_path),
        checkpoint="postgres",
        database_url=os.environ["ONCALL_TEST_POSTGRES"],
    )
    first = Runtime(settings)
    state = first.start(IncidentRequest())
    first.close()
    second = Runtime(settings)
    try:
        restored = second.snapshot(state["incident_id"])
        assert restored["status"] == "awaiting_approval"
        assert restored["pending"]
        result = second.decide(
            state["incident_id"],
            Decision(
                action_id=state["incident_id"],
                approved=True,
                reviewer="pg-test",
            ),
        )
        assert result["status"] == "verified"
    finally:
        second.close()
