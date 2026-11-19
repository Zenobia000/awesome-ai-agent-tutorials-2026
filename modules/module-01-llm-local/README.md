# 模組 1：LLM 底層與本地環境

原理（token、下一個 token、attention、記不住對話、Hugging Face 生態系、API 計費）寫在 `00_concepts.md`；notebook 直接用 `tiktoken`、`huggingface_hub`、`transformers`、OpenAI SDK、LiteLLM 看模型在算什麼、跟它對話，寫出整門課共用的模型客戶端，最後算清楚每次呼叫的費用。

| notebook／檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md`（先讀） | 原理紀要：token 與 BPE、下一個 token 預測與 softmax、溫度／top-p、attention 與 Q/K/V、O(N²) context 成本、為什麼記不住對話、幻覺、Hugging Face 生態系、API 怎麼計費 | — |
| `01_tokens.ipynb` | 用 tiktoken 與 Qwen tokenizer 看切分、印出 BPE 合併規則、中英文 token 數比較、數 token 估費用、chat template 吃掉的 token | 下載 Qwen tokenizer（數 MB） |
| `02_huggingface.ipynb` | Hugging Face 入門：Hub 查模型與 model card、gated 與 `HF_TOKEN`、只下載 `config.json` 比四種尺寸、本機快取與大小圖、tokenizer／model／`pipeline` 對話、參數分布圖、`safetensors`、`datasets` 的 `map` 與切分、`peft`／`accelerate` 的位置、HF vs Ollama | 網路；下載約 1GB（與 03 共用快取）、ag_news 約 20MB |
| `03_next_token.ipynb` | 打開 Qwen2.5-0.5B 看 logits 與 top-k 機率；`generate()` 調溫度、top-p；畫真實模型的 attention 熱圖；看幻覺 | 下載約 1GB；GPU 可選 |
| `04_chat_api.ipynb` | 用 OpenAI SDK 連 Ollama：看一次原始 JSON、system 訊息、溫度、記不住對話與越聊越貴、`finish_reason`、串流；OpenAI Responses API 與 Chat Completions 對照（`previous_response_id` 需 `OPENAI_API_KEY`） | Ollama |
| `05_dual_track.ipynb` | Lab 1：本地失敗自動切雲端的客戶端，成品是 `course_utils/llm.py` | Ollama；雲端金鑰選填 |
| `06_multimodal_api.ipynb` | 圖片放進 messages、圖片 token、生成圖片、文字轉語音、log-mel 頻譜圖、本機 Whisper 與雲端轉錄對照 | `OPENAI_API_KEY` 選填；下載 whisper-tiny 約 150MB |
| `07_providers.ipynb` | 換 base_url 連 Ollama／OpenRouter／DeepSeek／OpenAI，Ollama 原生 API，Anthropic 格式對照與延遲圖 | Ollama；各家金鑰選填 |
| `08_litellm_and_cost.ipynb` | LiteLLM `completion()` 一個函式打四家、統一回應與錯誤型別、`Router` fallback；查價目表、手算費用對帳 `completion_cost()`、推理 token 與 `reasoning_effort` 的費用差、中英文／輸入輸出／長對話的費用圖、預算追蹤器、LiteLLM Proxy 是什麼 | Ollama；各家金鑰選填（有 OpenAI 金鑰時最多 8 次 `gpt-5.4-nano` 雲端呼叫，花費不到 0.01 美元） |

**驗證環境**（2026-11-19 全部重跑通過）：Python 3.12.13、openai 3.55.1、tiktoken 0.14.0、huggingface_hub 2.4.0、transformers 5.23.0、datasets 5.2.0、safetensors 0.8.0、peft 0.21.3、accelerate 1.16.0、torch 2.15.0、litellm 1.110.1、requests 2.34.2；Ollama 0.40.16（qwen2.5:3b）。

## 準備

Ollama 安裝見 [infra/services/ollama.md](../../infra/services/ollama.md)；沒有 GPU 見 [infra/cloud-gpu.md](../../infra/cloud-gpu.md)。

```bash
uv sync --group m1
cp .env.example .env
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-01-llm-local
```

notebook 從本資料夾開啟（`01_tokens` 讀的是相對路徑 `data/one_piece.txt`）。

雲端金鑰都是選填，放在 `.env`：`OPENAI_API_KEY`（04、06、07、08）、`OPENROUTER_API_KEY`、`DEEPSEEK_API_KEY`、`ANTHROPIC_API_KEY`（07、08）。沒填的步驟會印出說明並略過，notebook 照樣能跑完。

雲端模型（2026-11）：文字一律用 `gpt-5.4-nano`（推理模型，不收 `max_tokens`、要寫 `max_completion_tokens`；`temperature` 只在 `reasoning_effort="none"` 時可調），每本只在一個變數定義；轉錄用 `gpt-transcribe`；語音合成沿用 `gpt-4o-mini-tts`（官方已公告 2027-01-06 停用，`audio.speech` 尚無後繼模型）。
`06` 生成的圖片和語音已存在 `data/`（`gen_ship.jpg`、`luffy_line.mp3`），檔案存在就不會重打 API；想自己生成就先刪掉檔案。
Hugging Face 的下載預設存在 `~/.cache/huggingface`，磁碟不夠就在 `.env` 設 `HF_HOME` 指到大磁碟；`hf cache ls` 看各模型佔多少空間（`02` 有示範）。

## 已存的輸出

notebook 裡保留了一次執行結果，方便先讀再跑。模型回答每次可能不同；
`qwen2.5:3b` 對海賊王的知識很弱、常答錯，這正好是模組 3 RAG 要解決的問題。
