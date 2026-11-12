# 模組七 素材地圖

> 對象：學過深度學習（神經網路、softmax、反向傳播、embedding、遷移學習），沒學過 NLP／生成式 AI／Agent。
> 所有 URL 皆於 2026-11-12 以 WebFetch 實際開啟核實；打不開或要登入的已剔除（例：舊版 Cherry Studio 文件 `docs.cherry-ai.com` 連線被拒，改用新站）。

## 論點清單

1. **MCP 解決的是「N 個 AI 應用 × M 個工具」的整合爆炸，把 N×M 個客製接頭降成 N+M 個標準介面。**
2. **MCP 的角色分工是 Host → Client（一對一）→ Server；協定分成「資料層（JSON-RPC 訊息）」與「傳輸層（stdio／Streamable HTTP）」兩層。**
3. **Server 提供三種原語，差別在「誰決定何時用」：Tools＝模型決定、Resources＝應用程式決定、Prompts＝使用者決定。**
4. **傳輸方式：本機用 stdio（Host 啟動子行程），遠端用 Streamable HTTP；舊的 HTTP+SSE 已棄用。stdio 的頭號地雷是往 stdout 印東西。**
5. **生態已經成形：客戶端（Claude Desktop、Cherry Studio、VS Code、Cursor…）設定一次就能接任何 Server；用 FastMCP／官方 SDK 幾行 Python 就能寫出自己的 Server。**
6. **低代碼（Dify、n8n）和純代碼（LangGraph）不是二選一：前者適合固定流程、快速交付與大量第三方整合，後者適合有狀態、動態分支、需要精細控制的 Agent；兩者都能透過 MCP 互相接上。**

## 素材

### 論點 1：MCP 解決 N×M 整合爆炸

- **Hugging Face MCP Course — Unit 1: Key Concepts and Terminology** — Hugging Face — https://huggingface.co/learn/mcp-course/unit1/key-concepts（已核實 2026-11-12）
  - 適合程度：免費、免登入的入門課程，直接用「M×N 問題 → M+N 解法」開場，有「Without MCP / With MCP」對照圖，不需要任何 NLP 前置知識。
  - 可借的圖解結構：左右兩欄對照。左欄「Without MCP」：左側 3 個 AI 應用、右側 4 個工具，每對之間都拉一條線（12 條交錯線）；右欄「With MCP」：中間一條 MCP 匯流排，應用各拉 1 條、工具各拉 1 條（7 條線）。線數直接寫在圖下方。
  - 搭橋：類比深度學習框架的 ONNX——沒有交換格式時，每個訓練框架 × 每個推論引擎都要寫轉換器；有了中間格式就只要各自實作匯出／匯入。
- **Introducing the Model Context Protocol** — Anthropic（2024-11-25）— https://www.anthropic.com/news/model-context-protocol（已核實 2026-11-12）
  - 適合程度：一頁短文，講清楚動機：「每個新資料源都要自己的客製實作，連接系統難以擴展」。適合拿來當「歷史起點」那張投影片的引文。
  - 可借的圖解結構：本文無架構圖，適合做「引言卡」——一句原文引文 + 發布日期 + 「後來捐給 Linux Foundation」的時間軸（2024-11 發布 → 2025-12 捐給 AAIF → 2026-07 無狀態版 spec）。
  - 搭橋：無需搭橋，作為動機與時間脈絡。注意：原文沒有寫「N×M」字樣，N×M 是社群（如 HF 課程）的整理說法。
- **What is the Model Context Protocol (MCP)?** — modelcontextprotocol.io 官方 — https://modelcontextprotocol.io/docs/getting-started/intro（已核實 2026-11-12）
  - 適合程度：官方入門頁，用「AI 應用的 USB-C 接口」比喻，並列出支援的客戶端（Claude、ChatGPT、VS Code、Cursor）。
  - 可借的圖解結構：中間一個 USB-C 集線器（MCP），左邊接 AI 應用（Claude／ChatGPT／IDE），右邊接三類外部系統：資料源（檔案、資料庫）、工具（搜尋、計算機）、工作流（特化 prompt）。
  - 搭橋：USB-C 比喻夠直觀，不需額外搭橋。

