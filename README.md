# AI Agent 工程實戰：20 小時，從 LLM 原理做到可上線的 Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Notebooks](https://img.shields.io/badge/notebooks-47%20本，全部實跑-2ea44f.svg)
![Slides](https://img.shields.io/badge/投影片-220%20頁-orange.svg)
![Verified](https://img.shields.io/badge/套件驗證-2026--11--19-blue.svg)

**一套免費、在自己電腦上就能跑完的 AI Agent 課程。** 220 頁投影片講觀念，47 本 notebook 動手做，8 份原理紀要補上「為什麼」。從「LLM 到底在算什麼」開始，一路做到一個會查資料、會等人審批、做完能拿數字證明效果的值班 agent。

- **給誰用**：想轉職 AI 工程師的軟體工程師、學過深度學習但沒做過 LLM 應用的學生、要在公司導入 agent 的團隊，以及想拿現成教材開課的講師。
- **它解決什麼**：網路上的教學不是停在「呼叫一次 API」，就是一開始就丟一個大框架。這門課先把原理講清楚，再用 2026 年主流工具實作，每一步都看得到中間結果。
- **有什麼不同**：
  - 預設全部走本機 Ollama，不用金鑰、不花錢。
  - 每本 notebook 都實際執行過並存了輸出，打開就能先讀再跑。
  - 套件全部驗證到 2026-11-19 的最新版。
  - 效果用實測數字說話，小模型答錯的地方也照實保留，當成教材。

---

## 從哪裡開始

| 你是… | 建議路線 | 大約時間 |
|---|---|---|
| **完全沒碰過 AI** | 先看[精簡版投影片](docs/slides/lite/deck.pdf)（60 頁）→ 讀 [M1 原理紀要](modules/module-01-llm-local/00_concepts.md) → 跑 M1-01～04 | 半天 |
| **學過深度學習，沒做過 LLM 應用** | [完整投影片](docs/slides/deck/deck.pdf)的 M1～M3 → M1、M2、M3 全部 notebook | 2～3 天 |
| **會寫 Python，想直接做 agent** | M5-01 自己寫 ReAct → M5-02～06（LangGraph、harness）→ M7 MCP → M8 評估 | 2 天 |
| **準備 AI 工程師面試** | 每個模組的投影片面試頁 → [M8-05 面試沙盤](modules/module-08-eval-career/05_interview_sandbox.ipynb)：把評估結果寫成履歷句，再讓模擬面試官打分 | 1 天 |
| **講師或企業內訓** | [課綱](curriculum-ai-agent-20h.md)（20 小時排程）＋完整投影片＋[教材總覽](modules/README.md) | 照課綱 |

---

## 課程資訊

| | |
|---|---|
| **時數** | 20 小時（講授＋實作），8 個模組 |
| **程度** | 入門到中階；M5、M8 接近實務 |
| **先修** | 會寫 Python。學過深度學習更好，投影片每章都有「你已經會的」對照框，沒學過也可以跳過 |
| **語言** | 繁體中文，程式碼註解也是 |
| **費用** | 免費。雲端 API 只用在少數選填段落，沒有金鑰會自動跳過；全部雲端範例跑一次只要幾美分 |
| **硬體** | 一般筆電可跑大部分內容；M6 微調建議有 GPU，沒有可租[雲端算力](infra/cloud-gpu.md) |
| **授權** | MIT，可自由學習、改編、商用 |

---

## 學完你會做什麼

1. 說明 LLM 為什麼會幻覺、為什麼記不住對話、為什麼 context 越長越貴，並用 token 數算出 API 費用。
2. 用 Pydantic 讓模型輸出程式能直接用的結構，並擋下 prompt injection 與危險的 SQL。
3. 建一條 RAG 管線：混合檢索、重排序，再用 Hit@k／MRR 證明它真的變好。
4. 自己寫一個 ReAct agent，再用 LangGraph、deepagents、OpenAI／Claude Agent SDK、CrewAI 做同一件事，知道各框架替你做了什麼。
5. 把公司內部工具包成 MCP server，讓模型能讀、不能亂改；寫入動作一律走「審批 → 執行 → 驗證」。
6. 用 LLM 評審、回歸測試、Langfuse／Opik 追蹤，讓每次修改都有數字可比。

---

## 課程地圖

每個模組先讀 `00_concepts.md`（原理紀要），再依序跑 notebook。

| 模組 | 時數 | 你會動手做 | 主要工具 |
|---|---|---|---|
| [**M1 LLM 底層與本地環境**](modules/module-01-llm-local/) | 2h | token 與費用、看 logits 調溫度、Chat 與 Responses API、多模態（圖片、語音）、換供應商、LiteLLM 與費用計算 | Ollama、Hugging Face、OpenAI SDK、OpenRouter、LiteLLM |
| [**M2 提示詞與結構化輸出**](modules/module-02-prompt-structured/) | 2h | 好壞 prompt 對照、CoT、結構化輸出、prompt injection 攻防、Text2SQL | Pydantic、SQLite |
| [**M3 RAG**](modules/module-03-rag/) | 4h | embedding、第一個 RAG、分塊、BM25＋向量＋RRF、重排序、評估、PDF 解析 | Chroma、LlamaIndex、sentence-transformers、PyMuPDF |
| [**M4 GraphRAG**](modules/module-04-graphrag/) | 2h | 用 LLM 抽三元組、多跳查詢、Cypher、圖 vs 向量實測 | networkx、Neo4j |
| [**M5 Agent**](modules/module-05-agent-harness/) | 5h | **自己寫 ReAct**、function calling 迴圈、狀態與 checkpoint、人工審批、harness、六種框架對照 | LangGraph、deepagents、OpenAI Agents SDK、Claude Agent SDK、CrewAI |
| [**M6 LoRA 微調**](modules/module-06-lora/) | 2h | 微調 0.5B 小模型、合併權重、匯出給 Ollama、什麼時候不該微調 | PEFT、transformers |
| [**M7 MCP**](modules/module-07-mcp/) | 1.5h | MCP client、Excel 分析 agent、掛到 Claude Code／Cursor 與安全邊界 | MCP Python SDK 2.x |
| [**M8 評估與求職**](modules/module-08-eval-career/) | 1.5h | LLM 當評審、回歸評估、trace、履歷量化、模擬面試 | Langfuse、Opik |

完整 notebook 清單、取材來源與框架對照表見 [modules/README.md](modules/README.md)。

---

## 教材形式

| 教材 | 用途 | 位置 |
|---|---|---|
| 完整投影片（220 頁） | 上課主教材，每章有白話入口、選型表、踩坑與面試題 | [docs/slides/deck/deck.pdf](docs/slides/deck/deck.pdf) |
| 精簡版投影片（60 頁） | 給沒學過 agent 設計的一般讀者 | [docs/slides/lite/deck.pdf](docs/slides/lite/deck.pdf) |
| 原理紀要（8 份） | 每個模組的「為什麼」：白話、圖解、名詞表、常見坑 | `modules/*/00_concepts.md` |
| Notebook（47 本） | 動手實作，已存執行結果，可以先讀再跑 | `modules/*/` |
| 課綱 | 20 小時排程、每堂目標、踩坑、面試題 | [curriculum-ai-agent-20h.md](curriculum-ai-agent-20h.md) |

---

## 快速開始

```bash
git clone https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026.git
cd awesome-ai-agent-tutorials-2026

uv sync --group m1                 # 每個模組一個依賴群組：m1 … m8
cp .env.example .env               # 預設連本機 Ollama，不需要金鑰
ollama pull qwen2.5:3b && ollama pull bge-m3
uv run jupyter lab modules/module-01-llm-local
```

- 還沒有 [uv](https://docs.astral.sh/uv/)：`pip install uv`。
- 還沒有 Ollama：見 [infra/services/ollama.md](infra/services/ollama.md)。
- CrewAI 與 Opik 的最新版還要求舊版 openai，所以裝在另一個環境，只有 M5-09、M8-01、M8-04 用得到。安裝方式見 [modules/README.md](modules/README.md#兩個環境主環境與相容環境)。

---

## 教學設計

- **先原理，後工具。** 原理寫在每個模組的 `00_concepts.md`；notebook 從第一格就用業界套件，並印出套件內部的中間結果，讓原理看得見。
- **只有一個地方手寫：自己寫 ReAct agent。** 這是看懂所有 agent 框架的基本功。
- **先看它壞掉，再修。** 沒有檢索時的幻覺、沒有審批的寫入、評審的偏誤，都先跑出來給你看。
- **單一 agent 優先。** 一個 agent 配 skills 與 MCP 工具；只有在平行、互相獨立的任務才拆多個 agent。M5-09 用實測說明為什麼依角色硬拆多個 agent 不划算。
- **不教維運花招。** 沒有 Kubernetes、Triton、vLLM 叢集；服務部署另見 [infra/](infra/README.md)。

---

## 旗艦專案：值班助理（建置中）

課程的各個模組最後會組成一個值班 agent：

- 帶三個 skill：查文件（M3）、查資料庫（M2 Text2SQL）、運維排錯。
- 透過 MCP 呼叫日誌與監控工具（M7）。
- 唯讀的調查交給 subagent 平行處理（M5）。
- 重啟、改設定一律走「審批 → 執行 → 驗證」，並用評估集證明效果（M8）。

各部分都已經在對應模組裡做出來了，整合版放在 `projects/incident-autonomous-agent/`，目前只有基礎服務設定，整合工作還在進行。

---

## 倉庫結構

```text
├── curriculum-ai-agent-20h.md   20 小時課綱
├── modules/                     8 個模組：00_concepts.md＋notebook，總覽見 modules/README.md
├── course_utils/                共用模型客戶端（M1-05 寫出來的成品）
├── docs/slides/deck/            完整投影片（HTML 原始檔與 deck.pdf）
├── docs/slides/lite/            精簡版投影片
├── infra/                       Ollama、Chroma、Neo4j 等服務的部署說明
├── projects/                    旗艦專案（建置中）
├── pyproject.toml               依賴群組 m1～m8、compat
└── AGENTS.md                    給 AI coding agent 的專案規則
```

---

## 常見問題

**沒有 GPU 可以上嗎？**
可以。除了 M6 微調，其他模組在一般筆電上都能跑，只是本地模型回答比較慢。

**沒有 OpenAI 或其他雲端金鑰呢？**
不影響。預設全部走本機 Ollama；需要雲端的段落會自動跳過，notebook 照樣跑完。

**小模型常答錯，是不是教材有問題？**
是刻意的。本課預設用 3B 的本地模型，答錯的地方保留下來，用來說明幻覺、評估與防護為什麼重要。換成更大的模型只要改 `.env` 一行。

**套件會不會很快過時？**
每個模組的 README 都寫了驗證時的套件版本與日期。框架改版時，先看這幾行就知道教材是在哪個版本上跑過的。

---

## 授權

[MIT License](LICENSE)。歡迎拿去上課、改編、做公司內訓。如果這套教材對你有幫助，給個 Star 讓更多人找到它。
