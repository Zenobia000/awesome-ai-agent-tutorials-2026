# 模組四 素材地圖

> 對象：懂深度學習（NN、softmax、反向傳播、embedding 層、遷移學習），沒學過 NLP／生成式 AI／Agent；已上完模組三（向量 RAG）。
> 用途：參考下列來源的「圖解結構」自行重畫，不直接搬圖。所有網址於 2026-11-12 以 WebFetch 實際打開核實；需要登入或打不開的已剔除。

## 論點清單

1. **向量 RAG 有兩種問題答不好：要串多個事實的「多跳」問題，和要看完整個語料的「全局」問題**。chunk 是彼此獨立的碎片，相似度檢索只能撈「像問題的片段」，撈不到「關係」也撈不到「全貌」。
2. **知識圖譜把文字變成「節點＋有型別的邊＋屬性」**：實體／關係／屬性；LPG（Neo4j，邊上可以掛屬性）與 RDF（主詞–謂詞–受詞三元組、URI 識別）是兩種資料模型，各有適用場景。
3. **Cypher 是「畫出來的查詢」，Text2Cypher 是模組二 Text2SQL 的圖版本**：`(a)-[:REL]->(b)` 的 ASCII 圖案就是查詢；讓 LLM 寫 Cypher 要給 schema、範例、驗證與修正迴圈。
4. **用 LLM 建圖＝抽取 SPO 三元組＋實體消歧**：LLM 從每段文字抽出（主詞, 關係, 受詞），但同一實體會以不同名字出現，必須做 entity resolution 才不會變成一堆孤立節點。
5. **Microsoft GraphRAG 的索引：Leiden 階層社群＋預先生成的社群報告**：建索引時就把圖切成由細到粗的社群、每個社群請 LLM 寫好摘要；代價是建索引的 LLM 成本很高（因此出現 LazyGraphRAG 這類「延後計算」的變體）。
6. **GraphRAG 的查詢：Global 用 map-reduce 讀社群報告，Local 從問題中的實體切入，DRIFT 結合兩者**：入口都是向量檢索（模組三），差別在之後讀「社群摘要」還是「實體鄰域」；全局查詢的 token 成本可用動態社群篩選剪枝。

## 素材
### 論點 1：向量 RAG 答不好多跳與全局問題

- **GraphRAG: Unlocking LLM discovery on narrative private data** — Jonathan Larson、Steven Truitt / Microsoft Research Blog（2024-02-13） — https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/（已核實 2026-11-12）
  - 適合程度：GraphRAG 的原始發表文，用真實資料集（VIINA，數千篇俄烏新聞）做對照實驗，不需要任何 NLP 背景就能看懂失敗案例。
  - 可借的圖解結構：三題對照表——「What is Novorossiya?」兩者都答得好；「What has Novorossiya done?」baseline RAG 撈到的 chunk 沒一個提到它（Figure 1 的檢索結果表）；「What are the top 5 themes?」baseline 給出無關主題、GraphRAG 引用社群報告答出來。可重畫成三列 ✓／✗ 對照表當模組開場。另有 Figure 3：GPT-4 Turbo 建出的知識圖譜，節點大小＝關係數、顏色＝社群。
  - 搭橋：向量檢索＝k-NN，只找「長得像 query」的點；但「top 5 themes」這種問題與任何單一片段都不像，像是要對整個資料集做 clustering 再摘要——學生做過 k-means／t-SNE 就懂。

- **Graph RAG Explained** — Nir Diamant / DiamantAI Substack（2025-03-11，免登入可讀全文） — https://newsletter.diamant-ai.com/p/graph-rag-explained（已核實 2026-11-12；舊網址 diamantai.substack.com 會 301 轉到此）
  - 適合程度：比喻密度高、寫給入門者：一般 RAG 像一疊互不相連的線索卡，Graph RAG 像偵探牆上用紅線連起來的線索板；社群摘要像「圖的章節摘要」；全局查詢像主持人彙整多位專家的發言。
  - 可借的圖解結構：偵探牆比喻圖（左：散落卡片；右：卡片＋紅線＋分群圈）可直接做開場；另有「Graph RAG vs Traditional RAG」對照圖與五步驟查詢流程圖。
  - 搭橋：「卡片之間的紅線」＝資料之間的結構資訊，向量 RAG 把每張卡片獨立 embedding，等於丟掉了樣本間的關聯（像把圖資料當成 i.i.d. 表格資料處理）。

