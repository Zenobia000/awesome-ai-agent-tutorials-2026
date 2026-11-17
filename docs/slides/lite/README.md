# 精簡版：AI Agent 入門（60 頁）

完整版（`../deck/`，210 頁、20 小時）的精簡版，給還不懂 agent 設計的讀者：

- 主線用生活比喻；深度學習對照框改標為「學過深度學習的話（可跳過）」
- 拿掉公式、多數程式碼、Lab 細節、選型表與面試頁；保留每章的白話入口與核心圖
- 八步路線：LLM → 下指令 → RAG → 知識圖譜 → **Agent** → 微調 → MCP → 上線

## 怎麼更新

精簡版不手改頁面，一律從完整版產生：

```bash
cd docs/slides/lite && uv run python make_lite.py --pdf
```

- 頁序與文字改寫都在 `make_lite.py`（`PAGES`、`PER_PAGE`）；完整版改了被改寫的字句時，腳本會直接報錯，不會靜默漏改
- 精簡版專屬頁放在 `own/`
- `assets/` 是指向 `../deck/assets` 的連結；`slides/`、`index.html`、`print.html`、`deck.pdf`、`build.py` 都是產物
