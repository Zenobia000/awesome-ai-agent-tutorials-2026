# 模組 2：提示詞與結構化輸出

把 prompt 當成一份輸入規格來寫，用數字比較好壞；再讓模型的輸出變成程式能直接用、而且驗證過的物件。
最後把這些組成 Lab 2 的 Text2SQL：中文問題變成安全的唯讀查詢。

| 檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md` | 原理紀要：prompt 為什麼有效、CoT、約束解碼、注入為什麼擋不乾淨、Text2SQL 的風險、怎麼評估 | 閱讀即可 |
| `01_prompt_basics.ipynb` | 壞 prompt 與四段結構對照；同題跑 5 次算格式一致率 | Ollama |
| `02_cot_and_chaining.ipynb` | 直接回答 vs 思維鏈的準確率與字數；三步串接，步驟間插程式檢查與重寫 | Ollama |
| `03_structured_output.ipynb` | `json.loads` 失敗 → SDK `parse()` 與 Ollama `format` → Pydantic 業務規則 → 驗證失敗回饋重試 | Ollama、`openai`、`ollama`、`pydantic` |
| `04_prompt_injection.ipynb` | 五種攻擊 × 七種防禦的成功率熱圖；關鍵字與 LLM 偵測器的誤判 | Ollama |
| `05_text2sql.ipynb` | Lab 2：建 SQLite、DDL 注入、`SQLGenerationResult` 只放行 SELECT、唯讀連線、錯誤回饋重試、14 題正確率 | Ollama、內建 `sqlite3` |
| `06_eval_prompts.ipynb` | 用標註工單比較兩版 prompt：dev/test 切分、分類報告、混淆矩陣、bootstrap | Ollama、`scikit-learn` |

## 準備

```bash
uv sync --group m2
cp .env.example .env
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-02-prompt-structured
```

notebook 從本資料夾開啟（`05` 寫入 `data/ops.db`、`06` 讀 `data/tickets.csv`，都是相對路徑）。
建議先讀 `00_concepts.md` 對應的那一節再跑 notebook。

## 資料

| 檔案 | 內容 |
|---|---|
| `data/tickets.csv` | 48 張自寫的虛構工單（網路／資料庫／帳號／帳務），dev 12 張、test 36 張 |
| `data/ops.db` | `05_text2sql` 執行時用固定亂數種子重建：8 個服務、60 筆訂單、50 則告警（約 16KB） |

公司「星帆雲端」與所有客戶、人名都是虛構的。

## 注意事項

- 本模組全部用本機 `qwen2.5:3b`。小模型的錯誤（時間換算、JOIN、把說話的人當負責人）都保留在輸出裡，當作教學點。
- 有溫度大於 0 的實驗（`01`、`02`、`04`），每次重跑的數字會不同；notebook 裡的說明寫的是趨勢，不是固定數字。
- 結構化輸出走 Ollama 的 OpenAI 相容介面（`response_format`）。換成雲端模型只要改 `.env` 的端點。
- `04` 的攻擊只針對本 Lab 的工單分流情境，數字為 0% 不代表能擋住沒測過的攻擊。
