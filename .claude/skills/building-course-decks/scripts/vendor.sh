#!/usr/bin/env bash
# 把 rough.js 與字型下載到 <deck>/assets/vendor/（離線截圖、教室斷網都能放）。用法：./vendor.sh <deck 目錄>
# 字型預設 Huninn＋JetBrains Mono（OFL），要換就改 FONTS；之後 base.css 用 @font-face 指向 vendor/。
set -euo pipefail
V="${1:?deck 目錄}/assets/vendor"; mkdir -p "$V"; G=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -sSfL -o "$V/rough.js" https://unpkg.com/roughjs@4.6.6/bundled/rough.js
FONTS=("huninn/Huninn-Regular.ttf" "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf")
for f in "${FONTS[@]}"; do d=${f%%/*}; n=$(basename "$f" | sed 's/%5B.*%5D//'); curl -sSfL -o "$V/$n" "$G/$f"; curl -sSfL -o "$V/OFL-$d.txt" "$G/$d/OFL.txt"; done
ls -la "$V"
