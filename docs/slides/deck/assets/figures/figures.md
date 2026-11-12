# 實物素材總表

合併自 `figures-papers.md`（論文、演講）與 `figures-docs.md`（官方文件圖、logo）；兩份原檔保留。清單外的圖不准上投影片（見 BRIEF「實物層」）。

- **direct**：可放原圖，`.src` 寫出處與授權
- **redraw**：原圖只在 `_ref/` 供對照，投影片上用真實數據或結構重畫
- **link**：只放標題＋網址
- **Logo 暫緩**：Docker、Anthropic、OpenAI、Neo4j 條款未確認或要求事先授權，工具頁先用文字；PostgreSQL 不可和其他 logo 並排

---

# 論文／演講實物素材清單（figures-papers.md）

核實日：2026-11-12。範圍：模組一至六的論文架構圖、論文數據、公開演講投影片。

## 讀這份清單前

- **授權判斷依據**：每篇都抓 `arxiv.org/abs/<id>` 頁面 HTML，讀其中的授權連結（CC BY 4.0 → `direct`；`arxiv.org/licenses/nonexclusive-distrib/1.0` → `redraw`）。arXiv 授權標在「最新版」，下表即以最新版為準。
- **圖檔來源**：CC BY 論文的圖，取自 arXiv 原始 LaTeX 檔（`arxiv.org/e-print/<id>`）裡的圖檔，PDF 圖以 `pdftoppm -cropbox` 轉成 PNG（≥2000px 寬）。GraphRAG Fig. 1 是 TikZ 直接畫在論文裡、沒有獨立圖檔，所以從論文 PDF 第 4 頁 350dpi 渲染後裁出圖框。
- **頁碼**：一律是 arXiv PDF 的頁碼（最新版）。表號、圖號用論文自己的編號。
- **`redraw` 的 `_ref/` 圖**：僅供重繪時對照，**不准上投影片**。
- **既有檔案**：`m3/_ref/d-cr-*.png`、`m5/_ref/d-bea-*.png`、`m7/`、`logos/` 不是這份清單產生的，沒動。
- **圖號對照**：圖號、表號以論文 PDF 內文為準，並與 arXiv HTML 版的圖說交叉比對過。

## 統計

| 模組 | 項數 | direct | redraw | link |
|---|---|---|---|---|
| 一 | 8 | 0 | 5 | 3 |
| 二 | 5 | 4 | 0 | 1 |
| 三 | 6 | 1 | 5 | 0 |
| 四 | 2 | 2 | 0 | 0 |
| 五 | 5 | 3 | 1 | 1 |
| 六 | 8 | 5 | 2 | 1 |
| 合計 | 34 | 15 | 13 | 6 |

（一項＝一張圖或一頁數據。Karpathy 的投影片拆成 4 項（模組一 2、二 1、五 1）、CS25 拆成 2 項，因為每項對應不同模組、不同頁。已下載到 `assets/figures/` 的圖：direct 圖 11 張（可上投影片）、redraw 對照圖 8 張（放 `_ref/`，不上投影片），共 19 張；`link` 項不下載。）

## 目標清單核實結果（我記憶中的編號全部正確，沒有找不到的）

| 目標 | arXiv | 標題（已核實） | 授權 |
|---|---|---|---|
| Attention Is All You Need | 1706.03762 | Attention Is All You Need | arXiv 預設 → redraw |
| Lost in the Middle | 2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | arXiv 預設 → redraw |
| Chain-of-Thought | 2201.11903 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | CC BY 4.0 → direct |
| Tree of Thoughts | 2305.10601 | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | CC BY 4.0 → direct |
| RAG | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | arXiv 預設 → redraw |
| Self-RAG | 2310.11511 | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | CC BY 4.0 → direct |
| CRAG | 2401.15884 | Corrective Retrieval Augmented Generation | arXiv 預設 → redraw |
| GraphRAG | 2404.16130 | From Local to Global: A Graph RAG Approach to Query-Focused Summarization | CC BY 4.0 → direct |
| ReAct | 2210.03629 | ReAct: Synergizing Reasoning and Acting in Language Models | CC BY 4.0 → direct |
| LoRA | 2106.09685 | LoRA: Low-Rank Adaptation of Large Language Models | arXiv 預設 → redraw |
| QLoRA | 2305.14314 | QLoRA: Efficient Finetuning of Quantized LLMs | CC BY 4.0 → direct |
| LoRA Learns Less and Forgets Less | 2405.09673 | LoRA Learns Less and Forgets Less | CC BY 4.0 → direct |
| 綜述（另找） | 2308.11432 | A Survey on Large Language Model based Autonomous Agents | CC BY 4.0 → direct |

## 授權與使用注意（先看這段）

1. **ToT Fig. 1 的標號是原文筆誤**：圖下方寫 (a) IO、(c) CoT、(c) CoT-SC、(d) ToT（CoT 的標號應為 b）。直接放原圖時，旁邊口頭或標註註明「圖中兩個 (c) 是原文筆誤」，避免學生以為自己看錯。
2. **Wang et al. 綜述 Fig. 2 含第三方元素**：頂端有 OpenAI logo、下方有 stock 小圖示。CC BY 4.0 涵蓋論文本身，不一定涵蓋這些第三方素材。放原圖前建議裁掉頂端 logo 列與四欄的小圖示，只留四欄文字結構，或乾脆改用 redraw。
3. **Lilian Weng 的文章沒有授權聲明**（頁尾只有 `© 2026 Lil'Log`），圖與文都按 `redraw` 處理；而且該文章並沒有引用 Wang et al. 綜述，這兩者是各自獨立的資源，不要在投影片上寫成「Weng 引用」。
4. **Contextual Retrieval 是 Anthropic 部落格**，頁面沒有授權聲明 → `redraw`，只用文章裡的數字重畫。`m3/_ref/d-cr-*.png` 是別的任務放的部落格原圖，僅供對照。
5. **Karpathy、CS25 投影片沒有授權聲明**，且內含第三方圖（例如 CS25 第 30 頁的 Transformer 圖與變形金剛玩具照、第 91 頁整張 ToT Fig. 1）→ 一律 `link`，不下載進 deck。
6. **CS336 投影片所在 repo 掛 MIT 授權**（GitHub API 回報 `stanford-cs336/spring2025-lectures`: MIT），但投影片內嵌第三方圖，所以仍只用結構 `redraw`，原圖不上投影片。
7. **數據頁的 `direct`／`redraw`**：數字本身是事實，不受授權限制；標 `redraw` 的論文，數據頁一樣可以用，只是 `.src` 要寫「依 ○○ Table N 重繪」，且不放原圖。

---

# 模組一：從深度學習到 LLM

### m1-transformer-fig1
- 檔案：assets/figures/m1/_ref/p-transformer-fig1.png（1520×2239，僅供重繪參考）
- 來源：Vaswani et al.（2017）〈Attention Is All You Need〉Fig. 1，p.3 — https://arxiv.org/abs/1706.03762 （已核實 2026-11-12）
- 授權：redraw — arXiv 頁標 arXiv.org perpetual non-exclusive license
- 建議用在：111-transformer-block 之後的 160 原圖對照（用 rough.js 重畫左右兩半，並圈出 Multi-Head Attention、Add & Norm、Feed Forward、Positional Encoding）
- 頁型：原圖對照
- 給學生的一句話：左半 encoder、右半 decoder，每一塊裡的「Multi-Head Attention ＋ Feed Forward ＋ 殘差加正規化」就是你剛學的那一層；GPT 類模型只留右半（decoder）。

### m1-transformer-complexity
- 檔案：無（數字與符號重繪）
- 來源：Vaswani et al.（2017）〈Attention Is All You Need〉Table 1，p.6 — https://arxiv.org/abs/1706.03762 （已核實 2026-11-12）
- 授權：redraw — arXiv 預設授權；只用表內的複雜度符號重畫
- 建議用在：112-context-cost 之後的 165 數據比較（四種層的複雜度並排）
- 頁型：數據比較
- 可用數據（Table 1，n＝序列長度，d＝表示維度，k＝卷積核大小，r＝受限自注意力鄰域大小）：
  - Self-Attention：每層複雜度 O(n²·d)；循序操作數 O(1)；最大路徑長度 O(1)
  - Recurrent：O(n·d²)；O(n)；O(n)
  - Convolutional：O(k·n·d²)；O(1)；O(log_k(n))
  - Self-Attention (restricted)：O(r·n·d)；O(1)；O(n/r)
  - 補充（Table 2，p.8，EN-DE BLEU／訓練成本 FLOPs）：Transformer (base) 27.3／3.3·10¹⁸；Transformer (big) 28.4／2.3·10¹⁹；ConvS2S Ensemble 26.36／7.7·10¹⁹；GNMT+RL Ensemble 26.30／1.8·10²⁰
- 給學生的一句話：自注意力對 n 是平方，RNN 對 n 是線性——但前者一步就能連到任何位置（路徑長度 O(1)），而且能平行算；這就是 context 越長越貴、卻比 RNN 好訓的原因。

### m1-lostmiddle-fig1
- 檔案：assets/figures/m1/_ref/p-lostmiddle-fig1.png（1807×1696）、assets/figures/m1/_ref/p-lostmiddle-fig5.png（2009×596，三個子圖：10／20／30 份文件）。僅供重繪參考
- 來源：Liu et al.（2023）〈Lost in the Middle: How Language Models Use Long Contexts〉Fig. 1（p.1）、Fig. 5（p.5） — https://arxiv.org/abs/2307.03172 （已核實 2026-11-12）
- 授權：redraw — arXiv 頁標 arXiv.org perpetual non-exclusive license
- 建議用在：112-context-cost 之後、113-no-memory 之前的 161 原圖對照（只畫 GPT-3.5-Turbo 那一條 U 形曲線加紅色虛線 closed-book 56.1）
- 頁型：原圖對照
- 給學生的一句話：答案放在第 1 篇或最後 1 篇，模型答得最準；放在中間，準確率掉到比「完全不給文件」（紅虛線）還低——context window 大不等於每個位置都看得清楚。

### m1-lostmiddle-data
- 檔案：無（數字重繪；圖見上一項）
- 來源：Liu et al.（2023）〈Lost in the Middle〉Table 1（p.5）、Table 5／6／7（附錄 G，p.18） — https://arxiv.org/abs/2307.03172 （已核實 2026-11-12）
- 授權：redraw — arXiv 預設授權；只用表內數字重畫折線
- 建議用在：161 之後的 166 數據比較
- 頁型：數據比較
- 可用數據（多文件問答準確率；「Index n」＝含答案的文件排在第 n+1 位）：
  - Table 1（p.5）closed-book／oracle：LongChat-13B (16K) 35.0%／83.4%；MPT-30B-Instruct 31.5%／81.9%；GPT-3.5-Turbo 56.1%／88.3%；GPT-3.5-Turbo (16K) 56.0%／88.6%；Claude-1.3 48.3%／76.1%；Claude-1.3 (100K) 48.2%／76.4%
  - Table 6（p.18）20 份文件（~4K tokens），Index 0／4／9／14／19：
    - GPT-3.5-Turbo 75.8／57.2／53.8／55.4／63.2（%）
    - GPT-3.5-Turbo (16K) 75.7／57.3／54.1／55.4／63.1
    - Claude-1.3 59.9／55.9／56.8／57.2／60.1
    - Claude-1.3 (100K) 59.8／55.9／57.0／57.4／60.0
    - MPT-30B-Instruct 53.7／51.8／52.2／52.7／56.3
    - LongChat-13B (16K) 68.6／57.4／55.3／52.5／55.0
  - Table 5（p.18）10 份文件，Index 0／4／9：GPT-3.5-Turbo 76.8／61.2／62.4；Claude-1.3 62.9／58.3／59.7；MPT-30B-Instruct 60.2／56.2／59.7；LongChat-13B (16K) 72.1／58.9／58.5
  - Table 7（p.18）30 份文件，Index 0／4／9／14／19／24／29：GPT-3.5-Turbo (16K) 73.4／55.1／50.5／50.9／51.8／54.9／63.7；Claude-1.3 59.1／55.1／54.8／55.7／56.4／56.2／59.9；MPT-30B-Instruct 51.6／51.3／51.2／49.0／49.6／51.3／54.1；LongChat-13B (16K) 66.9／54.8／52.5／52.9／52.2／51.3／55.1
  - 原文結論（p.5）：「GPT-3.5-Turbo's multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document settings is lower than performance without any input documents (i.e., closed-book performance; 56.1%)」
- 給學生的一句話：Table 6 第一列就是答案：GPT-3.5 在第 10 位只剩 53.8%，比不給文件的 56.1% 還低——檢索回來的片段排哪裡，直接影響答對率。

