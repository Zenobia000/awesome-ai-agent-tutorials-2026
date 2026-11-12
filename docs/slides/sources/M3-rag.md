# 模組三 素材地圖

> 對象：懂深度學習（NN、softmax、反向傳播、embedding 層、遷移學習），沒學過 NLP／生成式 AI／Agent。
> 用途：參考下列來源的「圖解結構」自行重畫，不直接搬圖。所有網址於 2026-11-12 以 WebFetch 實際打開核實；需要登入或打不開的已剔除。

## 論點清單

1. **RAG 解決的是「權重是凍結的記憶」**：LLM 的知識固化在訓練好的參數裡，私有／新資料進不去；RAG 不改權重，而是在推論時把查到的文字塞進輸入。整套系統拆成「離線建索引」與「在線檢索＋生成」兩條鏈路。
2. **文字 embedding 就是「預訓練 encoder 的特徵向量」**：和拿 ImageNet 預訓練 CNN 抽特徵一樣，句子經 encoder 變成固定維度向量，用 cosine 相似度找近鄰；問句和文件各自編碼（bi-encoder），所以文件向量可以事先算好存進向量庫（ChromaDB），再用 metadata 過濾縮小範圍。
3. **切塊（chunking）與索引表示決定檢索上限**：固定長度 → 結構感知（MarkdownHeaderTextSplitter）→ 語義／agentic chunking → contextual retrieval；「搜尋用的單位」和「餵給 LLM 的單位」可以不同（Parent Document Retriever、Document-to-QA、PDF 表格轉 Markdown）。
4. **稀疏（BM25）與稠密（向量）檢索各有盲區，混合檢索用 RRF 依名次融合**：BM25 抓型號、代碼、專有名詞；向量抓同義改寫；兩路分數尺度不同，所以按「名次」而非「分數」融合。
5. **兩階段檢索：bi-encoder 粗召回、cross-encoder 精排**：cross-encoder 把 query 和文件拼在一起過一次 transformer，準但無法預先計算，只能用在少量候選上（Top-K 20–150 → Top-N 3–5）。
6. **從固定流水線到「會檢查自己」的流程：Self-RAG 與 CRAG**：在檢索後加評分節點，決定改寫問題、重查或上網搜尋，這是模組五 Agent／LangGraph 的前奏。

## 素材
### 論點 1：RAG 解決的是「權重是凍結的記憶」，系統分離線／在線兩條鏈路

- **What Is Retrieval-Augmented Generation, aka RAG?** — Rick Merritt / NVIDIA Blog（2023-11 初版、2025-01-31 更新） — https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/（已核實 2026-11-12）
  - 適合程度：完全不用 NLP 前置知識；用「法官（LLM）派書記官（retriever）去法律圖書館找判例」的比喻，一分鐘講完 RAG 動機；也交代了 RAG 一詞出自 Patrick Lewis 2020 年論文。
  - 可借的圖解結構：開場比喻圖——左邊法官（只靠通識）、右邊書記官跑進書庫拿回判例、兩者合成判決；對應到「LLM／retriever／向量庫」三格。
  - 搭橋：LLM 的知識＝訓練後凍結的權重；要更新知識只能重訓或微調（成本高）。RAG 等於不動權重、改輸入，類比「推論時餵額外的條件輸入」。

- **Retrieval and RAG: Architectures and Building Blocks** — LangChain 官方文件（v1） — https://docs.langchain.com/oss/python/langchain/retrieval（已核實 2026-11-12）
  - 適合程度：官方概念頁，先講 LLM 兩個限制（context 有限、訓練資料靜態），再列元件（document loaders、text splitters、embedding models、vector stores、retrievers），名詞定義簡短。
  - 可借的圖解結構：(1) 管線流程圖：資料源 → 載入 → 切塊 → embedding → 向量庫 → retriever → LLM；上半部「建庫」、下半部「查詢」，正好畫成課綱的離線／在線雙鏈路。(2) 2-Step RAG／Agentic RAG／Hybrid RAG 三張小圖＋比較表（控制度、彈性、延遲），可作為本模組收尾、銜接模組五。
  - 搭橋：離線鏈路＝資料前處理＋預先算好特徵（像把整個資料集先過 backbone 存成 feature bank）；在線鏈路＝推論時的查表＋前向傳播。

