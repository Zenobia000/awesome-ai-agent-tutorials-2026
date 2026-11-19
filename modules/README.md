# 實作教材總覽（modules/）

投影片講概念，這裡讓你動手做。每個模組先讀一份 `00_concepts.md`（原理紀要），再依序跑 notebook。

## 教學原則

1. **原理寫在文件，notebook 用工具做事。** 學 Python 是學工具整合，不是從底層重造輪子。每個模組的 `00_concepts.md` 用白話和圖講清楚「為什麼需要、核心原理、關鍵名詞、常見坑」。
2. **用套件時「點一下」原理。** 印出套件內部的中間結果（tokenizer 切出的 token、retriever 的分數、agent 的 messages 清單），讓原理看得見，而不是自己重寫一遍。
3. **一個例外：自己寫一個 ReAct agent。** 模組 5 前兩本手寫 agent 迴圈，這是理解所有 agent 框架的基本功；之後才換 LangGraph、deepagents、OpenAI／Claude Agent SDK、CrewAI。
4. **一本 notebook 只講一件事。** 20～40 個 cell，跑完不超過 15 分鐘，每一步都印出結果。
5. **先看它壞掉。** 先跑出錯的版本（沒有檢索的幻覺、沒有審批的寫入），再修。
6. **本地優先、免費優先。** 預設走 Ollama；雲端 API 只是 `.env` 換一行。
7. **不教維運花招。** 不碰 Kubernetes、Triton、vLLM 叢集、DeepSpeed、分散式訓練；服務部署另見 `infra/`。

## 每本 notebook 的固定骨架

```
# Lab X-Y：標題
目標／你會學到／前置條件／對應投影片（用投影片標題）
## Step 1 …（先一段白話說明，再一個 code cell，再印結果）
## Step N …
## 試試看（2～3 題小改動）
## 小結（三句話：做了什麼、為什麼、下一本接什麼）
```

## 環境

```bash
uv sync --group m1          # 每個模組一個依賴群組：m1 … m8
cp .env.example .env        # 預設連本機 Ollama，不需要任何金鑰
ollama pull qwen2.5:3b && ollama pull bge-m3
uv run jupyter lab
```

整門課一次裝好用 `uv sync --all-groups`（含 torch 約 6GB）。幾本 notebook 跨群組：M4-04、M5-03 會用到 m3 的 Chroma 與 BM25。

Ollama 安裝與設定見 [infra/services/ollama.md](../infra/services/ollama.md)；沒有 GPU 可租雲端算力，見 [infra/cloud-gpu.md](../infra/cloud-gpu.md)。其他服務（Chroma、Neo4j、Langfuse、Opik）見 [infra/README.md](../infra/README.md)。

各模組共用的程式只有 `course_utils/`（模型客戶端與小工具），模組之間不互相 import。

## 模組與 notebook

每個模組先讀 `00_concepts.md`（原理紀要），再依序跑 notebook。標「選讀」的可跳過。

