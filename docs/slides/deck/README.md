# 投影片：AI Agent 與大模型全棧工程師（20 小時）

## 怎麼看
- **上課播放**：用瀏覽器開 `index.html` → 點任一頁開始。← / → 翻頁，ESC 回總覽，P 列印
- **PDF**：`deck.pdf`（1920×1080，文字可搜尋；`build.py --pdf` 產生）
- 需要網路：字體（Huninn、JetBrains Mono）與手繪線條（rough.js）從 CDN 載入

## 結構
| 段落 | 檔名前綴 |
|---|---|
| 開場：封面、為什麼學、先備、DL→Agent 地圖、四大支柱、工具、課程地圖、旗艦專案 | 0xx |
| 模組一～八：章首 → 搭橋 → 概念 → Lab → 踩坑 → 面試 → 小結 | 1xx–8xx |
| 大總結、面試心法、參考文獻、術語表 | 9xx |

## 修改與重建
- 每頁一個檔案在 `slides/`；共用樣式 `assets/base.css`、繪圖工具 `assets/draw.js`；設計與講法規則見 `BRIEF.md`
- 內容依據：`../sources/product-facts.md`（課綱勘誤）、`../sources/M*-*.md`（素材地圖）
- 截圖檢查：`./shoot.sh <前綴>`（離線可跑）→ `uv run --with pillow python contact.py <前綴> 總覽.png`
- 實物素材：`assets/figures/`，清單與授權見 `assets/figures/figures.md`
- 新增或刪除頁面後：`uv run python build.py --pdf`（更新目錄與 PDF）