### m1-cs336-l3-modern-block
- 檔案：assets/figures/m1/_ref/p-cs336-l3-modern-vs-original.png（1920×1080，PDF 第 5 頁；僅供重繪參考）
- 來源：Stanford CS336（Spring 2025）〈Lecture 3: Everything you didn't want to know about LM architecture and training〉第 5 頁「What you implemented – simple, modern variant」 — https://stanford-cs336.github.io/spring2025/ ；PDF：https://github.com/stanford-cs336/spring2025-lectures/blob/main/nonexecutable/2025%20Lecture%203%20-%20architecture.pdf （已核實 2026-11-12；PDF 共 68 頁）
- 授權：redraw — repo 為 MIT，但投影片內嵌第三方論文圖；只用結構重畫（LayerNorm 前置、RoPE、SwiGLU、無 bias）
- 建議用在：111-transformer-block 之後的 170 進階延伸（標「進階」），與 160 原圖並排：2017 原版 vs 現代 LLM 版
- 頁型：進階延伸
- 給學生的一句話：現在的 LLM 不是照 2017 年論文原樣蓋的，主要改了 4 件事：正規化放前面、位置編碼換 RoPE、FFN 換 SwiGLU、拿掉 bias。

### m1-karpathy-nextword
- 檔案：無，link
- 來源：Karpathy（2023）《[1hr Talk] Intro to Large Language Models》投影片第 4 頁（Neural Network：「cat sat on a」→ mat (97%)） — 影片 https://www.youtube.com/watch?v=zjkBMFhNj_g ；投影片 PDF https://drive.google.com/file/d/1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7/view （已核實 2026-11-12；影片 2023-11-22 上傳；PDF 共 45 頁，我下載並逐頁看過文字）
- 授權：link — 影片說明未標授權；投影片未標授權
- 建議用在：107-temperature 之後的 171 進階延伸（只放標題＋網址＋頁碼）
- 頁型：進階延伸
- 給學生的一句話：想看同一件事由 Karpathy 講：一個神經網路只做一件事——給 4 個詞，預測下一個詞（mat 97%）；你在 105 頁看到的 softmax 長條圖就是這個輸出層。

### m1-karpathy-pipeline
- 檔案：無，link
- 來源：Karpathy（2023）《[1hr Talk] Intro to Large Language Models》投影片第 10 頁（Summary: how to train your ChatGPT：Stage 1 預訓練約 10TB 文字、約 6,000 張 GPU、約 $2M、約 12 天 → base model；Stage 2 微調約 100K 高品質問答 → assistant model）；第 2 頁（LLM＝一個參數檔＋約 500 行 C 程式） — 同上連結 （已核實 2026-11-12）
- 授權：link — 未標授權
- 建議用在：114-pretrain-sft 之後的 172 進階延伸（只放標題＋網址＋頁碼）
- 頁型：進階延伸
- 給學生的一句話：預訓練是「每年才做一次的大工程」、微調是「每週就能做一次的小調整」；數字是他 2023 年 11 月的口頭估計，不是實測值，不要當規格抄。

### m1-cs25-v6-overview
- 檔案：無，link
- 來源：Feng & Singh 等（2026-04-02）Stanford CS25 Transformers United V6〈Overview of Transformers〉投影片 — https://web.stanford.edu/class/cs25/ ；投影片 https://drive.google.com/file/d/153Gu4BIfpnn6jj6WmXlsyD7kv702zcrB/view （已核實 2026-11-12；PDF 共 156 頁）
- 授權：link — 課程頁與投影片都未標授權
- 建議用在：這一份橫跨多章的總覽，只在對應章的進階頁放網址與頁碼（PDF 頁碼，非投影片右下角的印刷頁碼，兩者差 1–3）：
  - 模組一：p.30「The Final Transformer」（Vaswani Fig. 1 加變形金剛玩具照，不可轉載）、p.31「RNNs vs. Transformers」→ 111-transformer-block 之後
  - 模組二：p.89–94（CoT、ToT、Program-of-Thought、問題拆解）；p.91 整頁是 ToT Fig. 1 的截圖
  - 模組三：p.68–70「Retrieval Augmented Gen. – Basic Idea」（User Query → LLM → Output，加上 Retriever 與文件的三步動畫）→ 301-bridge
  - 模組五：p.102–107（什麼是 AI agent、自我改進、Reflexion、ReAct）
- 頁型：進階延伸
- 給學生的一句話：Stanford 開給研究生的 Transformer 總覽；上完這一章想要一份 150 頁的全景地圖，就從這份開始。

---

# 模組二：提示詞工程與結構化輸出

### m2-cot-fig1
- 檔案：assets/figures/m2/p-cot-fig1.png（2009×979）
- 來源：Wei et al.（2022）〈Chain-of-Thought Prompting Elicits Reasoning in Large Language Models〉Fig. 1，p.1 — https://arxiv.org/abs/2201.11903 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：204-cot 之後的 260 原圖對照（用 rough.js 圈出藍色「推理步驟」與綠色「最終答案」，拉箭頭到旁邊說明：這塊＝你要在 prompt 裡示範的思考過程）
- 頁型：原圖對照
- 給學生的一句話：左右兩個 prompt 唯一的差別，是範例答案裡有沒有把中間算式寫出來；寫了，模型就跟著一步一步算，最後答對（9），沒寫就直接猜（27）。

### m2-cot-gsm8k-scale
- 檔案：無（數字重繪）
- 來源：Wei et al.（2022）〈Chain-of-Thought Prompting Elicits Reasoning in Large Language Models〉附錄 B Table 2（p.21）、Table 1（p.20） — https://arxiv.org/abs/2201.11903 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：204-cot 之後、與 260 相鄰的 265 數據比較（x 軸＝模型大小，兩條線＝standard 與 CoT）
- 頁型：數據比較
- 可用數據（GSM8K 準確率 %，standard → CoT，附錄 Table 2 p.21）：
  - PaLM：8B 4.9 → 4.1；62B 9.6 → 29.9；540B 17.9 → 56.9
  - LaMDA：420M 2.6 → 0.4；2B 3.6 → 1.9；8B 3.2 → 1.6；68B 5.7 → 8.2；137B 6.5 → 14.3
  - GPT-3：350M 2.2 → 0.5；1.3B 2.4 → 0.5；6.7B 4.0 → 2.4；175B 15.6 → 46.9
  - Codex（code-davinci-002）19.7 → 63.1
  - Table 1（p.20）PaLM 540B 五個資料集 standard → CoT：GSM8K 17.9 → 56.9；SVAMP 69.4 → 79.0；ASDiv 72.1 → 73.9；AQuA 25.2 → 35.8；MAWPS 79.2 → 93.3
  - 前人最佳（finetuning）GSM8K：55（Cobbe et al. 2021，見 Table 1 p.20）
- 給學生的一句話：模型小的時候，加了思考步驟反而更差（LaMDA 8B：3.2 → 1.6）；只有大到某個規模（PaLM 62B 以上）才有效——思維鏈是大模型才有的能力，不是 prompt 本身的魔法。

### m2-tot-fig1
- 檔案：assets/figures/m2/p-tot-fig1.png（2001×986）
- 來源：Yao et al.（2023）〈Tree of Thoughts: Deliberate Problem Solving with Large Language Models〉Fig. 1，p.2 — https://arxiv.org/abs/2305.10601 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：205-tot 之後的 261 原圖對照（四個方法由左到右，圈出 (d) 的綠色路徑＝保留的分支、粉紅＝被剪掉的分支）
- 頁型：原圖對照
- 給學生的一句話：IO、CoT 是一條線，CoT-SC 是多條線最後投票，ToT 是一棵樹——每走一步先評分，爛的分支剪掉（粉紅），好的繼續長（綠）。注意：原圖下方標號是 (a)(c)(c)(d)，兩個 (c) 是論文筆誤。

### m2-tot-game24
- 檔案：無（數字重繪）
- 來源：Yao et al.（2023）〈Tree of Thoughts〉Table 2（Game of 24 Results），p.6 — https://arxiv.org/abs/2305.10601 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：205-tot 之後的 266 數據比較（橫向長條圖）
- 頁型：數據比較
- 可用數據（Game of 24 成功率，GPT-4）：IO prompt 7.3%；CoT prompt 4.0%；CoT-SC (k=100) 9.0%；ToT (b=1) 45%；ToT (b=5) 74%；IO + Refine (k=10) 27%；IO (best of 100) 33%；CoT (best of 100) 49%
  - 同頁文字：「around 60% of CoT samples already failed the task after generating the first step」
- 給學生的一句話：同一個 GPT-4，CoT 只有 4%，ToT 一棵 5 寬的樹到 74%——代價是要多呼叫好幾倍（Fig. 3a 以「走訪節點數」為橫軸比較）。

### m2-karpathy-prompt-injection
- 檔案：無，link
- 來源：Karpathy（2023）《[1hr Talk] Intro to Large Language Models》投影片第 39–42 頁（Prompt injection：Riley Goodside 白字攻擊範例、搜尋結果頁藏指令、Bard 讀共享 Google Doc 後外洩資料）；第 28 頁（System 2：Tree of Thoughts 引用） — 影片 https://www.youtube.com/watch?v=zjkBMFhNj_g ；投影片 PDF https://drive.google.com/file/d/1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7/view （已核實 2026-11-12）
- 授權：link — 未標授權
- 建議用在：206-injection 之後的 270 進階延伸（只放標題＋網址＋頁碼）
- 頁型：進階延伸
- 給學生的一句話：注入不是只發生在聊天框——網頁、共享文件裡的隱藏文字，只要被模型讀進 context，就等於被餵了一條指令。

---

# 模組三：企業級 RAG

### m3-rag-fig1
- 檔案：assets/figures/m3/_ref/p-rag-fig1.png（2003×575，僅供重繪參考）
- 來源：Lewis et al.（2020）〈Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks〉Fig. 1，p.2 — https://arxiv.org/abs/2005.11401 （已核實 2026-11-12）
- 授權：redraw — arXiv 頁標 arXiv.org perpetual non-exclusive license
- 建議用在：301-bridge 之後的 360 原圖對照（重畫四個盒子：Query Encoder → MIPS 檢索 → Document Index → Generator，加上 Marginalize）
- 頁型：原圖對照
- 給學生的一句話：RAG 最早的樣子：query 先經編碼器去文件索引撈出 top-k，再連同 query 一起丟給生成器，最後對各文件的結果做加權（marginalize）。
- 備註：圖中 retriever（非參數）與 generator（參數）的分工，對應課程的「RAG＝改輸入、微調＝改權重」。

### m3-rag-table1
- 檔案：無（數字重繪）
- 來源：Lewis et al.（2020）〈Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks〉Table 1（Open-Domain QA Test Scores），p.6 — https://arxiv.org/abs/2005.11401 （已核實 2026-11-12）
- 授權：redraw — arXiv 預設授權；只用表內數字重畫
- 建議用在：301-bridge 之後的 365 數據比較（Closed Book vs Open Book，NQ 一欄即可）
- 頁型：數據比較
- 可用數據（Exact Match，NQ／WQ；TQA 欄有兩個數字，標準測試集／TQA-Wiki 測試集）：
  - Closed Book：T5-11B 34.5／37.4（TQA −／50.1）；T5-11B+SSM 36.6／44.7（TQA −／60.5）
  - Open Book：REALM 40.4／40.7；DPR 41.5／41.1（TQA 57.9／−）；RAG-Token 44.1／45.5（TQA 55.2／66.1）；RAG-Sequence 44.5／45.2（TQA 56.8／68.0）
  - 同頁文字：RAG 在答案不在任何檢索文件裡時，NQ 仍有 11.8% 準確率（抽取式模型為 0%）
- 給學生的一句話：同樣問答題，把外部文件接進來（NQ 44.5）比把全部知識塞進 110 億參數（34.5）高了 10 分。

### m3-selfrag-fig1
- 檔案：assets/figures/m3/p-selfrag-fig1.png（2983×1579）
- 來源：Asai et al.（2023）〈Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection〉Fig. 1，p.2 — https://arxiv.org/abs/2310.11511 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：315-self-rag-crag 之後的 361 原圖對照（左半＝一般 RAG、右半＝Self-RAG；圈出右半的 Retrieve、Relevant／Irrelevant、Supported 標記與 Step 3 的「批改後挑最好那段」）
- 頁型：原圖對照
- 給學生的一句話：一般 RAG 不管需不需要，一律撈 K 篇塞進去；Self-RAG 讓模型自己決定要不要撈（下方的「寫暑假作文」就不撈），撈回來還要逐篇批改（相關？有依據？），最後只用最好的那一段。

