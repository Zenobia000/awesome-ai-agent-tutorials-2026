# 模組 7：MCP——把工具寫一次，接到任何 Host

原理（N×M、三角色、JSON-RPC、兩種傳輸）寫在 `00_concepts.md`；notebook 直接用官方 SDK 寫 server、當 client，接上本地模型；
再做 Lab 7 的 Excel 分析 agent，最後把同一支 server 掛到 Claude Code、Cursor、Cherry Studio，守住唯讀與審批的邊界。

| notebook／檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md`（先讀） | 原理紀要：N×M 轉接問題、Host／Client／Server、Tools／Resources／Prompts、JSON-RPC 訊息長相、stdio 與 streamable-http、stdout 不能亂 print | — |
| `01_mcp_client.ipynb` | 官方 SDK 的 `Client` 連 `ops_server.py`：list_tools、call_tool、讀 Resource；MCP 工具轉 OpenAI 格式，接上 tool calling 迴圈 | Ollama `qwen2.5:3b` |
| `02_excel_agent.ipynb` | Lab 7：Excel 分析 agent。先看小模型亂猜工作表名稱，再用 Resource 放資料地圖修好；四個中文分析題、自動畫圖、對標準答案 | Ollama `qwen2.5:3b` |
| `03_mcp_in_practice.ipynb` | 各家 Host 的設定檔（只產生、不執行）；重現「設定好了卻連不上」；白名單、唯讀、寫入前審批三道關卡 | 純 Python |
| `servers/ops_server.py` | 虛構公司「星港物流」的唯讀維運 server：3 個工具＋值班手冊 Resource | `mcp` |
| `servers/excel_server.py` | Lab 7 的唯讀 Excel server：`list_sheets`、`describe`、`query`、`make_chart`＋`excel://schema` Resource | `mcp`、`pandas`、`openpyxl` |
| `data/sales.xlsx` | 虛構「青山家電」2025 年銷售資料（訂單、產品、業務目標三張表），由 `02` 的 `make_sales()` 產生 | — |

## 準備

```bash
uv sync --group m7
cp .env.example .env
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-07-mcp
```

notebook 從本資料夾開啟（server 路徑、`data/`、`outputs/` 都是相對路徑）。
server 單獨啟動：`uv run python modules/module-07-mcp/servers/excel_server.py`（會停在那裡等 stdin，這是正常的）。

## 注意事項

- 本模組用 `mcp` 2.x（協定版本 2026-07-28），notebook、server 與投影片「Lab7 Server 程式」寫法一致：server 端 `from mcp.server import MCPServer`，client 端 `from mcp import Client, StdioServerParameters`。
  從 1.x 搬過來的程式要改：`FastMCP` → `MCPServer`；`host`／`port` 從建構子移到 `run()`；`ClientSession`＋`initialize()` → `async with Client(...)`；
  結果欄位 camelCase → snake_case（`inputSchema` → `input_schema`、`isError` → `is_error`、`mimeType` → `mime_type`、`readOnlyHint` → `read_only_hint`）；
  想讓模型讀到的錯誤要 `raise ToolError(...)`，其他例外只會回 `Error executing tool <name>`。詳見官方 migration guide：https://py.sdk.modelcontextprotocol.io/migration/
- stdio server 裡不能有 `print()`：stdout 是協定通道。除錯訊息一律用 `logging`（寫 stderr）。
- `outputs/`（圖表、server 日誌）是執行時產生的，已列入 `.gitignore`。
- 刪掉 `data/sales.xlsx` 再跑 `02`，會用固定亂數種子重新產生同樣的檔案。

## 驗證環境

mcp 2.3.0、openai 3.55.1、pandas 3.1.1、openpyxl 3.1.5、matplotlib 3.11.2、pydantic 2.14.3；Ollama `qwen2.5:3b`。驗證日期 2026-11-19。

## 已存的輸出

notebook 裡保留了一次執行結果。`qwen2.5:3b` 的回答每次可能不同：沒給資料地圖時常會猜一個不存在的工作表名稱（例如「銷售數據」）；
有時把繁體字寫成簡體（「扫地機器人」），讓 `02` 的字串比對判錯——這兩件事都是刻意留下的教學點。
