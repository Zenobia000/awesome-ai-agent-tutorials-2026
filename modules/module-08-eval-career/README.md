# 模組 8：評估、可觀測性與求職

先學會「量」：用現成指標和自寫的 LLM 評審打分、拿人工標註校準評審、用固定題庫擋回歸、
用 Langfuse 與 Opik 替每一步打點。最後把量到的數字變成履歷與面試回答。

原理（評分器種類、judge 偏誤、校準、回歸評估、trace／span／generation、指標怎麼選、Langfuse vs Opik）
寫在 [`00_concepts.md`](00_concepts.md)，先讀它再開 notebook；notebook 一開始就用套件做事。

本模組自帶一個受測系統：虛構公司「山嵐雲端」的內部 FAQ 助理（`mini_rag.py`，bge-m3 ＋ numpy 的最小 RAG），
不 import 其他模組。

| notebook | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md` | 原理紀要（不是 notebook） | — |
| `01_llm_as_judge.ipynb` | Opik 內建指標（字串相似度、Hallucination 經 LiteLLM 接 Ollama）＋結構化輸出寫 judge；重現位置偏誤與長度偏誤；四種評分器對 10 筆人工標註算一致率、TPR、TNR、混淆矩陣 | Ollama |
| `02_regression_eval.ipynb` | 40 題固定題庫，改 top_k、改 prompt 前後各跑一次；對比表、分標籤長條圖、回歸閘門與 pytest 版 | Ollama；約 240 次模型呼叫 |
| `03_langfuse.ipynb` | Langfuse SDK（5.x，OTel 架構）替檢索、生成、judge 打點並寫回分數；延遲分布、每題 token、瀑布圖、錯誤分析 | Langfuse 金鑰選填 |
| `04_opik.ipynb` | Opik `@opik.track` 打點、`record_traces_locally` 看 trace；把 02 的回答交給三種評分器比較；有伺服器時跑 `opik.evaluate()` | Opik 伺服器選填；先跑 02 |
| `05_interview_sandbox.ipynb` | 把 01～03 的實測結果轉成履歷句子並查核數字出處；從投影片 21 題面試題抽題，judge 依「限制、結構、數字」打分 | Ollama；先跑 01～03 |

模組內的檔案：

| 檔案 | 用途 |
|---|---|
| `mini_rag.py` | 受測系統：檢索、生成、兩個 prompt 版本（`v1` 基準、`v2`「更親切」的改版） |
| `judge.py` | 本課評審：LLM 量表評分（結構化輸出）＋「參考答案的數字要出現」程式規則 |
| `opik_setup.py` | Opik 環境設定；沒有帳號時切到本機模式（`import opik` 之前呼叫） |
| `test_regression.py` | 02 的回歸閘門 pytest 版 |
| `data/faq.jsonl` | 20 份虛構公司 FAQ |
| `data/eval_set.jsonl` | 40 題評估集（question、reference、doc_id、tags；含 4 題資料裡沒有的題目） |
| `data/judge_samples.jsonl` | 10 筆人工標註（pass／fail＋理由），用來校準 judge |
| `data/interview_questions.json` | 從投影片 `190-interview` … `880-interview` 抽出的 21 題面試題 |
| `runs/` | 01～03 跑出來的結果（04、05 會讀）；重跑 notebook 會覆寫 |
| `images/` | notebook 與 `00_concepts.md` 用的圖解 |

## 準備

```bash
uv sync --group m8 --group dev
cp .env.example .env
ollama pull qwen2.5:3b && ollama pull bge-m3
uv run jupyter lab modules/module-08-eval-career
```

notebook 從本資料夾開啟，並**依序**執行：04 讀 02 的 `runs/`，05 讀 01～03 的 `runs/`。
跑 pytest 版閘門：

```bash
cd modules/module-08-eval-career
CANDIDATE=runs/prompt_v2.json uv run pytest -q test_regression.py
```

### Langfuse 與 Opik（選填）

沒有設定時，03 和 04（以及 01 用到 Opik 指標的部分）都會在「本機模式」執行，不會上傳任何資料：
03 用 OpenTelemetry 的 `InMemorySpanExporter` 收 span；Opik 的網址指到 `localhost:5173`（沒有伺服器，送出失敗後丟棄），
並關掉用量統計與錯誤回報，trace 用 `opik.record_traces_locally()` 看。

要接上真的平台，在 `.env` 加：

```bash
# Langfuse：雲端 https://cloud.langfuse.com，或照 https://langfuse.com/self-hosting 自架
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com   # 舊名稱 LANGFUSE_HOST 也認得

# Opik：雲端 https://www.comet.com/signup，或照 https://www.comet.com/docs/opik/self-host/local_deployment 自架
OPIK_API_KEY=...
OPIK_WORKSPACE=...
# 自架只要這行：OPIK_URL_OVERRIDE=http://localhost:5173/api
```

## trace 原理與平台

`00_concepts.md` 第 5 節用十行 context manager 示範最小的 trace：每一步一行 JSONL，記時間、輸入輸出、token、延遲。
這就是可觀測性平台的核心；平台多做的是父子關係、介面、完整保存、分數篩選、團隊協作。03、04 會逐欄對照。

選型一句話：

| 需求 | 建議 |
|---|---|
| 開源、能自架、trace 與 prompt 管理一起顧 | Langfuse（MIT，`ee/` 除外；2026-01 被 ClickHouse 收購，承諾維持 MIT） |
| 評估指標要現成、想在 notebook 或 CI 直接算分 | Opik（Apache 2.0） |
| 團隊已全用 LangChain／LangGraph、要現成的協作與標註介面 | LangSmith（閉源 SaaS） |

不管選哪個，底層是 OpenTelemetry 就能換後端；judge 一律先用人工標註校準。

## 注意事項

- **受測系統和 judge 是同一個 `qwen2.5:3b`。** 這違反「不要讓模型評自己」的原則，是為了全程本地而接受的限制，01 和 05 都有明講。
- **3B judge 偏嚴而且有雜訊。** 常因措辭差異給 3 分，同一份資料每次跑的一致率可能差 1～2 筆；02 的閘門因此留了 1 題的容許值。
- **數字規則有誤殺。** 參考答案寫「6 個月」、回答寫「半年」，或「4 門」寫成「四門」，都會被判不一致；它只當否決票。
- **履歷數字。** 05 的句子全部從 `runs/` 自動帶入；課綱與投影片「履歷改寫前後」的 68%→91% 等數字是範本（見 `docs/slides/sources/product-facts.md` 第 8 條），notebook 中已分開標示。
- **Opik LLM 指標** 的 prompt 是英文、針對大模型設計，3B 模型偶爾吐不出要求的 JSON，該格分數會是空的。
- 已存的輸出是某一次執行的結果，模型回答與分數每次可能不同。
