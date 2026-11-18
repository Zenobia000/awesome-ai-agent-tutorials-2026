"""值班助理的假工具：讀日誌、查指標、查 runbook、重啟服務。

情境：虛構公司「晨光外送」2026-11-18 14:00 起下單大量 502。
所有資料都在 data/ 底下，重啟只是改一個記憶體裡的旗標，不會碰到真的系統。

02 本 notebook 會一步一步寫出這些函式；後面幾本直接 import：

    from oncall_tools import read_logs, query_metrics, restart_service
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

DATA = Path(__file__).parent / "data"
SERVICES = ["web-gateway", "order-api", "order-db-proxy", "payment-api", "notification"]
Service = Literal["web-gateway", "order-api", "order-db-proxy", "payment-api", "notification"]

# 重啟 order-db-proxy 之後，哪些服務會跟著恢復（上游依賴鏈）
_RECOVERS_WITH = {"order-db-proxy": ["order-db-proxy", "order-api", "web-gateway"]}
_restarted: list[str] = []  # 模擬環境的狀態：被重啟過的服務


# ---------- 參數模型：每個工具的輸入都先過 Pydantic ----------
class ReadLogsArgs(BaseModel):
    service: Service | None = Field(None, description="只看這個服務；不填就看全部")
    level: Literal["INFO", "WARN", "ERROR"] | None = Field(None, description="只看這個等級")
    keyword: str | None = Field(None, description="日誌內容要包含的字")
    limit: int = Field(8, ge=1, le=30, description="最多回傳幾行（取最新的）")


class QueryMetricsArgs(BaseModel):
    service: Service = Field(..., description="服務名稱")
    metric: Literal["error_rate", "p95_latency_ms", "pool_used"] = Field(
        "error_rate", description="error_rate（%）、p95_latency_ms、pool_used（連線池已用數，只有 order-db-proxy 有）"
    )


class RestartArgs(BaseModel):
    service: Service = Field(..., description="要重啟的服務")


# ---------- 工具本體 ----------
def read_logs(service: str | None = None, level: str | None = None,
              keyword: str | None = None, limit: int = 8) -> str:
    """讀應用程式日誌，可依服務、等級、關鍵字過濾，回傳最新的幾行。"""
    rows = (DATA / "app.log").read_text(encoding="utf-8").splitlines()
    hits = [r for r in rows
            if (service is None or f" {service} " in r)
            and (level is None or f" {level} " in r)
            and (keyword is None or keyword.lower() in r.lower())]
    if not hits:
        return "（沒有符合的日誌）"
    return f"共 {len(hits)} 行符合，最新 {min(limit, len(hits))} 行：\n" + "\n".join(hits[-limit:])


def query_metrics(service: str, metric: str = "error_rate") -> str:
    """查某個服務的監控指標，回傳最近 6 個時間點與目前值。"""
    data = json.loads((DATA / "metrics.json").read_text(encoding="utf-8"))
    series = data["services"].get(service, {}).get(metric)
    if series is None:
        return f"查無指標：{service} 沒有 {metric}"
    times = list(data["times"])
    values = list(series)
    if any(service in _RECOVERS_WITH.get(s, [s]) for s in _restarted):
        times.append("14:30")
        values.append({"error_rate": 0.3, "p95_latency_ms": 130, "pool_used": 19}[metric])
    recent = ", ".join(f"{t}={v}" for t, v in zip(times[-6:], values[-6:]))
    cap = "（上限 50）" if metric == "pool_used" else ""
    return f"{service} {metric} 最近：{recent}；目前 {values[-1]}{cap}"


def restart_service(service: str) -> str:
    """重啟一個服務（寫入動作！真實環境要先經過審批）。"""
    _restarted.append(service)
    return f"已重啟 {service}（第 {_restarted.count(service)} 次）"


def calculator(expression: str) -> str:
    """計算簡單的四則運算，例如 '27.9 / 0.3'。"""
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return f"只接受數字與 + - * / ( )：{expression!r}"
    return str(round(eval(expression), 4))  # 已用白名單限制字元


def reset_env() -> None:
    """把模擬環境恢復成「還沒重啟過」的樣子。"""
    _restarted.clear()


def restarted() -> list[str]:
    return list(_restarted)
