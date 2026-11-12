# Lab 3／Lab 6 程式碼驗證紀錄（2026-11-12）

結論：5 張投影片共找到 **4 個會讓學生跑不起來或跑了沒效果的錯**，已改在 351、650；350、352、651 沒有需要改的程式文字。

| # | 位置 | 錯誤 | 驗證方式 | 後果 |
| --- | --- | --- | --- | --- |
| 1 | 650 YAML 缺 `do_train: true` | `do_train` 預設 False | 實跑 `llamafactory-cli train`（小模型） | exit 0，但只做評估，**完全沒訓練、沒存 adapter** |
| 2 | 650 `template: qwen3_nothink` | Qwen3-8B 是混合思考模型，應用 `qwen3` | 實跑 LLaMA-Factory 模板程式碼＋Qwen3-8B 真 tokenizer | 訓練格式與基座非思考模式（預填空 think）不一致 |
| 3 | 351/352 的 `text[d]` | `text` 從未定義（351 只有 `texts` 列表） | 實跑 | `NameError`；若學生自己取別名成列表則 `TypeError: list indices must be integers` |
| 4 | 351 `col.add(` | 350 寫「資料更新時重跑」，但 `add` 遇到已存在的 id 會**靜默略過** | 實跑（Chroma 1.5.9） | 重跑後舊內容、舊 `version` 都沒被更新，且不報錯 |

另有 2 個「能跑但效果不對」的設定也一併改了（650：`eval_strategy: steps`、缺 `logging_steps`），見 Lab 6 一節。

## 環境

| 項目 | 版本／備註 |
| --- | --- |
| 隔離環境（Lab 3） | `scratchpad/labcheck/.venv`，`uv venv` + `uv pip install`，torch 2.15.0+cpu（CPU 版 index） |
| Lab 3 套件 | sentence-transformers 6.3.0、transformers 5.22.2、chromadb 1.5.9、langchain-text-splitters 1.1.3、rank-bm25 0.2.2 |
| Lab 6 環境 | `scratchpad/lfenv/.venv`，llamafactory 0.9.6.dev0（GitHub main，commit f28b1b4），transformers 5.8.0、peft 0.18.1、trl 0.24.0 |
| 小模型代替 | `sentence-transformers/all-MiniLM-L6-v2`（代 bge-m3）、`cross-encoder/ms-marco-MiniLM-L6-v2`（代 bge-reranker-v2-m3）、`trl-internal-testing/tiny-Qwen3ForCausalLM`（Lab 6 小跑） |
| 路徑 | 全部在 `/tmp/claude-895651700/-home-os-sunnie-gd-weng-python-workstation-github-sunny-awesome-ai-agent-tutorials-2026/b6f32540-6798-4750-a681-89b2769cc43e/scratchpad/`（下稱 `$S`）的 `labcheck/`、`lfenv/`、`lf/` |

---

## Lab 3（RAG）

測試文件：`$S/labcheck/whitepaper.md`（6 節、含 `#`/`##`/`###` 三層標題、英文錯誤碼 `ORN-4012`、一節中文）。

### 350 架構圖（無程式碼，核對圖上的主張）

| 圖上主張 | 驗證 | 結果 |
| --- | --- | --- |
| 本地 Chroma 沒有內建混合檢索，是 Chroma Cloud 才有 | 實跑 `Collection.search(Search().rank(Rrf(...)))` | 套件有 `Search`/`Rrf` 類別，但呼叫本地 collection 回 `NotImplementedError: Search is not implemented for Local Chroma`。主張成立。 |
| `bge-m3`、`bge-reranker-v2-m3` 名稱 | HF API 查 repo | 兩者存在（見下「模型載入」） |
| BM25 那路也要套版本過濾 | 實跑（下 352） | 成立 |

**沒改。**

### 351 切分與入庫（左：MarkdownHeaderTextSplitter；右：SentenceTransformer＋Chroma）

驗證方式：實跑。把投影片 `.code` 的文字直接從 HTML 抽出來 `exec`（腳本 `$S/labcheck/e2e_from_slides.py`），只替換兩個模型名。

結果：
- 切成 6 段；每段 metadata 帶 `h1/h2/h3`；`strip_headers=False` 時標題留在內文，預設 True 時標題被拿掉（對照實測）。
  ```
  '## Authentication  \n### Token refresh  \nAccess tokens expire ...' {'h1': 'Orion Gateway Whitepaper', 'h2': 'Authentication', 'h3': 'Token refresh'}
  default strip_headers=True first chunk: 'Access tokens expire after 15 minutes. Clients must call the'
  ```
