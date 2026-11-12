# 投影片製作 brief（每位製作者必讀）

## 這份 deck 是什麼
把 `curriculum-ai-agent-20h.md`（repo 根目錄）做成 1920×1080 的 HTML 投影片。

**讀者：懂深度學習（神經網路、softmax、反向傳播、embedding 層、遷移學習、CNN／RNN），但沒學過 NLP、生成式 AI、Agent。** 簡報要深入淺出。
**能畫成圖的一律畫成圖（資訊圖表優先），文字只是註解。**

## 內容依據（三個來源，優先序由高到低）
1. `../sources/product-facts.md`——課綱裡過時或錯誤的寫法已在這裡改正。**和課綱衝突時以它為準**，課綱原文不要照抄。
2. `../sources/M<N>-*.md`——每章的素材地圖：論點清單、可借的圖解結構、搭橋建議、投影片建議。動手前先讀自己那章。
3. 課綱原文對應的模組小節。

## 講法硬規則（針對這群學生）
1. **從已知搭橋**：每章至少 2 頁用 `.bridge`「你已經會的」把新概念接到深度學習概念（例：語言模型＝詞表上的 softmax 分類器；LoRA＝凍結 W、只學 ΔW＝B·A；RAG＝改輸入、微調＝改權重；Agent＝把 f(x) 放進迴圈）。
2. **術語第一次出現就定義**：一句白話＋一個具體例子。不假設學生懂 token、prompt、chunk、tool call、checkpoint。
3. **先看實物再講抽象**：講 prompt／tool calling／agent／MCP 前，先用 `.code` 放一則真實的 messages JSON、trace 或程式片段。
4. **一頁一個概念**；難的概念拆成「直覺 → 機制 → 工程後果」最多三頁。
5. **不講框架歷史包袱**：學生沒用過舊版 LangChain。舊 API（AgentExecutor 等）只在面試題頁帶一句。

## 已核准的視覺方向：幾何色塊（系列延續，不得更改）
- 參考頁（必看）：`slides/005-pillars.html`、`slides/309-hybrid-rrf.html`；系列母版是 EDA 課的同款 deck
- 紙色底 `#f3efe6`；墨色 `#1b1b1b`；**靛藍 `ind` #2b4c7e、朱紅 `ver` #e0442b、芥黃 `mus` #e8b53a**；灰 `grey` #a8a296；淺色 #d9e1ee／#f7d6cf／#f7e7c0
- **形狀語意全 deck 一致：圓 ＝ LLM／會推理的模型（含 reranker、embedding 模型）；方 ＝ 狀態／資料／記憶／文件片段；三角 ＝ 工具動作／風險閘門（HITL、危險操作）**；朱紅＋叉 ＝ 錯誤示範
- 手繪感來自 rough.js；字體 Huninn；程式碼用 JetBrains Mono
- 構圖：一頁一個概念；大圖形當主角；文字在旁邊小欄；留白是構圖

## 共用元件（`assets/base.css`、`assets/draw.js`）
- `.bridge`：「你已經會的」。`<div class="bridge" style="left:…;top:…;width:…"><span class="k">你已經會的</span>…</div>`；單行版加 `inline`。**框會自動畫，不要再 D.rect。**
- `.code`：程式碼／JSON／trace 實物，字級 24px（本 deck 唯一允許 <26px 的正文）。高亮用 `<span class="hl">`，註解 `.c`、關鍵字 `.k`、字串 `.s`。框自動畫。一個 `.code` 最多 14 行。
- `.tag`：行內小標記，只用在「示意」「範本數字」「本課轉述」「本課整理」。
- 繪圖 API 見 `assets/draw.js` 開頭註解：`D.sq / D.rect / D.ci / D.tri / D.dia / D.line / D.dash / D.arrow / D.curve / D.poly / D.cross / D.bars / D.frame`
- **有文字的方塊用淺色實心**：`D.rect(x,y,w,h,'#d9e1ee',{fillStyle:'solid',stroke:D.C.ind,strokeWidth:3})`；排線填色只用在沒有字的大圖形
- **不要修改 `assets/`、`index.html`、`build.py` 與別人前綴的檔案**。需要新的繪圖函式，在自己頁面的 `<script>` 裡定義