- **RAG From Scratch**（影片播放清單＋notebooks） — Lance Martin / LangChain — https://github.com/langchain-ai/rag-from-scratch（已核實 2026-11-12；README 內含 YouTube 播放清單連結）
  - 適合程度：一系列 5–10 分鐘短片，從 indexing／retrieval／generation 基礎一路到 query 改寫、multi-representation indexing、CRAG、Self-RAG，每集一張手繪架構圖。程式碼是 2024 年舊版 LangChain，**只借概念與圖，不要照抄程式**。
  - 可借的圖解結構：README 頂部的「RAG 全景圖」：Query Translation → Routing → Query Construction → Indexing → Retrieval（含 Refinement、CRAG）→ Generation（含 Self-RAG），適合當模組三的目錄頁／地圖頁。
  - 搭橋：把整門模組畫成一張可以逐格點亮的地圖，每講完一個論點就點亮一格。

### 論點 2：文字 embedding＝預訓練 encoder 的特徵向量；向量庫與 metadata 過濾

- **The Illustrated Word2vec** — Jay Alammar（2019-03-27） — https://jalammar.github.io/illustrated-word2vec/（已核實 2026-11-12）
  - 適合程度：從「用兩個數字描述一個人的個性」開始，一步步推到詞向量，完全不預設 NLP 知識；Jay Alammar 是公認最會畫 ML 圖解的作者。
  - 可借的圖解結構：(1) 個性向量：兩軸平面上的人物箭頭，用 cosine 比誰最像；(2) king − man + woman ≈ queen 的向量算術；(3) embedding 矩陣查表：輸入詞 → 取出對應的一列。
  - 搭橋：學生熟悉的 `nn.Embedding` 正是「查表取一列」；word2vec 就是用「預測鄰近詞」這個代理任務去訓練那張表，跟自監督預訓練同一套路。

- **Sentence Transformers: Meanings in Disguise** — Pinecone Learning Center（NLP for Semantic Search 系列） — https://www.pinecone.io/learn/series/nlp/sentence-embeddings/（已核實 2026-11-12）
  - 適合程度：從 RNN encoder-decoder、attention 一路講到 BERT、SBERT，有說明 mean pooling 與 siamese 訓練；對懂 NN 的人剛好補上「詞向量 → 句向量」的缺口。
  - 可借的圖解結構：(1) BERT 句子池化圖：token embeddings → mean pooling → 一個 768 維句向量；(2) siamese 訓練圖：兩句各自過同一個 BERT 得到 u、v，接 (u, v, |u−v|) → softmax 分類；(3) 相似度熱力圖（5 句兩兩 cosine）。
  - 搭橋：siamese network／共享權重、mean pooling（類比 CNN 的 global average pooling）、softmax 交叉熵當訓練目標——全部是學生已知的元件。

- **Metadata Filtering** — Chroma 官方文件 — https://docs.trychroma.com/docs/querying-collections/metadata-filtering（已核實 2026-11-12）
  - 適合程度：純 API 頁，但範例短：`where={"$and": [{"page": {"$gte": 5}}, {"page": {"$lte": 10}}]}`，加 `where_document={"$contains": ...}` 做文字過濾，直接對應 Lab 3「綁定文檔版本、模組名稱」。
  - 可借的圖解結構：「先過濾、再算相似度」漏斗圖：整個 collection → metadata 條件砍掉不符的 → 剩下的做向量近鄰。
  - 搭橋：等同訓練資料的 mask／條件索引；過濾縮小搜尋空間，相似度才在對的子集合裡比。

### 論點 3：切塊與索引表示決定檢索上限

- **5 Levels Of Text Splitting**（Jupyter notebook＋配套影片） — Greg Kamradt / FullStackRetrieval-com — https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb（已核實 2026-11-12；GitHub 網頁版預覽載入慢，raw 檔可下載）
  - 適合程度：本主題被引用最多的入門教材。LangChain 的 SemanticChunker 程式碼註明取自這份 notebook。五級：Character → Recursive → Document Specific（含「PDF 表格」小節）→ Semantic Chunking → Agentic Chunking；另有 Bonus「Alternative Representation／Hypothetical Questions」，直接對應課綱的 Document-to-QA。一份涵蓋課綱 4 個點。
  - 可借的圖解結構：(1) 五級階梯圖；(2) Level 4 的「相鄰句子 embedding 距離折線圖」：x 軸句子序號、y 軸 cosine 距離，超過百分位門檻的峰值就是切點；(3) Level 5：LLM 把段落改寫成獨立命題（proposition），再決定歸入哪個 chunk。
  - 搭橋：semantic chunking 的切點偵測＝在時間序列上找訊號突變（change-point detection），門檻用百分位數設定，跟調 threshold 一樣。