### 論點 2：知識圖譜資料模型——實體／關係／屬性，LPG vs RDF

- **What is a knowledge graph?** — John Stegeman / Neo4j Blog（2024-07-22） — https://neo4j.com/blog/knowledge-graph/what-is-knowledge-graph/（已核實 2026-11-12）
  - 適合程度：用電商例子（顧客、商品、訂單）從零建立節點、關係、organizing principle（schema／ontology）的概念，前半段很適合入門；後半段（triple store、reification、GQL）較技術，可略過。作者是 Neo4j 員工，比較段落偏向 LPG。
  - 可借的圖解結構：漸進式四張圖：(1) 只有節點（Customer、Product、Order）；(2) 加上 `PLACED` 箭頭；(3) 疊上商品分類層（organizing principle）；(4) 完整圖，用顏色區分「實例資料」與「schema 層」。適合做成同一張投影片的四段動畫。
  - 搭橋：節點類型＝類別標籤、屬性＝特徵向量、關係＝樣本之間的邊；「schema 層」類比資料集的 label taxonomy。

- **Neo4j Fundamentals — What is Neo4j?**（GraphAcademy 課程第一課） — Neo4j GraphAcademy — https://graphacademy.neo4j.com/courses/neo4j-fundamentals/1-graph-thinking/1-what-is-neo4j/（已核實 2026-11-12；課文內容公開可讀，免費註冊只用於記錄進度與取得沙盒資料庫）
  - 適合程度：四個元素各一段：Node（圓圈）、Label（類別，單數名詞，可多個）、Relationship（有型別、有方向，型別用動詞）、Property（鍵值對，schemaless）；附命名慣例，學生 Lab 4 建模時直接套用。
  - 可借的圖解結構：社群網路圖：圓圈＝人／公司，連線＝WORKS_AT、MARRIED_TO（雙向語意）、LOVES（單向語意）。可改畫成《凡人修仙傳》版本：韓立 –[:MEMBER_OF]→ 七玄門、韓立 –[:OWNS]→ 法寶。
  - 搭橋：label 像 one-hot 類別但可多標籤（multi-label classification）；「方向」對應有向圖的鄰接矩陣不對稱。

- **RDF vs. property graphs: Choosing the right approach for implementing a knowledge graph** — Jim Webber / Neo4j Blog（2024-06-04） — https://neo4j.com/blog/knowledge-graph/rdf-vs-property-graphs-knowledge-graphs/（已核實 2026-11-12）
  - 適合程度：用同一個小例子（Daniel 與 Sunita 是手足、Sunita 2011-01-10 買了一台 Volvo、Dan 從 2013-03-15 開始開它）分別用 RDF 與 LPG 表示，差異一目了然：RDF 要在「關係上掛日期」得額外拆出節點與三元組，LPG 直接把日期放在邊上。作者為 Neo4j 首席科學家，立場偏 LPG，投影片需補一句 RDF 的強項（標準化、URI 全域識別、推理與開放資料生態）。
  - 可借的圖解結構：左右對照圖——左 RDF：所有東西都是「點–箭頭–點」三元組，「購買日期」被迫變成中間節點；右 LPG：兩個節點一條 `BOUGHT {date: 2011-01-10}` 邊。
  - 搭橋：RDF＝把所有資訊攤平成 (s, p, o) 的長表格；LPG＝節點與邊都帶特徵向量的屬性圖，接近 GNN 裡「node features＋edge features」的表示法。

### 論點 3：Cypher 與 Text2Cypher

- **What is Cypher?** — Neo4j Getting Started 官方文件 — https://neo4j.com/docs/getting-started/cypher/（已核實 2026-11-12）
  - 適合程度：專講 Cypher 的「ASCII art」語法：節點用圓括號 `(:Person)`、關係用方括號加箭頭 `-[:LIKES]->`；範例 `MATCH (p:Person)-[r:LIKES]->(t:Technology) RETURN p, r, t` 與 `CREATE (sally:Person {name:'Sally'})-[r:IS_FRIENDS_WITH]->(john:Person {name:'John'})`；七張圖。本頁沒有 `MERGE`，建圖要另外補（批次寫入三元組必用 MERGE 防重複）。
  - 可借的圖解結構：「查詢字串 ↔ 圖」對照圖：上排是 Cypher 文字，下排是對應的圓圈與箭頭，同顏色標出對應部分；另有 Sally／John／Graphs／Neo4j 四節點小圖可當範例資料。
  - 搭橋：Cypher 是「描述要找的子圖形狀」的宣告式語言——類比用一個 template 在大圖上做 pattern matching（像 convolution 的 kernel 在圖上滑動找匹配，但匹配的是結構）。