### m3-selfrag-crag-data
- 檔案：無（數字重繪）
- 來源：Asai et al.（2023）〈Self-RAG〉Table 2（p.8）；Yan et al.（2024）〈Corrective Retrieval Augmented Generation〉Table 1（p.7） — https://arxiv.org/abs/2310.11511 ；https://arxiv.org/abs/2401.15884 （已核實 2026-11-12）
- 授權：redraw — 兩篇混在同一頁：Self-RAG 的 arXiv 頁標 CC BY 4.0，CRAG 為 arXiv 預設授權；整頁依較嚴的一方處理，`.src` 寫「依 Asai et al. Table 2、Yan et al. Table 1 重繪」
- 建議用在：315-self-rag-crag 之後的 366 數據比較
- 頁型：數據比較
- 可用數據：
  - Self-RAG Table 2（p.8；PopQA／TriviaQA／PubHealth／ARC-Challenge，皆為準確率 %）：
    - Llama2 7B（不檢索）14.7／30.5／34.2／21.8
    - Llama2 7B（加檢索）38.2／42.5／30.0／48.0
    - Alpaca 7B（加檢索）46.7／64.1／40.2／48.0
    - ChatGPT 29.3／74.3／70.1／75.3；Ret-ChatGPT 50.8／65.7／54.7／75.3
    - Self-RAG 7B 54.9／66.4／72.4／67.3；Self-RAG 13B 55.8／69.3／74.5／73.1
  - CRAG Table 1（p.7；PopQA 準確率／Bio FactScore／PubHealth 準確率／ARC 準確率）：
    - LLaMA2-hf-7b：RAG 50.5／44.9／48.9／43.4；CRAG 54.9／47.7／59.5／53.7
    - SelfRAG-LLaMA2-7b：RAG 52.8／59.2／39.0／53.2；CRAG 59.8／74.1／75.6／68.6；Self-RAG 54.9／81.2／72.4／67.3；Self-CRAG 61.8／86.2／74.8／67.2
- 給學生的一句話：加了「檢索後自我批改」之後，PubHealth 這類容易被雜訊文件帶偏的任務（Llama2 7B 加檢索 30.0）可以拉到 72–75；CRAG 是外掛式的補強，掛在 RAG 或 Self-RAG 上都有加分。

### m3-crag-fig2
- 檔案：assets/figures/m3/_ref/p-crag-fig2.png（2414×1780，僅供重繪參考）
- 來源：Yan et al.（2024）〈Corrective Retrieval Augmented Generation〉Fig. 2（CRAG inference 總覽），p.4 — https://arxiv.org/abs/2401.15884 （已核實 2026-11-12）
- 授權：redraw — arXiv 頁標 arXiv.org perpetual non-exclusive license
- 建議用在：315-self-rag-crag 之後的 362 原圖對照（重畫：檢索評估器分三路：Correct → 精煉知識；Ambiguous → 兩者並用；Incorrect → 改寫查詢、聯網搜尋）
- 頁型：原圖對照
- 給學生的一句話：撈回來的文件先過一個「評分員」：夠好就精煉後使用，不夠好就丟掉、改寫問題上網重找，介於中間就兩邊都用。

### m3-contextual-retrieval
- 檔案：無，數字重繪（部落格原圖別的任務已放在 m3/_ref/d-cr-*.png，僅供對照）
- 來源：Anthropic（2024-09-19）《Introducing Contextual Retrieval》— https://www.anthropic.com/news/contextual-retrieval （已核實 2026-11-12：直接抓頁面 HTML 比對數字）
- 授權：redraw — 頁面無授權聲明，只用文章中的數字重畫，不放原圖
- 建議用在：313-doc-to-qa 之後的 367 數據比較（四根長條：基線 → 加 contextual embeddings → 再加 contextual BM25 → 再加 rerank）
- 頁型：數據比較
- 可用數據（top-20 chunk 檢索失敗率＝1 − recall@20；各知識領域平均；最佳 embedding 設定為 Gemini Text 004）：
  - 標準 embedding 基線 5.7%
  - Contextual Embeddings 3.7%（降 35%，原文「5.7% → 3.7%」）
  - Contextual Embeddings + Contextual BM25 2.9%（降 49%，「5.7% → 2.9%」）
  - 再加 reranking 1.9%（降 67%，「5.7% → 1.9%」；reranking 流程：先取 top 150，再重排取 top 20）
  - 文中一次性成本：每百萬文件 token $1.02（假設 800 token 區塊、8k token 文件、50 token 指令、每區塊補 100 token 上下文，用 prompt caching）
  - 領域：程式碼庫、小說、arXiv 論文、科學論文
- 給學生的一句話：同一個知識庫，只在每個區塊前面補一兩句「這段來自哪份文件的哪一節」，檢索失敗率就從 5.7% 降到 3.7%，加上 BM25 和重排最後到 1.9%。

---

# 模組四：知識圖譜與 GraphRAG

### m4-graphrag-fig1
- 檔案：assets/figures/m4/p-graphrag-fig1.png（1650×1044；由論文 PDF 第 4 頁渲染後裁切，原為 TikZ 向量圖）
- 來源：Edge et al.（2024）〈From Local to Global: A Graph RAG Approach to Query-Focused Summarization〉Fig. 1，p.4 — https://arxiv.org/abs/2404.16130 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：407-two-schools 之後的 460 原圖對照（左欄藍色＝Indexing Time：文件 → 區塊 → 實體與關係 → 知識圖譜；右欄綠色＝Query Time：社群 → 社群摘要 → 社群答案 → 全局答案；圈出中間的「community detection」箭頭）
- 頁型：原圖對照
- 給學生的一句話：左欄是離線建索引（花 LLM 呼叫抽實體、建圖），右欄是線上回答（每個社群各答一次，再彙整成一份）——它回答的是「整份文件講什麼」，不是「某一句話在哪」。

### m4-graphrag-winrate
- 檔案：無（數字重繪）
- 來源：Edge et al.（2024）〈From Local to Global〉Fig. 2（p.10）、Table 2（p.10）、Table 6（附錄 G，p.26）、§5.1 Experiment 1（p.9–10） — https://arxiv.org/abs/2404.16130 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：408-global-search 之後的 465 數據比較（兩個長條組：勝率；token 用量）
- 頁型：數據比較
- 可用數據：
  - 條件代號：SS＝傳統向量 RAG；TS＝全文 map-reduce 摘要（無圖）；C0／C1／C2／C3＝GraphRAG 由根層到最底層的社群摘要
  - Fig. 2（p.10）各條件「勝過 SS（向量 RAG）」的勝率 %，每格為 125 題、每題重複 5 次平均：
    - Podcast 完整性（comprehensiveness）：TS 83；C0 72；C1 75；C2 78；C3 79
    - Podcast 多樣性（diversity）：TS 82；C0 77；C1 75；C2 81；C3 81
    - News 完整性：TS 80；C0 72；C1 75；C2 79；C3 79
    - News 多樣性：TS 67；C0 62；C1 65；C2 71；C3 69
    - 「賦能（empowerment）」結果混雜，原文說兩邊差異不明確；「直接性（directness）」向量 RAG 最高（此為原文用來驗證評分有效的檢查指標）
  - Table 2（p.10）每次查詢用到的 context token：
    - Podcast（上下文單元數／token）：C0 34／26,657；C1 367／225,756；C2 969／565,720；C3 1,310／746,100；TS 1,669／1,014,611
    - News：C0 55／39,770；C1 555／352,641；C2 1,797／980,898；C3 2,142／1,140,266；TS 3,197／1,707,694
    - 佔 TS 的比例：Podcast C0 2.6%、C1 22.2%、C2 55.8%、C3 73.5%；News C0 2.3%、C1 20.7%、C2 57.4%、C3 66.8%
  - Table 6（p.26）精確平均勝率，Podcast 完整性 C0 vs SS 71.92%、C3 vs SS 78.96%、TS vs SS 83.12%
  - 圖規模（p.9）：Podcast 8,564 節點／20,691 邊；News 15,754 節點／19,520 邊
  - 原文結論（p.10）：C0（根層）只需 TS 不到 3% 的 token，仍保有完整性 72%、多樣性 62% 的勝率
- 給學生的一句話：問「整批文件在講什麼」這種全局問題，GraphRAG 各層社群摘要對向量 RAG 的勝率落在 62–81%（完整性與多樣性）；只用最粗那層（C0），token 成本只有全文摘要的 2–3%，勝率也只小幅下降。

---

# 模組五：AI Agent 與 LangGraph

### m5-react-fig1
- 檔案：assets/figures/m5/p-react-fig1.png（2408×1969）
- 裁切版：assets/figures/m5/p-react-fig1-1d-crop.png（1180×612；只截 Fig. 1 右上 (1d) ReAct 格的上半，到 Obs 2 為止，內容未改動；原圖整張字太小，560-react-original 用此裁切版）
- 來源：Yao et al.（2022）〈ReAct: Synergizing Reasoning and Acting in Language Models〉Fig. 1，p.2 — https://arxiv.org/abs/2210.03629 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：503-react-loop 之後的 560 原圖對照（上半 HotpotQA：Standard、CoT、Act-only 都答錯，只有 ReAct 答對；下半 ALFWorld：Act-only 卡在「Nothing happens」，ReAct 先 Think 再行動）
- 頁型：原圖對照
- 給學生的一句話：只推理（CoT）會編造「Apple TV」；只行動（Act）不會規劃而亂搜；Thought／Act／Obs 交錯，才能邊查邊修正方向、最後答對。

### m5-react-data
- 檔案：無（數字重繪）
- 來源：Yao et al.（2022）〈ReAct〉Table 1（p.5）、Table 3（p.8）、Table 4（p.8）、Table 2（p.6） — https://arxiv.org/abs/2210.03629 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：503-react-loop 之後的 565 數據比較（建議只畫 ALFWorld 與 WebShop 兩張，最能看出「有 Thought 比沒有好」）
- 頁型：數據比較
- 可用數據：
  - Table 1（PaLM-540B；HotpotQA EM／Fever 準確率）：Standard 28.7／57.1；CoT 29.4／56.3；CoT-SC 33.4／60.4；Act 25.7／58.9；ReAct 27.4／60.9；CoT-SC → ReAct 34.2／64.6；ReAct → CoT-SC 35.1／62.0；監督式 SoTA 67.5／89.5
  - Table 3（ALFWorld 成功率 %，All 欄）：Act (best of 6) 45；ReAct (avg) 57；ReAct (best of 6) 71；ReAct-IM (avg) 48；ReAct-IM (best of 6) 53；BUTLER_g (best of 8) 22；BUTLER (best of 8) 37。ReAct (best of 6) 分項：Pick 92／Clean 58／Heat 96／Cool 86／Look 78／Pick2 41
  - Table 4（WebShop；Score／成功率 SR）：Act 62.3／30.1；ReAct 66.6／40.0；IL 59.9／29.1；IL+RL 62.4／28.7；人類專家 82.1／59.6
  - Table 2（p.6，人工檢視 HotpotQA 各 50 條軌跡）：ReAct 成功案例中「幻覺」6%，CoT 14%；失敗原因中 CoT 的幻覺佔 56%，ReAct 的推理錯誤佔 47%、搜尋結果無用佔 23%
- 給學生的一句話：HotpotQA 上 ReAct（27.4）其實輸給 CoT（29.4）；但在要一步步操作的 ALFWorld，同樣有工具、有沒有 Thought 差了 45 → 71——工具讓模型接地，思考讓模型不亂跑。

### m5-agent-survey-fig2
- 檔案：assets/figures/m5/p-agent-survey-fig2.png（2402×1084）
- 來源：Wang et al.（2023；Front. Comput. Sci. 2025）〈A Survey on Large Language Model based Autonomous Agents〉Fig. 2（A unified framework for the architecture design of LLM-based autonomous agent），p.4 — https://arxiv.org/abs/2308.11432 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0（**注意**：圖頂端的 OpenAI logo 與下方 stock 小圖示是第三方素材，CC BY 不一定涵蓋；放原圖前建議裁掉，或改用結構重畫）
- 建議用在：504-workflow-vs-agent 之後的 570 進階延伸（標「進階」；把四欄對應到課程的元件：Profile＝system prompt 角色、Memory＝checkpointer／向量庫、Planning＝ReAct／Plan、Action＝tool calling）
- 頁型：進階延伸
- 給學生的一句話：研究界把 LLM agent 拆成 Profile、Memory、Planning、Action 四塊；這門課的 LangGraph 全部都落在這四塊裡，看懂這張圖就知道別人講的 agent 在講哪一塊。

### m5-weng-agent-overview
- 檔案：assets/figures/m5/_ref/p-weng-agent-overview.png（1999×793，僅供重繪參考）
- 來源：Weng（2023-06-23）〈LLM Powered Autonomous Agents〉Fig. 1「Overview of a LLM-powered autonomous agent system」 — https://lilianweng.github.io/posts/2023-06-23-agent/ （已核實 2026-11-12）
- 授權：redraw — 頁面無授權聲明（頁尾僅 © 2026 Lil'Log），依「看不到授權就標 redraw」；只用結構（Planning：子目標拆解／反思精煉；Memory：短期／長期；Tool use）重畫，並註明「依 Weng (2023) 重繪」
- 建議用在：501-bridge 或 504-workflow-vs-agent 之後的 571 進階延伸（與 570 二選一：想要有圖的用 570，想要最簡版本用本項）
- 頁型：進階延伸
- 給學生的一句話：Weng 這篇是 agent 領域被引用最多的科普長文，圖把 agent 簡化成「LLM 當大腦＋規劃＋記憶＋工具」；先看這張再讀論文最省力。

