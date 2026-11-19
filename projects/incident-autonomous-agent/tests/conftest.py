"""只在隔離目錄執行模擬操作，絕不觸碰實際服務。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from oncall_agent.models import Settings  # noqa: E402
from oncall_agent.runtime import Runtime  # noqa: E402


@pytest.fixture
def runtime(tmp_path):
    instance = Runtime(Settings(data_dir=str(tmp_path)))
    yield instance
    instance.close()