- **Text2Cypher**（GraphRAG Pattern Catalog） — Neo4j / graphrag.com（CC BY 4.0） — https://graphrag.com/reference/graphrag/text2cypher/（已核實 2026-11-12）
  - 適合程度：一頁講完前處理（schema 要給 node labels＋屬性型別、relationship types、source–rel–target 模式）、四步檢索流程、常見失敗（新語法、關係方向、別名對不上值）、防護（人工審核、語法檢查、唯讀執行、帶錯誤訊息重試）。
  - 可借的圖解結構：線性流程圖：使用者問題＋Schema → LLM → Cypher → 圖資料庫 → 結果 → LLM → 答案；在「Cypher → 圖資料庫」之間插一個「驗證／錯誤回饋」回圈。可與模組二 Text2SQL 的流程圖並排，只換掉資料庫圖示。
  - 搭橋：schema＝給模型的條件輸入；錯誤訊息回饋重試＝用 loss 訊號修正輸出的迴圈（只是不更新權重）。

- **Text2Cypher guide: When and How to Implement Text2Cypher in Agentic Applications** — Alex Gilmore / Neo4j Blog（2026-02-09） — https://neo4j.com/blog/genai/text2cypher-guide/（已核實 2026-11-12）
  - 適合程度：最新的實務指南，結論清楚：Text2Cypher 適合「探索或兜底」，高頻、複雜的查詢應寫成參數化的固定 Cypher 工具；schema 太大要做子 schema 檢索；修正可用 LLM 迴圈或確定性工具（regex、CyVer、LangChain `CypherQueryCorrector` 修反向關係）；評估分「比對查詢字串」與「比對執行結果」兩種。
  - 可借的圖解結構：「查詢頻率 × 複雜度」四象限圖，決定該用固定 Cypher 工具還是 Text2Cypher；以及 agent 版 Text2Cypher 工作流（取 schema → 生成 → 驗證 → 執行 → 錯誤回饋重生成）。
  - 搭橋：「評估：字串比對 vs 執行結果比對」類比 exact-match accuracy vs 功能等價的評估指標；四象限圖是很好的工程取捨教材。

### 論點 4：LLM 抽取 SPO 三元組與實體消歧

- **Implementing 'from local to global' GraphRAG with Neo4j and LangChain: Constructing the graph** — Tomaž Bratanič / Neo4j Developer Blog（2024-07-09） — https://neo4j.com/blog/developer/global-graphrag-neo4j-langchain/（已核實 2026-11-12）
  - 適合程度：把 Microsoft GraphRAG 的建圖流程在 Neo4j 上重做一遍，每一步都有圖。實體消歧的流程是目前最完整的公開教學：名稱＋描述 embedding → k-NN 圖（topK 10、相似度 ≥ 0.95）→ 弱連通分量分組 → 編輯距離 < 3 過濾 → LLM 判斷是否同一實體 → `apoc.refactor.mergeNodes` 合併；作者也提醒此法對人名、組織有效，對日期不佳。同一篇還用 GDS 跑階層 Leiden（`includeIntermediateCommunities=True`），可同時支援論點 5。
  - 可借的圖解結構：(1) 建圖管線圖：文件 → LLM 抽取 → 圖 → 社群 → 摘要；(2) 實體消歧漏斗：候選對（k-NN）→ 分組（WCC）→ 字串過濾 → LLM 裁決 → 合併前後對照圖；(3) 節點度數 log-scale 直方圖（power-law）。
  - 搭橋：消歧第一步就是 embedding 近鄰搜尋——等同 face clustering／去重：先用特徵向量找候選，再用更貴的判斷器確認（跟模組三的「粗召回＋精排」同一個模式，可以點出來）。

