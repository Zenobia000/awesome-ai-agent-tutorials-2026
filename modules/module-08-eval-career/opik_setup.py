"""Opik 的環境設定：一定要在 `import opik` 之前呼叫。

    from opik_setup import setup_opik
    LIVE = setup_opik()
    import opik

有 `OPIK_API_KEY`（雲端）或 `OPIK_URL_OVERRIDE`（自架）時照常連線；
都沒有時進「本機模式」：網址指到自架預設位址 localhost:5173（沒有伺服器，送出會失敗並丟棄），
並關掉用量統計與錯誤回報，資料不會離開這台機器。評估指標照常在本機算。
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

SETUP_HELP = """沒有 Opik 設定，改用「本機模式」：trace 不上傳，評估指標照常在本機算。

想接上真的 Opik，二選一：
  1. 雲端免費方案：到 https://www.comet.com/signup 註冊，拿 API key
  2. 自架（需要 Docker，約數 GB 磁碟）：照 https://www.comet.com/docs/opik/self-host/local_deployment
     用官方的 docker compose 起服務，介面在 http://localhost:5173

再把設定加到 .env，重開 kernel：
  OPIK_API_KEY=...            # 雲端
  OPIK_WORKSPACE=...          # 雲端
  OPIK_URL_OVERRIDE=http://localhost:5173/api   # 自架只要這行"""


def setup_opik(project: str = "m8-mini-rag", verbose: bool = True) -> bool:
    """設定 Opik 環境變數，回傳是否連得上真的伺服器（LIVE）。"""
    load_dotenv()
    local_marker = os.getenv("M8_OPIK_LOCAL") == "1"  # 同一個 kernel 重跑時，別把自己設的網址當成真的伺服器
    live = not local_marker and bool(os.getenv("OPIK_API_KEY") or os.getenv("OPIK_URL_OVERRIDE"))
    if not live:
        os.environ.update({
            "M8_OPIK_LOCAL": "1",
            "OPIK_URL_OVERRIDE": "http://localhost:5173/api",
            "OPIK_ANALYTICS_ENABLE": "false",
            "OPIK_SENTRY_ENABLE": "false",
            "OPIK_ENABLE_LITELLM_MODELS_MONITORING": "false",
        })
    os.environ.setdefault("OPIK_PROJECT_NAME", project)
    if verbose:
        print("找到 Opik 設定，trace 會送到伺服器。" if live else SETUP_HELP)
    return live