- **Introducing Contextual Retrieval** — Anthropic（2024-09-19） — https://www.anthropic.com/engineering/contextual-retrieval（已核實 2026-11-12；舊網址 anthropic.com/news/contextual-retrieval 本次抓取失敗，請用 engineering 路徑）
  - 適合程度：問題講得具體（chunk「該公司營收成長 3%」不知道是哪家公司），解法簡單（用 LLM 為每個 chunk 寫 50–100 token 的情境前綴再 embedding／建 BM25），而且有量化結果。同一篇也順帶畫了 embedding＋BM25 混合與 rerank，可同時支援論點 4、5。
  - 可借的圖解結構：(1) 前處理流程圖：整份文件＋單一 chunk → LLM 生成情境句 → 情境句＋chunk → 同時進向量索引和 BM25 索引；(2) 堆疊長條圖：Top-20 檢索失敗率基線 5.7% → contextual embeddings 3.7%（−35%）→ ＋contextual BM25 2.9%（−49%）→ ＋rerank 1.9%（−67%）。
  - 搭橋：等於做資料增強——不改模型，改輸入讓特徵更具辨識度；成本約每百萬文件 token 1.02 美元（靠 prompt caching）。

- **Parent-Child Retriever**（GraphRAG Pattern Catalog） — Neo4j / graphrag.com（CC BY 4.0） — https://graphrag.com/reference/graphrag/parent-child-retriever/（已核實 2026-11-12）
  - 適合程度：官方 LangChain 的 Parent Document Retriever 教學頁已下線（見事實核實），這頁是目前最乾淨的概念說明：小 chunk 拿來 embedding 才準，但生成時需要大段上下文，所以「搜小的、回傳大的」。四步驟清楚，另附可選的「同一 parent 的分數取 max／平均」。
  - 可借的圖解結構：兩層樹：Parent chunk（約 1–2k token）下掛數個 child chunk（約 100–400 token）；只有 child 進向量索引，查到 child 後沿 `HAS_CHILD` 邊往上取 parent，並對同一 parent 去重。
  - 搭橋：類比偵測模型用小 anchor 精準定位、再裁出較大的 ROI 做後續處理；也可預告模組四——這已經是一個「圖」。

### 論點 4：BM25 與向量檢索互補，混合檢索用 RRF 融合

- **Hybrid Search Explained** — Erika Shorten / Weaviate Blog（2025-01-27） — https://weaviate.io/blog/hybrid-search-explained（已核實 2026-11-12）
  - 適合程度：一篇講完 BM25（TF-IDF＋文件長度懲罰）、dense vector、兩種融合法（RRF、relativeScoreFusion）與 alpha 權重；例子好記：「How to catch an Alaskan Pollock」——向量懂 catch＝釣魚，關鍵字抓得到 Alaskan Pollock 這個專有名詞。
  - 可借的圖解結構：(1) RRF 計算表：文件 A/B/C 在 BM25 與 dense 各自的名次 → 融合分數（B 1.5、A 1.3、C 0.83），可重畫成兩欄名次＋連線＋合併結果；(2) alpha 滑桿：0＝純關鍵字、0.5＝各半、1＝純向量。
  - 搭橋：兩路分數尺度不同（BM25 無上界、cosine 介於 −1～1），直接相加就像把沒標準化的特徵相加；RRF 只看名次，等於先做 rank normalization。