- **User Guide: Knowledge Graph Builder** — neo4j-graphrag-python 官方文件 — https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html（已核實 2026-11-12）
  - 適合程度：Neo4j 官方維護的建圖套件，元件切分很清楚，可當「建圖管線有哪些零件」的權威清單：Data loader → Text splitter → Chunk embedder → Schema builder（手寫 `SchemaBuilder` 或由 LLM 從文字推出 `SchemaFromTextExtractor`）→ `LLMEntityRelationExtractor` → `Neo4jWriter` → Entity resolver；`SimpleKGPipeline` 一行串起全部。三種內建消歧器：`SinglePropertyExactMatchResolver`（同 label 同 name 合併）、`SpaCySemanticMatchResolver`（embedding cosine）、`FuzzyMatchResolver`（RapidFuzz 編輯距離）。
  - 可借的圖解結構：頁面上的「KG Builder pipeline」方塊流程圖；可重畫成七格管線，並把「Schema builder」標成限制 LLM 輸出空間的關鍵一格。
  - 搭橋：schema 限定可抽的實體與關係類型＝把開放式生成變成「在固定類別集合上分類」，約束輸出空間就降低錯誤（像把 open-vocabulary 偵測改成固定類別偵測）。

- **Building Knowledge Graphs with LLMs**（GraphAcademy 課程，約 1 小時） — Neo4j GraphAcademy — https://graphacademy.neo4j.com/courses/llm-knowledge-graph-construction/（已核實 2026-11-12；課程頁公開，進行實作需免費註冊取得 Aura 沙盒）
  - 適合程度：用瀏覽器內的 LLM Graph Builder 不寫程式就看到「文件 → Chunk → Entity」的建圖結果，適合課前／課後讓學生先有直覺；含「自訂 schema」一課（如 `(Technology)-[:HAS]->(Capability)`）。不含實體消歧。
  - 可借的圖解結構：Lexical graph（Document → Chunk）與 Domain graph（Entity – Entity）雙層結構圖：下層是文件切塊、上層是抽出的實體網，中間以 `HAS_ENTITY` 連接——這是之後追溯出處的關鍵。
  - 搭橋：雙層結構讓每個實體都能追回原文 chunk，等於保留「預測 → 輸入證據」的對應，類比可解釋性裡的 attribution。

### 論點 5：Microsoft GraphRAG 的索引——Leiden 社群與社群報告

- **GraphRAG 官方文件：Welcome / Default Indexing Dataflow** — Microsoft — https://microsoft.github.io/graphrag/ 、https://microsoft.github.io/graphrag/index/default_dataflow/（已核實 2026-11-12）
  - 適合程度：官方權威流程。索引六階段：Compose TextUnits（預設 1200 token）→ Document Processing → Graph Extraction（LLM 抽實體、關係，選配 claims）→ Graph Augmentation（階層 Leiden 社群）→ Community Summarization（每個社群寫報告）→ Text Embedding（TextUnit、實體描述、社群報告）。另有 FastGraphRAG 模式改用傳統 NLP 抽取以省成本。首頁列出四種查詢：Global、Local、DRIFT、Basic。
  - 可借的圖解結構：六階段總覽流程圖＋每階段產出的資料表（Documents、TextUnits、Entities、Relationships、Communities、Community Reports）——可畫成「原文 → 表格群」的轉換圖，強調社群報告是**索引時預先生成**的。
  - 搭橋：社群報告＝預先算好的聚合特徵（像 feature pyramid 的不同層級：低層細節多、高層摘要粗）；Leiden 階層＝由細到粗的分群樹，與 hierarchical clustering 的 dendrogram 同概念。

- **LazyGraphRAG: Setting a new standard for quality and cost** — Darren Edge、Ha Trinh、Jonathan Larson / Microsoft Research Blog（2024-11-25，2025-06-06 編註） — https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/（已核實 2026-11-12）
  - 適合程度：用來講「GraphRAG 的成本問題與後續演進」：把 LLM 工作延後到查詢時，索引成本與向量 RAG 相同、約為完整 GraphRAG 的 0.1%。Table 1 逐步比較 GraphRAG 與 LazyGraphRAG 在索引、摘要、查詢各階段做了什麼。注意：編註表示已整合進 Microsoft Discovery 與 Azure Local，**開源 graphrag 套件未見此功能**。
  - 可借的圖解結構：「LLM 成本花在哪個階段」的對照長條：GraphRAG 前重後輕（索引時全做完）、LazyGraphRAG 前輕後重（查詢時才做）。
  - 搭橋：eager vs lazy computation——預先算好全部特徵 vs 推論時按需計算，是學生熟悉的計算／儲存取捨。

