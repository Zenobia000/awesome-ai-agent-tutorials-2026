"""Lab 7 的維運查詢 MCP Server：虛構公司「星港物流」的服務狀態與日誌。

只提供唯讀工具，資料是寫死在檔案裡的假資料。啟動方式（通常由 Host 代勞）：

    uv run python modules/module-07-mcp/servers/ops_server.py

注意：stdio Server 的 stdout 是協定專用管線，這個檔案裡不能有 print()。
要留除錯訊息就用 logging（預設寫到 stderr）。
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import Field

logging.basicConfig(level=logging.INFO, format="[ops-server] %(message)s")
log = logging.getLogger(__name__)

Service = Literal["payment", "order", "inventory"]
Level = Literal["ERROR", "WARN", "INFO"]

# ---- 假資料：三個服務的狀態與最近日誌 ----
STATUS: dict[str, dict] = {
    "payment": {"state": "degraded", "p95_ms": 2310, "error_rate": 0.084, "version": "v3.2.1"},
    "order": {"state": "healthy", "p95_ms": 180, "error_rate": 0.002, "version": "v5.0.4"},
    "inventory": {"state": "healthy", "p95_ms": 95, "error_rate": 0.0, "version": "v2.7.0"},
}

LOGS: list[dict] = [
    {"time": "09:58:12", "service": "payment", "level": "INFO", "msg": "部署 v3.2.1 完成"},
    {"time": "10:02:40", "service": "payment", "level": "WARN", "msg": "資料庫連線池使用率 92%"},
    {"time": "10:03:05", "service": "payment", "level": "ERROR", "msg": "連線池耗盡：等待連線逾時 2000ms"},
    {"time": "10:03:41", "service": "payment", "level": "ERROR", "msg": "呼叫銀行閘道逾時，訂單 A-1182 付款失敗"},
    {"time": "10:04:10", "service": "order", "level": "WARN", "msg": "付款回應過慢，訂單 A-1182 進入重試佇列"},
    {"time": "10:05:22", "service": "payment", "level": "ERROR", "msg": "連線池耗盡：等待連線逾時 2000ms"},
    {"time": "10:06:00", "service": "inventory", "level": "INFO", "msg": "每小時庫存同步完成，共 1,204 筆"},
    {"time": "10:07:15", "service": "order", "level": "INFO", "msg": "重試佇列清空"},
]

RUNBOOK = """# 星港物流值班手冊（節錄）
- payment 的 p95 超過 1000ms 或錯誤率超過 5%：視為降級，先查 ERROR 日誌。
- 「連線池耗盡」通常跟最近一次部署有關：比對部署時間。
- 任何重啟、回滾都要先經過值班主管核准，不能由 agent 直接執行。
"""

mcp = MCPServer("ops", version="1.0.0", instructions="星港物流的唯讀維運查詢：服務狀態、日誌、值班手冊。")
logging.getLogger("mcp").setLevel(logging.WARNING)  # 關掉 SDK 每個請求一行的訊息
READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


@mcp.tool(annotations=READ_ONLY)
def get_service_status(service: Service) -> str:
    """查詢一個服務目前的狀態：state、p95 延遲（毫秒）、錯誤率、版本。"""
    log.info("get_service_status(%s)", service)
    return json.dumps({"service": service, **STATUS[service]}, ensure_ascii=False)


@mcp.tool(annotations=READ_ONLY)
def search_logs(
    service: Service,
    level: Level | None = None,
    limit: Annotated[int, Field(ge=1, le=20, description="最多回傳幾筆，上限 20")] = 5,
) -> str:
    """查詢某個服務最近的日誌，可依等級（ERROR、WARN、INFO）篩選，新的在前。"""
    log.info("search_logs(%s, %s, %s)", service, level, limit)
    rows = [r for r in LOGS if r["service"] == service and (level is None or r["level"] == level)]
    rows = sorted(rows, key=lambda r: r["time"], reverse=True)[:limit]
    return json.dumps(rows, ensure_ascii=False) if rows else "沒有符合條件的日誌"


@mcp.tool(annotations=READ_ONLY)
def list_services() -> str:
    """列出可以查詢的服務名稱。"""
    return ", ".join(STATUS)


@mcp.resource("ops://runbook", name="runbook", description="值班手冊節錄", mime_type="text/markdown")
def runbook() -> str:
    return RUNBOOK


if __name__ == "__main__":
    mcp.run(transport="stdio")
