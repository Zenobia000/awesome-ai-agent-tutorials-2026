# 事實核實總表（2026-11-12）

彙整自各模組素材地圖的「事實核實」節；出處網址見各 `M*-*.md`。投影片上出現的版本號、API 名稱都要能對到這裡。

## 必須改寫的課綱內容

| 模組 | 課綱寫法 | 實際狀況 | 投影片怎麼寫 |
|---|---|---|---|
| 1 | GPT-4o 當商業 API 代表 | `gpt-4o-2024-05-13` 已於 2026-10-23 關閉；其餘 4o 版本與 4o-mini 2027-01-14 關閉 | 換成現行商業模型，不寫死型號 |
| 1 | DeepSeek-R1-Distill 8B | Ollama `deepseek-r1:8b` 現在是 R1-0528-Qwen3-8B；原 Distill-Llama 要拉 `8b-llama-distill-q4_K_M` | 寫明拉哪個 tag |
| 1 | Qwen2.5-3B/7B | 仍可拉但兩年未更新；Ollama 已有 `qwen3.5`（0.8b–122b） | 改用 Qwen3.5 小尺寸 |
| 1 | DeepSeek 雲端 API | 定價頁列 `deepseek-flash`（V4.1）、`deepseek-v4-pro`；舊名 `deepseek-chat` 是否可用未查到 | Lab1 用新名字，開課前再驗一次 |
| 1 | 「生產任務 Temperature 必須置 0」「溫度高會幻覺」 | R1 distill 官方建議 0.5–0.7、設 0 易重複；temperature 只管隨機性，不管對錯 | 改成「看模型官方建議值」＋「溫度≠正確性」 |
| 1 | （未提） | Ollama 預設 `num_ctx` 4096，超過會被截斷 | 和「為什麼記不住對話」放同一頁演示 |
| 2 | 結構化輸出「百分之百穩定」 | 拒答或被 max tokens 截斷時仍可能不符 schema | 加但書 |
| 2 | LangChain OutputParser 正則清理 | OpenAI、Anthropic（`output_config.format`）、Ollama 都有原生 structured outputs | 主推原生，正則清理當舊做法一句帶過 |
| 2 | XML 標籤硬隔離＝防禦 | OWASP、Simon Willison：分隔符號擋不住 prompt injection | 改成「降低風險的一層」，搭配權限最小化 |
| 2 | R1 用「角色設定」system prompt | R1 distill 官方建議不用 system prompt | 角色設定頁註明例外 |
| 5 | LangChain 1.0＝LangGraph 為唯一執行中樞 | 1.0 於 2025-10-22 發布，現為 1.5.0；主角是 `langchain.agents.create_agent`＋middleware（跑在 LangGraph 上） | 加講 `create_agent` 與 middleware |
| 5 | AgentExecutor | 已移到 `langchain-classic` | 只在面試頁帶一句 |
| 5 | `recursion_limit` 強制終止 | langgraph ≥1.1.4 預設 10,007（舊版 25），預設擋不住死循環 | 要求明確設小值＋呼叫次數上限 middleware |
| 5 | `Command approve` | 正確是 `Command(resume=...)`；HITL middleware 用 `Command(resume={"decisions": [...]})` | Lab5-B 照正確寫法 |
| 5 | Supervisor 用 `langgraph-supervisor` | 套件已封存，官方推「子 agent 包成工具」 | Lab5-C 用工具包裝法，不裝該套件 |
| 5 | DeepAgent | 正式名 Deep Agents，套件 `deepagents` 0.7.x；`write_todos` 從 v0.7 起要手動開 | 改名 |
| 5 | 「智能體動物園」 | 非 Anthropic 原文用語 | 標「本課轉述」 |
| 6 | LoRA「不到 1% 參數達到全量微調效果」 | 參數量對；效果只在中小資料集、且 LoRA 加在所有層時相當；程式碼與繼續預訓練明顯落後 | 加條件 |
| 6 | Chat template 不符導致「無法收斂」 | 實際症狀多半是 loss 正常下降，但推理不停、重複、角色錯亂 | 改寫症狀 |
| 6 | 混入 15% 通用資料 | 找不到權威出處 | 標「經驗值」 |
| 6 | QLoRA 合併 | 必須合併到原精度基座，不能合到 4-bit | Lab6 補匯出合併步驟 |
| 6 | Qwen3-VL | 沒錯但非最新；Qwen3.5 原生可看圖，LLaMA-Factory v0.9.5 支援 | 可並列 |
| 7 | 傳輸 STDIO＋SSE | 現為 stdio＋Streamable HTTP；HTTP+SSE 2025-03-26 起被取代，2026-07-28 版正式棄用 | 改寫 |
| 7 | （未提） | spec 最新 2026-07-28：無狀態、拿掉 initialize 握手與 session、新增 `server/discover`；Sampling／Roots／Logging 棄用 | 只教現行版本 |
| 7 | 「Anthropic 推出的 MCP」 | 起源 Anthropic，2025-12-09 捐給 Linux Foundation 旗下 Agentic AI Foundation | 兩件事都講 |
| 7 | Resources＝靜態資料 | 唯讀、由應用程式決定何時取用，可用模板動態產生、可訂閱 | 改定義 |
| 7 | FastMCP | 官方 SDK 教學改用 `from mcp.server import MCPServer`；獨立 `fastmcp`（Prefect 維護）4.x | Lab 用官方 SDK 寫法 |
| 7 | Lab7 用 Dify 接本地 MCP | Dify 只接 HTTP 傳輸；在 Docker 裡 `localhost` 指容器自己；n8n MCP Trigger 也不支援 stdio | Lab7 改走 Streamable HTTP＋`host.docker.internal` |
| 7 | 踩坑 | stdio server 往 stdout `print()` 會破壞訊息 | 補進踩坑頁 |
| 8 | LangChain Chat-UI | 正式名 Agent Chat UI，repo 於 2026-11-03 封存 | 旗艦專案前端要另選或註明 |
| 8 | WorkBuddy 是研發工具 | 騰訊雲的 AI 辦公工作台，不是寫程式工具 | 換成 Cursor／Claude Code 等 |
| 8 | 「2026 年興起的 Vibe Coding」 | Karpathy 2025-02 提出 | 改年份 |
| 8 | LangSmith「Prompt 在線微調」 | 是 Playground 調 prompt，不是調模型 | 改用詞 |
| 8 | AI 產業三層架構 | 課綱自整理框架，非權威 | 標「本課整理」 |
| 8 | 履歷數字 68%→91%、−35%、−42% | 課綱範本，非實測 | 頁面標「範本數字」 |