### m5-karpathy-llm-os
- 檔案：無，link
- 來源：Karpathy（2023）《[1hr Talk] Intro to Large Language Models》投影片第 31 頁（LLM OS：LLM 當 CPU，周邊接 file system、browser、calculator／Python interpreter、其他 LLM） — 影片 https://www.youtube.com/watch?v=zjkBMFhNj_g ；投影片 PDF https://drive.google.com/file/d/1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7/view （已核實 2026-11-12）
- 授權：link — 未標授權
- 建議用在：520-supervisor 之後的 572 進階延伸（只放標題＋網址＋頁碼）
- 頁型：進階延伸
- 給學生的一句話：Karpathy 的比喻：LLM 像作業系統的核心，檔案、瀏覽器、計算器是它的周邊——這就是後面「工具」與 MCP 想標準化的那一圈。

---

# 模組六：LoRA 微調與私有化部署

### m6-lora-fig1
- 檔案：assets/figures/m6/_ref/p-lora-fig1.png（1800×1568，僅供重繪參考）
- 來源：Hu et al.（2021）〈LoRA: Low-Rank Adaptation of Large Language Models〉Fig. 1，p.1 — https://arxiv.org/abs/2106.09685 （已核實 2026-11-12）
- 授權：redraw — arXiv 頁標 arXiv.org perpetual non-exclusive license
- 建議用在：603-lora-ab 之後的 660 原圖對照（重畫：藍色 W∈ℝ^{d×d} 凍結；旁路 A（高斯初始化 𝒩(0,σ²)，d→r）與 B（初始化為 0，r→d）；輸出相加成 h）
- 頁型：原圖對照
- 給學生的一句話：B 初始化為 0，所以剛開始旁路輸出為 0、模型行為與預訓練完全一樣；只訓練 A 和 B，W 不動。

### m6-lora-table4
- 檔案：無（數字重繪）
- 來源：Hu et al.（2021）〈LoRA〉Table 4（GPT-3 175B，p.8）；摘要（p.1）；§4.2 Practical Benefits and Limitations（p.5） — https://arxiv.org/abs/2106.09685 （已核實 2026-11-12）
- 授權：redraw — arXiv 預設授權；只用表內數字重畫
- 建議用在：604-param-count 之後的 665 數據比較（x 軸＝可訓練參數量〔對數軸〕，y 軸＝WikiSQL 準確率）
- 頁型：數據比較
- 可用數據：
  - Table 4（GPT-3 175B；可訓練參數／WikiSQL 準確率 %／MNLI-m 準確率 %／SAMSum R1/R2/RL）：
    - 全量微調 FT：175,255.8M／73.8／89.5／52.0/28.0/44.5
    - BitFit：14.2M／71.3／91.0／51.3/27.4/43.5
    - PreEmbed：3.2M／63.1／88.6／48.3/24.2/40.5
    - PreLayer：20.2M／70.1／89.5／50.8/27.3/43.5
    - Adapter^H：7.1M／71.9／89.8／53.0/28.9/44.8；40.1M／73.2／91.5／53.2/29.0/45.1
    - **LoRA：4.7M／73.4／91.7／53.8/29.8/45.9；37.7M／74.0／91.6／53.4/29.2/45.1**
  - 摘要（p.1）：可訓練參數減少 10,000 倍，GPU 記憶體需求減少 3 倍
  - §4.2（p.5）：GPT-3 175B 訓練時 VRAM 由 1.2TB 降到 350GB；r＝4、只調 q 與 v 時，checkpoint 由 350GB 降到 35MB；存 100 個微調版本只需 350GB＋35MB×100≈354GB，而不是 100×350GB≈35TB
- 給學生的一句話：4.7M 個參數（全量的約 1/37,000）在 WikiSQL 上做到 73.4，與全量微調的 73.8 幾乎一樣；而 100 個客製版本只佔一個基座＋100 個 35MB 的小檔。

### m6-qlora-fig1
- 檔案：assets/figures/m6/p-qlora-fig1.png（2400×1050）
- 來源：Dettmers et al.（2023）〈QLoRA: Efficient Finetuning of Quantized LLMs〉Fig. 1，p.3 — https://arxiv.org/abs/2305.14314 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：606-qlora 之後的 661 原圖對照（三欄由左到右：全量微調 → LoRA → QLoRA；圈出左欄 32-bit 的優化器狀態大方塊、中欄 16-bit 底座、右欄 4-bit 底座與粉紅色的 CPU paging 箭頭）
- 頁型：原圖對照
- 給學生的一句話：全量微調要放 32-bit 優化器狀態（最左大方塊）；LoRA 把它縮成幾個小方塊；QLoRA 再把底座壓成 4-bit，並讓優化器狀態在顯存吃緊時暫存到 CPU（粉紅箭頭）。

### m6-qlora-memory
- 檔案：assets/figures/m6/p-qlora-fig6-mem.png（2000×1544；論文 Fig. 6 的堆疊長條圖）
- 來源：Dettmers et al.（2023）〈QLoRA〉Fig. 6（附錄 G，p.26）、Table 6（p.10）、§2 Background 末段（p.4）、摘要（p.1） — https://arxiv.org/abs/2305.14314 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：606-qlora 之後的 666 數據比較（用 Fig. 6 的原圖或重繪成長條圖）
- 頁型：數據比較
- 可用數據：
  - Fig. 6（p.26）：LLaMA 4-bit QLoRA 訓練時的記憶體組成，圖上數字單位為 MB；圖例顏色：藍＝Model、紅＝Adapters、黃＝Weight gradient、綠＝Optimizer、橘＝Input gradient。長條下方標示總量：7B（6.9 GB）、13B（11.3 GB）、33B（24.7 GB）、65B（45.0 GB）
    - Model（藍）：7B 5046；13B 8476；33B 19302；65B 37074
    - Optimizer（綠）：7B 1152；13B 1800；33B 3510；65B 5760
    - Adapters（紅框數字，我以顏色對應與長條比例推得，圖中未用文字標明類別）：7B 288；13B 450；33B 877.5；65B 1440
    - Weight gradient（黃）與 Input gradient（橘）沒有數字標註；使用 Fig. 6 時以原圖為準，不要自行補數
    - 圖說：input gradient 的大小是 batch size 1、序列長度 512 估計值
  - §2 Background 末段（p.4；7B LLaMA、FLAN v2、batch size 1、LoRA 權重約為原模型 0.2%）：LoRA input gradient 567 MB；LoRA 參數 26 MB；啟用 gradient checkpointing 後 input gradient 平均 18 MB／序列；4-bit 底座 5,048 MB
  - 摘要（p.1）：65B 模型微調的記憶體需求由 >780GB 降到 <48GB，單張 48GB GPU 即可，且不損失 16-bit 微調的表現
  - Table 6（p.10；Vicuna 基準，以 ChatGPT 為 100% 的平均分數％、記憶體）：Guanaco 65B 4-bit 41 GB 99.3%；Guanaco 33B 4-bit 21 GB 97.8%；Guanaco 13B 4-bit 10 GB 90.4%；Guanaco 7B 4-bit 5 GB 87.0%；Vicuna 13B 16-bit 26 GB 94.9%；GPT-4 114.5%；Bard 94.8%
- 給學生的一句話：65B 模型 4-bit 後底座只佔約 37GB，加上優化器、adapter 等合計 45GB，一張 48GB 卡就能微調；而且 Guanaco 65B 在 Vicuna 基準達到 ChatGPT 的 99.3%。

### m6-loralearns-fig1
- 檔案：assets/figures/m6/p-lora-learns-less-fig1.png（3796×3519）
- 來源：Biderman et al.（2024；TMLR）〈LoRA Learns Less and Forgets Less〉Fig. 1，p.5 — https://arxiv.org/abs/2405.09673 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：605-lora-vs-full 之後的 662 原圖對照（建議只截 A、B 兩個程式碼子圖；數學的 C、D 另放或略過）
- 頁型：原圖對照
- 給學生的一句話：Llama-2-7B 學寫程式：全量微調（黑線）一路拉高，LoRA 的 rank 越大（16→64→256）越接近，但小 rank 在持續預訓練（左欄）明顯落後；指令微調（右欄）只有 r=256 追得上。

### m6-loralearns-fig2-3
- 檔案：assets/figures/m6/p-lora-learns-less-fig2.png（3826×3514，遺忘曲線）、assets/figures/m6/p-lora-learns-less-fig3.png（3780×3468，學習 vs 遺忘取捨散點圖）
- 來源：Biderman et al.（2024）〈LoRA Learns Less and Forgets Less〉Fig. 2（p.7）、Fig. 3（p.8） — https://arxiv.org/abs/2405.09673 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：680-pitfalls 之後的 663 原圖對照（災難性遺忘；Fig. 3 以「橫軸＝源領域保留分數、縱軸＝目標領域表現」說明取捨）
- 頁型：原圖對照
- 給學生的一句話：LoRA 學得比較少，但忘得也比較少：Fig. 3 的黑線（全量）往左上衝、同時往左掉，LoRA 的點停在右邊（保留原本能力）——沒有免費午餐，是取捨。

### m6-loralearns-data
- 檔案：無（數字重繪）
- 來源：Biderman et al.（2024）〈LoRA Learns Less and Forgets Less〉附錄 D Table S1、S2（p.27）、Table S5、S6（p.28） — https://arxiv.org/abs/2405.09673 （已核實 2026-11-12）
- 授權：direct — arXiv 頁標 CC BY 4.0
- 建議用在：605-lora-vs-full 之後的 667 數據比較（LoRA vs 全量，兩張並排：左＝學習，右＝遺忘）
- 頁型：數據比較
- 可用數據（Llama-2-7B；遺忘分數＝HellaSwag、ARC-Challenge、WinoGrande 三項平均，越高代表保留越多）：
  - Table S1（p.27；Starcoder-Python 持續預訓練，HumanEval pass@1；訓練 token 0.25／0.5／1／2／4／8／16／20 B）：
    - LoRA r=16：0.143／0.144／0.141／0.141／0.154／0.159／0.162／0.162
    - LoRA r=64：0.142／0.146／0.141／0.153／0.157／0.176／0.194／0.196
    - LoRA r=256：0.144／0.142／0.143／0.159／0.159／0.208／0.211／0.224
    - 全量微調：0.152／0.153／0.172／0.181／0.218／0.258／0.255／0.263
  - Table S2（p.27；同上，遺忘分數）：LoRA r=16 0.645→0.635；r=64 0.646→0.626；r=256 0.644→0.617；全量 0.625→0.545（0.25B→20B token）
  - Table S5（p.28；Magicoder-Evol-Instruct-110K 指令微調，HumanEval pass@1；epoch 1／2／4／8／16）：LoRA r=16 0.197／0.275／0.358／0.338／0.324；r=64 0.249／0.339／0.417／0.392／0.405；r=256 0.299／0.385／0.498／0.437／0.466；全量 0.302／0.464／0.470／0.497／0.416
  - Table S6（p.28；同上，遺忘分數）：LoRA r=16 0.653／0.648／0.652／0.646／0.609；r=64 0.652／0.651／0.632／0.580／0.510；r=256 0.655／0.659／0.631／0.552／0.517；全量 0.595／0.579／0.512／0.446／0.414
  - 摘要（p.1）：全量微調學到的擾動 rank 是典型 LoRA 設定的 10–100 倍
  - 其他表：Table S3／S4（OpenWebMath，GSM8K／遺忘）、S7／S8（MetaMathQA）在同兩頁，需要數學例子時可直接取用
- 給學生的一句話：同樣訓練到最後，程式碼持續預訓練（Starcoder-Python）全量微調 HumanEval 0.263、LoRA r=256 只有 0.224；但遺忘分數全量掉到 0.545，LoRA 只掉到 0.617——學得少、忘得也少。

### m6-cs25-lampinen
- 檔案：無，link
- 來源：Lampinen（2026-05-07）Stanford CS25 V6〈Distinct Modes of Generalization from Parameters and Context, and Paths to Bridge the Gap〉投影片 — 課程頁 https://web.stanford.edu/class/cs25/ ；投影片 https://drive.google.com/file/d/1-YIOa5Yal4RCjAsV-0tnW_NNDGbY1GTo/view （已核實 2026-11-12；PDF 共 50 頁，我下載並逐頁看過文字）
- 授權：link — 課程頁與投影片都未標授權
- 建議用在：602-decision-matrix 之後的 670 進階延伸（只放標題＋網址＋頁碼）：p.3「Language models have two different ways of 'learning'」（改參數 vs 放進 context）；p.12（逆轉詛咒：把整個資料集放進 context 的 ICL，遠勝微調）；p.41–42（三條補救路：訓練期資料擴增、測試期檢索、測試期靠 RL 學會自己重述）
- 頁型：進階延伸
- 給學生的一句話：想知道「為什麼有時候把資料塞進 prompt（RAG）比微調進權重更能舉一反三」，這場演講是最直接的實驗證據。
- 備註：演講背後的論文 Lampinen et al.（2025）〈On the generalization of language models from in-context learning and finetuning: a controlled study〉arXiv:2505.00661，arXiv 頁標 CC BY 4.0（已核實）；其 Fig. 2 起的結果圖可作 `direct` 使用，這次未下載（不在目標清單內）。論文 Fig. 1 為 Rogers & McClelland 的「Reproduced with permission」，不可用。