### 論點 2：Host / Client / Server 與兩層架構

- **Architecture overview** — modelcontextprotocol.io 官方 — https://modelcontextprotocol.io/docs/learn/architecture（已核實 2026-11-12）
  - 適合程度：官方最權威、且已更新到 2026-07-28 版。用 VS Code 當例子：連一個 Server 就生一個 Client 物件；有完整 JSON-RPC 往返範例（discover → tools/list → tools/call → 通知）。
  - 可借的圖解結構：(a) 一個大框「MCP Host（AI 應用）」內含 Client 1～4，往外各拉一條「Dedicated connection」到 Server A（本機檔案系統）、B（本機資料庫）、C（遠端 Sentry；Client 3、4 都連到它）。(b) 同心圓：內圈「資料層：JSON-RPC、原語、能力探索」、外圈「傳輸層：stdio／Streamable HTTP、認證」。(c) 循序圖四步：`server/discover` → `tools/list` → `tools/call` → `notifications/tools/list_changed`。
  - 搭橋：資料層／傳輸層的分離，對應 PyTorch 的「模型定義」與「device（CPU/GPU）」分離——同一份計算圖可以搬到不同裝置，同一份 JSON-RPC 訊息可以走不同傳輸。
- **Hugging Face MCP Course — Unit 1: Architectural Components** — Hugging Face — https://huggingface.co/learn/mcp-course/unit1/architectural-components（已核實 2026-11-12）
  - 適合程度：把一次互動拆成 7 步（使用者輸入 → Host 判斷 → Client 連線 → 能力探索 → 呼叫 → Server 執行 → 結果回填 LLM 上下文），且明確提醒「很多文章把 Host 和 Client 混用，嚴格說不同」。
  - 可借的圖解結構：把 7 步畫成編號泳道圖，三條泳道：使用者／Host（含 LLM）／Client／Server，箭頭依序編號。
  - 搭橋：「結果回填 LLM 上下文」可接到學生熟悉的「輸入向量」——工具結果最後只是被串接進模型的下一次輸入序列，模型權重完全不變（對比模組六的微調是改權重）。

### 論點 3：Tools / Resources / Prompts——差在「誰決定用」

- **Understanding MCP servers** — modelcontextprotocol.io 官方 — https://modelcontextprotocol.io/docs/learn/server-concepts（已核實 2026-11-12）
  - 適合程度：官方表格直接給「Who controls it」欄：Tools＝Model、Resources＝Application、Prompts＝User；並用「規劃巴塞隆納旅行」一個情境串起三種原語與多個 Server。
  - 可借的圖解結構：3 欄卡片表（原語／例子／控制者 icon：🤖 模型、🖥 應用、👤 使用者），下方接一條流程：使用者選 Prompt「plan-vacation」→ 應用附上 Resources（行事曆、旅遊偏好）→ 模型呼叫 Tools（searchFlights、checkWeather、bookHotel 需確認）。
  - 搭橋：Tools 的 `inputSchema`（JSON Schema）就是函式簽名；模型「決定呼叫哪個工具」本質上是在候選工具上做一次分類（可類比 softmax over actions），但輸出是結構化文字而非 one-hot。
- **Hugging Face MCP Course — Unit 1: Capabilities** — Hugging Face — https://huggingface.co/learn/mcp-course/unit1/capabilities（已核實 2026-11-12）
  - 適合程度：有「控制者／副作用／是否需核准／典型用途」四維對照表，比官方多了「副作用」一欄，適合解釋為什麼 Tools 要使用者核准。
  - 可借的圖解結構：2×2 象限——橫軸「有無副作用」、縱軸「誰觸發」；Resources 落在「無副作用／應用觸發」、Tools 落在「有副作用／模型觸發」、Prompts 落在「無副作用／使用者觸發」。
  - 搭橋：無。**注意**：該頁仍把 Sampling 列為第四種能力，但 Sampling 在 2026-07-28 版 spec 已標為 Deprecated，引用時要刪掉或加註。

### 論點 4：傳輸方式——stdio 與 Streamable HTTP