## 檔案規則
- 每頁一個檔案：`slides/<編號>-<英文短名>.html`。**只能用分配給你的前綴**
- 骨架（照抄）：

```html
<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><title>頁面標籤（概覽牆用，6–10 字）</title>
<link rel="stylesheet" href="../assets/base.css"><script src="https://unpkg.com/roughjs@4.6.6/bundled/rough.js"></script><script src="../assets/draw.js"></script>
<style>/* 本頁專用樣式 */</style></head><body><div class="slide">
  <h1>標題</h1><p class="lead">一句話說明</p>
  <!-- 文字用 class="abs" + style="left/top" 絕對定位 -->
  <div class="read"><em>怎麼讀：</em>從哪裡看起、要記住哪一點（一行）</div>
</div><svg class="rough" id="r" width="1920" height="1080"></svg>
<script>const D=Draw('r'); /* 繪圖 */</script></body></html>
```

## 硬規則
1. 字級：標題 ≥ 72px（h1 預設 80px）；正文 ≥ 26px；標籤 ≥ 22px（`.lbl`／`.note` 24px）；`.code` 24px
2. **數字只能來自課綱或 `product-facts.md`／素材地圖**，不准編。示意圖標 `<span class="tag">示意</span>`；課綱履歷數字（68%→91%、−35%、−42%）標「範本數字」；非權威框架標「本課整理」／「本課轉述」
3. 不放頁碼、進度、全大寫小標籤；01/02/03 只在內容本身是順序時使用；不用 emoji
4. 每個概念頁底部有 `.read`「怎麼讀」，**一行**（目標頁、小結頁除外）
5. 文字不得互相重疊、不得被圖形蓋住、不得超出畫面；`.read` 上方要留空，不能和圖或 `.bridge` 撞到
6. 不搬別人的圖：素材地圖裡的「可借的圖解結構」是要你用 rough.js 重畫
7. 小說《凡人修仙傳》只用人物／宗門／法寶的關係當例子，不引用原文段落

## 每一章固定結構
1. **章首頁** `<前綴>00-goals.html`：左側大字「模組 N」＋章名＋本章心法（`.lead`）；右側「學習目標」（`ul.dots`）；底部淺黃框寫「本章實戰」。配一個大幾何形（依章輪流：圓／方／三角）
2. **搭橋頁** `<前綴>01-bridge.html`：本章從你已知的哪裡出發（左：你會的 DL 概念；右：本章新概念；連線）
3. **概念頁**：照下方清單，每頁一張主圖
4. **Lab 頁** `<前綴>5x`：架構圖一頁＋關鍵程式片段（`.code`）
5. **踩坑頁** `<前綴>80`、**面試頁** `<前綴>90`：踩坑用「症狀 → 原因 → 修法」三欄圖；面試題 2–3 題，每題附「回答維度」短句
6. **章末小結頁** `<前綴>99-recap.html`：標題「模組 N 小結」，左側 3–5 點重點，右側縮小版的本章主視覺（★）；右下角 `<div class="next">下一章：○○○</div>`

## 實物層（第二輪新增）：原圖、數據、logo
手繪負責「第一次講懂」；實物負責「這是真的」與「想再深入」。素材一律來自 `assets/figures/figures.md` 清單，**清單外的圖不准用**。

| 頁型 | 編號 | 做法 |
|---|---|---|
| 原圖對照 | X60–X64 | 原圖放在白底卡片（`.fig`），用 rough.js 在圖上圈出重點、拉箭頭到旁邊的說明：「這塊＝剛剛講的 ○○」。底部 `.src` 寫出處 |
| 數據比較 | X65–X69 | 論文／官方的真實數字重畫成乾淨圖表（不用 rough 抖動線，用 SVG 直線），標 `.src`。數字只能用 figures.md 記錄的 |
| 進階延伸 | X70–X79 | 標 `<span class="tag">進階</span>`：公式推導、設計取捨、延伸論文。上課可跳過 |

- **授權分級**（figures.md 的 `license` 欄決定）：`direct`＝CC BY／官方允許，可直接放原圖；`redraw`＝只能用真實數據重畫，`.src` 寫「依 ○○ Fig. N 重繪」；`link`＝只放標題＋網址，不放圖
- **Logo**：只放在工具頁、Lab 架構圖旁，高度 ≤ 48px，不改形狀與顏色，用來指稱「這是哪個套件」
- `.src` 格式：`來源：作者（年份）〈標題〉Fig. N，授權`；字級 22px