- `PersistentClient`、`get_or_create_collection`、`query_embeddings` 傳入、`where={"version": "v2"}` 全部正常。
- `where` 過濾確實生效（把 c3 改成 `v1`）：
  ```
  dense with where v2 : ['c0', 'c1', 'c2', 'c4', 'c5'] (c3 excluded: True)
  dense without where : ['c3', 'c0', 'c1', 'c2', 'c4', 'c5']
  ```
- Chroma collection 預設距離是 `l2`（讀 `col.configuration` 確認）；bge-m3 的 `modules.json` 含 `2_Normalize`，向量已正規化，l2 與 cosine 排序等價，所以不必設 `hnsw:space`。

發現的錯與修改：

1. **`add` 重跑不更新（錯 #4）**。實測：
   ```
   before: 6 c1 version = v2
   after add():   doc = '## Authentication  \n### Token refresh  \n' version = v2 count = 6   <- 新內容被略過
   after upsert():doc = 'NEW TEXT' version = v3 count = 6
   ```
   改：`col.add(` → `col.upsert(`；下方註解句加上「重跑用 `upsert`，同 id 才會被覆寫（`add` 會靜默略過）」。
2. **`text` 未定義（錯 #3）**。352 的 `text[d]` 需要「id → 內文」字典。改 351 右欄：新增 `ids = [...]` 與 `text = dict(zip(ids, texts))  # id → 內文，查詢要用`，`upsert` 改用 `ids=ids`。右欄由 12 行變 13 行（上限 14）。
3. 版面：右欄變高，下方註解 `.nt` 與框底相碰，`top:858px` → `top:892px`。`./shoot.sh 351` 重截，無溢出、無重疊。

改後重跑（從投影片 HTML 抽碼）：第一次建庫、第二次重跑都成功，`indexed: 6 chunks`（沒有重複寫入）。

### 352 召回、融合、重排、組裝

驗證方式：實跑（同上，抽碼 exec）。投影片沒給的 `bm25_top_ids` 我用 `rank_bm25.BM25Okapi` 自寫（與投影片「自己做的 BM25」一致，且套同一個 `version` 過濾）。

| 片段 | 結果 |
| --- | --- |
| `col.query(... n_results=20 ...)` | 庫內只有 6 段時回 6 段，不報錯 |
| BM25 + dense 兩路 | 問 `What does error ORN-4012 mean?`：BM25 抓到含錯誤碼的 c1（dense 也排第 1）；問改寫句 `how long before my login credential stops working`：BM25 排 c3、dense 排 c1，兩路確有互補 |
| `rrf()` | 手算對照通過：`rrf([[x,y,z],[y,z,w]])` 得 `['y','z','x','w']`，與 y=1/62+1/61 > z=1/63+1/62 > x=1/61 > w=1/63 一致 |
| `CrossEncoder.predict` → `sorted(zip(...))` → `top3` | 回傳 `ndarray float32`，`top3 = ['c1','c4','c2']`，prompt 串接正常 |
| 「BM25 也要套過濾，否則舊版片段混進來」 | 成立：未過濾的 BM25 回 `['c3','c2','c0','c4']`（c3 是 v1），過濾後 `['c0','c2','c4']` |

**程式文字沒改**（錯 #3 的修正在 351）。原 `text[d]` 沒定義的重現：
```
fused ... scores = reranker.predict([(q, text[d]) for d in fused])
TypeError: list indices must be integers or slices, not str      # text 若取別名成 texts 列表
```

實作時踩到、但投影片沒寫（未改，列入「未驗證／建議」）：
- BM25 若不丟掉分數 0 的文件，會把完全不相關的段落以任意順序塞進 RRF；我的版本用 `if s > 0` 濾掉。
- `rank_bm25` 需要自己斷詞；中文要用 jieba 或單字／bigram，不能直接 `split()`。我只用單字切（`[一-鿿]`）驗流程，沒評估中文品質。

### 模型載入（bge-m3、bge-reranker-v2-m3）

驗證方式：HF 模型頁／API 核對＋用「真實 config 縮小尺寸、隨機權重」的本地副本跑同樣的載入呼叫。**沒有下載 2.2GB 真權重。**