- **Transports（Specification 2026-07-28）** — modelcontextprotocol.io 官方規格 — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports（已核實 2026-11-12）
  - 適合程度：規格文件偏硬，但「Overview」一段很短：標準傳輸只有兩種——stdio（子行程標準串流、換行分隔 JSON-RPC）與 Streamable HTTP（每則訊息一個 POST，回覆是 JSON 或請求範圍的 SSE 串流）。講師備課用，投影片只取結論。
  - 可借的圖解結構：左右對照。左「stdio」：Host 方框內 fork 出一個子行程，stdin→、←stdout 兩條管線，stderr 另一條通往 log 檔。右「Streamable HTTP」：Client → `POST /mcp` → 遠端 Server，回程箭頭分叉成「一次性 JSON」或「SSE 串流（進度通知）」。
  - 搭橋：stdio 類比 Python `subprocess.Popen` 的 stdin/stdout 管線；Streamable HTTP 類比呼叫一個推論 API（如 TorchServe／Triton 的 HTTP endpoint）。
- **Key Changes（2026-07-28 changelog）** — modelcontextprotocol.io 官方規格 — https://modelcontextprotocol.io/specification/2026-07-28/changelog（已核實 2026-11-12）
  - 適合程度：講師用。確認 HTTP+SSE 傳輸自 2025-03-26 起棄用、本版正式列入 Deprecated；並記錄本版移除 initialize 握手與 session（協定變成無狀態）。
  - 可借的圖解結構：版本時間軸：2024-11-05（HTTP+SSE）→ 2025-03-26（Streamable HTTP 取代 HTTP+SSE）→ 2025-11-25 → 2026-07-28（無狀態、移除 session、`server/discover`、Sampling/Roots/Logging 棄用）。
  - 搭橋：無。
- **Build an MCP server** — modelcontextprotocol.io 官方教學 — https://modelcontextprotocol.io/docs/develop/build-server（已核實 2026-11-12）
  - 適合程度：做一個天氣 Server（`get_alerts`、`get_forecast`）接到 Claude Desktop；頁首就用醒目框警告「STDIO Server 絕不能寫 stdout，`print()` 會破壞 JSON-RPC 訊息」——這正是課綱「進程權限與通訊阻塞」踩坑的另一半成因。
  - 可借的圖解結構：一條 stdout 管線裡混進一行 `print("Processing request")`，把前後兩個 JSON 物件「切壞」，Client 端解析失敗的紅叉。旁邊示範正解：`logging` 寫到 stderr。
  - 搭橋：類比訓練時把 debug 訊息寫進要被下游讀的 CSV 輸出檔——資料管線被污染。

### 論點 5：客戶端生態與 FastMCP

- **Connect to local MCP servers** — modelcontextprotocol.io 官方教學 — https://modelcontextprotocol.io/docs/develop/connect-local-servers（已核實 2026-11-12）
  - 適合程度：一步步截圖：Claude Desktop → Settings → Developer → Edit Config → 貼 `claude_desktop_config.json`，接上官方 Filesystem Server；含排錯清單（路徑要絕對路徑、看 `mcp-server-*.log`、Windows `APPDATA` 環境變數）。直接對應課綱踩坑表。
  - 可借的圖解結構：設定檔 JSON 拆解圖——`mcpServers` → `"filesystem"`（顯示名稱）→ `command: npx` → `args: [-y, 套件名, 允許的資料夾…]`，每個欄位拉註解箭頭；旁邊放「每次操作都要使用者核准」的對話框示意。
  - 搭橋：`command + args` 就是 Host 替你在終端機下的那行指令；類比用 `torchrun` 啟動訓練腳本時傳參數。
- **MCP（Cherry Studio 文件：Extending Agent Capabilities → MCP）** — Cherry Studio 官方文件 — https://cherryai.com/docs/en/advanced-basic/extensions/mcp/（已核實 2026-11-12）
  - 適合程度：課綱 Lab 7 的客戶端。說明 Settings → MCP → MCP Servers → Add（Quick Create／Import from JSON／DXT／MCPB），本機用 stdio、遠端用 SSE 或 Streamable HTTP URL；有內建 MCP 清單；MCP 要逐一綁定到 Agent 才生效。
  - 可借的圖解結構：三段式：「新增 Server（本機 command / 遠端 URL）」→「啟用並確認健康狀態、檢視其 tools/resources/prompts」→「綁到某個 Agent」。強調第三步常被漏掉。
  - 搭橋：無。