- **Leiden**（Graph Data Science 演算法文件） — Neo4j GDS 官方文件 — https://neo4j.com/docs/graph-data-science/current/algorithms/leiden/（已核實 2026-11-12）
  - 適合程度：一段話講清 Leiden 是 Louvain 的改良（修正 Louvain 可能產生「內部不連通的社群」），以 modularity 為目標、`gamma` 調解析度、階層式合併；`includeIntermediateCommunities=true` 時每個節點會得到每一層的社群 ID 清單。只有一張示例圖，公式要另外補。
  - 可借的圖解結構：兩群示例圖＋「每個節點的 intermediateCommunityIds = [第1層, 第2層]」表格，可重畫成「同一張圖在兩個層級下的分群著色」。
  - 搭橋：modularity＝「群內邊比隨機期望多多少」的目標函數；Leiden 是在離散空間上做貪婪最佳化（沒有梯度），`gamma` 像控制群數的正則化係數。

### 論點 6：GraphRAG 的查詢——Global／Local／DRIFT 與成本

- **Global Search / Local Search / DRIFT Search** — Microsoft GraphRAG 官方文件 — https://microsoft.github.io/graphrag/query/global_search/ 、https://microsoft.github.io/graphrag/query/local_search/ 、https://microsoft.github.io/graphrag/query/drift_search/（已核實 2026-11-12）
  - 適合程度：三頁各有一張資料流圖，文字短。Global：社群報告切成批次 → 每批產出帶重要度分數的要點（map）→ 篩選高分要點合成答案（reduce）；社群層級越低越細、越貴。Local：用 query 與「實體描述 embedding」比對找出切入實體 → 拉出相關 text units、社群報告、鄰近實體與關係、covariates → 排序過濾塞進同一個 context window。DRIFT：先用 top-K 社群報告產生初步答案與追問（primer），再對追問做 local search，形成問答階層。
  - 可借的圖解結構：(1) Global 的 map-reduce 扇出扇入圖：Query → N 個打亂的報告批次 → N 個帶分數的中間答案 → 排序過濾 → 最終答案；(2) Local 的星形圖：中央「比對到的實體」，四條射線到 Text Units／Community Reports／Entities & Relationships／Covariates，各自排序過濾後匯流；(3) DRIFT 的 A/B/C 三階段問答樹。
  - 搭橋：map-reduce＝把資料切 batch、各自前向、再聚合（像 data parallel 後 all-reduce 梯度）；Local 的實體比對仍是模組三的向量檢索，只是檢索對象從 chunk 換成「實體描述」。

- **GraphRAG: Improving global search via dynamic community selection** — Bryan Li、Ha Trinh、Darren Edge、Jonathan Larson / Microsoft Research Blog（2024-11-15） — https://www.microsoft.com/en-us/research/blog/graphrag-improving-global-search-via-dynamic-community-selection/（已核實 2026-11-12）
  - 適合程度：直接回應課綱踩坑表的「全局檢索 Token 開銷過大」：靜態做法把某層所有社群報告都丟進 map-reduce；動態做法從根節點往下，LLM 先判斷報告是否相關，不相關就整枝剪掉。
  - 可借的圖解結構：社群樹剪枝圖：根 → 子社群 → 孫社群，每個節點標「相關／不相關」，不相關的整個子樹變灰。附數字：level 1 時 token 成本約 −77%、品質接近靜態做法。
  - 搭橋：就是樹搜尋的 pruning／beam search 的「早剪枝」；也可類比 cascade classifier——先用便宜的判斷擋掉大部分。

- **Integrating Microsoft GraphRAG into Neo4j** — Tomaž Bratanič / Neo4j Developer Blog（2024-08-13） — https://neo4j.com/blog/developer/microsoft-graphrag-neo4j/（已核實 2026-11-12）
  - 適合程度：把 Microsoft GraphRAG 的輸出匯入 Neo4j，並用 Cypher 重寫 local／global retriever——剛好是 Lab 4（Neo4j）與 Microsoft GraphRAG 概念之間缺的那座橋。Local：向量索引找 top-k `__Entity__` → 一段 Cypher 收集相關 chunk（top 3）、社群報告（top 3）、對外關係與內部關係（各 top 10）；Global：Cypher 只負責取某層 `__Community__` 報告，map/reduce 交給 LLM。
  - 可借的圖解結構：圖 schema：`__Chunk__ –HAS_ENTITY→ __Entity__ –RELATED– __Entity__ –IN_COMMUNITY→ __Community__`；以及 local／global retriever 兩張架構圖。可做成「同一個圖、兩種讀法」的對照投影片。
  - 搭橋：清楚呈現「向量檢索找入口、圖遍歷擴展上下文」的兩段式——入口用 embedding（模組三學過），擴展用結構（本模組新學的）。