- **Practical BM25 — Part 2: The BM25 Algorithm and its variables** — Shane Connelly / Elastic Blog（2018-04-19） — https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables（已核實 2026-11-12）
  - 適合程度：逐項拆公式：IDF（稀有詞權重高）、k1（詞頻飽和，預設 1.2）、b（長度正規化，預設 0.75），每個變數配一個例子。
  - 可借的圖解結構：詞頻飽和曲線：x 軸詞頻、y 軸分數貢獻，TF-IDF 線性上升 vs BM25 漸近飽和。
  - 搭橋：k1 的飽和效果像 sigmoid／tanh 的壓縮；b 像依樣本長度做的正規化。BM25 不需要訓練，是一個「手工設計特徵」的 baseline，可對照 CNN 之前的 SIFT/HOG。

- **Reciprocal rank fusion** — Elasticsearch 官方參考文件 — https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion（已核實 2026-11-12）
  - 適合程度：公式 `score = Σ 1/(k + rank)` 加完整手算例子（5 份文件、兩路名次），學生可以照著在投影片上算一遍。
  - 可借的圖解結構：兩欄名次表（BM25 名次、kNN 名次）→ 每份文件逐項加總 → 最終排序；只出現在一路的文件也會得分。
  - 搭橋：k（預設 60）是平滑常數，作用類似 label smoothing——壓低「第 1 名」與「第 2 名」之間的差距，避免單一路徑主導。

### 論點 5：兩階段檢索——bi-encoder 粗召回、cross-encoder 精排

- **Rerankers and Two-Stage Retrieval** — Pinecone Learning Center（Retrieval Augmented Generation 系列） — https://www.pinecone.io/learn/series/rag/rerankers/（已核實 2026-11-12）
  - 適合程度：先講「為何不能把檢索到的全塞進 context」（召回率 vs LLM 使用 context 的能力），再講兩階段解法與成本：小型 BERT reranker 對 4,000 萬筆逐一打分要 50 小時以上，向量搜尋不到 100 ms。
  - 可借的圖解結構：(1) 兩階段漏斗：百萬文件 → 向量庫召回 Top-25 → reranker → Top-3 → LLM；(2) bi-encoder 圖（query、doc 各自壓成一個向量）vs reranker 圖（query＋doc 一起進 transformer 輸出一個分數）。
  - 搭橋：bi-encoder＝siamese network，可預算；cross-encoder＝把兩張圖 concat 後進同一個網路做 early fusion，資訊不先被壓縮所以準，但每對都要重算。也可類比 two-stage detector（RPN 粗提案 → head 精修）。

- **Cross-Encoders（Applications）** — Sentence Transformers 官方文件（sbert.net） — https://sbert.net/examples/cross_encoder/applications/README.html（已核實 2026-11-12）
  - 適合程度：一張 Bi-Encoder vs Cross-Encoder 對照圖＋一句結論「需要可索引的向量用 bi-encoder，固定的一組 pair 要打分用 cross-encoder」；附「1 萬句分群：cross-encoder 約 65 小時 vs bi-encoder 5 秒」。
  - 可借的圖解結構：左右對照圖——左：句 A、句 B 各過 BERT → pooling → u、v → cosine；右：[A; SEP; B] 一起過 BERT → 分類頭 → 0～1 分數。
  - 搭橋：右圖就是一個二元分類器（sigmoid 輸出），學生秒懂；bge-reranker 正是這種架構（見事實核實）。

- **Advanced RAG on Hugging Face documentation using LangChain**（Cookbook notebook） — Aymeric Roucher / Hugging Face Open-Source AI Cookbook — https://huggingface.co/learn/cookbook/advanced_rag（已核實 2026-11-12）
  - 適合程度：全開源模型的完整 RAG：token 為單位的切塊（512、overlap 1/10）、gte-small embedding、FAISS、zephyr-7b reader、召回 30 → ColBERTv2 rerank 取 5；作者強調「先建評估集再調參」。適合學生課後照做。
  - 可借的圖解結構：RAG 全流程圖，用藍色標出「可調的旋鈕」（切塊大小、embedding 模型、top_k、是否 rerank、prompt、reader 模型）——適合做「調參地圖」投影片。
  - 搭橋：把 RAG 當成一條有超參數的 pipeline 來調，跟調學習率、batch size 同一種思維，而且要有 validation set。

### 論點 6：Self-RAG 與 CRAG——在流水線中加入「自我檢查」

