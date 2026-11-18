# 模組 3：RAG 檢索增強生成

先看模型對公司內部的事怎麼亂答，再用 Chroma 把文件塞給它；接著逐一加上分塊、混合檢索、重排序，最後用題庫量出每一步的效果。
原理（為什麼、名詞、常見坑、多模態 RAG 的取捨）寫在 [`00_concepts.md`](00_concepts.md)，notebook 直接用套件做事。

| notebook | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md` | 原理紀要：embedding、分塊、BM25／RRF、重排、評估、PDF 解析、MinerU、RAG-Anything 的判斷 | 閱讀 |
| `01_embeddings.ipynb` | bge-m3 向量、cosine、PCA 散點圖、KMeans 分群、相似不等於相關 | Ollama |
| `02_first_rag.ipynb` | 沒有 RAG 時的幻覺 → Chroma 建索引、查詢、組 prompt → metadata 過濾擋掉舊版文件 | Ollama、chromadb |
| `03_chunking.ipynb` | LlamaIndex 的固定長度 vs 依標題切 vs 補上下文，畫長度分布、比命中率 | Ollama、llama-index-core |
| `04_hybrid_rrf.ipynb` | jieba＋rank_bm25 的關鍵字檢索、RRF 合併、LlamaIndex `QueryFusionRetriever` 對答案 | Ollama、rank-bm25、jieba |
| `05_rerank_and_query.ipynb` | cross-encoder 重排、名次變化圖、查詢改寫、HyDE、small-to-big | 下載重排模型約 470MB；GPU 可選 |
| `06_rag_eval.ipynb` | **Lab 3**：Hit@k、MRR、規則版與 LLM 評審的答對率、錯誤歸因，基線 vs 最佳組合 | 同上；約 5～10 分鐘 |
| `07_llamaindex.ipynb` | 用 LlamaIndex 重組整條管線，自訂 BM25 Retriever、重排 postprocessor，對照拼裝版 | Ollama、llama-index |
| `08_pdf_parsing.ipynb` | 選讀：雙欄交錯、表格攤平、區塊偵測；MinerU 與 olmocr 的輸出長什麼樣 | pymupdf（不下載模型） |

## 準備

```bash
uv sync --group m3
cp .env.example .env
ollama pull qwen2.5:3b && ollama pull bge-m3
uv run jupyter lab modules/module-03-rag
```

notebook 要從本資料夾開啟（讀的是相對路徑 `data/`，並 `import rag_utils`）。

## 資料

- `data/docs/`：虛構電商「海風科技」的 30 份內部技術文件（服務說明、runbook、事故回顧、FAQ、政策），含 2 份已封存的舊版說明。
  文件刻意放了大量錯誤碼、指令、版本號，讓純向量檢索有機會出錯。模組 5 與旗艦專案會沿用這份語料。
- `data/qa.jsonl`：38 題評估題庫（`question`、`answer`、`doc_ids`、`type`）。23 題靠關鍵字、15 題靠語意。
- `data/parser_sample/`：*Attention Is All You Need* 第 8 頁 Table 2 的 pymupdf 與 olmocr 解析結果（論文首頁聲明允許學術用途重製表格），供 `08` 對照。
- `rag_utils.py`：前幾本做過的步驟整理成的小函式（讀文件、切塊、建 Chroma collection、BM25、RRF、評估指標、帶重試的 `ask`）。

## 注意事項

- **Linux／Windows 用 uv 安裝時，LlamaIndex 的 `SentenceSplitter` 可能報 `PermissionError: refusing multiply-linked file`。** uv 預設用硬連結安裝套件，LlamaIndex 內附的 NLTK 資料會被安全檢查擋下。解法擇一：
  - 安裝時改成複製：`UV_LINK_MODE=copy uv sync --group m3 --reinstall-package llama-index-core`
  - 或打破那個資料夾的硬連結：`d=.venv/lib/python3.*/site-packages/llama_index/core/_static/nltk_cache; cp -r $d $d.tmp && rm -rf $d && mv $d.tmp $d`
  本模組 notebook 用 `MarkdownNodeParser`、`TokenTextSplitter`，不受影響。

- Chroma 一律用 `EphemeralClient`（只在記憶體）；`02` 示範 `PersistentClient` 時寫到暫存資料夾並刪除，不要把資料庫檔放進 repo。
- LlamaIndex 預設的 `SentenceSplitter` 需要 NLTK 資料；本模組改用 `MarkdownNodeParser` 與 `TokenTextSplitter`，不受影響。
- `qwen2.5:3b` 當生成器與評審都不穩：同一題重跑可能從對變錯，當評審時與規則版的一致率不高。檢索指標（Hit@k、MRR）是確定的，答對率差一兩題不要過度解讀。
- Ollama 被多人同時使用時偶爾逾時，`rag_utils.ask` 會自動重試；notebook 輸出裡的「第 1 次呼叫失敗」訊息就是這個。
- 已存的輸出是一次實際執行的結果，模型回答每次可能不同。

## 對應投影片

「RAG 是什麼」「搭橋：改輸入還是改權重」「RAG 離線與在線兩條鏈路」「向量空間與 metadata 過濾」「固定長度切分的截斷」「依標題切分並保留章節」「語義切分 vs 代理切分」「補背景讓檢索失敗率下降」「BM25 與向量的盲區」「混合檢索與重排」「RRF 怎麼算」「重排漏斗與模型」「雙塔與 Cross-Encoder」「父子片段：小的找、大的回」「文件轉問答：多開搜尋入口」「PDF 表格：轉成 Markdown」「Lab 3 架構」「Lab 3 切分與入庫」「Lab 3 檢索到組裝」「RAG 常見踩坑」「面試：RAG 檢索」