---

# 找不到／不能用／有疑慮的項目

1. **目標清單全部找到，arXiv 編號與標題全部與記憶相符**，沒有錯號。
2. **授權導致不能放原圖的目標（只能 redraw）**：Transformer、Lost in the Middle、RAG、CRAG、LoRA——五篇皆為 arXiv 預設授權，原圖只存 `_ref/` 供重繪。
3. **LoRA Learns Less 的 Fig. 1–3 是點線圖，圖上沒有逐點數字**；逐點數字在附錄 Table S1–S8，本清單已抄 S1、S2、S5、S6，其餘（OpenWebMath、MetaMathQA）要用再抄。
4. **Lost in the Middle 的 Fig. 1／Fig. 5 不能放原圖**（redraw），但附錄 G 有完整數字（Table 5／6／7），重畫的曲線可以逐點對得上。
5. **QLoRA Fig. 6 的紅框數字（288／450／877.5／1440）類別是我推定為 Adapters 的**：依據是紅色與圖例「Adapters」同色，且長條比例吻合（7B：288MB 約佔 6.9GB 的 4%）。論文圖上沒有明寫。上投影片直接放原圖最穩，不要另外加註這四個數字的類別。
6. **演講類沒有一張可直接放原圖**：Karpathy、CS25 皆無授權聲明 → 全部 `link`；CS336 repo 雖為 MIT，但投影片含第三方圖 → `redraw` 結構。
7. **Karpathy 投影片的數字是口頭估計**：約 6,000 GPU、約 $2M、約 12 天、約 10TB 是他 2023 年 11 月的粗略說法，引用時標「示意」，不要當規格。
8. **經典 agent 綜述**：找到並核實 Wang et al. 2308.11432（CC BY 4.0）。另外核實 Xi et al. 2309.07864〈The Rise and Potential of LLM Based Agents〉為 arXiv 預設授權、Park et al. 2304.03442〈Generative Agents〉為 arXiv 預設授權；這兩篇這次沒抽圖（不是目標），要用的話都只能 redraw。


---

# 官方文件／部落格架構圖與套件 logo 清單（figures-docs）

核實日期：2026-11-12（所有頁面皆用 WebFetch 實際打開；圖檔皆已下載並用看圖確認內容）。
論文圖不在本檔（另一位同事負責，檔名 `p-*`）。

## 先看這三點

1. **Anthropic 官方部落格的圖一律 `redraw`**：頁面只有「© 2026 Anthropic PBC」，沒有任何開放授權。圖放在 `m<N>/_ref/` 只供參考，不得放進投影片。
2. **LangChain 文件、GraphRAG 文件、MCP 文件的 GitHub repo 有明確開放授權**（見各項），所以其中的圖標 `direct`；`.src` 要寫明授權與版權人。
3. **Host／Client／Server（MCP）、GraphRAG 管線、LangGraph／Deep Agents 的 HITL 流程，官方現行頁面不是圖檔而是 Mermaid 程式碼**，沒有圖可下載；本檔只記錄結構，一律用 rough.js 重畫。

### 配色對照（重畫 Anthropic 圖時）
Anthropic 圖語意：綠框＝LLM 呼叫、粉紅圓角＝輸入／輸出／外部環境、紫框＝非 LLM 的程式邏輯（Gate、Aggregator、Stop、Retrieval、Tools、Memory）、灰實線＝必經路徑、灰虛線＝選擇性／動態路徑。
重畫成本 deck 語意：LLM 呼叫＝圓（靛藍）；Gate／Stop／工具＝三角；In／Out／資料／記憶＝方；虛線箭頭保留「動態決定」的意思。

---

## 一、架構圖

### m5-bea-augmented-llm
- 檔案：assets/figures/m5/_ref/d-bea-augmented-llm.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉（2024-12-19）段落「Building block: The augmented LLM」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 頁面無授權條款，僅 © Anthropic PBC
- 建議用在：502-real-trace 之前或 501-bridge（講「LLM＋檢索＋工具＋記憶」是 agent 的零件）
- 圖的結構：上排 In（粉紅圓角）→ LLM（綠框）→ Out（粉紅圓角），兩段實線箭頭。LLM 正下方三個紫框並排：左 Retrieval、中 Tools（略低）、右 Memory；LLM 與三者之間各有一條雙向虛線箭頭，標籤分別是 Query/Results、Call/Response、Read/Write。
- 給學生的一句話：Agent 的基本零件就是一顆 LLM 加三條雙向線——查資料、呼叫工具、讀寫記憶。

### m5-bea-prompt-chaining
- 檔案：assets/figures/m5/_ref/d-bea-prompt-chaining.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Prompt chaining」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent（workflow 三種寫法之一）
- 圖的結構：由左到右一條線：In → LLM Call 1 →（標籤 Output 1）→ Gate（紫框）。Gate 往右上實線弧到 LLM Call 2（標 Pass），LLM Call 2 →（標 Output 2）→ LLM Call 3 → Out。Gate 往右下虛線弧到 Exit（粉紅圓角，標 Fail）。
- 給學生的一句話：把大任務切成固定的幾步，每步之間放一個檢查閘門，不合格就提早退出。

### m5-bea-routing
- 檔案：assets/figures/m5/_ref/d-bea-routing.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Routing」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；也可呼應 508-conditional-edges（條件邊＝路由）
- 圖的結構：In → LLM Call Router（綠框，兩行字）→ 三個垂直排列的 LLM Call 1／2／3（Call 1 的箭頭是實線、Call 2 與 3 是虛線，表示只走其中一條）→ 三條弧線匯到 Out。
- 給學生的一句話：先讓一個 LLM 判斷「這題該交給誰」，再走對應的那條路——這就是條件邊。

### m5-bea-parallelization
- 檔案：assets/figures/m5/_ref/d-bea-parallelization.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Parallelization」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；509-reducer 的動機（多節點同時寫入要合併）
- 圖的結構：In 扇出三條實線到 LLM Call 1／2／3（垂直排列），三者再扇入同一個 Aggregator（紫框），Aggregator → Out。
- 給學生的一句話：同一件事同時問多個 LLM（或同時處理多段），最後由一個聚合器合併。

### m5-bea-orchestrator-workers
- 檔案：assets/figures/m5/_ref/d-bea-orchestrator-workers.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Orchestrator-workers」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：520-supervisor（Supervisor 拆任務給子 agent 再統整的概念原型）
- 圖的結構：In → Orchestrator（綠框）→ 三條「虛線」弧到 LLM Call 1／2／3（虛線表示 worker 數量與內容由 orchestrator 當場決定）→ 三條虛線匯入 Synthesizer（綠框）→ Out。與 Parallelization 的差別：中間是虛線、前後各有一個 LLM（拆解者與整合者）。
- 給學生的一句話：Supervisor 不是固定流程——拆成幾個子任務、交給誰，是 LLM 當場決定的。

### m5-bea-evaluator-optimizer
- 檔案：assets/figures/m5/_ref/d-bea-evaluator-optimizer.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Evaluator-optimizer」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；315-self-rag-crag 可回頭呼應（檢索後自評再改寫）
- 圖的結構：In → LLM Call Generator → 上方弧線（標 Solution）→ LLM Call Evaluator；Evaluator 下方弧線回到 Generator（標 Rejected + Feedback）；Evaluator → Out（標 Accepted）。形成一個生成／評審的小迴圈。
- 給學生的一句話：一個 LLM 寫、一個 LLM 批改，不過關就帶著意見重寫，直到通過。

### m5-bea-autonomous-agent
- 檔案：assets/figures/m5/_ref/d-bea-autonomous-agent.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Agents」（圖名 Autonomous agent）— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：503-react-loop（Thought→Action→Observation 的最簡示意）；501-bridge（f(x) 放進迴圈）
- 圖的結構：中間 LLM Call（綠框）。右側 Environment（粉紅圓角）；LLM Call → Environment 上弧線（標 Action），Environment → LLM Call 下弧線（標 Feedback），構成迴圈。左側 Human（粉紅圓角）與 LLM Call 之間一條雙向虛線（隨時可介入）。LLM Call 正下方一條虛線箭頭到 Stop（紫框）。
- 給學生的一句話：Agent 就是把模型放進「行動→環境回饋→再行動」的迴圈，直到自己決定停。

### m5-bea-coding-agent
- 檔案：assets/figures/m5/_ref/d-bea-coding-agent.png（2400×1666）
- 來源：Anthropic〈Building effective agents〉段落「Agents」（圖名 High-level flow of a coding agent）— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：502-real-trace 之後（把一段真實 trace 對到時序圖）；505-minimal-agent
- 圖的結構：時序圖，四條垂直生命線：Human（粉紅圓角）、Interface（紫框）、LLM（綠框）、Environment（粉紅圓角）。訊息由上而下：Query（Human→Interface）；虛線框「Until tasks clear」內：Clarify（Human→LLM）、Refine（LLM→Human）；Send context（Interface→LLM）；Search files（LLM→Environment）、Return paths（回）；虛線框「Until tests pass」內：Write code→Status、Test→Results；Complete（LLM→Interface）；Display（Interface→Human）。
- 給學生的一句話：Coding agent 有兩個迴圈——跟人問到需求清楚為止，跟環境測到測試通過為止。

### m5-lc-agent-workflow（direct，可放原圖）
- 檔案：assets/figures/m5/d-lc-agent-workflow.png（4572×2047）
- 來源：LangChain〈Workflows and agents〉— https://docs.langchain.com/oss/python/langgraph/workflows-agents（已核實 2026-11-12）；原檔 https://github.com/langchain-ai/docs/blob/main/src/oss/images/agent_workflow.png
- 授權：direct — langchain-ai/docs repo 的 LICENSE 為 MIT License，Copyright (c) 2025 LangChain。`.src` 寫：「來源：LangChain Docs〈Workflows and agents〉，MIT License © 2025 LangChain」。頁面本身沒有另列授權，以 repo LICENSE 為依據；若要更保守可降為 redraw。
- 建議用在：504-workflow-vs-agent（主圖的對照來源）
- 圖的結構：白底，三欄虛線分隔。左欄「Workflows」：Prompt Chaining、Parallelization 兩個小圖；中欄：Orchestrator-Worker、Evaluator-optimizer、Routing 三個小圖；右欄「Agent」：In → LLM call ⇄ Tool（action／feedback）→ Out。最底下三句說明：左與中欄「LLM is embedded in predefined code paths」／「LLM directs control flow through predefined code paths」，右欄「LLM directs its own actions based on environmental feedback」。手繪（Excalidraw）風、腦袋圖示代表 LLM。
- 給學生的一句話：左邊流程是程式寫死的，右邊流程是模型自己決定——差別只在「誰掌控下一步」。

### m5-lc-workflow-patterns（direct，可放原圖；單一模式的大圖）
- 檔案：assets/figures/m5/d-lc-prompt-chaining.png（1412×444）、d-lc-parallelization.png（1020×684）、d-lc-routing.png（1214×678）、d-lc-orchestrator-worker.png（1486×548）、d-lc-evaluator-optimizer.png（1004×340）、d-lc-agent-loop.png（1732×712）
- 來源：LangChain〈Workflows and agents〉各小節（圖片 alt 依序為 Prompt chaining、parallelization.png、routing.png、worker.png、evaluator_optimizer.png、agent.png）— https://docs.langchain.com/oss/python/langgraph/workflows-agents（已核實 2026-11-12，頁面共 8 張圖含 agent_workflow 與 augmented_llm）
- 授權：direct — 同上，MIT License © 2025 LangChain
- 建議用在：需要「真實出處的單一模式圖」時，放在 504-workflow-vs-agent 之後；其中 d-lc-agent-loop 可放 503-react-loop；d-lc-orchestrator-worker 可放 520-supervisor
- 圖的結構：都是 Excalidraw 手繪風，虛線圓角方框內放腦袋圖示代表 LLM。Prompt chaining：In → 兩個串聯 LLM call → Out；Parallelization：In 分兩路，各自一個 LLM → 各自 Out；Routing：In → Router → 三個 LLM（虛線箭頭）→ 各自 Out；Orchestrator-worker：In → Orchestrator → 三個 worker → Synthesizer → Out；Evaluator-optimizer：Generator → Evaluator → Out，Evaluator 有回箭頭；Agent：In → LLM call → action → Tool → Out，Tool 有 feedback 弧線回 LLM call。
- 給學生的一句話：這幾種模式是 LangGraph 官方範例實際在做的事，後面 Lab 會用狀態圖把它們寫出來。