- **Self-Reflective RAG with LangGraph** — Ankush Gola / LangChain Blog（2024-02-07） — https://www.langchain.com/blog/agentic-rag-with-langgraph（已核實 2026-11-12；舊網址 blog.langchain.com/agentic-rag-with-langgraph/ 會 301 轉到這裡）
  - 適合程度：同一篇對照 CRAG 與 Self-RAG，並說明「論文要訓練特殊 token，工程上改用獨立的評分節點＋條件分支」——這正是課堂上要做的簡化。
  - 可借的圖解結構：(1) CRAG 流程圖：Retrieve → Grade documents（逐份二元判斷）→ 有不相關就 Rewrite query → Web search → Generate；(2) Self-RAG 流程圖：Retrieve → Grade → 全不相關則改寫重查 → Generate → 幻覺檢查（答案有無被文件支持）→ 答案是否回答問題 → 不行就回到改寫。兩張圖都是「節點＋菱形判斷＋回圈」，可直接當模組五 LangGraph 狀態圖的預告。
  - 搭橋：評分節點就是一個小分類器（相關／不相關）；回圈像訓練迴圈裡的 early stopping 條件判斷。

- **Self-RAG: Learning to Retrieve, Generate and Critique through Self-Reflection**（官方專案頁） — Akari Asai 等 / University of Washington（ICLR 2024） — https://selfrag.github.io（已核實 2026-11-12）
  - 適合程度：比讀論文輕；三步驟（Retrieve／Generate／Critique）各一段文字，搭一張 teaser 圖與 reflection token 表。
  - 可借的圖解結構：reflection token 四類表：Retrieve（要不要查）、ISREL（文件相關嗎）、ISSUP（答案有被支持嗎）、ISUSE（有用程度 1–5）；可畫成生成序列中插入的彩色特殊 token。
  - 搭橋：Self-RAG 是把「評估」直接訓練進模型的輸出詞表（多加幾個類別的 softmax），對照 LangGraph 版本是「外掛分類器」。兩種做法的取捨＝端到端訓練 vs 模組化。

- **Corrective RAG (CRAG)** — Cobus Greyling / Substack（2024-02-05，免登入可讀全文） — https://cobusgreyling.substack.com/p/corrective-rag-crag（已核實 2026-11-12）
  - 適合程度：把 CRAG 論文的三個關鍵元件講白：輕量 retrieval evaluator 給信心分數 → Correct／Incorrect／Ambiguous 三條路 → decompose-then-recompose 把文件拆細、濾掉雜訊。
  - 可借的圖解結構：三岔路圖：evaluator 信心高 → 精煉內部文件；低 → 丟棄並上網搜尋；中間 → 兩者合併。
  - 搭橋：evaluator 的信心門檻＝分類器的 decision threshold；三分類取代二分類以處理「不確定」區間。

### 備選素材（已核實，但超出「每論點 1–3 份」上限，必要時替換上面的條目）

- [論點 1] **What is Retrieval-Augmented Generation (RAG)?** — Marina Danilevsky / IBM Technology（YouTube） — https://www.youtube.com/watch?v=T-D1OfcDW1M（已核實 2026-11-12，oEmbed 可取得）：白板手繪，講「LLM 會過時、不給出處」兩個問題，再引出 RAG；可直接當課前影片。
- [論點 1] **Introduction to RAG** — LlamaIndex 官方文件 — https://developers.llamaindex.ai/python/framework/understanding/rag/（已核實 2026-11-12）：把 RAG 拆成 Loading／Indexing／Storing／Querying／Evaluation 五階段，每個術語（Document、Node、Retriever、Node Postprocessor、Response Synthesizer）各一句話定義，適合做名詞表。
- [論點 2] **Vector embeddings（Embeddings guide）** — OpenAI API 官方文件 — https://developers.openai.com/api/docs/guides/embeddings（已核實 2026-11-12；舊網址 platform.openai.com/docs/guides/embeddings 已 301 轉址）：一頁講清楚「維度」「距離函數」兩個工程問題：text-embedding-3-small 預設 1536 維、-large 3072 維，可用 `dimensions` 參數縮短；向量已正規化成長度 1，所以 cosine＝內積。
- [論點 3] **Chunking Strategies for LLM Applications** — Roie Schwaber-Cohen、Arjun Patel / Pinecone Learning Center（2025-06-28） — https://www.pinecone.io/learn/chunking-strategies/（已核實 2026-11-12）：把切塊方法排成一條光譜：固定長度 → 句子／段落 → 遞迴字元切分（RecursiveCharacterTextSplitter）→ 文件結構（Markdown、HTML、LaTeX、PDF）→ semantic chunking → 用 LLM 做 contextual chunking；也談「切塊大小要配合 embedding 模型的 context window」。注意：本文**沒有**介紹 agentic chunking。
- [論點 3] **Docling 文件** — IBM Research Zurich 發起、LF AI & Data Foundation 託管 — https://docling-project.github.io/docling/（已核實 2026-11-12）：說明 PDF 解析要處理版面、閱讀順序、表格結構、公式，輸出可選 Markdown，直接對應課綱「表格 Markdown 結構化轉換」；開源，Lab 可直接用。

