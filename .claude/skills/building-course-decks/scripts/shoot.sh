#!/usr/bin/env bash
# 前提：deck 的字型與 rough.js 已放在 assets/vendor（headless Chrome 抓 CDN 常卡死）
# 用本機 Chrome 無頭模式截圖：./shoot.sh [檔名前綴…]（預設全部）。字型與 rough.js 已在 assets/vendor，不需網路
cd "$(dirname "$0")"; mkdir -p shots
CHROME=${CHROME:-google-chrome}; PROFILE=$(mktemp -d); trap 'rm -rf "$PROFILE"' EXIT   # 獨立 profile：多個 agent 同時截圖不互卡
# SLIDES=dir-1/slides ./shoot.sh 可拍 design-demos 的方向頁，輸出名加上 dir-1- 前綴
SLIDES=${SLIDES:-slides}; PRE=""; [ "$SLIDES" != slides ] && PRE="${SLIDES%%/*}-"
for f in "$SLIDES"/${1:-}*.html; do n=$PRE$(basename "$f" .html)
  timeout 60 "$CHROME" --headless=new --user-data-dir="$PROFILE" --disable-gpu --hide-scrollbars --window-size=1920,1080 \
    --virtual-time-budget=8000 --screenshot="shots/$n.png" "file://$PWD/$f" 2>/dev/null; done