### m5-lc-checkpoints（direct）
- 檔案：assets/figures/m5/d-lc-checkpoints.jpg（2316×748）、d-lc-get-state.jpg（2692×1056）
- 來源：LangChain〈Checkpointers〉（alt 為 Checkpoints／State）— https://docs.langchain.com/oss/python/langgraph/checkpointers（已核實 2026-11-12；舊的 /persistence 頁面現在沒有任何圖）
- 授權：direct — langchain-ai/docs，MIT License © 2025 LangChain（`.src` 同上）
- 建議用在：511-checkpointer（checkpointer 存什麼、thread 是什麼）
- 圖的結構：由上而下的對照表，左欄名詞、中欄圖示、右欄一句說明。Graph：state "I" → Node 1（粉紅圓）→ Node 2（藍圓）→ state "I heart langgraph"，說明「Control flow of nodes, edges」；Super-steps：每個依序節點是獨立 super-step、平行節點共用同一個；Checkpoints：粉紅與藍色圓角框，內含 state／next／id，說明「State and relevant metadata packaged at every super-step」；Thread：虛線框圈住所有 checkpoint，說明「Collection of checkpoints」；StateSnapshot：checkpoint 的型別。get_state 圖多兩列：Graph.get_state()＝最新一筆、Graph.get_state_history()＝全部清單。
- 給學生的一句話：每走完一個 super-step 就存一份快照，同一個 thread_id 的快照串成一條可回頭看的歷史。

### m5-lc-time-travel（direct）
- 檔案：assets/figures/m5/d-lc-replay.png（2276×986）、d-lc-checkpoints-fork.jpg（3705×2598）
- 來源：LangChain〈Use time-travel〉（alt 為 Replay／Fork）— https://docs.langchain.com/oss/python/langgraph/use-time-travel（已核實 2026-11-12）；Checkpointers 頁也用同兩張圖
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：512-time-travel
- 圖的結構：延續上一張的表格，往下加列。Replay 圖多一列 `Graph.stream(None,{checkpoint_id, thread_id})`：從指定 checkpoint 重播，「該 checkpoint 之前的步驟不重跑、之後的步驟會重跑」。Fork 圖（完整版）再加：`Graph.update_state({thread_id},{state:"I like cold brew"})` 從目前 checkpoint 分叉出新 checkpoint（綠色）；`update_state({checkpoint_id,thread_id},{state:"I like"})` 從指定舊 checkpoint 分叉（紫色）；最後 `Graph.stream(None,{checkpoint_id,thread_id})` 從分叉點繼續跑，「因為該 checkpoint 沒被執行過」。
- 給學生的一句話：拿舊快照可以重播，改過狀態再存就是分叉出一條新時間線。
- 注意：Fork 圖有 3705×2598、文字很小，上課前要裁切成「分叉那兩列」再放大。

### m5-lc-durable-execution（direct）
- 檔案：assets/figures/m5/d-lc-durable-execution.png（962×545，深色底）
- 來源：LangChain〈Going to production〉（Deep Agents）alt「Durable execution: when a worker crashes mid-run, another worker picks the run up from the latest checkpoint」— https://docs.langchain.com/oss/python/deepagents/going-to-production（已核實 2026-11-12）；原檔 src/oss/images/deepagents/production/durable-execution.png
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：511-checkpointer（為什麼正式環境要 PostgresSaver）；552-lab5b-code
- 圖的結構：標題「Durable Execution: Crash Recovery」。左上方框 Worker A：c1 → c2 → 打叉的圓「crash」；右上方框 Worker B：c2 → c3；下方長條「Persistence layer (Postgres)」內 c1、c2、c3 三個圓；Worker A 的 c1、c2 以虛線存入 Postgres，由 c2 一條實線標「resume from c2」指向 Worker B 的 c2，Worker B 的 c3 再存回 Postgres。
- 給學生的一句話：Worker 掛了沒關係，換一台從最後一個 checkpoint 接著跑——前提是 checkpoint 存在 Postgres 而不是記憶體。
- 注意：深色底，放進紙色底 deck 要放在 `.fig` 白底卡片外再加深色邊框，或直接重畫。

### m5-lc-hitl-interrupt（direct，但目前線上頁面沒有引用）
- 檔案：assets/figures/m5/d-lc-hitl-interrupt.png（1160×792，深色底）
- 來源：langchain-ai/docs repo 的檔案 https://github.com/langchain-ai/docs/blob/main/src/oss/images/deepagents/hitl.png（已核實檔案存在，2026-11-12）。**線上現行頁面沒有任何一頁引用這張圖**：Deep Agents〈Human-in-the-loop〉頁（https://docs.langchain.com/oss/python/deepagents/human-in-the-loop）只有 Mermaid 流程圖；LangGraph〈Interrupts〉頁只有 Studio 表單截圖；LangChain〈Human-in-the-loop〉頁完全沒有圖。
- 授權：direct — 檔案在 MIT repo 內；`.src` 請引用 repo 檔案路徑而非某個網頁。
- 建議用在：513-hitl（`interrupt()` 暫停 → 人工決定 → `Command(resume=...)` 恢復的完整往返）；514-hitl-code
- 圖的結構：左右兩個大框：左框 Human（內有 Review）、右框 Agent（內有 Draft Action → interrupt() → continue）。interrupt() 以粉紅線標「Surface Payload」指向 Human 的 Review；interrupt() 另一條虛線標「Save」指向中間的圓柱 checkpointer；Review 以藍線標「Command(resume=decision)」指向 Agent 的 continue；checkpointer 以虛線標「Load」指向 continue。
- 給學生的一句話：interrupt() 把現場存進 checkpointer 然後停下，人給了決定後再讀回來接著跑。
- 風險：因為官方網站目前沒有放這張圖，日後 repo 可能刪檔。建議本地備份（已存），並以重畫為主、原圖為輔。

### m5-lc-hitl-flow-mermaid（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼，沒有圖檔）
- 來源：LangChain Deep Agents〈Human-in-the-loop〉— https://docs.langchain.com/oss/python/deepagents/human-in-the-loop（已核實 2026-11-12；原始碼 src/oss/deepagents/human-in-the-loop.mdx）
- 授權：redraw — 文字與結構取自 MIT repo，但沒有圖檔可放，直接用 rough.js 重畫
- 建議用在：513-hitl
- 圖的結構：由左到右：Agent → 菱形「Interrupt?」。no → Execute；yes → 菱形 Human。Human 四條出路：approve → Execute、edit → Execute、reject → ToolMessage、respond → ToolMessage（LangChain 頁面版本只有 approve／edit／reject 三條）。Execute → Agent、ToolMessage → Agent（回到 Agent 迴圈）。
- 給學生的一句話：人有四種回應——放行、改了再放行、拒絕、用文字回覆；後兩種會變成一則 ToolMessage 回到 agent。

### m5-lc-pattern-subagents（direct）
- 檔案：assets/figures/m5/d-lc-pattern-subagents.png（1020×734）
- 來源：LangChain〈Multi-agent〉段落「Visual overview」（alt「Subagents pattern: main agent coordinates subagents as tools」）— https://docs.langchain.com/oss/python/langchain/multi-agent（已核實 2026-11-12）
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：520-supervisor、521-subagent-as-tool（「子 agent 包成工具」）
- 圖的結構：Mermaid 渲染圖。User request（圓角）→ Main Agent（方框）；Main Agent 與 Subagent A／B／C（右側三個方框）各有雙向箭頭（呼叫與回傳）；Main Agent 另一條箭頭 → Response（圓角）。
- 給學生的一句話：所有路由都經過主 agent，子 agent 就像主 agent 手上的三個工具。
- 注意：頁面沒有 supervisor 一詞，也沒有 supervisor 專用圖；課程用詞「Supervisor」與此圖的「Main Agent」對應。

### m5-lc-patterns-others（direct）
- 檔案：assets/figures/m5/d-lc-pattern-handoffs.png（1568×464）、d-lc-pattern-router.png（1560×556）、d-lc-pattern-skills.png（874×734）
- 來源：LangChain〈Multi-agent〉段落「Visual overview」— https://docs.langchain.com/oss/python/langchain/multi-agent（已核實 2026-11-12）
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：524-agent-zoo（多 agent 四種模式比較）；d-lc-pattern-skills 放 525-skills
- 圖的結構：Handoffs：User request → 框「Agents」內 Agent A ⇄ Agent B ⇄ Agent C（彼此雙向、A↔C 也有）；A、B、C 各有一條箭頭到 Response。Router：User request → Router → Agent A／B／C（三路）→ Synthesize → Response。Skills：User request → Agent → Skill A／B／C（三條單向箭頭）；Agent → Response。
- 給學生的一句話：多 agent 不只 Supervisor 一種——交棒、分流、載入技能各有取捨。

### m5-mars-orchestrator-worker
- 檔案：assets/figures/m5/_ref/d-mars-orchestrator-worker.png（4584×2579）、d-mars-process.png（4584×4584）
- 來源：Anthropic〈How we built our multi-agent research system〉（2025-06-13）— https://www.anthropic.com/engineering/multi-agent-research-system（已核實 2026-11-12，頁面共 3 張圖，兩張為架構圖）
- 授權：redraw — 無授權條款
- 建議用在：520-supervisor（真實系統的 Supervisor 長相）；522-context-passing（Memory 與只回報結果）
- 圖的結構：架構圖標題「High-level Architecture of Advanced Research」。左側灰色區「Claude.ai chat」（使用者提問）；右側灰色區「Multi-agent research system」：中央大藍框「Lead agent (orchestrator)」，框內寫 Tools: search tools + MCP tools + memory + run_subagent + complete_task；左邊 Citations subagent（單向箭頭出去）、右邊 Memory（雙向箭頭）、下方三個 Search subagent（各與 Lead 雙向箭頭、各自有自我迴圈箭頭）。左右之間兩條箭頭：User request →、← Final report。時序圖標題「Multi-agent System Process Diagram」：七條生命線 User、System、LeadResearcher、Subagent1、Subagent2、Memory、CitationAgent；LeadResearcher 在「Iterative Research Process」框內 think（plan approach）→ save plan 到 Memory → retrieve context → create subagent for aspect A／B → 子 agent 各自 web_search、think（evaluate）→ complete_task 回報 → think（synthesize）→ 判斷「More research needed?」（Exit loop／Continue loop）；結束後 complete_task 把結果交給 System，CitationAgent 處理文件與報告插入引用，System 持久化並回傳帶引用的結果。
- 給學生的一句話：真實的 Supervisor 會先把計畫存進記憶、並行派出多個子 agent，最後由專門的 agent 補上引用。

### m5-skills-progressive-disclosure
- 檔案：assets/figures/m5/_ref/d-skills-progressive-disclosure.jpg（2292×673）、d-skills-context-window.jpg（1650×929）、d-skills-bundle-files.jpg（1650×1069）
- 來源：Anthropic〈Equipping agents for the real world with Agent Skills〉（2025-10-16，2025-12-18 更新）— https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills（已核實 2026-11-12，頁面共 6 張圖）
- 授權：redraw — 無授權條款
- 建議用在：525-skills
- 圖的結構：progressive disclosure 是一張表（直接重畫成三層階梯即可）：Level 1「SKILL.md Metadata (YAML)」— Always loaded — 約 100 tokens；Level 2「SKILL.md Body (Markdown)」— Loaded when Skill triggers — 少於 5k tokens；Level 3+「Bundled files (text files, scripts, data)」— Loaded as-needed by Claude — unlimited*（以上數字是圖上寫的，要放進投影片須標「依 Anthropic 部落格」）。context-window 圖標題「Skills and the Context Window」：大框 Context Window，上半是 Agent's System Prompt 與一排技能名稱小標籤（bigquery、docx、nda-review、pdf、pptx、…、xlsx），左側註解「Short snippets from each Skill appended to the system prompt」；下半依序是 User 訊息、Claude 決定觸發 PDF Skill、Tool use: Bash("cat /mnt/skills/pdf/SKILL.md")、Tool result、再 cat forms.md 與其結果，右側註解標出「Claude decides to trigger」「follow the reference to forms.md」。
- 給學生的一句話：技能平常只佔幾十個 token 的說明，真的要用時才把正文和附檔讀進 context。

### m3-cr-standard-rag
- 檔案：assets/figures/m3/_ref/d-cr-standard-rag.png（3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉（2024-09-19）圖「A Standard Retrieval-Augmented Generation (RAG) system that uses both embeddings and Best Match 25 (BM25) to retrieve information」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：303-two-pipelines（離線 vs 在線的真實例子）；309-hybrid-rrf 之後
- 圖的結構：標題「Standard RAG」，兩個大底板：左「PREPROCESSING」、右「RUNTIME」。左：Corpus（文件堆疊）→（標 Chunks）→ 分兩路：Embedding model →（Embeddings）→ Vector database；TF-IDF →（TF-IDF encodings）→ TF-IDF index。右：Query（人像）分別連到 Vector database 與 TF-IDF index；兩者輸出匯入 Rank fusion →（Top K chunks）→ Generative model（右上角有 Claude 圖示）→ Response。
- 給學生的一句話：向量與關鍵字兩路各自索引，查詢時兩路一起找，再用排名融合合併。
- 注意：圖上框裡寫的是「TF-IDF」，但文章標題與說明寫 BM25。重畫時請標 BM25，並加註「原圖標示 TF-IDF，BM25 為其改良版」避免學生比對時困惑。