## 事實核實

- **`MarkdownHeaderTextSplitter`**：在 `langchain-text-splitters` 套件（最新 1.1.3，2026-10-02），`from langchain_text_splitters import MarkdownHeaderTextSplitter`；參數 `headers_to_split_on=[("#","Header 1"), ...]`，`strip_headers` **預設 True**（標題從 chunk 內文移除、只留在 metadata）。與課綱一致；但若想讓 embedding 吃到章節脈絡，需設 `strip_headers=False` 或手動把 metadata 標題拼回內文。出處：https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter 、PyPI wheel 檢查。
- **`ParentDocumentRetriever`（LangChain 1.x）**：LangChain v1（`langchain` 最新 1.5.0，2026-11-11）把舊的 `langchain.retrievers` 整包移到 `langchain-classic`（最新 1.0.8）。目前位置 `from langchain_classic.retrievers import ParentDocumentRetriever`（wheel 內確認有 `langchain_classic/retrievers/parent_document_retriever.py`）。舊的 how-to 教學頁 python.langchain.com/docs/how_to/parent_document_retriever 已 308 轉址到 v1 總覽頁，**官方教學已不存在**，只剩 API reference。出處：https://docs.langchain.com/oss/python/migrate/langchain-v1 、https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever 。**與課綱不一致**：課綱把它當主流元件介紹，實際上是 legacy。
- **`EnsembleRetriever`（混合檢索）**：同樣在 `langchain_classic.retrievers.ensemble`，實作是「加權 RRF」，常數 `c=60`。出處：https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever 、wheel 原始碼。
- **Semantic chunking 工具**：LangChain 的 `SemanticChunker` 在 `langchain_experimental.text_splitter`，而 `langchain-experimental` README 標示「**is being sunset**」（最新 0.4.2，2026-05-22）。目前仍可用的替代：LlamaIndex `SemanticSplitterNodeParser`（`buffer_size=1, breakpoint_percentile_threshold=95`）。出處：https://github.com/langchain-ai/langchain-experimental 、https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/ 。
- **Agentic chunking**：沒有任何主流框架提供標準 API；Pinecone 的切塊指南也沒有收錄。主要參考仍是 Greg Kamradt 的 notebook（proposition-based）。**與課綱不一致**：課綱寫「基於語義段落邊界由模型自動判斷」，混用了 semantic chunking（以 embedding 距離找切點，不用 LLM）與 agentic chunking（由 LLM 判斷）兩件事。
- **ChromaDB 目前 API**：`chromadb` 最新 1.5.9（2026-05-05）；`client.get_or_create_collection`、`collection.add(documents, metadatas, ids)`、`collection.query(query_texts, n_results, where, where_document)` 仍是主要介面；本地持久化用 `chromadb.PersistentClient(path=...)`。metadata 運算子：`$eq $gt $gte $lte $in $nin $and $or`，陣列型 metadata 用 `$contains/$not_contains`（文件頁未列出 `$ne`）。**新的 Search API（支援 BM25／SPLADE 稀疏向量＋RRF 原生混合檢索）「available in Chroma Cloud only」**，單機版尚未支援。出處：https://docs.trychroma.com/docs/querying-collections/metadata-filtering 、https://docs.trychroma.com/cloud/search-api/overview 、https://docs.trychroma.com/cloud/search-api/hybrid-search 、https://pypi.org/project/chromadb/ 。**影響課綱**：Lab 3 用本地 Chroma，BM25 必須另外做（`bm25s` 0.3.16 或 `rank-bm25`，後者 2022 年後未更新），再自行融合。
- **`BAAI/bge-reranker`**：不是一個實際存在的模型 ID。BGE reranker 家族：`bge-reranker-base`、`bge-reranker-large`（xlm-roberta，**僅中英**）、`bge-reranker-v2-m3`（以 bge-m3 為底、多語、Apache-2.0、最常用）、`bge-reranker-v2-gemma`、`bge-reranker-v2-minicpm-layerwise`（LLM 型，較重）。用法：`FlagEmbedding.FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True).compute_score([q, p], normalize=True)`（normalize 套 sigmoid 映到 0–1）；也可用 sentence-transformers 的 `CrossEncoder` 載入。`FlagEmbedding` 最新 1.4.2（2026-08-24）。出處：https://huggingface.co/BAAI/bge-reranker-v2-m3 。**與課綱不一致**：需指定為 `BAAI/bge-reranker-v2-m3`（課綱強調跨語種，base/large 只支援中英）。
- **`bge-m3`**：1024 維、最長 8192 token、100+ 語言、MIT 授權；同一個模型可同時輸出 dense、sparse（lexical weights）、multi-vector（ColBERT）三種表示。與課綱「跨語種用 bge-m3」一致；補充：它本身就能產出稀疏權重，可作為 BM25 之外的另一條混合檢索路線。出處：https://huggingface.co/BAAI/bge-m3 。
- **`text-embedding-3`**：仍是 OpenAI 目前列出的最新 embedding 系列（small 1536 維／large 3072 維，皆可用 `dimensions` 縮短，最大輸入 8192 token），沒有更新的型號。與課綱一致。出處：https://developers.openai.com/api/docs/guides/embeddings 。
- **Contextual Retrieval 數字**：Top-20 失敗率 5.7% → 3.7%（−35%，contextual embeddings）→ 2.9%（−49%，＋contextual BM25）→ 1.9%（−67%，＋rerank，從 150 取 20）。出處：https://www.anthropic.com/engineering/contextual-retrieval 。課綱未提此技術，但在本次素材範圍內。
- **RRF 常數**：Elasticsearch `rank_constant` 預設 60；Chroma Cloud `Rrf` 的 k 預設 60；Weaviate 也用 60；LangChain `EnsembleRetriever` `c=60`。出處：見上列各文件。