## 檢查流程（每做完 3–4 頁就做一次）
```bash
cd docs/slides/deck
./shoot.sh <你的前綴>                                                    # 截圖到 shots/
uv run --with pillow python contact.py <你的前綴> <scratchpad>/<任意名>.png   # 拼成總覽，用看圖能力檢查
```
再逐張打開單頁截圖看細節。發現重疊、溢出、太空、太擠、字太小 → 修好再截一次。**全部做完至少整章再看一輪。**

---

## 分工與每章頁面清單
★＝本章主視覺。內容細節回 `sources/` 與課綱核對。

### 前綴 0xx 開場、9xx 收尾
- 001-cover：「AI Agent 與大模型全棧工程師」＋「20 小時實戰」；一個大圓（模型）被方與三角環繞的構圖
- 002-why：模型本身的三個缺口（沒有長期記憶、不能動手操作外部、知識有截止日）→ 四支柱各補哪個
- 003-prereq：先備自我檢核：softmax、embedding 層、反向傳播、遷移學習、Python 基礎（打勾清單＋每項一句「會到什麼程度」）
- 004-dl-to-agent ★：從深度學習到 Agent 的地圖：左欄「你會的」（softmax 分類器、embedding、RNN、遷移學習、訓練迴圈），右欄「這門課補的」（LLM、RAG、微調、Agent 迴圈、MCP），連線
- 005-pillars：**已完成（showcase），不要改**
- 006-tools：環境與工具（Python、Ollama、Docker、PostgreSQL、Neo4j、ChromaDB、LangGraph、LangSmith），依模組分組
- 007-course-map：8 模組地圖＋時數（2／2／4／2／5／2／1.5／1.5h），標出重點章（模組三、五）
- 008-flagship：旗艦專案預告：Supervisor → DocAgent／DBAgent／OpsAgent，OpsAgent 前有 HITL 三角閘門
- 009-glossary-howto：本課術語怎麼查（第一次出現就定義；附錄術語表在 9xx）
- 900-summary：大總結：四支柱 × 8 模組各一句
- 901-interview-mindset：面試三心法（談工程不談神話、談架構不談玩具、指標說話）
- 902-references-1、903-references-2：從 `sources/M*.md` 每模組挑 2–3 份最好懂的，列標題＋作者＋網址
- 904-glossary-1、905-glossary-2：全課術語表（各前綴頁面裡第一次定義過的術語；先從課綱與素材地圖整理）

### 前綴 1xx 模組一：從深度學習到 LLM（`M1-llm-foundations.md`）
- 100-goals：本章實戰＝Lab1 本地／雲端雙軌對話客戶端
- 101-bridge
- 102-tokenize：同一句中文和英文切成 token 的實物圖（彩色方塊＋下方 id）
- 103-vocab：token id 與詞表大小；為什麼不是一個字一個 token
- 104-embedding：one-hot → 向量（接學生已知的 embedding 層）
- 105-lm-softmax ★：語言模型＝詞表上的 softmax 分類器（長條圖：下一個 token 的機率）
- 106-next-token：逐字生成：輸出接回輸入，一輪一個 token
- 107-temperature：同一分佈換溫度（示意）；**溫度只管隨機性，不管對錯**；用模型官方建議值（R1 distill 建議 0.5–0.7）
- 108-rnn-bottleneck：RNN 逐步傳遞的瓶頸
- 109-attention-intuition：attention 直覺：每個位置加權看其他位置
- 110-qkv：Q／K／V 小矩陣圖
- 111-transformer-block：一層 Transformer 的組成
- 112-context-cost：O(N²)（示意）與 context window
- 113-no-memory：為什麼記不住對話：每次重送整串訊息；Ollama 預設 `num_ctx` 4096 會截斷
- 114-pretrain-sft：預訓練 → 指令微調 → 對話模型
- 115-open-vs-api：開放權重 vs 商業 API（隱私、成本、可客製）；商業模型不寫死型號
- 116-local-models：依顯存選本地模型（Qwen3.5 小尺寸、`qwen3:14b` 9.3GB、`deepseek-r1:8b` 現在的底模型；4-bit 量化）
- 117-messages-json：OpenAI 相容 API 的一則 messages JSON 實物；本地端點 `http://localhost:11434/v1`
- 150-lab1-arch：雙軌客戶端架構（本地 Ollama 為主、雲端備援，故障切換）
- 151-lab1-stream：generator 串流的程式片段
- 180-pitfalls：顯存溢出（OOM）、溫度誤解、`num_ctx` 截斷
- 190-interview
- 199-recap：下一章：提示詞工程與結構化輸出