### m3-cr-contextual-preprocess
- 檔案：assets/figures/m3/_ref/d-cr-contextual-preprocess.png（3840×2160；右側被裁切，只有前處理部分完整）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖「Contextual Retrieval is a preprocessing technique that improves retrieval accuracy」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：302-three-pains（上下文斷裂的解法）；313-doc-to-qa（同屬「入庫前先用 LLM 加工」）
- 圖的結構：標題「Contextual Retrieval Preprocessing」，底板「PREPROCESSING (new)」，藍色表示新增步驟。Corpus 中取出一份文件 → 切成 Chunk 1、Chunk 2、…、Chunk X（藍色小框）→ 一個大藍框「Run prompt for every chunk to situate it within the document」（Claude 圖示）；整份文件另有一條藍線也送進這個大藍框。輸出 Context 1 + Chunk 1、Context 2 + Chunk 2、…、Context X + Chunk X，旁註「For every prompt, Claude responds with 50–100 tokens of context, which is then prepended to the corresponding chunk」。之後接回原有的 Embedding model → Vector database、TF-IDF → TF-IDF index（灰色）。
- 給學生的一句話：入庫前，先讓 LLM 讀整份文件，替每個 chunk 補一小段「你在文件的哪裡」再去做向量與關鍵字索引。
- 注意：「50–100 tokens」是圖上旁註的原文，放進投影片時標明出處。

### m3-cr-rerank-pipeline
- 檔案：assets/figures/m3/_ref/d-cr-rerank-pipeline.png（3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖「Combine Contextual Retrieval and Reranking to maximize retrieval accuracy」（原標題有 Retrieva 拼字錯誤）— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：311-rerank（粗篩再精排的完整管線）；303-two-pipelines
- 圖的結構：標題「Combined」。左底板「PREPROCESSING (with Contextual Retrieval)」，內容同上一張（縮小）；右底板「RUNTIME (with Reranking)」：Query 連到 Vector database 與 TF-IDF index，兩者 → Rank fusion →（Top N chunks）→ Reranker →（Top K chunks）→ Generative model → Response。
- 給學生的一句話：先多撈一些（Top N），再讓重排器精選少數幾個（Top K）交給模型。
- 注意：圖上只寫 Top N／Top K，沒有數字。文章內文提到的具體數字（先撈 150、重排後取 20）是從頁面摘要得到，放進投影片前請回原文逐字核對。

### m3-cr-results（數據，供 X65–X69 數據比較頁）
- 檔案：assets/figures/m3/_ref/d-cr-results-contextual.png（4 根長條）、d-cr-results-rerank.png（6 根長條）（皆 3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖說「Combining Contextual Embedding and Contextual BM25 reduce the top-20-chunk retrieval failure rate by 49%」與「Reranked Contextual Embedding and Contextual BM25 reduces the top-20-chunk retrieval failure rate by 67%」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 圖不能放；**數字可以用乾淨圖表重畫**，`.src` 寫「依 Anthropic〈Introducing Contextual Retrieval〉(2024) 圖重繪」
- 建議用在：311-rerank 之後的數據頁
- 圖的結構：縱軸「Average % Failed Retrievals @20」（top-20 檢索失敗率）。左組 Standard Retrieval：Embedding 5.7%、Embedding + BM25 5.0%、Reranked embedding + BM25 3.5%；右組 Contextual Retrieval：Contextual embedding 3.7%、Contextual embedding + contextual BM25 2.9%、Reranked contextual embedding + contextual BM25 1.9%。圖說的相對降幅：5.7%→2.9% 為 49%、5.7%→1.9% 為 67%（5.7%→3.7% 約 35%，是由圖上數字算出，不是圖說寫的）。
- 給學生的一句話：補上下文、加關鍵字、再重排，失敗率從 5.7% 一路降到 1.9%。

### m4-graphrag-kg-viz（direct）
- 檔案：assets/figures/m4/d-graphrag-kg-viz.jpg（600×611）
- 來源：Microsoft GraphRAG 文件首頁 Figure 1「An LLM-generated knowledge graph built using GPT-4 Turbo」— https://microsoft.github.io/graphrag/（已核實 2026-11-12）；原檔 https://github.com/microsoft/graphrag/blob/main/docs/img/GraphRag-Figure1.jpg
- 授權：direct — microsoft/graphrag repo 為 MIT License，Copyright (c) Microsoft Corporation。`.src` 寫「來源：Microsoft GraphRAG 文件 Figure 1，MIT License © Microsoft」。網站頁尾只有「© 2025 Microsoft」，授權依據是 repo LICENSE。
- 建議用在：402-why-graph 或 410-query-modes（「大規模圖譜長這樣」）；與論文 Fig. 1（`m4/p-graphrag-fig1.png`）內容相近，擇一即可
- 圖的結構：白底散點圖，無框線無箭頭：大量圓點（疏密不一），顏色代表社群、圓大小代表實體的度（連線數），彼此疏密不同形成團塊。
- 給學生的一句話：每個圓是一個實體，同顏色是同一個社群——全局檢索就是讀這些社群的摘要。
- 注意：Microsoft Research 部落格〈GraphRAG: Unlocking LLM discovery on narrative private data〉（https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/）的 Figure 3 是同一張圖，但部落格沒有授權條款，所以不要從部落格取圖，用 repo 版。

### m4-graphrag-drift（direct）
- 檔案：assets/figures/m4/d-graphrag-drift.png（2048×339，很扁）
- 來源：Microsoft GraphRAG〈DRIFT Search〉Figure 1 — https://microsoft.github.io/graphrag/query/drift_search/（已核實 2026-11-12）；原檔 docs/img/drift-search-diagram.png
- 授權：direct — 同上 MIT License © Microsoft Corporation
- 建議用在：410-query-modes（Global／Local／DRIFT／Basic 的 DRIFT 一格）
- 圖的結構：一棵由上往下展開的大樹，樹根標 A，第二層節點裡標 B，第三層標 C；節點是帶缺口的藍色圓（缺口大小表示「是否繼續展開」的信心），葉端是許多細小紅點。圖說（頁面）：三個階段是 Primer（拿查詢對最相關的 top-K 社群報告，產生初步答案與追問）、Follow-Up（用 local search 細化追問，每個節點帶信心分數決定是否繼續展開）、Output Hierarchy（輸出一棵依相關度排序的問答階層）。
- 給學生的一句話：DRIFT 先用社群報告給一個粗答案和追問，再一層層用局部檢索追下去。
- 注意：圖很扁、無文字，只有 A／B／C 三個標記，建議裁出左半或重畫成簡化樹。

### m4-graphrag-index-dataflow（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼）
- 來源：Microsoft GraphRAG〈Indexing Dataflow〉— https://microsoft.github.io/graphrag/index/default_dataflow/（已核實 2026-11-12）；原始碼 docs/index/default_dataflow.md
- 授權：redraw — 內容在 MIT repo 內，但沒有圖檔可放；用 rough.js 重畫
- 建議用在：407-two-schools（Microsoft 派的離線建圖流程）；408-global-search 之前
- 圖的結構：標題「Dataflow Overview」，由上而下六個階段（方框分組）。Phase 1 Compose TextUnits：Documents → Chunk → Text Units（預設 chunk 大小 1200 tokens，依該頁原始碼 default_dataflow.md 的文字）。Phase 2 Document Processing：Documents 與 Text Units → Link to TextUnits → Documents Table。Phase 3 Graph Extraction：Text Units → Entity & Relationship Extraction → Entity & Relationship Summarization → Claim Extraction → Graph Tables。Phase 4 Graph Augmentation：Graph Tables → Community Detection → Communities Table。Phase 5 Community Summarization：Communities Table → Community Summarization → Community Reports Table。Phase 6 Text Embeddings：Text Units → Text Embedding、Graph Tables → Description Embedding、Community Reports → Content Embedding。
- 給學生的一句話：先把文件切成 TextUnit，抽實體關係、分社群、寫社群報告，最後三種東西各做一份 embedding。

### m4-graphrag-global-local-search（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼）
- 來源：Microsoft GraphRAG〈Global Search〉https://microsoft.github.io/graphrag/query/global_search/ 與〈Local Search〉https://microsoft.github.io/graphrag/query/local_search/（皆已核實 2026-11-12）
- 授權：redraw — 同上
- 建議用在：408-global-search、409-local-search
- 圖的結構：**Global Search Dataflow**（由左到右）：User Query 與 Conversation History 匯成一個點，把「打亂的社群報告批次 1…N」各送進一個方塊，每批產生一則「Rated Intermediate Response」（附重要性評分）→ Ranking + Filtering → Aggregated Intermediate Responses → Response（map 平行、reduce 合併）。**Local Search Dataflow**：User Query 與 Conversation History →（實體描述 embedding）→ Extracted Entities；由實體展開五路候選：Entity-Text Unit Mapping → Candidate Text Units、Entity-Report Mapping → Candidate Community Reports、Entity-Entity Relationships → Candidate Entities、同一關係 → Candidate Relationships、Entity-Covariate Mappings → Candidate Covariates；每路各自 Ranking + Filtering 成 Prioritized 版本，與 Conversation History 一起匯入 Response。
- 給學生的一句話：全局檢索是「每批社群報告各答一次、再合併」，局部檢索是「先找實體，再往外抓相關資料」。

### m7-mcp-simple-diagram（direct）
- 檔案：assets/figures/m7/d-mcp-simple-diagram.png（3840×1500）
- 來源：Model Context Protocol〈What is the Model Context Protocol (MCP)?〉— https://modelcontextprotocol.io/docs/getting-started/intro（已核實 2026-11-12，會轉址到 /docs/2026-07-28/getting-started/intro）；原檔 https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/images/mcp-simple-diagram.png
- 授權：direct — repo LICENSE 寫明「專案正由 MIT 轉換到 Apache-2.0；新的程式碼與規格貢獻為 Apache-2.0；文件貢獻（不含規格）為 CC-BY-4.0；尚未取得重新授權同意的貢獻維持 MIT」。三種授權都允許轉載，都要求保留出處／授權聲明。這張圖 2025-04 由 Alex Isken 取代、2025-10 有錯字修正（Koichi ITO），無法確定適用哪一種，`.src` 寫「來源：Model Context Protocol 文件，MIT／Apache-2.0／CC BY 4.0（見 repo LICENSE）」。
- 建議用在：702-nxm（N×M 整合爆炸 → 一個協定）
- 圖的結構：白底。中央藍色方塊「MCP — Standardized protocol」。左側三個黑框（欄底標「AI applications」）：Chat interface（Claude Desktop, LibreChat）、IDEs and code editors（Claude Code, Goose）、Other AI applications（5ire, Superinterface）。右側三個黑框（欄底標「Data sources and tools」）：Data and file systems（PostgreSQL, SQLite, GDrive）、Development tools（Git, Sentry, etc.）、Productivity tools（Slack, Google Maps, etc.）。六個框各用一條雙向箭頭接到中央方塊，兩側各標「Bidirectional data flow」。
- 給學生的一句話：左邊的 AI 應用和右邊的資料／工具都只對 MCP 說話，不用每對組合各寫一套整合。
- 注意：圖上的案例（Claude Desktop、LibreChat、5ire…）是官方的舉例，不是完整清單。

### m7-mcp-host-client-server（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼，網頁上沒有 img）
- 來源：Model Context Protocol〈Architecture overview〉段落「Participants」— https://modelcontextprotocol.io/docs/learn/architecture（已核實 2026-11-12）；另有規格頁〈Architecture〉https://modelcontextprotocol.io/specification/latest/architecture（已核實 2026-11-12）
- 授權：redraw — 文件為 CC BY 4.0／Apache-2.0／MIT 混合（見上），但沒有圖檔可放；用 rough.js 重畫，`.src` 同上寫出處
- 建議用在：703-host-client-server
- 圖的結構：**Learn 版**：一個大框「MCP Host (AI Application)」內有四個 MCP Client（Client 1–4）。框外三個 Server：Server A「Local（例：Filesystem）」、Server B「Local（例：Database）」、Server C「Remote（例：Sentry）」。連線：Client 1–Server A、Client 2–Server B、Client 3–Server C、Client 4–Server C，每條標「Dedicated connection」（Server C 同時被兩個 client 連線，表示遠端 server 可服務多個 client）。**規格版**（多一層邊界）：「Application Host Process」框內 Host → Client 1／2／3；「Local machine」框內 Server 1（Files & Git）、Server 2（Database）與各自雙向連到的 Local Resource A／B（圓柱）；「Internet」框內 Server 3（External APIs）雙向連到 Remote Resource C。Client 1→Server 1、Client 2→Server 2、Client 3→Server 3。
- 給學生的一句話：一個 Host 為每個 Server 各開一個 Client，一對一連線；Server 可以在本機也可以在遠端。
- 文字重點（頁面原文）：Host＝協調並管理多個 client 的 AI 應用；Client＝維持與一個 server 的連線並取得 context；Server＝提供 context 的程式。

---

## 二、找不到或不適用的項目

