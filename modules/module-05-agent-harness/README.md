# 模組 5：Agent、狀態圖與 Harness

先自己寫一個 agent 迴圈，看懂它只是「模型＋迴圈＋工具」；再用 LangGraph 把迴圈變成可以存檔、可以暫停等人核准的狀態圖；
最後用 deepagents 組一個完整的 harness，並把同一個任務交給 OpenAI Agents SDK、Claude Agent SDK、CrewAI 比一比。

全模組同一個情境：虛構公司「晨光外送」14:00 起下單一直 502。值班 agent 查日誌、查指標、查 runbook，必要時要求重啟服務（寫入動作）。
所有資料都是本地假資料，重啟只改記憶體裡的旗標。

**先讀 [`00_concepts.md`](00_concepts.md)**：原理（ReAct、function calling、狀態圖、HITL、harness、何時拆多 agent、框架選型）都在那份文件裡。

| notebook | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md` | 原理紀要：從 f(x) 到迴圈、狀態圖、審批流程、harness 組成、多 agent 何時值得、框架選型 | 閱讀 |
| `01_react_from_scratch.ipynb` | 只靠 prompt 手寫 ReAct：工具註冊表、`stop`、解析失敗回饋、`max_steps`、完整 trace | Ollama |
| `02_function_calling_loop.ipynb` | 手寫 function calling 迴圈：Pydantic 產生 schema、印出每輪 messages、token 時間軸、workflow 對照 | Ollama |
| `03_rag_as_tool.ipynb` | Chroma＋BM25（RRF）包成 `search_runbooks` 工具，看 agent 何時會查、何時漏查 | Ollama（`bge-m3`） |
| `04_state_checkpoint.ipynb` | Lab 5-A：LangGraph `StateGraph`、reducer、`InMemorySaver`、thread_id、時光旅行、`recursion_limit` | Ollama |
| `05_human_approval.ipynb` | Lab 5-B：固定圖「提議 → 規範檢查 → 審批（`interrupt`）→ 執行 → 驗證」，核准／拒絕／規範擋下三條路 | Ollama |
| `06_harness.ipynb` | Lab 5-C：`create_deep_agent`（skills、AGENTS.md、log-checker 子 agent、`interrupt_on`），為 3B 瘦身並看內部 trace | Ollama |
| `07_openai_agents_sdk.ipynb` | OpenAI Agents SDK 接 Ollama（Responses API）：`function_tool`、agents-as-tools、guardrail、`needs_approval` | Ollama 0.13.3 以上 |
| `08_claude_agent_sdk.ipynb` | Claude Agent SDK：SDK MCP 工具、`can_use_tool`、`PreToolUse` hook、子 agent、skills | 實際呼叫需 `ANTHROPIC_API_KEY`；沒有也能跑完 |
| `09_crewai_multiagent.ipynb` | CrewAI 實測：單一 agent vs 依角色硬拆 vs 平行查證＋審查，比 token、時間、結果 | Ollama；**相容環境 `.venv-compat`**（見下方） |
| `10_framework_map.ipynb` | 六種寫法的核心行數、控制權、適用情境對照與地圖 | 不需模型 |

## 準備

```bash
uv sync --group m5
cp .env.example .env
ollama pull qwen2.5:3b && ollama pull bge-m3
uv run jupyter lab modules/module-05-agent-harness
```

**09 要在相容環境跑**：CrewAI 最新版仍要求 `openai<3`，跟本模組其他 notebook 用的 `openai` 3.x 不能裝在同一個環境，
所以放在獨立的 `compat` 群組與 `.venv-compat` 虛擬環境（在 repo 根目錄執行；不要對主環境 `.venv` 跑 `uv sync --group compat`，會把 m5 的套件換掉）：

```bash
UV_PROJECT_ENVIRONMENT=.venv-compat uv sync --group compat
UV_PROJECT_ENVIRONMENT=.venv-compat uv run --no-sync jupyter lab modules/module-05-agent-harness
```

notebook 要從本資料夾開啟：它們用相對路徑讀 `data/`、`oncall/`，並 import 同資料夾的 `oncall_tools.py`（假工具）與 `agent_loop.py`（02 的迴圈整理版）。

## 資料夾

| 路徑 | 內容 |
|---|---|
| `data/app.log` | 五個服務 13:40～14:15 的假日誌（47 行） |
| `data/metrics.json` | 每 5 分鐘一筆的假指標：error_rate、p95_latency_ms、pool_used |
| `data/runbooks/` | 五份短手冊：502、連線池用盡、付款重試、重啟規範、部署凍結 |
| `oncall/` | 06、08 用的 agent 家目錄：`AGENTS.md` 與兩個 skill（`ops-runbook`、`incident-report`） |
| `oncall_tools.py` | 讀日誌、查指標、重啟（模擬）、計算機，參數都是 Pydantic 模型 |
| `agent_loop.py` | 02 手寫迴圈的可重用版，03、05 使用 |

`workspace/`、`workspace_claude/` 是 06、08 執行時複製出來的工作目錄，已列入 `.gitignore`。

## 注意事項

- **小模型會錯，而且錯得很有自信。** `qwen2.5:3b` 會跳步、自己心算、沒查手冊卻說「根據手冊」、說已重啟其實沒呼叫工具。notebook 保留這些輸出當教材，也示範對應的修法（`stop`、拆小任務、固定流程、審查者）。每次執行結果可能不同。
- **Ollama 的 context 是 4096。** deepagents 預設的 prompt 超過這個長度，06 示範怎麼量、怎麼瘦身；換成雲端大模型就不需要瘦身。
- **08 需要 Claude Code CLI 與 `ANTHROPIC_API_KEY` 才會真的呼叫模型**；沒有金鑰時只跳過最後一格，其餘（工具、權限、hook 的單元測試）照常執行。
- 07 會關掉 Agents SDK 的 tracing（預設上傳到 OpenAI）；09 會關掉 CrewAI 的遙測與 tracing。
- notebook 裡保留了一次執行結果，方便先讀再跑。

## 驗證環境

主環境（01～08、10）：openai 3.55.1、langchain 1.5.2、langchain-core 1.8.3、langchain-openai 1.8.3、langgraph 1.2.22、deepagents 0.7.40、openai-agents 0.25.0、claude-agent-sdk 0.2.185、chromadb 1.5.9、rank-bm25 0.2.2、pydantic 2.14.3。
相容環境 `.venv-compat`（09）：crewai 1.15.42、openai 2.54.0、litellm 1.105.7。Ollama 0.40.16（`qwen2.5:3b`、`bge-m3`）。驗證日期 2026-11-19。