### 前綴 2xx 模組二：提示詞工程與結構化輸出（`M2-prompt-structured-output.md`）
- 200-goals：本章實戰＝Lab2 Text2SQL 解析引擎
- 201-bridge
- 202-prompt-anatomy ★：一則提示詞的四段結構（角色、背景與任務、約束、示例），實物標註
- 203-few-shot：不改權重的「從示例學格式」（對照：微調要改權重）
- 204-cot：思維鏈；推理模型時代從「教它怎麼想」轉成「定義評估標準」；R1 distill 不建議用 system prompt
- 205-tot：思維樹（分支 → 評估 → 剪枝）與局限
- 206-injection：注入攻擊實例；XML 標籤隔離**只是一層**，擋不住全部 → 搭配權限最小化
- 207-moderation：內容審核（`omni-moderation-latest`）放在管線哪裡
- 208-structured-ladder：結構化輸出三層保障（提示要求 → 原生 structured outputs／tool calling → Pydantic 驗證）；拒答或被截斷仍可能不符 schema
- 250-lab2-flow：Text2SQL 流程（DDL 注入 → 生成 → 驗證 → 拒絕破壞性指令）
- 251-lab2-schema：`SQLGenerationResult` Pydantic 程式片段
- 280-pitfalls：模型多吐 Markdown／說明文字、指令覆蓋攻擊
- 290-interview
- 299-recap：下一章：企業級 RAG

### 前綴 3xx 模組三：企業級 RAG（`M3-rag.md`；重點章）
- 300-goals：本章實戰＝Lab3 私有技術文檔多路召回問答
- 301-bridge：RAG＝改輸入，微調＝改權重
- 302-three-pains：傳統 RAG 三痛點（精度不足、缺大局觀、上下文斷裂）
- 303-two-pipelines ★：離線鏈路（載入 → 分塊 → 向量化 → 入庫）與在線鏈路（改寫 → 召回 → 重排 → 組裝 → 生成）
- 304-fixed-chunk：固定長度切分的語義截斷
- 305-structure-chunk：按標題層級切分＋保留父章節 metadata（`MarkdownHeaderTextSplitter`，`strip_headers` 預設 True）
- 306-semantic-vs-agentic：**分清兩件事**：semantic chunking 用 embedding 距離找切點；agentic chunking 才用 LLM 判斷（無標準 API）
- 307-embedding-filter：向量空間＋ ChromaDB metadata 過濾
- 308-bm25-vs-dense：BM25 與向量各自的盲區（型號、錯誤碼 vs 換句話說）
- 309-hybrid-rrf：**已完成（showcase），不要改**
- 310-rrf：RRF 怎麼算：1／(k＋名次) 的小例子（數字標示意）
- 311-rerank：Cross-Encoder vs 雙塔（一起讀 vs 各自算向量）；Top-K 粗篩 10–20 → Top-N 精排 3–5；`BAAI/bge-reranker-v2-m3`
- 312-parent-child：小片段命中、回傳大段落
- 313-doc-to-qa：預先生成問答對擴充入口
- 314-pdf-tables：表格轉 Markdown＋專用 metadata
- 315-self-rag-crag：檢索後自評 → 不夠就改寫或聯網
- 350-lab3-arch：Lab3 架構圖（本地 Chroma；BM25 自己做；RRF 融合；重排）
- 351-lab3-index：切分與入庫程式片段
- 352-lab3-query：檢索 → 融合 → 重排 → 組裝程式片段
- 380-pitfalls：噪聲片段致幻覺、跨語種檢索失效（用 bge-m3）
- 390-interview
- 399-recap：下一章：知識圖譜與 GraphRAG

