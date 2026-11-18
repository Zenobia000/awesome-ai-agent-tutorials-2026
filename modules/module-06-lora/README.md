# 模組 6：LoRA 微調

用 PEFT 微調 Qwen2.5-0.5B，教它用固定格式回答 IT 維運問診，最後合併權重、說明怎麼匯出給 Ollama。

先讀 `00_concepts.md`（原理紀要：LoRA 為什麼能用不到 1% 的參數微調、對話模板與 loss 遮罩、什麼時候不該微調），再依序開 notebook。

| 檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md` | 原理：凍結 W＋B×A、r 與 alpha、參數量算式、合併、loss 遮罩、prompt／RAG／微調怎麼選、常見坑 | 只要讀 |
| `01_peft_finetune.ipynb` | Lab 6：PEFT LoRA 微調 Qwen2.5-0.5B-Instruct；印出可訓練參數與 LoRA 模組結構、`Trainer` 依驗證 loss 挑 checkpoint、微調前後對比 | GPU 約 5GB，訓練不到 1 分鐘 |
| `02_merge_and_serve.ipynb` | 載入 adapter、`merge_and_unload`、驗證 `W + B·A × scaling`、GGUF 與 Modelfile 步驟 | 先跑 01；`/tmp` 暫用約 1GB |
| `03_when_not_to_finetune.ipynb` | 選讀：同一任務改用 prompt＋值班手冊（0.5B、3B）對比 LoRA | 先跑 01；Ollama `qwen2.5:3b` |

## 準備

```bash
uv sync --group m6
uv run python modules/module-06-lora/make_dataset.py   # 資料已附在 data/，改模板後才需要重跑
uv run jupyter lab modules/module-06-lora
```

notebook 從本資料夾開啟（讀的是相對路徑 `data/`，並 import 同資料夾的 `lab6_utils.py`）。

## 資料

`make_dataset.py` 用模板產生虛構的 IT 維運問診資料（14 種故障，服務與主機名稱都是假的）：

| 檔案 | 筆數 | 用途 |
|---|---|---|
| `data/itops_train.jsonl` | 320 | 訓練 |
| `data/itops_val.jsonl` | 28 | 挑 checkpoint；症狀說法與服務名稱都沒在訓練集出現 |
| `data/itops_test.jsonl` | 30 | 最後評估；又換一種說法 |

輸出格式固定兩行：`可能原因：…` 與 ``第一步檢查：`指令` ``。

## 注意

- 只用 `Qwen/Qwen2.5-0.5B-Instruct`（bf16，不用 4-bit）。GPU 跟 Ollama 共用，batch 設 8。Trainer 的中間 checkpoint 放 `/tmp/m6_checkpoints`，訓練完自動刪除。
- adapter 存在 `/tmp/m6_lora_adapter`（約 18MB），02、03 從這裡讀；重開機會消失，重跑 01 即可。想保留就複製到 `outputs/`（已列入 `.gitignore`）。
- 02 合併後的完整權重存在 `/tmp/m6_merged`，notebook 最後會刪掉。GGUF 轉換與 `ollama create` 只寫步驟，不在本機執行。
- 已存的輸出是一次執行結果。0.5B 模型微調後格式幾乎全對，但指令正確率約八成，答錯時格式一樣漂亮：這是 01 Step 9 與 03 的教學重點。