- **FastMCP — Welcome / Running Your Server** — Prefect（FastMCP 維護者）— https://gofastmcp.com/getting-started/welcome 、 https://gofastmcp.com/deployment/running-server（已核實 2026-11-12）
  - 適合程度：用 decorator `@mcp.tool` 把普通 Python 函式變成工具，5 行程式碼就能跑；`run()` 支援 STDIO（預設）、HTTP（Streamable）、SSE（標為 Legacy，「新專案不該用」）。
  - 可借的圖解結構：左邊一段 Python 函式（含 type hints + docstring），右邊自動生成的 tool 定義 JSON（`name`、`description`、`inputSchema`），中間箭頭標「FastMCP 自動轉換」——讓學生看到型別註記 → JSON Schema 的映射。
  - 搭橋：decorator 註冊機制類比 PyTorch 的 `nn.Module` 自動註冊參數，或 `@torch.no_grad()`；型別註記 → schema 類比 dataset 的欄位定義。

### 論點 6：低代碼（Dify、n8n）vs 純代碼（LangGraph）的邊界

- **Building effective agents** — Anthropic Engineering — https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
  - 適合程度：給出最清楚的分界定義：Workflow＝LLM 與工具走「預先定義的程式路徑」；Agent＝LLM 自行決定流程與工具使用。每種模式都有一張簡潔方塊圖，非常適合入門。
  - 可借的圖解結構：一條光譜，左端「Prompt chaining / Routing / Parallelization」（固定路徑，Dify／n8n 畫布擅長）→ 中間「Orchestrator-workers / Evaluator-optimizer」→ 右端「Autonomous agent（LLM ⇄ 工具環境迴圈）」（LangGraph 擅長）。在光譜上方標「可預測性」、下方標「彈性」。
  - 搭橋：固定路徑 workflow 類比固定計算圖（靜態圖）；Agent 類比動態計算圖（PyTorch eager 依輸入決定走哪個分支）。
- **Workflow & Chatflow** ＋ **MCP Server（發布）** ＋ **Dify Tools（MCP 分頁）** — Dify 官方文件 — https://docs.dify.ai/en/cloud/use-dify/build/workflow-chatflow.md 、 https://docs.dify.ai/en/cloud/use-dify/publish/publish-mcp.md 、 https://docs.dify.ai/en/cloud/use-dify/workspace/tools.md（已核實 2026-11-12）
  - 適合程度：Workflow（跑一次、可排程觸發）vs Chatflow（每則訊息觸發、必有 Answer 節點）一張表講完；並確認 Dify 雙向支援 MCP——可把外部 MCP Server 匯入成工具（僅支援 HTTP 傳輸，不支援 stdio），也可把 Dify App 一鍵發布成 MCP Server 給 Claude Desktop／Cursor 用。
  - 可借的圖解結構：雙向箭頭圖：左「外部 MCP Server（HTTP）」→ 匯入 → 中「Dify 工作流畫布（節點：User Input → LLM → Tool → Output）」→ 發布為 MCP Server → 右「Claude Desktop / Cursor」。
  - 搭橋：節點 = 一層運算、連線 = 張量流向，畫布就是一張可視化的計算圖。
- **MCP Server Trigger node** ＋ **MCP Client Tool node** — n8n 官方文件 — https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcptrigger/ 、 https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/（已核實 2026-11-12）
  - 適合程度：n8n 同樣雙向：MCP Client Tool 讓 n8n 的 AI Agent 節點呼叫外部 MCP 工具；MCP Server Trigger 把 n8n 工作流暴露成 MCP Server（支援 SSE 與 Streamable HTTP，不支援 stdio）。
  - 可借的圖解結構：沿用 Dify 那張雙向圖換成 n8n 節點，並加上 n8n 的強項——左側一排觸發器（排程、Webhook、Slack、Email），凸顯「n8n＝整合／排程優先，AI 只是其中一個節點」。
  - 搭橋：無。