| 項目 | 結果 |
|---|---|
| LangGraph HITL 流程圖 | 現行 LangGraph〈Interrupts〉、LangChain〈Human-in-the-loop〉頁**沒有流程圖**（前者只有兩張 LangSmith Studio 截圖，後者零圖）。唯一的圖檔 `hitl.png` 只存在於 repo、網站未引用（見 m5-lc-hitl-interrupt）；Deep Agents 頁只有 Mermaid（見 m5-lc-hitl-flow-mermaid） |
| LangGraph supervisor 圖 | 現行〈Multi-agent〉頁**沒有 supervisor 圖**，頁面也不使用該詞。repo 內有 `supervisor.png`，但沒有任何頁面引用，且 `langgraph-supervisor` 已封存，所以未下載，改用 d-lc-pattern-subagents |
| LangGraph〈Persistence〉頁 | 該頁已無圖；圖搬到〈Checkpointers〉頁 |
| MCP Host／Client／Server 圖檔 | 官方頁面是 Mermaid，沒有圖檔（見 m7-mcp-host-client-server） |
| Microsoft GraphRAG 管線圖 | 官方文件首頁、Indexing Overview、Microsoft Research 部落格與專案頁**都沒有管線示意圖**（只有 Mermaid 與一張知識圖譜視覺化）。管線圖只在論文 *From Local to Global* 裡，那是論文同事的範圍；部落格圖沒有授權條款，不可直接放 |
| Anthropic〈Contextual Retrieval〉圖的授權 | 無任何開放授權，全部 redraw；只有圖上的數字（5.7／5.0／3.5／3.7／2.9／1.9）可以拿來重畫 |

## 三、logo（存放於 assets/figures/logos/）

通則：
- 所有檔案**未改形狀**；只有兩種修改：（1）simple-icons 的單色 SVG 在 `<svg>` 標籤加上 `fill="#官方色碼"`（simple-icons 預設無填色，會顯示成黑色），色碼取自 simple-icons 的 `data/simple-icons.json`；（2）`openai.svg` 的填色由白改黑。其餘（Python、Docker、PostgreSQL、LangChain 三件、ChromaDB、LLaMA-Factory、Cherry Studio）都是官方原檔。
- simple-icons 整個專案是 CC0，但它的 DISCLAIMER 明說「CC0 不代表每個 icon 本身都是 CC0；logo 是各品牌的商標」。所以 CC0 只解決「檔案能不能散布」，**商標使用仍受品牌條款約束**；下表第四欄寫的是品牌條款。
- 使用規則（BRIEF）：高度 ≤ 48px、不改形狀與顏色、只用來指稱「這是哪個套件」。
- 19 個全部都找到檔案。其中 **4 個的條款有風險或未能直接核實**（Docker、Anthropic、OpenAI、Neo4j），另有 7 個找不到品牌條款（見第四節）。

| 名稱 | 檔案 | 來源 URL | 授權／品牌條款 |
|---|---|---|---|
| Python | logos/python.svg | https://www.python.org/static/community_logos/python-logo-generic.svg（官方，頁面 https://www.python.org/community/logos/） | 官方雙色版（含 python 字樣）。PSF 頁面：鼓勵使用 Python 的專案與公司在網站、手冊等處放此 logo；商標屬 Python Software Foundation，細節見 PSF Trademark Usage Policy；**使用衍生版本或有疑慮請先詢問**（所以未採用 simple-icons 的單色衍生版）。原樣使用，無修改 |
| Ollama | logos/ollama.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/ollama.svg（simple-icons 登錄的來源是 Ollama 維護者在 https://github.com/ollama/ollama/issues/2152 提供的 logo.svg） | 檔案 CC0；Ollama 沒有品牌使用頁（程式碼 repo 為 MIT，不含商標）。色碼 #000000。注意：找不到官方品牌條款 |
| Docker | logos/docker.svg | 官方 Logo Kit https://www.docker.com/static/Docker-Logos-1.zip 內 `docker-logo-ocean-blue.svg`（頁面 https://www.docker.com/company/newsroom/media-resources/） | 官方 Ocean Blue 版（符合「只能用 Ocean Blue／Light Blue／Deep Blue／白色」）。**注意：條款偏嚴**。品牌頁：不得翻轉、傾斜、擠壓、拉伸、裁切、去色、單獨用字標；至少 24px。商標指引（https://www.docker.com/legal/trademark-guidelines/）：教育／說明用途只開放「字標」（文字 Docker），**logo 圖形需 Docker 事先授權**，且 logo「只能取自 Docker 的產品頁並經授權」。建議：工具頁先用文字「Docker」；要放 logo 請先寄 trademark@docker.com 確認 |
| PostgreSQL | logos/postgresql.svg | https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg（頁面 https://wiki.postgresql.org/wiki/Logo） | 官方 Slonik 全彩版。商標政策（https://www.postgresql.org/about/policies/trademarks/）：可在不暗示背書的前提下，用來指稱 PostgreSQL（例如文件、文章、活動）；**不得修改、不得與其他商標或 logo 並排呈現**；商業用途建議加 ®；建議附註「Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.」。注意：「不得與其他 logo 並排」對「工具頁一排 logo」的版面有影響，Lab 架構圖旁各放各的、不要排成一列 |
| Neo4j | logos/neo4j.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/neo4j.svg（simple-icons 註記來源與指引 https://neo4j.com/brand/#logo） | 檔案 CC0，色碼 #4581C3。**注意：品牌條款未能核實**：neo4j.com/brand 現在轉址到 Needle 設計系統站 https://www.neo4j.design/（抓到的只有站名，沒有條款文字），商標指引頁（neo4j.com 法務條款）也沒找到；simple-icons 的色碼可能是改版前的顏色。使用前請到 neo4j.design 確認現行 logo 與規定 |
| ChromaDB | logos/chromadb.svg | https://github.com/chroma-core/chroma/blob/main/docs/mintlify/images/light-logo.svg（Chroma 官方 repo 的文件 logo，淺色底版） | 檔案在 Apache-2.0 repo 內（Apache-2.0 第 6 條不授予商標權）。官網 https://www.trychroma.com/brand 是登入頁，沒有品牌頁。注意：找不到品牌條款。這是「圖形＋Chroma 字樣」的橫式 logo，寬高比約 4:1，高 48px 時寬約 190px。repo 內另有 favicon.svg 但內含第三方圖庫（Streamline）標記，未採用 |
| LangChain | logos/langchain.svg | https://www.langchain.com/brand-assets 的 `LangChain_Lockup_Black.svg`（官方 zip：https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a9998494f7b532d49a38525_langchain-brand-assets.zip） | 官方：「approved for use in documentation, presentations, press coverage, and community content, subject to the usage guidelines」。規定：維持原比例與間距、使用提供的淺／深色版本不要自行換色、不拉伸、不加特效、背景對比要夠、不用 Community logo 取代官方 logo。本檔用黑色版，放在白底或紙色底 |
| LangGraph | logos/langgraph.svg | 同上官方 zip 內 `LangGraph_OSS Lockup_light.svg` | 同 LangChain 的規定。深藍圓角底＋淺藍圖示＋「langgraph」字樣的淺色版 lockup |
| LangSmith | logos/langsmith.svg | https://www.langchain.com/brand-assets 頁面上的 `LangSmith_Wordmark_Black 1.svg`（https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a9936e524dccd963978bf0f_LangSmith_Wordmark_Black%201.svg） | 同 LangChain 的規定。只有字標（官方未提供 LangSmith 圖形符號）；官方 zip 內沒有 LangSmith 的 SVG，所以 SVG 是從頁面連結單獨取得 |
| Hugging Face | logos/huggingface.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/huggingface.svg（指引 https://huggingface.co/brand） | 檔案 CC0，色碼 #FFD21E（與官方品牌頁的 #FFD21E 一致）。官方品牌頁只提供下載（hf-logo 等 svg／png／ai），**沒有寫使用條款**，頁面僅寫「Download the official Hugging Face brand assets to use in your projects」。注意：條款未明示，只能視為允許指稱用途 |
| Qwen | logos/qwen.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/qwen.svg（來源 https://qwen.ai） | 檔案 CC0，色碼 #6950EF。注意：找不到官方品牌條款 |
| DeepSeek | logos/deepseek.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/deepseek.svg（來源 https://www.deepseek.com） | 檔案 CC0，色碼 #5786FE。注意：找不到官方品牌條款 |
| LLaMA-Factory | logos/llama-factory.png（1400×400，白底不透明） | https://github.com/hiyouga/LLaMA-Factory/blob/main/assets/logo.png（專案 README 首圖） | repo 為 Apache-2.0（不含商標授權）；專案沒有品牌頁，simple-icons 也沒收錄。注意：找不到品牌條款。圖內含標語「Easy and Efficient LLM Fine-Tuning」，需放在白底上 |
| MCP | logos/mcp.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/modelcontextprotocol.svg（來源是 MCP 文件的 logo/light.svg，https://github.com/modelcontextprotocol/docs/blob/573dc60c2e7aab2605b29d0bf27194aa7b02e4fb/logo/light.svg） | 檔案 CC0；MCP repo LICENSE 為 MIT／Apache-2.0／CC-BY-4.0 過渡（見 m7-mcp-simple-diagram）。色碼 #000000。沒有獨立的 logo 使用規範 |
| Dify | logos/dify.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/dify.svg（來源 https://github.com/langgenius/dify/blob/48f6b2e885eb40230dfe318fe4d3fb71b50dbc02/web/public/logo/logo.svg） | simple-icons 登錄授權為自訂：https://dify.ai/end-user-license-agreement；品牌條款 https://dify.ai/dify-brand-usage-terms：可在部落格、文件、簡報、教學影片、演講中**不需事先核准**用來指稱 Dify；不得改色、字型、比例、效果，不得與其他 logo 組合成新標誌，不得暗示背書；**付費訓練／課程若暗示官方背書需書面核准**；商業廣告與周邊需書面核准（marketing@dify.ai）。色碼 #0033FF 為官方色。注意：本課若是收費課程，頁面不可寫成「官方合作」 |
| n8n | logos/n8n.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/n8n.svg（來源 https://guidelines.n8n.design/logo） | 檔案 CC0，色碼 #FF91AC（官方粉）。官方 logo 頁：符號版提供粉／黑／白三色；留白＝符號高度；與夥伴 logo 並排時用加號連接、n8n 在左或上。頁面沒有寫誤用規則與最小尺寸。這是符號版，不含 n8n 字樣 |
| Cherry Studio | logos/cherry-studio.png（512×512） | https://github.com/CherryHQ/cherry-studio/blob/main/build/icons/512x512.png（官方 repo 的應用圖示） | repo 為 AGPL-3.0（Community Edition，另有商業授權可洽 bd@cherry-ai.com）；README 沒有 logo 或商標條款。注意：AGPL 管的是程式碼，圖示的商標與著作權使用條款找不到 |
| Anthropic | logos/anthropic.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/anthropic.svg（來源 https://www.anthropic.com） | 檔案 CC0，色碼 #191919。**注意：條款最嚴**。Anthropic 商標指引（https://www.anthropic.com/legal/trademark-guidelines）寫「You may only use our trademarks as specifically permitted by us and only in materials we approve beforehand」，禁止任何改色、字型、比例變更，也不提供公開 logo 下載；教育性指稱的用法在指引中沒有明文開放。建議：用文字「Anthropic」，要放 logo 先寄 marketing@anthropic.com |
| OpenAI | logos/openai.svg | https://github.com/openai/openai-agents-python/blob/main/docs/assets/logo.svg（OpenAI 官方 repo，MIT；原檔是白色填色，本檔只把填色改成 #000000 以便放在淺色底） | **注意：條款未能直接核實**。官方品牌頁 https://openai.com/brand/ 與 https://openai.com/design 對自動化存取回 403，讀不到原文；simple-icons 已不收錄 OpenAI；GitHub 組織頭像只有 200×200，不符 ≥256px，所以沒用。依搜尋結果摘要與第三方整理（非官方原文）：第三方可依品牌指引使用，不得改動、需有足夠留白與對比、用黑或白色、不得暗示背書、不得用在周邊，OpenAI 可隨時要求停用。建議：放之前在瀏覽器打開 openai.com/brand 讀一次原文 |

## 四、風險彙整

- **條款需要先確認才能放 logo**：Docker（logo 圖形需授權）、Anthropic（需事先核准）、OpenAI（原文未能讀取）、Neo4j（品牌站改版，條款未能讀取）。這四個建議工具頁先用文字，確認後再放圖。
- **找不到品牌條款但風險低**（僅用來指稱）：Ollama、Qwen、DeepSeek、ChromaDB、LLaMA-Factory、Cherry Studio、Hugging Face（有下載頁但沒寫條款）。
- **條款明確且允許**：Python、PostgreSQL（但不得與其他 logo 並排）、LangChain／LangGraph／LangSmith、Dify（收費課程不得暗示官方背書）、MCP、n8n。
- 所有檔案都只是存檔，沒有執行；zip 檔（LangChain 品牌包、Docker logo kit）解壓在 scratchpad，只取出需要的 SVG，並確認 SVG 內沒有 script 或外部連結。
- 授權是否足以支撐「公開散布這份 deck」超出技術判斷，最後由課程方決定；本檔只記錄事實與條款原文要點。
