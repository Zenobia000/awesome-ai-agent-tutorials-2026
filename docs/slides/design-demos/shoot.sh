#!/usr/bin/env bash
# 截圖：./shoot.sh [dir-N]（預設全部）→ shots/<dir>-<頁名>.png
cd "$(dirname "$0")"; mkdir -p shots
for f in ${1:-dir-*}/slides/*.html; do d=$(echo "$f" | cut -d/ -f1); n=$(basename "$f" .html)
  timeout 60 google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 \
    --virtual-time-budget=8000 --screenshot="shots/$d-$n.png" "file://$PWD/$f" 2>/dev/null; done
ls shots
