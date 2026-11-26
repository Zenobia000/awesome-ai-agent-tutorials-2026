# 台灣 AI Agent 極速實戰課｜20 小時，打造你的 AI Agent

![20 小時打造你的 AI Agent：台灣 AI Agent 極速實戰課，8 個模組、47 本 Notebook、繁體中文、開源免費](assets/marketing/agent-course-hero.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-ef542d.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776ab.svg)](pyproject.toml)
[![47 Notebooks](https://img.shields.io/badge/Notebooks-47-ef542d.svg)](modules/README.md)
[![繁體中文](https://img.shields.io/badge/教材-繁體中文-242424.svg)](modules/)

**這次，把 AI Agent 做出來。**

為台灣開發者打造的 **20 小時 AI Agent 工程實戰路線**。從 LLM 原理、RAG 到工具呼叫、人工審批與效果評估，把散落的知識接成一條能動手完成的學習路線。

**8 個模組 · 47 本實作 Notebook · 220 頁完整投影片 · 開源免費**

[**立即開始實作 →**](#快速開始)　[**先看 60 頁精華 →**](docs/slides/lite/deck.pdf)　[**看完整課綱 →**](curriculum-ai-agent-20h.md)

> 20 小時為課綱的講授與實作安排；環境安裝、模型下載、完整跑完 47 本 notebook 與延伸練習另計。模組教材可分別學習；[旗艦值班助理](projects/incident-autonomous-agent/)另提供可執行的整合示範。

## 把你的 Python，升級成 Agent 工程力

**給想快速做出第一個 Agent 的你，也給準備轉職、導入企業應用、開設內訓的你。** 先備能力是基本 Python；LLM 與深度學習觀念由教材補上。

- **原理、程式、結果，一次接起來。** 每個模組有原理紀要，47 本 notebook 都保留執行輸出，打開就能讀到實際結果。
- **雲端優先，本機兜底。** 填了雲端金鑰，文字對話與主要 Agent 練習就走雲端模型；沒填或斷線自動退回 Ollama，不需先購買 API 額度也能全程跑完。
- **從會回答，練到會做事。** 查文件、查資料庫、呼叫 MCP 工具，再加入狀態保存與人工審批。
- **用數字，說明你做了什麼。** 用檢索指標、回歸評估與執行追蹤檢查結果，累積可展示、可解釋的作品素材。
- **學習、改編、企業內訓都開放。** 本倉庫採 MIT 授權；外部模型、資料與服務另依各自授權及條款。

## 快速開始

先安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/) 與 [Ollama](https://ollama.com/download)，並啟動 Ollama。以下指令使用 macOS／Linux／WSL 的 Bash；Windows PowerShell 請以 `Copy-Item .env.example .env` 複製設定檔。

```bash
git clone https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026.git
cd awesome-ai-agent-tutorials-2026

# 安裝 M1 依賴，沿用倉庫鎖定版本
uv sync --locked --group m1

# 首次設定時複製；已有 .env 請保留原設定
cp -n .env.example .env

# 下載本機對話模型；Ollama 需保持啟動
ollama pull qwen2.5:3b

# 保留剛安裝的模組環境，開啟 JupyterLab
uv run --no-sync jupyter lab modules/module-01-llm-local
```

開啟 [M1-04：第一次模型對話](modules/module-01-llm-local/04_chat_api.ipynb)，依序執行本機對話段落。**看到模型回覆與串流文字，就完成第一次本機 LLM 呼叫。** 需要雲端金鑰的段落可略過。想從原理開始，先讀 [M1 原理紀要](modules/module-01-llm-local/00_concepts.md)，再從 `01_tokens.ipynb` 依序學習。

接著進入 [M5：打造 Agent](modules/module-05-agent-harness/)，或按下方路線補齊基礎。進入需要 embedding 的練習前，再執行 `ollama pull bge-m3`。

<details>
<summary><strong>安裝、硬體與相容環境</strong></summary>

- Python 宣告支援 3.11+；實際驗證版本見各模組 README。首次安裝與模型下載需要網路及磁碟空間。
- 多數練習可使用 CPU；速度與可載入的模型取決於記憶體及硬體。M6 微調建議使用 GPU。
- 更換模組時，使用對應依賴群組 `m1`～`m8`；跨模組依賴與完整安裝方式見[教材環境說明](modules/README.md#環境)。
- CrewAI、Opik 使用獨立 `compat` 環境，對應 M5-09、M8-01、M8-04。請依[雙環境說明](modules/README.md#兩個環境主環境與相容環境)安裝。
- 本機執行不收 API 費；選填雲端 API、雲端算力與付費服務依供應商計費。金鑰請放 `.env`，設定項目見 [.env.example](.env.example)。

</details>

## 選一條路，現在出發

| 你的目標 | 建議路線 | 第一個成果 |
|---|---|---|
| **第一次接觸 LLM** | [60 頁精華](docs/slides/lite/deck.pdf) → [M1](modules/module-01-llm-local/) → [M2](modules/module-02-prompt-structured/) | 在自己電腦上對話，取得結構化輸出 |
| **直接做 Agent** | [M5](modules/module-05-agent-harness/) → [M7](modules/module-07-mcp/) → [M8](modules/module-08-eval-career/)；需要時回補 M2、M3 | 工具呼叫、審批流程與評估結果 |
| **打造知識助理** | [M3](modules/module-03-rag/) → [M4](modules/module-04-graphrag/) → [M5](modules/module-05-agent-harness/) | 混合檢索、圖查詢與檢索指標 |
| **準備轉職與面試** | 實作主線 → [M8-05 面試沙盤](modules/module-08-eval-career/05_interview_sandbox.ipynb) | 用自己的評估結果，整理作品與履歷敘述 |
| **講師／企業內訓** | [20 小時課綱](curriculum-ai-agent-20h.md)＋[完整投影片](docs/slides/deck/deck.pdf)＋[教材總覽](modules/README.md) | 可按對象選用、改編的教學路線 |

## 學完，拿得出這些工程成果

| 能力 | 你會動手產出的東西 |
|---|---|
| **LLM 與結構化輸出** | 本地／雲端模型客戶端、Pydantic 輸出驗證、Text2SQL 練習 |
| **RAG 與 GraphRAG** | Dense＋Sparse＋RRF 混合檢索、重排序、圖查詢，以及 Hit@k／MRR 比較 |
| **Agent 與狀態管理** | 手寫 ReAct／function calling 迴圈、LangGraph checkpoint 與人工審批 |
| **MCP 工具整合** | 本機 MCP server、Excel 分析工具與工具存取邊界 |
| **評估與可觀測性** | LLM 評審、回歸評估、Langfuse／Opik 追蹤練習 |
| **模型微調** | LoRA adapter、權重合併與 Ollama 匯出流程 |

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
| [**M7 MCP**](modules/module-07-mcp/) | 1.5h | MCP client、Excel 分析 agent、掛到 Claude Code／Cursor 與安全邊界 | MCP Python SDK |
| [**M8 評估與求職**](modules/module-08-eval-career/) | 1.5h | LLM 當評審、回歸評估、trace、履歷量化、模擬面試 | Langfuse、Opik |

完整 notebook 清單、取材來源與框架對照表見 [modules/README.md](modules/README.md)。


20 小時主線以[課綱](curriculum-ai-agent-20h.md)為準；框架比較、供應商範例與延伸練習可依需求選讀。各模組 README 列出 notebook 前置條件與已驗證環境。

## 教材直接拿走

| 教材 | 用法 |
|---|---|
| [**完整投影片 · 220 頁**](docs/slides/deck/deck.pdf) | 系統學習、授課、內訓 |
| [**精簡投影片 · 60 頁**](docs/slides/lite/deck.pdf) | 先建立 Agent 工程全貌 |
| [**實作教材 · 47 本 Notebook**](modules/README.md) | 讀輸出、跑程式、改參數、做練習 |
| [**20 小時課綱**](curriculum-ai-agent-20h.md) | 安排進度與課堂目標 |
| [**M1 原理入口**](modules/module-01-llm-local/00_concepts.md) | 每個模組都有一份 `00_concepts.md`：原理、圖解與常見坑 |

## 工程習慣，從第一個 Agent 開始練

- **先讀原理，再用工具。** Notebook 使用主流套件，印出中間結果，讓每一步都能解釋。
- **親手寫一次迴圈。** M5 的 ReAct 與 function calling 練習，幫你看懂框架替你處理的事。
- **把失敗留下來。** 小模型的幻覺、錯誤工具選擇與評審偏誤，都是觀察與改善的起點。
- **讓寫入經過審批。** 練習「審批 → 執行 → 驗證」、狀態保存與明確的迴圈上限；防護措施需配合權限及測試。
- **先掌握單一 Agent。** 再用實驗比較，何時值得加入 skills、subagent 與多 Agent 協作。

## 把整門課接起來：值班助理

[**打開旗艦專案 →**](projects/incident-autonomous-agent/)

查文件、查訂單、讀監控，再由你決定是否修復。值班助理提供 HTTP／SSE 操作頁面、混合檢索、MCP 工具與完整的「人工審批 → 執行 → 驗證」流程。

- **先跑免模型 Demo**：合成故障資料，能看到拒絕、核准及修復驗證的完整結果。
- **再接 Live 整合**：Ollama／Deep Agents、三個 skills、唯讀子 agent、MCP、Chroma 與 PostgreSQL checkpoint；Neo4j 可選。
- **用測試確認邊界**：涵蓋重複審批、過期審批、禁用服務與驗證失敗，附[固定情境評估報告](eval_benchmarks/results/incident-demo.json)。

服務操作限定教學模擬環境；可先在本機完成整合實作，再自行接入企業的受控系統。

## 常見問題

**20 小時能跑完全部 47 本嗎？** 20 小時是講授與實作課綱；完整教材包含延伸內容，下載、除錯及自主練習需另外安排時間。

**沒有 GPU、沒有雲端金鑰可以開始嗎？** 可以先做本機 CPU 練習，模型速度視硬體而定。主要文字與 Agent 路線使用 Ollama；雲端專屬段落選填，M6 微調建議 GPU。

**程式與結果可以直接放作品集嗎？** 可以改編教材，但請使用自己執行的結果，說明資料、模型、測試條件與限制；模型回答每次可能不同。

**如何確認套件版本？** [pyproject.toml](pyproject.toml) 定義依賴群組，[uv.lock](uv.lock) 記錄鎖定版本；各模組 README 提供驗證日期與環境。Notebook 已存輸出可先閱讀，實際重跑仍取決於本機環境及外部服務。

## 回報問題，一起把教材做好

遇到安裝或 notebook 問題，請到 [GitHub Issues](https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026/issues) 附上作業系統、Python 版本、模組與 notebook 名稱，以及移除金鑰後的錯誤訊息。歡迎透過 Pull Request 修正錯字、補充說明與可重現的相容性修正。

教材取材與改寫來源見[教材總覽](modules/README.md#模組與-notebook)。本倉庫採 [MIT License](LICENSE)，使用及散布時請保留授權要求的聲明；第三方素材另依原始授權。

**準備好了？[打開第一本對話實作 →](modules/module-01-llm-local/04_chat_api.ipynb)**

喜歡這條學習路線，歡迎 Star、分享給一起學 AI 的朋友，或直接拿去安排下一場內訓。

<details>
<summary>分享這門課</summary>

![這次，把 AI Agent 做出來。20 小時工程實戰，8 個模組、47 本 Notebook，繁體中文、開源免費](assets/marketing/agent-course-social.png)

[下載橫幅](assets/marketing/agent-course-hero.png) · [下載社群宣傳圖](assets/marketing/agent-course-social.png)

</details>