### 備選素材（已核實，但超出「每論點 1–3 份」上限，必要時替換上面的條目）

- [論點 2] **RDF 1.1 Primer** — W3C Working Group Note — https://www.w3.org/TR/rdf11-primer/（已核實 2026-11-12）：RDF 官方入門，三元組定義只有一段：「主詞與受詞是節點、謂詞是弧」；例子是 Bob、Alice、蒙娜麗莎、達文西。

## 事實核實

- **Microsoft GraphRAG 版本與狀態**：最新 **v3.3.0（GitHub release 2026-10-08）**；README 明示「This project is **largely in maintenance mode**, and won't be accepting new PRs or implementing new features」，只做 bug 修正與相依更新；並警告「GraphRAG indexing can be an expensive operation… start small」，也強烈建議先做 prompt tuning。小版本升級需 `graphrag init --root [path] --force`，大版本有 migration notebook。出處：https://github.com/microsoft/graphrag 、PyPI `graphrag` 3.3.0、GitHub releases API。**與課綱不一致**：課綱把它當持續演進的主流框架介紹，實際上已進入維護模式。
- **GraphRAG 查詢模式**：官方目前列出 **Global、Local、DRIFT、Basic** 四種（Basic＝傳統 top-k 向量 RAG）。Global Search 另有「dynamic community selection」改良（2024-11），LazyGraphRAG 不在開源套件中（整合到 Microsoft Discovery／Azure Local）。出處：https://microsoft.github.io/graphrag/ 、https://microsoft.github.io/graphrag/query/drift_search/ 。**與課綱不一致**：課綱表格只有 Global／Local，缺 DRIFT（以及做為對照組的 Basic）。
- **GraphRAG Local Search 機制**：以 query 與「實體描述 embedding」比對找切入實體，再透過實體–text unit、實體–社群報告、實體–實體、實體–covariate 的對應關係收集候選，各自排序過濾後組成單一 context。官方文件**沒有**描述固定的 1-hop／2-hop 拓撲展開，也不使用 Cypher 或 Neo4j（預設輸出為資料表＋向量庫）。出處：https://microsoft.github.io/graphrag/query/local_search/ 、https://microsoft.github.io/graphrag/index/default_dataflow/ 。**與課綱不一致**：課綱寫「用戶提問實體識別、圖中定位、1-hop／2-hop 多跳拓撲展開」，比較接近 Neo4j 的 `VectorCypherRetriever`／graphrag.com 的模式，而非 Microsoft GraphRAG 本身。
- **GraphRAG 索引細節**：TextUnit 預設 1200 token；Leiden 為階層式（hierarchical Leiden）；claims（covariates）抽取預設關閉；另有 FastGraphRAG（NLP 抽取、跳過 claims）。出處：https://microsoft.github.io/graphrag/index/default_dataflow/ 。
- **`LLMGraphTransformer`（LangChain 三元組抽取）**：舊路徑 `langchain_experimental.graph_transformers`（多數部落格範例，包括 Bratanič 2024 文章仍用此路徑），但 `langchain-experimental` 已標示「is being sunset」。目前應改用 `from langchain_neo4j import LLMGraphTransformer`（`langchain-neo4j` 0.11.0，2026-10-09，wheel 內確認有 `langchain_neo4j/graph_transformers/llm.py`）。同套件也提供 `Neo4jGraph`、`GraphCypherQAChain`、`Neo4jVector`。出處：https://github.com/langchain-ai/langchain-experimental 、PyPI wheel 檢查。
- **`neo4j-graphrag`（Neo4j 官方 GraphRAG 套件）**：最新 1.24.0（2026-11-10）。提供 `SimpleKGPipeline`（標示 experimental）、三種 entity resolver，以及 `VectorRetriever`、`VectorCypherRetriever`、`HybridRetriever`、`HybridCypherRetriever`、`Text2CypherRetriever`（參數 `neo4j_schema`、`examples`；生成的 Cypher 不保證可執行，失敗時拋 `Text2CypherRetrievalError`）、`ToolsRetriever`。出處：https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html 、https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html 。課綱未提，但 Lab 4 的建圖、消歧、Text2Cypher 都可以直接用它。
- **Neo4j 與 Cypher 版本**：Neo4j 已改用年月版號（2026.xx）；自 2026.02 起，新建資料庫的預設查詢語言是 **Cypher 25**，並持續加入 GQL 對齊語法（如 2026.07 的 `GROUP BY`、`cardinality()`）。Neo4j 官方建議避開 2026.07.0（`trim()` bug 可能損壞字串資料）。Python driver `neo4j` 最新 6.4.1（2026-10-15）。出處：https://neo4j.com/release-notes/database/neo4j-2026-02/ 、https://neo4j.com/docs/cypher-manual/25/appendix/gql-conformance/ 。影響：LLM 訓練資料多為舊 Cypher 語法，Text2Cypher 生成的語法可能與新版不一致（graphrag.com 也點名「模型對新 Cypher 語法掌握差」）。
- **Leiden 參數**：Neo4j GDS `gds.leiden.*`，`gamma` 預設 1.0、`theta` 預設 0.01、`maxLevels` 預設 10、`includeIntermediateCommunities` 預設 false。出處：https://neo4j.com/docs/graph-data-science/current/algorithms/leiden/ 。
- **RDF 版本**：現行 W3C Recommendation 仍是 RDF 1.1；RDF 1.2（引入 triple terms，可對「陳述」本身再下陳述，等於補上「邊上掛屬性」）截至 2026-09 仍是 Working Draft。出處：https://www.w3.org/TR/rdf11-primer/ 、https://www.w3.org/TR/2026/WD-rdf12-trig-20260915/ 。影響：「RDF 無法在關係上加屬性」的說法要改成「RDF 1.1 需要額外建模（reification），1.2 草案正在補」。

