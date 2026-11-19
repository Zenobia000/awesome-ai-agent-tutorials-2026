"""所有 Agent 工具都有 Pydantic schema，且不提供服務寫入能力。"""

import asyncio
import json
import os
import sys

from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .models import LogArgs, SearchArgs, ServiceArgs, SQLArgs
from .retrieval import ROOT


class ReadTools:
    def __init__(self, operations, runbooks, topology, use_mcp=False):
        self.operations = operations
        self.runbooks = runbooks
        self.topology = topology
        self.use_mcp = use_mcp

    async def _mcp(self, name, args):
        environment = {
            **os.environ,
            "ONCALL_DATA_DIR": str(self.operations.path.parent),
            "PYTHONPATH": str(ROOT),
        }
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "mcp_servers/ops_server.py")],
            env=environment,
        )
        async with stdio_client(parameters) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                result = await asyncio.wait_for(
                    session.call_tool(name, {"args": args}), timeout=20
                )
                if result.is_error:
                    raise RuntimeError("MCP 唯讀工具呼叫失敗")
                if result.structured_content is not None:
                    return result.structured_content.get(
                        "result", result.structured_content
                    )
                return json.loads(
                    "".join(
                        item.text
                        for item in result.content
                        if item.type == "text"
                    )
                )

    def metrics(self, service):
        args = ServiceArgs(service=service)
        if self.use_mcp:
            return asyncio.run(self._mcp("get_metrics", args.model_dump()))
        return self.operations.status(args.service)

    def logs(self, service, limit=10):
        args = LogArgs(service=service, limit=limit)
        if self.use_mcp:
            return asyncio.run(self._mcp("search_logs", args.model_dump()))
        return self.operations.logs(args.service, args.limit)

    def query(self, sql):
        args = SQLArgs(sql=sql)
        if self.use_mcp:
            return asyncio.run(self._mcp("query_orders", args.model_dump()))
        return self.operations.query(args.sql)

    def definitions(self):
        return [
            StructuredTool.from_function(
                self.metrics,
                name="get_metrics",
                description="讀取服務健康狀態與指標。",
                args_schema=ServiceArgs,
            ),
            StructuredTool.from_function(
                self.logs,
                name="search_logs",
                description="讀取服務日誌，檢查故障證據。",
                args_schema=LogArgs,
            ),
            StructuredTool.from_function(
                self.query,
                name="query_orders",
                description="唯讀查詢 orders(id,status,service)，上限100筆。",
                args_schema=SQLArgs,
            ),
            StructuredTool.from_function(
                self.runbooks.search,
                name="search_runbooks",
                description="Dense+BM25+RRF 混合檢索操作手冊。",
                args_schema=SearchArgs,
            ),
            StructuredTool.from_function(
                self.topology.lookup,
                name="service_topology",
                description="查詢 Neo4j 服務依賴，失敗時使用本地拓撲。",
                args_schema=ServiceArgs,
            ),
        ]