| 問題 | 結果 | 依據 |
| --- | --- | --- |
| `SentenceTransformer("BAAI/bge-m3")` 要不要 `trust_remote_code` | **不用**。`config.auto_map` 為空，架構 `XLMRobertaModel`，library 為 sentence-transformers | HF API；模型頁用法就是 `SentenceTransformer("BAAI/bge-m3")` |
| bge-m3 載入後是否正規化 | 是。`modules.json` = Transformer → Pooling(CLS) → Normalize，維度 1024，`max_seq_length` 8192 | `modules.json`、`1_Pooling/config.json`；本地副本實跑 `norms: [1. 1.]` |
| `CrossEncoder("BAAI/bge-reranker-v2-m3")` 能否直接載 | **能**。架構 `XLMRobertaForSequenceClassification`、`id2label` 只有一個 label（`num_labels=1`），模型頁用法就是 `CrossEncoder(...)`＋`predict` | HF 模型頁；本地副本實跑 `CrossEncoder num_labels: 1` |
| reranker 要不要 `trust_remote_code` | 不用（只有 `bge-reranker-v2-minicpm-layerwise` 才要） | HF 模型頁 |
| 分數範圍 | `CrossEncoder.predict` 預設會套 **Sigmoid**（config 沒指定 activation、`num_labels==1`），分數落在 0–1；模型頁範例的負數是 `FlagReranker` 的原始 logit。排序相同，只是數字不同 | sentence-transformers `get_default_activation_fn()` 原始碼；本地副本 `default activation_fn: Sigmoid`、範圍檢查 True |
| 備註 | bge-m3 repo 只有 `pytorch_model.bin`（無 safetensors） | HF API 檔案清單 |

**沒改。**

---

## Lab 6（LoRA）

### 650 `clinic_lora.yaml`

驗證方式：
1. **對文件／原始碼**：讀 GitHub 主分支 `hiyouga/LlamaFactory`（原 `LLaMA-Factory`，舊網址會轉址）的 `examples/train_lora/qwen3_lora_sft.yaml`、`.sh`、`examples/merge_lora/qwen3_lora_sft.yaml`、`src/llamafactory/hparams/{finetuning,data,training}_args.py`、`data/template.py`、README 模型／模板表與硬體表。
2. **實跑解析**：用 LLaMA-Factory 自己的 `get_train_args` 解析投影片 YAML（真實 id `Qwen/Qwen3-8B`，不載入權重）；打錯鍵名會被擋（`Some keys are not used by the HfArgumentParser: ['lora_rnak']`），所以「解析通過」＝鍵名都存在。
3. **實跑小模型**：`trl-internal-testing/tiny-Qwen3ForCausalLM`＋60 筆 ShareGPT 假資料，跑 `llamafactory-cli train`（CPU，約 10 秒）與 `llamafactory-cli export`。

逐鍵核對：

| 鍵／值 | 結果 |
| --- | --- |
| `model_name_or_path: Qwen/Qwen3-8B` | 存在、Apache-2.0。官方範例用的是 `Qwen/Qwen3-4B-Instruct-2507`，但 8B 同樣支援（README 表：Qwen3 0.6B–235B） |
| `stage: sft` | 有效，**預設就是 sft**（`finetuning_args.py`） |
| `finetuning_type: lora` | 有效，預設也是 lora |
| `lora_rank: 8` | 有效，預設 8；官方範例同 |
| `lora_alpha: 16` | 有效；預設 None，原始碼 help 寫「default: lora_rank * 2」，註解「一般取 rank × 2」正確。adapter_config 實測 `r=8, lora_alpha=16` |
| `lora_target: all` | 有效，預設就是 all；實測展開成 q/k/v/o/gate/up/down 七類線性層，註解正確 |
| `dataset: clinic_sharegpt` | 鍵有效；**必須先在 `data/dataset_info.json` 註冊**（我用 `formatting: sharegpt`、`columns.messages: conversations` 註冊後跑通）。投影片沒顯示註冊步驟，見下 |
| `learning_rate: 1.0e-4`、`num_train_epochs: 3.0` | 有效，與官方範例完全相同 |
| `val_size: 0.1` | 有效（float，預設 0） |
| `eval_strategy` | 鍵有效（HF Trainer），但 `steps` 有問題，見下 |
| `output_dir`、`plot_loss` | 有效 |
| `template: qwen3_nothink` | **不適用 Qwen3-8B**，見下 |
| `llamafactory-cli train clinic_lora.yaml` | 寫法正確（實跑 exit 0）；另 `export`、`chat`、`api`、`webui` 子命令存在 |

#### 錯 #1：缺 `do_train: true`（嚴重）

投影片 YAML 原樣（只換小模型）實跑：
```
exit=0
***** Running Evaluation *****
  eval_loss = 11.9306
--- output_dir:
all_results.json  eval_results.json  trainer_log.jsonl        # 沒有 adapter_model.safetensors
```
加上 `do_train: true` 後才有 `Total optimization steps = 21`、`adapter_model.safetensors`、`checkpoint-21`。官方 `examples/train_lora/qwen3_lora_sft.yaml` 與 `qwen3_lora_sft_ds3.yaml` 都寫了 `do_train: true`。
→ 已加，並在行尾註解「沒寫就只評估、不訓練」。

#### 錯 #2：`template` 該用 `qwen3`，不是 `qwen3_nothink`