| 模組 | 內容 |
|---|---|
| **M1 LLM 底層與本地環境** | 00 原理：LLM 在算什麼、Hugging Face 生態系、API 計費 · 01 token 怎麼切 · 02 Hugging Face：Hub、transformers、datasets · 03 看 logits、調溫度與 top-p · 04 OpenAI SDK 對話、記不住對話、串流 · 05 Lab 1 雙軌客戶端 · 06 多模態：圖片、語音、生圖 · 07 換供應商：Ollama／OpenRouter／DeepSeek／Anthropic · 08 LiteLLM 統一介面與 API 費用計算 |
| **M2 提示詞與結構化輸出** | 00 原理 · 01 好 prompt 與壞 prompt · 02 CoT 與 chaining · 03 結構化輸出（Pydantic） · 04 prompt injection 攻防 · 05 Lab 2 Text2SQL · 06 用標註資料評估 prompt |
| **M3 RAG** | 00 原理（含 PDF 解析、MinerU、多模態 RAG、RAG-Anything 導讀） · 01 embedding · 02 第一個 RAG（Chroma） · 03 分塊策略 · 04 BM25＋向量＋RRF · 05 重排序與查詢改寫 · 06 Lab 3 評估 · 07 LlamaIndex · 08 PDF 解析（選讀） |
| **M4 GraphRAG** | 00 原理 · 01 LLM 抽三元組 · 02 networkx 多跳查詢 · 03 Neo4j 與 Cypher · 04 圖檢索 vs 向量檢索 |
| **M5 Agent** | 00 原理：agent、狀態圖、harness · 01 **手寫 ReAct** · 02 **手寫 function calling 迴圈** · 03 RAG 當工具 · 04 Lab 5-A 狀態與 checkpoint（LangGraph） · 05 Lab 5-B 人工審批 · 06 Lab 5-C harness（deepagents） · 07 OpenAI Agents SDK · 08 Claude Agent SDK · 09 CrewAI：多 agent 何時值得 · 10 框架地圖 |
| **M6 LoRA** | 00 原理 · 01 PEFT 微調 Qwen2.5-0.5B · 02 合併權重、匯出給 Ollama · 03 什麼時候不該微調（選讀） |
| **M7 MCP** | 00 原理：MCP 是什麼 · 01 官方 SDK client 接本地模型 · 02 Lab 7 Excel 分析 agent · 03 掛到 Claude Code／Cursor、安全邊界 |
| **M8 評估與求職** | 00 原理：評估、trace、可觀測性 · 01 LLM 當評審 · 02 回歸評估 · 03 Langfuse · 04 Opik · 05 履歷與模擬面試 |

取材：2025 教材 iSpan_2026_LLM-NLP-cookbooks（prompt-engineering 系列）、iSpan_LLM-One-Piece（notebook 骨架、LoRA lab）、multimodal-RAG-course（混合檢索、PDF 解析、MinerU）改寫；其餘為本次補齊。

## 2026 主流框架對照

| 框架／服務 | 在哪裡教 | 需要金鑰？ |
|---|---|---|
| Ollama | M1-04、05、07（之後全課預設） | 否 |
| OpenAI API（文字、圖片、語音） | M1-06 | 是（沒有就跳過） |
| OpenRouter、Anthropic Messages API | M1-07 | 是（沒有就跳過） |
| Hugging Face（Hub、transformers、datasets） | M1-02、03，M6 | 否 |
| LiteLLM（統一介面、費用計算） | M1-08 | 否（雲端部分要金鑰） |
| Chroma | M3-02 起 | 否 |
| LlamaIndex | M3-04、07 | 否 |
| MinerU（PDF 版面解析） | M3-00、08 導讀 | — |
| RAG-Anything | M3-00 導讀 | — |
| LangGraph | M5-04、05 | 否 |
| deepagents | M5-06 | 否 |
| OpenAI Agents SDK | M5-07 | 否（接 Ollama） |
| Claude Agent SDK | M5-08 | 是（沒有就跳過） |
| CrewAI | M5-09 | 否（接 Ollama） |
| MCP Python SDK | M7 | 否 |
| Langfuse、Opik | M8-03、04 | 否（沒有金鑰就只在本機記錄，不上傳） |

## 刻意不收的 2025 內容

| 內容 | 原因 |
|---|---|
| Triton、vLLM 生產部署、Kubernetes、CI/CD（One-Piece 02） | 維運技術，不是理解 agent 的必要條件 |
| DeepSpeed、DDP、FlashAttention、MQA/GQA 實作（One-Piece 01） | 訓練基礎建設，本課只微調小模型 |
| 八種 PEFT 方法逐一實作（One-Piece PEFT_Labs） | 只留 LoRA；其他放選型表 |
| olmocr GPU 管線、MinerU 批次部署、Qdrant 叢集（multimodal-RAG 03～05） | MinerU 只介紹用法與輸出，不在課堂上部署 |
| Assistants API、Swarm（cookbooks 720、960） | 官方已淘汰 |
| CrewAI manager 模式、依角色硬拆 | 只在 M5-09 當對照組實測，主線教「平行獨立任務＋審查者」這種值得拆的情況 |
| Streamlit、Gradio 介面 | 介面不是重點，notebook 直接印輸出 |
| Pinecone、多家向量庫比較 | Chroma 一家講清楚即可，其他放選型表 |
