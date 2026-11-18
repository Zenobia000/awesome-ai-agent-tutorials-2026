# 模組 1：LLM 底層與本地環境

先拆開模型看它在算什麼，再用 API 跟它對話，最後寫出整門課共用的模型客戶端。

| notebook | 做什麼 | 需要 |
|---|---|---|
| `01_tokens.ipynb` | 手寫 BPE 切詞器，再跟 tiktoken 比較 | 純 Python |
| `02_next_token.ipynb` | 打開 Qwen2.5-0.5B 看 logits，自己寫生成迴圈、溫度、top-p | 下載約 1GB；GPU 可選 |
| `03_attention.ipynb` | 用 numpy 手寫 attention，跟 PyTorch 對答案，量 O(N²) | numpy、torch |
| `04_chat_api.ipynb` | 用 `requests` 直接打 Chat API：messages、記不住對話、串流 | Ollama |
| `05_dual_track.ipynb` | Lab 1：本地失敗自動切雲端的客戶端，成品是 `course_utils/llm.py` | Ollama；雲端金鑰選填 |

## 準備

```bash
uv sync --group m1
cp .env.example .env
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-01-llm-local
```

notebook 從本資料夾開啟（`01_tokens` 讀的是相對路徑 `data/one_piece.txt`）。

## 已存的輸出

notebook 裡保留了一次執行結果，方便先讀再跑。模型回答每次可能不同；
`qwen2.5:3b` 對海賊王的知識很弱、常答錯，這正好是模組 3 RAG 要解決的問題。