證據（`$S/lfenv/tpl_check.py`，用 Qwen3-8B 真 tokenizer 與 LLaMA-Factory 模板程式碼渲染同一筆對話）：
```
template=qwen3         PROMPT '<|im_start|>user\n最近一直頭痛<|im_end|>\n<|im_start|>assistant\n'
                       RESPONSE(算 loss) '<think>\n\n</think>\n\n您好，我是安心診所的問診助理。...<|im_end|>\n'
template=qwen3_nothink PROMPT 同上
                       RESPONSE(算 loss) '您好，我是安心診所的問診助理。...<|im_end|>\n'      # 沒有 think 標籤
Qwen3-8B 原生 chat_template, enable_thinking=False 的生成提示:
  '...<|im_start|>assistant\n<think>\n\n</think>\n\n'
```
- LLaMA-Factory 載入 `qwen3` 時自己印警告：「If the base model is NOT a reasoning model (i.e., it has a separate Instruct variant), please add `_nothink` suffix」。README 同樣寫：模型同時有思考／非思考版本時才用 `_nothink` 區分，且「訓練與推理必須用同一個 template」。
- 官方範例用 `qwen3_nothink` 是因為它的基座是 **Instruct-2507**（純非思考、獨立 Instruct 版）。**Qwen3-8B 是混合思考模型**（沒有獨立 Instruct 版；其原生模板有 `enable_thinking`），應用 `qwen3`：訓練時回覆前補空 `<think>\n\n</think>\n\n` 並算 loss，與基座的非思考模式輸出一致。
- 若用 `qwen3_nothink` 訓練再用基座原生模板推理（非思考模式預填空 think），推理時看到的前綴是訓練沒見過的。這是由模板輸出推得的後果，**沒有真的訓練 8B 驗證實際影響大小**。
→ 已改 `template: qwen3`。

#### `eval_strategy: steps` 與 `logging_steps`（能跑但沒效果）

小模型實跑（21 步）：
- 原設定（`eval_strategy: steps`、沒寫 `logging_steps`）：`eval_steps`、`logging_steps` 都落到預設 500，訓練中**一次評估都不會觸發**（只在結束時評一次），訓練 loss 沒有任何記錄，`plot_loss` 印 `No metric loss to plot.`。
- 改為 `eval_strategy: epoch`、`logging_steps: 10` 後：每個 epoch 評估一次（3 筆 `eval_loss`），每 10 步一筆 `loss`（`trainer_log.jsonl` 共 6 行，含 2 筆 train loss、3 筆 eval loss）。這才對得上課綱 Lab 6「監控 Loss 下降趨勢」。
- 不寫 `eval_steps`：HF 會把它設成 `logging_steps`，若繼續用 `steps` 會變成每 10 步評估一次，所以選 `epoch`。
→ 已改，並加行尾註解。

#### YAML 取捨（`.code` 上限 14 行）

原本就是 14 行。要加 `do_train`、`logging_steps` 必須騰出位置，取捨如下，**請作者確認**：
- 刪 `stage: sft`（預設值，實跑省略後照樣跑通）。
- 刪 `plot_loss: true`（無 `logging_steps` 時沒有作用；有 `logging_steps` 時 loss 仍會印在終端與 `trainer_log.jsonl`，只是不出圖）。
- 其餘鍵都保留。

改後最終 YAML（從投影片 HTML 抽出，去註解）：
```
model_name_or_path: Qwen/Qwen3-8B
do_train: true
finetuning_type: lora
lora_rank: 8
lora_alpha: 16
lora_target: all
dataset: clinic_sharegpt
template: qwen3
learning_rate: 1.0e-4
num_train_epochs: 3.0
val_size: 0.1
eval_strategy: epoch
logging_steps: 10
output_dir: saves/qwen3-8b/lora/clinic
```
解析結果：`PARSE OK`，`do_train = True`、`eval_strategy = EPOCH`、`template = qwen3`、`lora_rank/alpha = 8 16`。同樣內容（換小模型）實跑通過：訓練、存 adapter（`adapter_config.json`：`r=8, lora_alpha=16`，七類 target）、`llamafactory-cli export` 合併（`Merged 1 adapter(s).`，輸出含 `model.safetensors` 與 Ollama 用的 `Modelfile`）。`./shoot.sh 650` 截圖確認 14 行未溢出 `.code` 框、無重疊。

### 651 微調前後對比

沒有 YAML 或程式碼，只有標「示意」的問答對照，**沒有可驗證的程式碼，沒改**。

---

## 實際改動清單

| 檔案 | 改了什麼 |
| --- | --- |
| `slides/351-lab3-index.html` | 右欄：新增 `ids`、`text = dict(zip(ids, texts))`；`col.add` → `col.upsert`；下方註解加 `upsert` 說明並把 `.nt` 由 `top:858px` 移到 `top:892px`（避免貼到框底） |
| `slides/650-lab6.html` | YAML：加 `do_train: true`；`template: qwen3_nothink` → `qwen3`；`eval_strategy: steps` → `epoch`；加 `logging_steps: 10`；刪 `stage: sft`、`plot_loss: true`；新增 3 條行尾註解 |
| `350`、`352`、`651` | 無改動（已與備份 diff 確認） |