## 核實相符

- Ollama OpenAI 相容端點 `http://localhost:11434/v1`（api_key 填任意值；不支援 `tool_choice`）
- `nomic-embed-text` v1.5，274MB
- OpenAI Moderation API：`omni-moderation-latest`，免費，文字＋圖片
- OWASP LLM Top 10 最新為 2025 版
- `qwen3:14b` 存在（9.3GB）
- LLaMA-Factory 預設 `lora_rank` 8、alpha 一般為 rank×2；支援 Qwen3／Qwen3-VL
- Cherry Studio、Dify、n8n 都支援 MCP

## 模組三、四

| 模組 | 課綱寫法 | 實際狀況 | 投影片怎麼寫 |
|---|---|---|---|
| 3 | `BAAI/bge-reranker` | 不是實際模型名；跨語種要用 `BAAI/bge-reranker-v2-m3`（base／large 只支援中英） | 寫完整名稱 |
| 3 | 兩路召回「集合去重」 | 去重不是融合 | 改教 RRF |
| 3 | ChromaDB 混合檢索 | 內建 BM25＋RRF 只在 Chroma Cloud；本地 Lab 的 BM25 要另做再自己融合 | Lab3 自己實作 RRF |
| 3 | ParentDocumentRetriever、EnsembleRetriever | 已移到 `langchain_classic`，官方教學頁下線 | 講概念（parent-child），實作不綁舊元件 |
| 3 | Agentic chunking＝語義段落邊界由模型判斷 | 混了兩件事：semantic chunking 用 embedding 距離、不用 LLM；agentic chunking 才用 LLM，且沒有標準 API | 拆成兩頁 |
| 3 | SemanticChunker | 在 `langchain-experimental`，已公告停止維護 | 改用 LlamaIndex `SemanticSplitterNodeParser` |
| 3 | `MarkdownHeaderTextSplitter` | 正確；`strip_headers` 預設 True | 踩坑頁提醒 |
| 4 | Local Search＝1-hop／2-hop 拓撲展開 | Microsoft GraphRAG 是用實體描述 embedding 找入口再收集上下文，不跑 Cypher、不用 Neo4j；Lab4 屬 Neo4j 系做法 | 分清兩派 |
| 4 | 只列 Global／Local | 官方有 Global、Local、DRIFT、Basic 四種 | 補齊 |
| 4 | （未提） | GraphRAG v3.3.0（2026-10-08），README 寫已大致進入維護模式 | 註明 |
| 4 | `LLMGraphTransformer` | import 要從 `langchain_neo4j` | Lab4 照新路徑 |
| 4 | Cypher | Neo4j 2026.02 起新資料庫預設 Cypher 25，LLM 生成的舊語法可能出錯 | 踩坑頁補 |
| 4 | RDF 關係不能掛屬性 | 是 RDF 1.1 限制，1.2 草案在補 | 改精確 |

核實相符：bge-m3、text-embedding-3。
