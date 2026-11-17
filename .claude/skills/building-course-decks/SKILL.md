---
name: building-course-decks
description: Use when turning a course syllabus or curriculum into teaching slides, lecture decks, or 講義/投影片, especially multi-hour courses produced with parallel subagents as 1920×1080 HTML pages, when the syllabus may contain outdated tools or APIs, or when the deck will include paper figures, logos, or be published to GitHub.
---

# Building Course Decks

## Overview
課綱 → 可上課、可公開的 HTML 投影片。核心：**先定學生從哪裡出發、先把課綱勘誤、先讓使用者從看得到的樣張選風格，才批量生產**。每階段有產出檔當關卡，檔案不在＝階段沒做。所有 ★ 的答案（含使用者事先已主動說明的）原話記進 `docs/slides/decisions.md`，答過就不再問。

**前置**：Chrome／Chromium（`CHROME=` 可指定路徑）、`uv`、`node`、`curl`；`vendor.sh` 需對外網路；Lab 實跑依課程需要 Docker、JVM 等。

## Phases（★＝停下等使用者）

| # | 階段 | 產出 | 關卡 |
|---|---|---|---|
| 0 | 定讀者與條件 | `decisions.md`：學生**已會／沒學過**、各模組時數、教室網路與實作環境、參考 deck 路徑 | ★ 一次問完，最多 4 題，學生背景必問 |
| 1 | 素材地圖＋勘誤 | `sources/M<N>-*.md`（agent）→ 主控合併成 `sources/product-facts.md` | — |
| 2 | 三方向 demo | `design-demos/dir-{1,2,3}/{slides,assets}`、`overview.html`（見下） | ★ 選擇寫進 `decisions.md` |
| 3 | Grammar | `deck/` 用 `templates/assets/`、`templates/BRIEF-template.md`；2 張 showcase | showcase 和 demo 差很多時 ★ 給使用者看 |
| 4 | 批量生產 | 每個 agent 一個前綴（0xx 開場、1xx–8xx 各模組、9xx 收尾） | — |
| 5 | 整合檢查 | `check_slides.mjs` 通過、主控看總覽圖、`build.py --pdf` | — |
| 6 | 修補＋Lab 實跑 | 弱頁重做、`sources/lab-verification.md` | — |
| 7 | 實物層 | agent 寫 `figures-*.md` → 主控合併 `figures.md`；5–6 張樣張 | ★ 樣張通過才補齊 X6x／X7x |
| 8 | 發布 | 分支或新 repo、`.gitignore`、`LICENSE` | ★ 公開／私人、LICENSE 種類 |

## 每階段要點
- **0**：頁數預算約每小時 8–10 頁。一章超過 25 頁就拆給兩個 agent，同一個前綴用編號區間分（例：500–519、520–599）。
- **1**：每 2 模組一個 agent（`templates/agent-briefs.md` A），找**別人系統整理過的圖解型二手資料**，並核實課綱每個版本號、API、工具名。衝突以 `product-facts.md` 為準。
- **2**（階段 2、3 由主控自己做，不派 agent：要和使用者來回）：在 `design-demos/` 下每個方向建 `dir-N/slides`、`dir-N/assets`（從 `templates/assets/` 起手，`vendor.sh design-demos/dir-N` 把字型與 rough.js 下載進去），複製 `shoot.sh` 到 `design-demos/`，用 `SLIDES=dir-N/slides ./shoot.sh` 截圖，`overview.html` 從 `templates/overview.html` 改。三方向結構要不同、不只換色；使用者有參考 deck 時，其中一個方向沿用它。給一個推薦，並寫出什麼條件會改推別的。
- **3**：`deck/` 從 `templates/assets/`（`index.html` 放 `deck/`，其餘放 `deck/assets/`）與 `templates/slide.html` 起手，把 `scripts/` 全部複製進 `deck/`，再跑 `vendor.sh deck`。BRIEF 寫死形狀／顏色語意與元件（`.bridge` 搭橋、`.code` 實物、`.tag`、`.read`）；`base.css` 的 `@font-face` 指向 `vendor/`。改 `draw.js` 後跑 `node --check`。
- **4**：用 agent-briefs B；只寫自己前綴、不改 assets、不編數字。X6x／X7x 先留空，到階段 7 才做。
- **5**：腳本全部複製到 `deck/` 再執行。頁數用 `ls slides | wc -l` 數，不用心算。agent 的自評要看截圖才算數。
- **6**：投影片上的程式與設定**實際跑**：用最小可重現環境（uv、Docker、小模型、小資料），設定檔用工具自己的解析器驗。「指令正常結束」不等於「有做事」，要看產物。改完頁就重跑 `build.py --pdf`。
- **7**：用 agent-briefs D。加頁後重跑 `build.py --pdf`。授權分 `direct`（CC BY／MIT，可放原圖）、`redraw`（原圖放 `_ref/`，只用數據或結構重畫）、`link`；logo 條款未確認先用文字。
- **8**：先確認 `index.html` 裡 manifest 的頁數＝`ls slides | wc -l`、PDF 頁數相同（不同就重跑 `build.py --pdf`）。`_ref/`、條款未確認的 logo、`shots/` 寫進 `.gitignore`；`deck.pdf`、`print.html` 要提交。用 grep 掃 secret 與個人資訊（有 gitleaks 就加跑）。LICENSE 註明第三方素材各自授權。既有 repo 走分支＋PR；推完用 GitHub API 確認排除檔不在遠端。

## Scripts（複製進 `deck/` 後執行）
`vendor.sh <目錄>`、`shoot.sh`（`CHROME=` 指定瀏覽器、`SLIDES=` 指定頁面目錄，每次獨立 profile）、`contact.py`（agent 自查）、`sheet.py`（主控審查用緊湊總覽）、`check_slides.mjs`、`build.py --title "課名" [--pdf]`（也吃 `CHROME=`）（需要 `index.html` 裡有 `DECK_MANIFEST`，所以要從 `templates/assets/index.html` 起手）。頁數超過 200 時 PDF 輸出可能逾時，可暫時把部分頁面移出 `slides/` 分批輸出再合併。

## Common Mistakes
| 錯誤 | 後果 | 修法 |
|---|---|---|
| 沒問學生背景就規劃 | 內容對錯人，整份重排 | 階段 0 必問 |
| 把課綱當事實 | 過時 API、錯的工具名上投影片 | 階段 1 勘誤 |
| 只做一個風格樣張 | 事後改風格要全部重做 | 三方向各 2 頁再選 |
| 沒寫死形狀／顏色語意 | 各 agent 各畫各的 | BRIEF 語意表 |
| 字型、rough.js 走 CDN | 截圖卡死、斷網全白 | 階段 2 前先 vendor |
| 編輯時整段重複貼上 | 頁面圖形消失，肉眼難發現 | `check_slides.mjs` |
| Lab 只「看起來對」 | 學生跑不起來或靜默失敗 | 最小環境實跑 |
| 論文圖直接公開 | 版權風險 | 授權分級，`_ref/` 不發布 |
| 心算頁數 | 回報數字錯 | 用指令數 |