備份在 `$S/slides_backup/`。截圖：`shots/350`、`351`、`352`、`650`、`651` 均已重截並逐張看過，無溢出、無重疊。

## 仍未驗證（與原因）

| 項目 | 原因／建議 |
| --- | --- |
| 真權重的 `bge-m3`／`bge-reranker-v2-m3` 載入與中文檢索品質 | 各約 2.2GB，依指示未下載；載入方式已由 HF 頁面、config、縮小副本三方核對。bge-m3 只有 `pytorch_model.bin`，推測舊 torch（< 2.6）搭配新版 transformers 可能拒絕載入 `.bin`（**推論，未實測**） |
| 中文 BM25 | 投影片沒給 `bm25_top_ids`；我只用單字切分驗流程。Lab 講義需補斷詞做法（jieba 或字／bigram）與「分數 0 不入榜」 |
| Qwen3-8B 實際 LoRA 訓練、顯存與耗時 | 無 GPU。README 硬體表估 16-bit LoRA 約 `2x` GB（8B 約 16GB）。**未加但建議作者決定**：`bf16: true`（LLaMA-Factory 對未開混合精度會警告 `We recommend enable mixed precision training.`）、`per_device_train_batch_size: 1`＋`gradient_accumulation_steps: 8`（官方範例用法；預設批次是 8，24GB 下是否 OOM 沒驗證）。受 14 行上限限制沒放進去，可考慮挪到右欄文字或拆一頁 |
| `clinic_sharegpt` 的註冊 | 需在 `data/dataset_info.json` 加 `formatting: sharegpt`、`columns.messages` 對應；投影片 650 只講「ShareGPT 格式」，沒講註冊。不確定別頁是否已涵蓋 |
| Windows 讀檔編碼 | 351 的 `open("whitepaper.md")` 沒指定編碼；白皮書若含中文，Windows 預設編碼可能出錯。只在 Linux 驗證，沒改 |
| 「`qwen3` vs `qwen3_nothink` 對 8B 推理表現的實際差距」 | 只驗證了訓練模板輸出與基座原生模板的差異，沒訓練比較 |

---

## 第二輪補洞（2026-11-12）：Lab 3 中文斷詞、Lab 6 顯存與資料集註冊

動到的檔案只有 `slides/352-lab3-query.html`、`380-pitfalls.html`、`651-lab6-compare.html`，以及 `650-lab6.html` 的一則行尾註解。備份在 `$S/slides_backup_r2/`。實驗腳本都在 `$S/labcheck/zh/`（Lab 3）、`$S/lfenv/reg/`（Lab 6）。

### A. Lab 3：中文 BM25 要先斷詞，分數 0 不入榜（352、380）

**結論：352 改用「字元 bigram」斷詞（純 Python 3 行，無額外套件），並以 `if v > 0` 濾掉 0 分；380 新增第四列，沒有替換任何一列。**

#### A1. 斷詞套件維護狀態（2026-11-12 查 PyPI JSON API 與 GitHub API）

| 套件 | PyPI 最新版 | 最後發布／提交 | 判斷 |
| --- | --- | --- | --- |
| `jieba` | 0.42.1 | PyPI 2020-01-20；GitHub master 最後提交 2020-02-15（repo 未封存、open issues 706） | **實質停更**。只有 sdist、無 wheel；在 Python 3.12 乾淨 venv 仍能 `pip install` 並執行（`pkg_resources` 缺席時有 fallback） |
| `rjieba`（jieba-rs 的 Python 綁定） | 0.2.2 | 2026-10-26；GitHub 同日有提交，jieba-rs 2026-10-15 有推送 | **維護中**，有各平台 wheel，MIT；沿用 jieba 的預設詞典（偏簡體） |
| `jieba-next` | 1.0.0rc1 | 2026-04-20 | 仍是 release candidate，不選 |
| `pkuseg` | 0.0.25 | 2020-07 | 停更 |
| `ckip-transformers` | 0.3.4 | 2023-04 | 要下載 transformer 模型，對本 Lab 太重 |
| `pyhanlp` | 0.1.89 | 2025-01 | 需要 Java |

#### A2. 實驗 A：9 段繁中小文件、8 題（`zh/exp1b.py`）

文件是 Orion 閘道白皮書的繁中版（權杖過期、ORN-4012／ORN-5503 錯誤碼、限流、設定檔路徑等）。「有命中」＝正解段落的分數 > 0 且排在第 1／前 3。