### 前綴 4xx 模組四：知識圖譜與 GraphRAG（`M4-graphrag.md`）
- 400-goals：本章實戰＝Lab4《凡人修仙傳》人物關係圖譜
- 401-bridge：沿用模組三「粗召回＋精排」的思路
- 402-why-graph：向量 RAG 答不了的兩種題：多跳關係、全局總結
- 403-entity-relation：實體、關係、屬性（用修仙例子）
- 404-lpg-vs-rdf：標籤屬性圖 vs 三元組；RDF 1.1 關係不能掛屬性（1.2 草案在補）
- 405-cypher：Cypher 基本句型；Neo4j 2026.02 起預設 Cypher 25
- 406-spo-extract：LLM 從文字抽 SPO 三元組（`LLMGraphTransformer` 從 `langchain_neo4j` 匯入）
- 407-two-schools ★：**兩派分清**：Microsoft GraphRAG（社群報告、實體 embedding 找入口，不跑 Cypher）vs Neo4j 系（Cypher 多跳查詢，本章 Lab 用這派）
- 408-global-search：Leiden 社群 → 社群報告 → Map-Reduce 聚合
- 409-local-search：Microsoft 的局部檢索：實體描述 embedding 找入口 → 收集上下文
- 410-query-modes：Global／Local／DRIFT／Basic；GraphRAG 已大致進入維護模式（v3.3.0）
- 450-lab4-graph：人物／宗門／法寶圖譜長相
- 451-lab4-multihop：提問 → 抽出角色 → Cypher 多跳 → 格式化成上下文 → 回答
- 480-pitfalls：同名與別名（實體消歧）、全局檢索 token 開銷
- 490-interview
- 499-recap：下一章：AI Agent 與 LangGraph

### 前綴 5xx 模組五（上）：Agent 核心與 LangGraph（`M5-agent-langgraph.md`；重點章）——編號 500–519
- 500-goals：本章實戰＝Lab5-A／B／C
- 501-bridge：f(x) 呼叫一次 vs 放進迴圈
- 502-real-trace：一段真實 tool calling 訊息串（user → assistant tool_call → tool 結果 → assistant 回答）
- 503-react-loop：Thought → Action → Observation
- 504-workflow-vs-agent：固定流程 vs 模型自己決定下一步；何時用哪個
- 505-minimal-agent：50 行手寫 agent 的解剖（迴圈、tool_calls 解析、終止條件）
- 506-why-graph：為什麼 agent 需要狀態圖（分支、重試、暫停、恢復）
- 507-stategraph ★：State、Node、Edge 三要素
- 508-conditional-edges：條件邊＝路由
- 509-reducer：`Annotated[list, operator.add]`：多節點同時寫入時怎麼合併（對照：覆蓋）
- 510-create-agent：LangChain 1.x 的 `create_agent`＋middleware，底下跑的是 LangGraph
- 511-checkpointer：`InMemorySaver` vs `PostgresSaver`；`thread_id` 隔離會話
- 512-time-travel：取歷史快照、改狀態、分支出新路徑
- 513-hitl ★：`interrupt()` 暫停 → 人工決定 → `Command(resume=...)` 恢復

### 前綴 5xx 模組五（下）：多智能體與 Lab——編號 520–599
- 520-supervisor ★：Supervisor 把需求拆給子 agent，再統整（**做法：子 agent 包成工具**；`langgraph-supervisor` 套件已封存，不用）
- 521-subagent-as-tool：子 agent 包成工具的介面長相
- 522-context-passing：子 agent 之間怎麼傳上下文、只回摘要
- 523-deep-agents：Deep Agents（`deepagents`）：規劃（`write_todos` 要手動開）＋子 agent＋虛擬檔案系統
- 524-agent-zoo：為每個場景各做一個 agent 的維護問題（標「本課轉述」）
- 525-skills：通用 Agent＋可插拔 Skills
- 550-lab5a：手寫 ReAct agent 的程式片段
- 551-lab5b-graph：審批級 SQL agent 的狀態圖（敏感操作前的三角閘門）
- 552-lab5b-code：`interrupt` 與 `Command(resume=...)` 程式片段；PostgresSaver
- 553-lab5c：CalendarAgent＋EmailAgent 包成工具 → SupervisorAgent
- 580-pitfalls：死循環與 token 耗盡（`recursion_limit` 預設 10,007 擋不住 → 明確設小值＋呼叫次數上限）；並發狀態覆蓋（reducer）
- 590-interview：舊版 AgentExecutor 只在這裡帶一句
- 599-recap：下一章：LoRA 微調

