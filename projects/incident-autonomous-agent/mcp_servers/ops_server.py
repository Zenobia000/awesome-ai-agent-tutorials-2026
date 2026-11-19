"""專案的唯讀 MCP server；stdout 僅供協定使用。"""

import os

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from oncall_agent.models import LogArgs, ServiceArgs, SQLArgs
from oncall_agent.storage import Operations

server = MCPServer("oncall-readonly", version="1.0.0")
operations = Operations(os.environ["ONCALL_DATA_DIR"])
READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


@server.tool(annotations=READ_ONLY)
def get_metrics(args: ServiceArgs) -> dict:
    """讀取教學服務狀態與指標。"""
    return operations.status(args.service)


@server.tool(annotations=READ_ONLY)
def search_logs(args: LogArgs) -> list[dict]:
    """讀取指定服務的教學日誌。"""
    return operations.logs(args.service, args.limit)


@server.tool(annotations=READ_ONLY)
def query_orders(args: SQLArgs) -> list[dict]:
    """唯讀查詢 orders 資料表，限制單一 SELECT。"""
    return operations.query(args.sql)


if __name__ == "__main__":
    server.run(transport="stdio")