| 斷詞方式 | hit@1 | hit@3 | 平均有幾段分數 > 0 |
| --- | --- | --- | --- |
| `doc.split()`（沒斷詞） | 0／8 | 0／8 | **0**（8 題全部 9 段都是 0 分） |
| 字元 bigram（352 的 `tok`） | 8／8 | 8／8 | 3.1 |
| jieba 0.42.1 | 8／8 | 8／8 | 2.6 |
| rjieba 0.2.2 | 7／8 | 8／8 | 2.4 |

- 沒斷詞時 `split()` 不會切開中文，整句變成一個詞，和查詢的詞完全對不上；若又沒有 `v > 0`，這些段落全是 0 分，`sorted(..., reverse=True)` 依 id 倒序排出 `['c6','c5','c4','c2','c1',…]`，這串**與問題無關的名單**會原樣進 RRF。
- 看得到 jieba／rjieba 對繁中技術詞的斷詞不穩：文件裡「回傳錯誤碼」被切成 `回傳錯／誤碼`，查詢「錯誤碼」被切成 `錯誤／碼`，兩邊對不上（預設詞典偏簡體、遇到沒收錄的詞靠 HMM 猜）。bigram 沒有這個問題。

#### A3. 實驗 B：1106 段真實繁中技術文字、18 題（`zh/exp2.py`、`exp3.py`、`exp4.py`）

語料＝本 repo 的 `sources/M*.md`、`product-facts.md`、課綱，每行當一段（平均 125 字）。18 題是我寫的自然問句（如「Ollama 預設的上下文長度會截斷嗎」），正解＝含指定關鍵字串的段落；排名只算分數 > 0 的段落。

| 斷詞方式 | hit@1 | hit@3 | hit@10 | MRR |
| --- | --- | --- | --- | --- |
| `split()` | 4 | 11 | 13 | 0.42（3 題完全撈不到） |
| 單字 | 11 | 15 | 17 | 0.73 |
| rjieba 0.2.2（濾標點） | 12 | 16 | 17 | 0.79 |
| jieba 0.42.1（濾標點） | 13 | 17 | 17 | 0.83 |
| **字元 bigram（352 的 `tok`）** | **15** | **17** | 17 | **0.88** |

- `split()` 在這份語料不是 0，是因為文件中英混排，英文詞還對得上；**純中文文件才會整個落空**（實驗 A）。
- 換句話說：bigram 不輸 jieba 系、不依賴套件、不用管詞典。**但差距只有 1–2 題，樣本小、題目是我寫的，不能當 benchmark**；可以下的結論只有「bigram 至少和斷詞套件一樣好，且更簡單、更穩」。
- 若用 rjieba／jieba，必須自己濾掉標點與空白 token，否則「，」「。」這類每篇都有的 token 會讓幾乎每段都有分，`v > 0` 就幾乎濾不掉東西（1106 段裡平均有分的段數：未濾 998.8、濾掉後 499.5）。這也是選 bigram 的原因之一：不用再多寫一個過濾函式（投影片放不下）。

#### A4. 352 實跑（把 `.code` 文字從 HTML 抽出來 `exec`；`zh/e2e_zh.py`）

環境同第一輪（rank-bm25 0.2.2、chromadb 1.5.9，bge 系列換成 MiniLM 小模型）。文件＝7 段的繁中白皮書，其中「限流」段改標 `version=v1`。

| 查詢 | 投影片程式（bigram＋`v > 0`） | `split()` | `split()`且沒有 `v > 0` | bigram 但沒有 `v > 0` |
| --- | --- | --- | --- | --- |
| 錯誤碼 ORN-5503 是什麼意思 | `['c4','c1','c0','c5']`，c4 第 1 | `[]` | 6 段，開頭 `['c6','c5','c4','c2','c1']`（全 0 分，依 id 倒序） | 6 段（多 2 段 0 分的） |
| 憑證快到期會怎樣 | `['c6']`（正解） | `[]` | 同上 6 段，與問題無關 | 6 段（多 5 段 0 分的） |
| 設定檔放在哪裡 | `['c5']`（正解） | `[]` | 同上 6 段 | 6 段（多 5 段 0 分的） |
| 今天台北天氣如何（庫裡沒有） | `[]` | `[]` | 同上 6 段 | 同上 6 段 |

- 6 題 `split()` 全為 `[]`（沒斷詞 → 關鍵詞那一路撈不到）；沒有 `v > 0` 時，連「庫裡沒有答案」的題也會交出 6 段無關名單。
- 版本過濾：標成 v1 的「限流」段（c3）**沒有**出現在任何一次 `sparse` 或 `dense`；`col.get(where={"version":"v2"})` 對 BM25 路有效。
- 兩個 `.code` 都是 14 行（上限），最寬一行左 52 字、右 56 字；`./shoot.sh 352` 確認沒有溢出、沒有重疊。