## 投影片建議

1. **把 Lab 4 與「Microsoft GraphRAG」的關係講清楚**：Lab 4 做的是「Neo4j＋LLM 抽三元組＋Cypher 多跳查詢」，這是 Neo4j 系的 GraphRAG（graphrag.com 的 Text2Cypher／VectorCypher 模式）；Microsoft GraphRAG 的 Local Search 不是 Cypher 多跳，而是「實體 embedding 比對＋對應表收集」。建議課綱表格的 Local Search 改寫成官方機制，另開一列「Neo4j 圖遍歷檢索（1-hop／2-hop Cypher）」給 Lab 用；Bratanič 的 *Integrating Microsoft GraphRAG into Neo4j* 正好示範兩者怎麼接在一起。
2. **Global Search 的「社群報告」用學生熟的「分層特徵」來講，並補上 DRIFT 與成本**：Leiden 階層＝由細到粗的 dendrogram；社群報告＝索引時預先算好的各層摘要；全局問答＝對報告做 map-reduce。接著一張投影片講成本（官方警告建索引昂貴、dynamic community selection 剪枝、LazyGraphRAG 延後計算），對應課綱踩坑表，並說明 Microsoft GraphRAG 已進入維護模式——面試講「概念與取捨」比講「套件 API」更穩。
3. **Text2Cypher 直接接在模組二 Text2SQL 後面講「同一套路、換一個資料庫」**，並納入 Neo4j 2026 年的實務結論：Text2Cypher 定位是探索與兜底，高頻查詢寫成參數化 Cypher 工具；一定要有 schema、少量範例、唯讀執行、錯誤回饋重試。也要提醒 Neo4j 預設已是 Cypher 25，LLM 生成的舊語法可能出錯。
4. **實體消歧用「粗召回＋精排」的模式講，連回模組三**：embedding k-NN 找候選（粗）→ 字串距離過濾 → LLM 裁決（精）→ 合併。學生剛學過兩階段檢索，這裡重用同一個心智模型，負擔最小；Lab 可直接用 `neo4j-graphrag` 的 `FuzzyMatchResolver`／`SpaCySemanticMatchResolver`，不用自己寫。
5. **LPG vs RDF 只用一張對照圖、不展開本體論**：2 小時的模組裡，這群學生只需要知道「Neo4j＝邊上能掛屬性的屬性圖、RDF＝標準化三元組＋URI，適合跨組織資料交換與推理」；用 Jim Webber 的 Volvo 例子一張圖講完即可，把時間留給建圖與 GraphRAG 檢索。