## 投影片建議

1. **Lab 3 的「各召回 Top-5 再集合去重」改成 RRF 融合**。去重只是聯集，沒有排序依據，接著做 rerank 時也看不出「兩路都命中」的訊號。用 `EnsembleRetriever`（加權 RRF，c=60）或 10 行手寫 RRF 就能做，而且 RRF 的手算例子本身就是很好的投影片。順便把召回數拉到各 10–20，與課綱自己寫的「Top-K 10–20 粗篩」一致。
2. **把「semantic chunking」與「agentic chunking」拆成兩張投影片**。semantic＝相鄰句 embedding 距離＋門檻找切點（不用 LLM，可用變化點偵測類比）；agentic＝讓 LLM 判斷命題歸屬（成本高、無標準 API）。再接 Anthropic 的 contextual retrieval 當作「最務實的 LLM 加持切塊法」，因為它有量化結果、實作簡單。
3. **Reranker 統一寫成 `BAAI/bge-reranker-v2-m3`，並用「bi-encoder＝siamese、cross-encoder＝早期融合的二元分類器」講原理**。這群學生最快的理解路徑是架構圖對照，而不是 NLP 術語；一張 sbert.net 風格的左右對照圖就夠。
4. **ParentDocumentRetriever 講「模式」而不是講「類別」**。在 LangChain 1.x 它已經是 `langchain_classic` 的 legacy 元件，官方教學頁也已下線；投影片用 graphrag.com 的「搜小回大」兩層樹圖解，Lab 用 Chroma＋dict（或 LangChain `InMemoryStore`）手寫 parent 映射，學生反而更清楚機制，也不受套件異動影響。
5. **在第一段就把「RAG vs 微調」講成「改輸入 vs 改權重」**。學生懂遷移學習與 fine-tune，這是最強的搭橋點：RAG 適合會變的事實、需要出處的答案；微調適合改格式與風格（銜接模組六）。課綱目前直接從「三大痛點」切入，缺這個動機鋪陳。