#### A5. 352 的版面取捨（請作者確認）

BM25 實作加進來後，原本兩個框放不下（約 33 行程式碼塞進 28 行）。做法：
- 左框＝BM25（斷詞、過濾、取前 20）＋向量；右框＝RRF、重排、組裝。**RRF 函式從左框搬到右框**。
- 原本的 `top3 = [...]` 一行併進 `ranked[:3]` 直接拼提示詞（少一行）。
- 原下方註記 `.nt` 改寫成「`split()` 切不開中文、取相鄰兩字；0 分不進榜；BM25 也套同一個 `version` 過濾」。
- 沒有新增 353 頁（範圍限定三張）。若作者想讓程式碼更寬鬆，建議把「重排＋組裝」拆成 353。

#### A6. 已知限制（沒有解決，也沒放進投影片）

1. **`rank_bm25` 的 idf 在小語料會歸零**：某詞出現在剛好一半的文件時 idf＝0。實測 6 段文件、查詢「權杖」出現在 3 段 → 6 段全是 0 分，`v > 0` 把真正含該詞的段落也濾掉了。語料大於十幾段就不明顯；`rank-bm25` 最後一次發布是 2022 年。
2. **替代方案 `bm25s` 0.3.16（2026-10-28 仍有發布）實測可用**：吃同一個 `tok`，idf 恆為正（上例得到 0.249／0.249／0.249／0／0／0），1106 段實驗 hit@1 14、hit@3 17、MRR 0.85（與 rank_bm25 版 0.88 無實質差）。代價：`index()` 要多一行、會印進度條、**`get_scores([])` 會丟 `IndexError`**（查詢不足兩個字時 bigram 為空）。這輪沒換，因為使用者指定的是 rank_bm25＋斷詞；若作者要換，需要多處理空查詢。
3. 查詢只有 1 個字時 `tok(q)` 為空，rank_bm25 回傳全 0（不報錯），所以 `sparse` 為 `[]`，仍可由向量路補上。
4. 程式每次查詢都重建 BM25（為了讓版本過濾與資料更新保持簡單），語料大時要改成建一次再重用。
5. 向量路與重排用的是**英文小模型替身**，所以中文的 dense／rerank 品質、`bge-m3` 與 `bge-reranker-v2-m3` 對中文的實際表現**沒有驗證**；A4 的 `top3` 只代表程式能跑通。

#### A7. 380 踩坑頁

- 新增第四列（放在「跨語種」之後、`strip_headers` 之前）：症狀「中文文件問中文，關鍵詞那一路幾乎撈不到」→ 原因「中文沒有空格，`split()` 後整句變成一個詞，和問題對不上」→ 修法「先斷詞再建索引：取相鄰兩字（bigram）或用 jieba 類套件；分數 0 不入榜」。
- 沒有替換任何一列：列高 160→128、間距 190→146 後四列放得下（`./shoot.sh 380` 確認）；標題與「怎麼讀」的「三」改「四」。若作者想維持三列，最弱的是 `strip_headers` 那列（351 已把該行標黃並在下方註記說明），但 `product-facts.md` 要求踩坑頁提醒它，所以我沒刪。

### B. Lab 6：24GB 顯存建議值與資料集註冊（651，650 只動註解）

**結論：651 新增兩塊註記；650 的 YAML 不動，只在 `dataset:` 行加註解「要先註冊，見下頁」。**

#### B1. 鍵名核對（LLaMA-Factory 主分支）

| 項目 | 來源與結果 |
| --- | --- |
| 版本 | `hiyouga/LlamaFactory` main，commit `6d1059c`（2026-11-12）；`data/README.md` 於 2026-11-12 抓取（`$S/lf_data_README_main.md`） |
| `dataset_info.json` 位置 | README：必須放在 `dataset_dir`（預設 `./data`）；自訂資料集「make sure to add a dataset description」並在 YAML 指定 `dataset: dataset_name` |
| ShareGPT 註冊鍵 | README「Sharegpt Format → Supervised Fine-Tuning」：`file_name`、`formatting: "sharegpt"`、`columns.messages: "conversations"`、`columns.system: "system"`（`system` 欄預設是 None） |
| ShareGPT 資料預設角色 | `tags` 預設 `role_tag: from`、`content_tag: value`、`user_tag: human`、`assistant_tag: gpt`，與 607 的資料範例（`from`／`value`／`human`／`gpt`）一致，所以不必寫 `tags` |
| 訓練三鍵 | 官方 `examples/train_lora/qwen3_lora_sft.yaml` 同時有 `per_device_train_batch_size: 1`、`gradient_accumulation_steps: 8`、`bf16: true` |

#### B2. 實跑