### 前綴 6xx 模組六：LoRA 微調與私有化部署（`M6-lora-finetune.md`）
- 600-goals：本章實戰＝Lab6 問診／客服風格微調
- 601-bridge：遷移學習 → 微調
- 602-decision-matrix ★：Prompt vs RAG vs 微調（知識更新頻率、輸出風格、幻覺與溯源）
- 603-lora-ab：凍結 W、旁路 ΔW＝B·A，畫出矩陣維度
- 604-param-count：可訓練參數比例（7B 約 0.06%–0.3%）
- 605-lora-vs-full：什麼條件下和全量微調相當（中小資料集、加在所有層），什麼情況落後
- 606-qlora：4-bit 基座＋LoRA
- 607-data-formats：Alpaca vs ShareGPT 格式實物
- 608-chat-template：對話模板；不符時的真實症狀（loss 正常但推理不停、重複、角色錯亂）
- 609-llamafactory-flow：資料 → 設定 → 訓練 → 評估 → 合併匯出
- 610-loss-curve：訓練／驗證 loss（示意）與過擬合
- 611-merge：合併權重；QLoRA 必須合到原精度基座
- 612-vision：多模態本地推理（Qwen3-VL；Qwen3.5 原生可看圖）
- 650-lab6：Lab6 設定（`lora_rank` 8、alpha 16＝LLaMA-Factory 常用值）＋前後對比
- 680-pitfalls：災難性遺忘（混通用資料比例標「經驗值」）、對話模板不符
- 690-interview
- 699-recap：下一章：MCP 與低代碼

### 前綴 7xx 模組七、8xx 模組八（`M7-mcp-lowcode.md`、`M8-observability-career.md`）
- 700-goals：本章實戰＝Lab7 Excel 自動分析智能體
- 701-bridge
- 702-nxm ★：N 個模型 × M 個工具的整合爆炸 → 一個協定
- 703-host-client-server：Host／Client／Server 架構
- 704-primitives：Tools、Resources（唯讀、由應用決定何時取用、可模板化）、Prompts
- 705-transport：stdio 與 Streamable HTTP（舊 HTTP+SSE 已棄用）；2026-07-28 版改為無狀態
- 706-governance：起源 Anthropic，2025-12 捐給 Linux Foundation 旗下 Agentic AI Foundation
- 707-clients：Cherry Studio、Claude Desktop 等客戶端接 MCP
- 708-lowcode-boundary：Dify／n8n vs LangGraph 的邊界
- 750-lab7：Lab7 架構（官方 SDK `MCPServer`；Streamable HTTP；Dify 在 Docker 裡用 `host.docker.internal`）
- 780-pitfalls：stdio server 印 stdout 破壞訊息、Docker 裡的 localhost、路徑與環境變數
- 790-interview
- 799-recap：下一章：轉職衝刺
- 800-goals：本章實戰＝Lab8 旗艦專案整合
- 801-bridge：訓練時看 loss 曲線 → 應用上線看 trace 與評測
- 802-trace：拆解一條 trace（每步耗時、token、輸入輸出）
- 803-evals：評測集、LLM-as-judge、回歸測試；兩派觀點（先做錯誤分析 vs 評測驅動）都呈現
- 804-vibe-coding：Karpathy 2025-02 提出；「自然語言規劃 → AI 生成 → 人審查」工作流；工具舉 Cursor、Claude Code
- 805-three-layers ★：AI 產業三層（標「本課整理」）
- 806-resume：履歷改寫 before／after（數字標「範本數字」）
- 850-flagship-arch ★：旗艦專案分層架構（前端 → Supervisor → Doc／DB／Ops Agent → PostgresSaver → LangSmith）；前端註明 Agent Chat UI 已封存
- 851-lab8：整合步驟與公開 trace
- 880-interview：兩個高頻考點＋回答維度
- 899-recap：下一步：大總結