- **Building AI Agents with LangGraph vs n8n: A Hands-On Comparison** — OrangeLoops（2025-06）— https://orangeloops.com/2025/06/building-ai-agents-with-langgraph-vs-n8n-a-hands-on-comparison/（已核實 2026-11-12）
  - 適合程度：同一個 HR 助理用兩種方式各做一次，比較開發速度、除錯、控制力，還有 47 題 LLM-as-judge 評分（LangGraph 7.99 vs n8n 7.74）。結論是兩者組合用。比純觀點文更有說服力。
  - 可借的圖解結構：雷達圖或對照表：原型速度／除錯可視性／狀態與記憶控制／動態分支／整合數量，兩條線交叉，強調「各有勝場」。
  - 搭橋：類比 Keras（高階、快）vs 自寫 PyTorch training loop（細控）——學生已有此直覺。
  - 備用：Jimmy Song《開源 AI Agent 平台比較》（有中文版，含 n8n／Dify／LangGraph／Coze／RAGFlow 定位與授權表）— https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/（已核實 2026-11-12；頁面已標 Archived，內容為 2025-08）。

## 事實核實

- **MCP 目前 spec 版本**：最新為 **2026-07-28**（`/specification/latest` 指向此版，schema 路徑 `schema/2026-07-28/schema.ts`）；前一版為 2025-11-25。本版重大變更：協定改為**無狀態**（移除 `initialize` 握手與 `Mcp-Session-Id`）、新增必實作的 `server/discover`、`subscriptions/listen` 取代 resources/subscribe、Tasks 移出核心成為擴充。出處：https://modelcontextprotocol.io/specification/latest 、https://modelcontextprotocol.io/specification/2026-07-28/changelog
- **傳輸方式（課綱寫 STDIO＋SSE）**：**與課綱不一致**。標準傳輸為 **stdio 與 Streamable HTTP**；舊的 HTTP+SSE 傳輸自 2025-03-26 起棄用，2026-07-28 正式列入 Deprecated 並要求遷移到 Streamable HTTP。SSE 仍以「Streamable HTTP 回應中的可選串流格式」形式存在，但已不是獨立傳輸。出處：https://modelcontextprotocol.io/specification/2026-07-28/basic/transports 、changelog（同上）
- **MCP 治理（課綱寫「Anthropic 推出」）**：起源正確（2024-11-25 Anthropic 發布），但**治理已變**：2025-12-09 Anthropic 將 MCP 捐給 Linux Foundation 旗下的 **Agentic AI Foundation（AAIF）**，與 Block 的 goose、OpenAI 的 AGENTS.md 同為創始專案；技術方向仍由既有 maintainers 經 SEP 流程決定，LF 不主導技術。出處：https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation 、https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
- **核心組件（課綱「三位一體」Resources/Prompts/Tools）**：Server 端三原語正確。但課綱 Resources 寫「提供靜態資料上下文」不精確——官方定義為「唯讀、由應用程式控制的資料來源」，可透過 Resource Templates 動態參數化（如 `weather://forecast/{city}/{date}`）且可訂閱變更，不是「靜態」。另外 Client 端原語目前只剩 Elicitation 為 Active；**Sampling、Roots、Logging 已於 2026-07-28 棄用**（很多二手教材仍列 Sampling）。出處：https://modelcontextprotocol.io/docs/learn/server-concepts 、https://modelcontextprotocol.io/docs/learn/architecture
- **Cherry Studio 是否支援 MCP**：支援。設定路徑 Settings → MCP → MCP Servers → Add；本機 stdio，遠端 SSE 或 Streamable HTTP；有內建 MCP 清單；需把 Server 綁到個別 Agent 才生效。舊文件網域 `docs.cherry-ai.com` 已連不上，新文件在 cherryai.com。出處：https://cherryai.com/docs/en/advanced-basic/extensions/mcp/ 、https://github.com/CherryHQ/cherry-studio
- **Claude Desktop**：仍是官方教學示範的 Host；本機 Server 透過 `claude_desktop_config.json` 設定，macOS／Windows／Linux 皆有版本。出處：https://modelcontextprotocol.io/docs/develop/connect-local-servers
- **FastMCP 現況**：由 **Prefect** 維護的獨立專案；FastMCP 1.0 的高階 API 於 2024 年併入官方 MCP Python SDK。PyPI 最新版 `fastmcp` **4.1.8**（2026-11-12 查詢；官方 README 提供 FastMCP 2、3 的升級指南）。官方 Python SDK `mcp` 已到 **2.3.0**，其教學程式碼改用 `from mcp.server import MCPServer`（不再是舊教材的 `from mcp.server.fastmcp import FastMCP`）。FastMCP 的 SSE 傳輸標為 Legacy。出處：https://gofastmcp.com/getting-started/welcome 、https://github.com/PrefectHQ/fastmcp 、https://pypi.org/pypi/fastmcp/json 、https://pypi.org/pypi/mcp/json 、https://modelcontextprotocol.io/docs/develop/build-server
- **Dify 是否支援 MCP**：支援雙向。作為 Client：Tools → MCP 分頁匯入外部 MCP Server，**僅支援 HTTP 傳輸**（不能直接接 stdio 的本機 Server）；作為 Server：App 的 Access Point → MCP Server 開關，產生帶憑證的 URL 給 Claude Desktop／Cursor。出處：https://docs.dify.ai/en/cloud/use-dify/workspace/tools.md 、https://docs.dify.ai/en/cloud/use-dify/publish/publish-mcp.md
- **n8n MCP 節點**：有兩個——**MCP Client Tool**（讓 AI Agent 節點呼叫外部 MCP Server；官方文件欄位仍寫「SSE Endpoint」）與 **MCP Server Trigger**（把 n8n 工作流暴露成 MCP Server，支援 SSE 與 Streamable HTTP，**不支援 stdio**）。n8n 另有 MCP registry 一鍵接入。出處：https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/ 、https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcptrigger/ 、https://docs.n8n.io/build/integrate-ai/mcp-servers.md
- **Lab 7 架構的隱含衝突**：課綱要「部署本地 Excel/Python MCP Server，在 Cherry Studio / Dify 中配置」。Cherry Studio 可直接用 stdio 接本地 Server；**Dify 只接 HTTP**，若用 Docker 部署的 Dify 要接本地 Server，Server 必須以 Streamable HTTP 啟動且讓 Dify 容器連得到（`localhost` 在容器內指的是容器自己）。出處：同上 Dify tools 頁。

