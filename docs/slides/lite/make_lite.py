"""從完整版 deck 產生精簡版：挑頁、改寫少數文字，再交給 build.py 組裝。

用法：cd docs/slides/lite && uv run python make_lite.py [--pdf]
完整版有更新時重跑即可同步；精簡版專屬的頁面放在 own/。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
FULL = ROOT.parent / "deck"
OUT = ROOT / "slides"

# 頁序（完整版檔名；own: 開頭為精簡版專屬頁）
PAGES = """
001-cover 004a-agent-products 004b-what-is-agent 005-pillars 002-why own:lite-map 008-flagship
099z-m1-prelude 100a-what-is-llm 100b-self-supervised 100c-paradigm-shift 102-tokenize 106-next-token
107a-hallucination 113-no-memory 115-open-vs-api
199z-m2-prelude 200a-what-is-prompt 202-prompt-anatomy 203-few-shot 208-structured-ladder 206-injection
299z-m3-prelude 300a-what-is-rag 303-two-pipelines 304-fixed-chunk 308-bm25-vs-dense 3115-rerank-funnel 3035-three-pains
399z-m4-prelude 400a-what-is-kg 402-why-graph 403-entity-relation
499z-m5-prelude 502-real-trace 503-react-loop 504-workflow-vs-agent 520-harness 525-skills 521-subagent-as-tool
526-when-split 513-hitl 527-workflow-shell 553-lab5c
599z-m6-prelude 600a-what-is-finetune 602-decision-matrix
699z-m7-prelude 700a-what-is-mcp 702-nxm 708-lowcode-boundary
799z-m8-prelude 800a-why-observe 802-trace 803-evals 805-three-layers
850-flagship-arch 900-summary 904-glossary-1 905-glossary-2
""".split()

# 全部頁面共用：DL 搭橋改成可跳過的對照框
GLOBAL = [('<span class="k">你已經會的</span>', '<span class="k">學過深度學習的話（可跳過）</span>')]

# 個別頁面：拿掉指向精簡版沒有的頁面／Lab 的字句
PER_PAGE = {
    "099z-m1-prelude": [('<div class="ttl">從深度學習到 LLM</div>', '<div class="ttl">LLM 是什麼</div>'), ('<div class="kick">模組 1</div>', '<div class="kick">第 1 步</div>')],
    "199z-m2-prelude": [('<div class="ttl">提示詞工程與結構化輸出</div>', '<div class="ttl">怎麼下指令</div>'), ('<div class="kick">模組 2</div>', '<div class="kick">第 2 步</div>')],
    "299z-m3-prelude": [('<div class="ttl">企業級 RAG</div>', '<div class="ttl">先查資料再回答：RAG</div>'), ('<div class="kick">模組 3</div>', '<div class="kick">第 3 步</div>')],
    "399z-m4-prelude": [('<div class="ttl">知識圖譜與 GraphRAG</div>', '<div class="ttl">把關係串起來：知識圖譜</div>'), ('<div class="kick">模組 4</div>', '<div class="kick">第 4 步</div>')],
    "499z-m5-prelude": [('<div class="ttl">Agent 核心與 LangGraph</div>', '<div class="ttl">讓它自己動手：Agent</div>'), ('<div class="kick">模組 5</div>', '<div class="kick">第 5 步</div>')],
    "599z-m6-prelude": [('<div class="ttl">LoRA 微調與私有化部署</div>', '<div class="ttl">改它的習慣：微調</div>'), ('<div class="kick">模組 6</div>', '<div class="kick">第 6 步</div>')],
    "699z-m7-prelude": [('<div class="ttl">MCP 與低代碼</div>', '<div class="ttl">接上外部工具：MCP</div>'), ('<div class="kick">模組 7</div>', '<div class="kick">第 7 步</div>')],
    "799z-m8-prelude": [('<div class="ttl">轉職衝刺</div>', '<div class="ttl">上線後盯著</div>'), ('<div class="kick">模組 8</div>', '<div class="kick">第 8 步</div>')],
    "001-cover": [("20 小時實戰", "精簡版"),
                  ("從你已經會的深度學習出發，<br>一路做到能上線、能審批、看得見的 Agent 系統。",
                   "不必先懂 agent：從你用過的產品出發，<br>看懂能上線、能審批、看得見的 Agent 系統。")],
    "106-next-token": [("分佈變尖或變平（下一頁）", "分佈變尖或變平")],
    "115-open-vs-api": [("本課 Lab 1 兩邊都接：本地 Ollama 為主，雲端 API 備援。",
                         "兩邊都能走 OpenAI 相容介面，換 base_url 就能切換。")],
    "513-hitl": [("恢復時 node 從頭重跑，<br>Lab 5-B 程式頁詳述", "恢復時 node 從頭重跑")],
    "526-when-split": [("對回「多 agent 的 token 代價」那頁：每多一個 agent，帳單就多一截。",
                        "每多一個 agent，token 帳單就多一截。")],
    "553-lab5c": [("<title>Lab5-C Harness agent</title>", "<title>動手看看：harness agent</title>"),
                  ("<h1>Lab 5-C：一個 harness agent</h1>", "<h1>動手看看：一個 harness agent</h1>")],
}


def transform(name: str, text: str) -> str:
    for old, new in GLOBAL + PER_PAGE.get(name, []):
        if name in PER_PAGE and (old, new) in PER_PAGE[name] and old not in text:
            raise SystemExit(f"[make_lite] {name}: 找不到要改的字句：{old[:40]}…（完整版改過了？）")
        text = text.replace(old, new)
    return text


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for i, page in enumerate(PAGES, 1):
        if page.startswith("own:"):
            name, src = page[4:], ROOT / "own" / f"{page[4:]}.html"
        else:
            name, src = page, FULL / "slides" / f"{page}.html"
        if not src.exists():
            raise SystemExit(f"[make_lite] 缺頁：{src}")
        (OUT / f"{i:03d}-{name}.html").write_text(transform(name, src.read_text(encoding="utf-8")), encoding="utf-8")
    assets = ROOT / "assets"
    if not assets.exists():
        assets.symlink_to("../deck/assets")
    shutil.copy(FULL / "index.html", ROOT / "index.html")
    build = (FULL / "build.py").read_text(encoding="utf-8").replace(
        "AI Agent 與大模型全棧工程師：20 小時實戰", "AI Agent 入門：精簡版")
    (ROOT / "build.py").write_text(build, encoding="utf-8")
    print(f"[make_lite] {len(PAGES)} 頁 → {OUT}")
    subprocess.run([sys.executable, str(ROOT / "build.py"), *sys.argv[1:]], check=True)


if __name__ == "__main__":
    main()
