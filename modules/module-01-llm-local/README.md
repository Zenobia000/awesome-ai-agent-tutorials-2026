# 模組 1：LLM 底層與本地環境

原理（token、下一個 token、attention、記不住對話）寫在 `00_concepts.md`；notebook 直接用 `tiktoken`、`transformers`、OpenAI SDK 看模型在算什麼、跟它對話，最後寫出整門課共用的模型客戶端。

| notebook／檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md`（先讀） | 原理紀要：token 與 BPE、下一個 token 預測與 softmax、溫度／top-p、attention 與 Q/K/V、O(N²) context 成本、為什麼記不住對話、幻覺 | — |
| `01_tokens.ipynb` | 用 tiktoken 與 Qwen tokenizer 看切分、印出 BPE 合併規則、中英文 token 數比較、數 token 估費用、chat template 吃掉的 token | 下載 Qwen tokenizer（數 MB） |
| `02_next_token.ipynb` | 打開 Qwen2.5-0.5B 看 logits 與 top-k 機率；`generate()` 調溫度、top-p；畫真實模型的 attention 熱圖；看幻覺 | 下載約 1GB；GPU 可選 |
| `03_chat_api.ipynb` | 用 OpenAI SDK 連 Ollama：看一次原始 JSON、system 訊息、溫度、記不住對話與越聊越貴、`finish_reason`、串流 | Ollama |
| `04_dual_track.ipynb` | Lab 1：本地失敗自動切雲端的客戶端，成品是 `course_utils/llm.py` | Ollama；雲端金鑰選填 |
| `05_multimodal_api.ipynb` | 圖片放進 messages、圖片 token、生成圖片、文字轉語音、log-mel 頻譜圖、本機 Whisper 與雲端轉錄對照 | `OPENAI_API_KEY` 選填；下載 whisper-tiny 約 150MB |
| `06_providers.ipynb` | 換 base_url 連 Ollama／OpenRouter／DeepSeek／OpenAI，Ollama 原生 API，Anthropic 格式對照與延遲圖 | Ollama；各家金鑰選填 |

## 準備

Ollama 安裝見 [infra/services/ollama.md](../../infra/services/ollama.md)；沒有 GPU 見 [infra/cloud-gpu.md](../../infra/cloud-gpu.md)。

```bash
uv sync --group m1
cp .env.example .env
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-01-llm-local
```

notebook 從本資料夾開啟（`01_tokens` 讀的是相對路徑 `data/one_piece.txt`）。

雲端金鑰都是選填，放在 `.env`：`OPENAI_API_KEY`（05、06）、`OPENROUTER_API_KEY`、`DEEPSEEK_API_KEY`、`ANTHROPIC_API_KEY`（06）。沒填的步驟會印出說明並略過，notebook 照樣能跑完。
`05` 生成的圖片和語音已存在 `data/`（`gen_ship.jpg`、`luffy_line.mp3`），檔案存在就不會重打 API；想自己生成就先刪掉檔案。

## 已存的輸出

notebook 裡保留了一次執行結果，方便先讀再跑。模型回答每次可能不同；
`qwen2.5:3b` 對海賊王的知識很弱、常答錯，這正好是模組 3 RAG 要解決的問題。