1. **YAML 鍵解析**：650 的 YAML ＋ `bf16: true`、`per_device_train_batch_size: 1`、`gradient_accumulation_steps: 8`，模型 id 用真實的 `Qwen/Qwen3-8B`，以 LLaMA-Factory 自己的 `get_train_args` 解析 → `PARSE OK`，`bs/ga = 1 8`、`bf16 = True`、compute dtype `torch.bfloat16`。對照組把 `gradient_accumulation_steps` 打錯 → `Some keys are not used by the HfArgumentParser: ['gradient_accumulation_step']`，所以「解析通過」＝鍵名正確。這台機器沒有可用的 CUDA torch，**純 CPU 解析 `bf16` 要加 `use_cpu: true`**（否則 `Your setup doesn't support bf16/gpu`，這是環境限制，不是鍵名錯）。
2. **註冊片段實跑**（`lfenv/reg/`）：把投影片 651 的 JSON 片段（從 HTML 抽出，外面補一層 `{}`，與實際訓練的 `dataset_info.json` 逐鍵相同）＋ 40 筆 ShareGPT 假資料（含 `system: 你是安心診所的問診助理`），用 tiny Qwen3 在 CPU 上 `llamafactory-cli train`（同樣的 `bf16`、批次 1、累積 8、`template: qwen3`）：exit 0，`Num examples = 36`、`Instantaneous batch size per device = 1`、`Gradient Accumulation steps = 8`、`Total optimization steps = 5`，存出 `adapter_model.safetensors`。
3. **`columns.system` 的後果（這一輪新發現）**：同一份資料，註冊時**拿掉** `"system": "system"`（README 範例的最小寫法）也同樣 exit 0，但 LLaMA-Factory 印出的第一筆 `inputs:` 從
   `<|im_start|>system\n你是安心診所的問診助理<|im_end|>\n<|im_start|>user…` 變成直接從 `<|im_start|>user…` 開始。**system 欄被靜默丟掉，不報錯**。本 Lab 的身份標籤就放在 system，所以投影片的註冊片段加了這一行，並在標籤上說明。

#### B3. 沒有、也不能驗證的部分

- **「24GB 單卡（RTX 4090）跑 Qwen3-8B LoRA 這組值不會 OOM」沒有實測。** 這台機器的 GPU 是 RTX 2000 Ada（16GB，已被桌面佔用 2GB），lfenv 的 torch 是 CPU 版；8B 的 bf16 權重本身就約 16GB，放不下。投影片依指示標「建議值，未在 8B 實測」。我只驗證了**鍵名與數值能被 LLaMA-Factory 解析、在小模型上能跑**，沒有驗證記憶體用量。
- README 硬體表對 16-bit LoRA 的估計（約 `2x` GB，8B 約 16GB）是我在第一輪讀到的；因為數字不在課綱或素材地圖，**沒有寫上投影片**。

#### B4. 651 版面改動

原頁下方 120px 是空的，放不下兩個程式框，所以：
- 面板內的兩行「使用者：最近一直頭痛」移走，改放進副標題（「同一句「最近一直頭痛」丟給基座和微調後的模型…」）；面板高度 382→274。
- 底部黃色結論框保留原文，只縮成單行（padding 縮小）。
- 新增兩個小標＋兩個 `.code`（各 4 行）：左「24GB 單卡（RTX 4090）加進 clinic_lora.yaml」（含 `# 建議值，未在 8B 實測`）；右「自訂資料集：在 data/dataset_info.json 註冊；資料有 system 欄就要列出，否則被略過」。JSON 是片段（要加進最外層物件），標籤已寫「加進／註冊」；若學生整檔覆蓋會蓋掉內建資料集，**講課時要口頭提醒**，投影片放不下。
- 「怎麼讀」補一句「最下面是開跑前要補的設定」。`./shoot.sh 651` 確認沒有重疊、沒有溢出 `.code` 框。

### C. 本輪改動清單

| 檔案 | 改了什麼 |
| --- | --- |
| `slides/352-lab3-query.html` | 補 BM25 實作（bigram 斷詞、`col.get(where=...)`、`v > 0`）；RRF 移到右框；`top3` 併入 `ranked[:3]`；兩標題、`.nt`、「怎麼讀」重寫；框上移（標題 top 272、框 top 322） |
| `slides/380-pitfalls.html` | 新增第四列「中文 BM25 沒斷詞」；列高 128、間距 146；標題與「怎麼讀」三→四 |
| `slides/651-lab6-compare.html` | 重排版（見 B4），新增 24GB 建議值與 `dataset_info.json` 註冊兩塊 |
| `slides/650-lab6.html` | 只有一則行尾註解：`dataset: clinic_sharegpt  # 要先註冊，見下頁` |

截圖：`shots/352`、`380`、`650`、`651` 已重截並逐張看過，無溢出、無重疊。