## 投影片建議

1. **傳輸那頁改成「stdio＋Streamable HTTP」**，SSE 只用一個註腳交代「舊版 HTTP+SSE 已棄用、Streamable HTTP 內部仍可用 SSE 串流回應」。否則學生照舊教學寫 SSE Server，接 Dify／新版客戶端會踩坑。
2. **「Anthropic 推出」改成「Anthropic 2024 發起，2025-12 起由 Linux Foundation 旗下 AAIF 中立治理」**；面試題「為何被視為外掛整合標準」的答案也該補上「中立治理＋OpenAI、Google、Microsoft 都是 AAIF 成員」這個論據。
3. **三組件改用「誰決定用」（模型／應用／使用者）來講，而不是「靜態資料／模板／函式」**。對沒碰過 Agent 的學生，「控制權」這條軸線比功能描述更好記，也自然導出「Tools 要核准」的安全觀念；Resources 不要說「靜態」。
4. **加一張「MCP 不改權重」的對照**：模組六微調＝改模型參數；模組三 RAG 與模組七 MCP＝改模型的輸入上下文。這是從深度學習（參數 vs 輸入）搭過來最省力的一座橋，也把三個模組串成一條線。
5. **Lab 7 預先處理兩個環境坑**：(a) stdio Server 禁止 `print()` 到 stdout（課綱踩坑表只寫環境變數與路徑，漏了這個最常見的成因）；(b) Dify 不支援 stdio、Docker 內 `localhost` 不是宿主機——建議 Lab 先在 Cherry Studio 用 stdio 跑通，再把同一支 FastMCP Server 改 `transport="http"` 接 Dify，順便示範「同一份資料層、換傳輸層」。
