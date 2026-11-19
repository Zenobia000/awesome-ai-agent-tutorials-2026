"""畫圖小工具：讓 matplotlib 顯示中文。

    from course_utils.viz import setup_cjk
    setup_cjk()
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import font_manager

# 依序嘗試：Linux、Windows、macOS 常見的繁中字型
_CANDIDATES = [
    "Noto Sans CJK TC",
    "Noto Sans TC",
    "Microsoft JhengHei",
    "PingFang TC",
    "Heiti TC",
    "Noto Sans CJK SC",
]


def setup_cjk() -> str | None:
    """設定第一個找得到的中文字型，回傳字型名稱；都找不到就回傳 None。"""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CANDIDATES:
        if name in installed:
            plt.rcParams["font.sans-serif"] = [name, *plt.rcParams["font.sans-serif"]]
            plt.rcParams["axes.unicode_minus"] = False
            return name
    print("找不到中文字型，圖上的中文會變成方塊；可安裝 Noto Sans CJK TC。")
    return None
