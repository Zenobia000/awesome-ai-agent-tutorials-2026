# 實作教材總覽（modules/）

投影片講概念，這裡讓你親手做一遍。每個模組是一組依序執行的 notebook，
從零寫出最小可用版本，再換成業界套件；看得懂每一行，才換下一層抽象。

## 教學原則（Karpathy 式）

1. **先手寫，再用套件。** RAG 先用 numpy 算 cosine，再換 Chroma；Agent 先寫 while 迴圈，再換 LangGraph。
2. **一本 notebook 只講一件事。** 20～40 個 cell，跑完不超過 15 分鐘。
3. **小資料、看得到輸出。** 每一步都印出中間結果（token、向量、分數、訊息清單），不藏在函式裡。
4. **先看它壞掉。** 先跑出錯的版本（例如沒有檢索的幻覺、沒有審批的寫入），再修。
5. **本地優先、免費優先。** 預設走 Ollama；雲端 API 只是 `.env` 換一行。
6. **不教維運花招。** 不碰 Kubernetes、Triton、vLLM 叢集、DeepSpeed、分散式訓練、監控大盤。

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

各模組共用的程式只有 `course_utils/`（模型客戶端與小工具），模組之間不互相 import。

## 模組與 notebook 規劃

圖例：🟢 取材自 2025 教材後改寫　🆕 本次補齊的缺口　📄 用 `.py`（伺服器或長時間訓練不適合 notebook）

| 模組 | notebook | 來源 |
|---|---|---|
| **M1 LLM 底層與本地環境** | 01 token 與 BPE 手寫 | 🆕 |
| | 02 下一個 token：看 logits、自己寫生成迴圈 | 🆕 |
| | 03 attention 手寫（numpy） | 🆕 |
| | 04 直接打 Chat API：messages、溫度、記不住對話、串流 | 🟢 cookbooks 101 |
| | 05 Lab 1 雙軌客戶端：本地 Ollama 失敗自動切雲端 | 🆕 |
| **M2 提示詞與結構化輸出** | 01 好 prompt 與壞 prompt 對照 | 🟢 102 |
| | 02 CoT 與 prompt chaining | 🟢 201、207 |
| | 03 結構化輸出：JSON mode → Pydantic schema → 驗證失敗重試 | 🟢 103、706 |
| | 04 prompt injection 攻防 | 🟢 202 |
| | 05 Lab 2 Text2SQL：SQLite、唯讀、Pydantic 驗證 | 🆕 |
| | 06 用準確率評估 prompt | 🟢 206 |
| **M3 RAG** | 01 embedding 與相似度、分群 | 🟢 601 |
| | 02 RAG 手寫：numpy cosine，不用向量庫 | 🟢 602 |
| | 03 分塊策略與 contextual chunking | 🟢 602 ＋ 🆕 |
| | 04 換成向量資料庫（Chroma） | 🟢 604 |
| | 05 BM25 ＋ 向量的混合檢索與 RRF 手寫 | 🆕（概念取自 multimodal-RAG 04） |
| | 06 重排序與查詢改寫：cross-encoder、HyDE、small-to-big | 🟢 605、607 |
| | 07 Lab 3 評估：Hit@k、MRR，前後對比 | 🟢 610 ＋ 🆕 |
| | 08 PDF 解析為什麼會壞（選讀） | 🟢 612、multimodal-RAG 03 |
| **M4 GraphRAG** | 01 用 LLM 抽三元組（海賊王自寫語料） | 🆕 |
| | 02 networkx 手寫圖檢索與多跳查詢 | 🆕 |
| | 03 換成 Neo4j 與 Cypher | 🆕 |
| | 04 圖檢索 vs 向量檢索：同一題比一比 | 🆕 |
| **M5 Agent** | 01 ReAct 手寫：只靠 prompt 的 agent | 🟢 711 |
| | 02 function calling 迴圈：模型＋迴圈＝agent | 🟢 702、703 |
| | 03 把 RAG 包成工具 | 🟢 705 |
| | 04 Lab 5-A 狀態與 checkpoint（LangGraph） | 🆕 |
| | 05 Lab 5-B 寫入前的人工審批（interrupt） | 🆕（概念取自 970 confirmation） |
| | 06 Lab 5-C harness：skills、subagent 當工具、檔案記憶 | 🆕（概念取自 970 agents-as-tools） |
| **M6 LoRA** | 01 LoRA 手寫：20 行 PyTorch 包住一個 Linear | 🆕 |
| | 02 用 PEFT 微調小模型（Qwen2.5-0.5B，16GB 顯卡可跑） | 🟢 One-Piece PEFT Lab-01、HF 03-PEFT |
| | 03 推論、合併權重、匯出給 Ollama | 🟢 One-Piece Lab-01 04 |
| **M7 MCP** | 01 MCP server 📄 ＋ client notebook | 🆕 |
| | 02 Lab 7 Excel 分析 agent | 🆕 |
| **M8 評估與求職** | 01 LLM-as-a-judge 手寫 | 🟢 206 ＋ 🆕 |
| | 02 回歸評估集：改 prompt 前後跑同一份題目 | 🆕 |
| | 03 最小 trace：每一步寫一行 JSONL | 🆕 |

## 刻意不收的 2025 內容

| 內容 | 原因 |
|---|---|
| Triton、vLLM 生產部署、Kubernetes、CI/CD（One-Piece 02） | 維運技術，不是理解 agent 的必要條件 |
| DeepSpeed、DDP、FlashAttention、MQA/GQA 實作（One-Piece 01） | 訓練基礎建設，本課只微調小模型 |
| 八種 PEFT 方法逐一實作（One-Piece PEFT_Labs） | 只留 LoRA；其他放選型表 |
| MinerU、olmocr GPU 管線、Qdrant 叢集（multimodal-RAG 03～05） | 只留「PDF 解析為什麼會壞」的概念 |
| Assistants API、Swarm（cookbooks 720、960） | 官方已淘汰 |
| CrewAI 角色分工、manager 模式 | 依角色切 agent 是本課明列的反模式 |
| Streamlit、Gradio 介面 | 介面不是重點，notebook 直接印輸出 |
| Pinecone、多家向量庫比較 | Chroma 一家講清楚即可，其他放選型表 |
