# 投影片製作 brief（每位製作者必讀）
<!-- 用法：複製到 deck/BRIEF.md，把 〈〉 換成本課內容，刪掉這行註解。實例：https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026/blob/main/docs/slides/deck/BRIEF.md -->

## 這份 deck 是什麼
把〈課綱檔〉做成 1920×1080 的 HTML 投影片。
**讀者：〈已會什麼〉，但〈沒學過什麼〉。** 能畫成圖的一律畫成圖，文字只是註解。

## 內容依據（優先序）
1. `../sources/product-facts.md`——課綱勘誤，衝突時以它為準
2. `../sources/M<N>-*.md`——素材地圖：論點、可借的圖解結構、搭橋建議
3. 課綱原文

## 講法硬規則
1. 從已知搭橋：每章至少 2 頁用 `.bridge`「你已經會的」接到學生已會的概念
2. 術語第一次出現就定義：一句白話＋一個例子
3. 先看實物再講抽象：用 `.code` 放真的設定檔／JSON／輸出
4. 一頁一個概念；難的拆成「直覺 → 機制 → 工程後果」最多三頁

## 已核准的視覺方向（見 `../decisions.md`）
- 參考頁（必看）：`slides/〈showcase-1〉.html`、`slides/〈showcase-2〉.html`
- 色票：〈底色、墨色、三個主色與淺色〉
- **形狀／顏色語意（全 deck 一致）**：〈例：圓＝模型、方＝資料／狀態、三角＝動作／風險〉；朱紅＋叉＝錯誤示範
- 構圖：一頁一個概念；大圖形當主角；文字在旁；留白是構圖

## 共用元件
- `.bridge`（搭橋，框自動畫）、`.code`（實物，24px，≤14 行）、`.tag`（只用於「示意」「範本數字」「本課整理」「進階」）
- 實物層：`.fig`（原圖卡片）、`.src`（出處，22px）、`.logo`（≤48px）
- **不要修改 `assets/`、`index.html`、`build.py` 與別人前綴的檔案**

## 硬規則
1. 字級：標題 ≥ 72px；正文 ≥ 26px；標籤 ≥ 22px；`.code` 24px
2. 數字只能來自課綱、facts、素材地圖或 `figures.md`；示意圖標「示意」
3. 不放頁碼、進度、全大寫小標籤、emoji；01/02/03 只用於真正的順序
4. 每個概念頁底部一行 `.read`「怎麼讀」
5. 文字不重疊、不被圖蓋住、不出畫面
6. 不搬別人的圖：素材地圖的圖解結構要重畫；原圖只用 `figures.md` 標 `direct` 的

## 實物層（階段 7 才做）
素材只能來自 `assets/figures/figures.md`。
- 原圖對照 X60–X64：`direct` 原圖放 `.fig`，用 rough 圈重點連到說明，底部 `.src`
- 數據比較 X65–X69：真實數字重畫成乾淨 SVG 圖表（不用抖動線），標 `.src`
- 進階延伸 X70–X79：標「進階」，上課可跳過
- `redraw` 只能重畫（原圖在 `_ref/` 只供對照）；`link` 只放標題＋網址；logo ≤48px，條款未確認先用文字
- `.src` 格式：`來源：作者（年份）〈標題〉Fig. N，授權`

## 每章固定結構
`X00-goals` 章首 → `X01-bridge` 搭橋 → 概念頁 → `X5x` Lab（架構＋程式）→ `X6x` 原圖／數據 → `X7x` 進階（標「進階」）→ `X80` 踩坑（症狀→原因→修法）→ `X90` 面試／自我檢核 → `X99-recap` 小結（右下 `.next`）
插頁用多一位數字：`311` 與 `312` 之間放 `3115-…`。

## 檢查流程（每 3–4 頁一次）
```bash
./shoot.sh <前綴>
uv run --with pillow python contact.py <前綴> <scratchpad>/<名>.png
node check_slides.mjs slides
```

## 分工與頁面清單
### 前綴 〈N〉xx 〈章名〉（`../sources/M<N>-*.md`）
- 〈N〉00-goals：本章實戰＝〈Lab〉
- 〈N〉01-bridge
- …
