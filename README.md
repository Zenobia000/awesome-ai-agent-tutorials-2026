# 🚀 2026 AI Agent & 大模型全棧工程師實戰手冊 (20-Hour Bootcamp)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![LangChain 1.0 / LangGraph](https://img.shields.io/badge/LangChain-1.0%20%2F%20LangGraph-green.svg)
![MCP Ready](https://img.shields.io/badge/MCP-Ready-purple.svg)

> **從 Vibe Coding 到規格驅動（Spec-Driven），從玩具 Demo 到企業級生產上線。**
> 本倉庫為「2026 AI Agent + 大模型全棧工程師」20 小時高強度轉職技術課程配套代碼庫，系統涵蓋 **Transformer 機制、工業級 RAG/GraphRAG 幻覺抑制、LangGraph 狀態工作流、單一 Agent Harness（skills＋subagent＋MCP）、LoRA 微調與評測驅動開發（EDD）**。

完整課綱：[curriculum-ai-agent-20h.md](curriculum-ai-agent-20h.md)

---

## 📌 為什麼需要這套手冊？（2026 轉職視角）

在 2026 年，單純呼叫 API 寫 Prompt 的初階「AI 封裝工程師」已被完全淘汰。企業急需能夠解決以下硬核工程問題的 **AI Agent 工程師**：

1. **可靠性與架構收斂**：懂得何時用固定流程圖、何時用單一 agent 配 skills 與工具，以及什麼情況才值得切出 subagent。
2. **檢索深度優化**：不只會向量檢索，更能熟練落地 **Contextual Chunking × 混合檢索（RRF）× Cross-Encoder Reranker**，將幻覺率壓至 5% 以下。
3. **協議與工具標準化**：全面放棄脆弱的硬編碼 Tool Calling，遷移至標準 **Model Context Protocol (MCP)** 生態。
4. **評測驅動開發 (EDD)**：以評測集和回歸測試（Ragas、LLM-as-a-Judge）驗證 Agent 演進，杜絕憑感覺調試。

---

## 📁 倉庫結構

```text
├── README.md
├── AGENTS.md                           # AI Coding Agent 專案指南 (Context Engineering)
├── curriculum-ai-agent-20h.md          # 20 小時完整課綱
├── docs/                               # 理論與架構拆解文檔
│   ├── 01-transformer-and-prompt/
│   ├── 02-rag-and-graphrag/
│   ├── 03-langgraph-and-agents/
│   └── 04-eval-and-mcp/
├── infra/                              # 服務部署教材（Ollama、Chroma、Neo4j…），見 infra/README.md
├── course_utils/                       # 共用模型客戶端（Lab 1-05 的成品）
├── modules/                            # 各模組 notebook，總覽見 modules/README.md
│   ├── module-01-llm-local/            # token、next-token、attention 手寫、Chat API、雙軌客戶端
│   ├── module-02-prompt-structured/    # 提示詞、結構化輸出、Text2SQL
│   ├── module-03-rag/                  # RAG 手寫、混合檢索 RRF、重排序、評估
│   ├── module-04-graphrag/             # 三元組抽取、圖檢索、Neo4j
│   ├── module-05-agent-harness/        # ReAct、function calling、LangGraph 審批、harness
│   ├── module-06-lora/                 # LoRA 手寫、PEFT 微調小模型
│   ├── module-07-mcp/                  # MCP server／client、Excel 分析 agent
│   └── module-08-eval-career/          # LLM-as-a-judge、回歸評估、最小 trace
├── projects/
│   └── incident-autonomous-agent/      # 企業級智慧運維事故處置平台
│       ├── docker-compose.yml
│       ├── mcp_servers/
│       ├── runbooks_graph/
│       └── agent_workflow/
└── eval_benchmarks/                    # 測試集與評測腳本 (Ragas / G-Eval)
```

---

## 🗺️ 20 小時核心課綱架構

| 模組 | 動手做什麼 | 時數 |
| :--- | :--- | :--- |
| **M1 LLM 底層與本地環境** | 手寫 BPE、看 logits 自己寫生成迴圈、numpy 手寫 attention、雙軌模型客戶端 | 2.0h |
| **M2 提示詞與結構化輸出** | 好壞 prompt 對照、CoT、Pydantic 結構化輸出、prompt injection、Text2SQL | 2.0h |
| **M3 RAG** | numpy 手寫 RAG、分塊、Chroma、BM25＋向量 RRF、重排序、Hit@k／MRR 評估 | 4.0h |
| **M4 GraphRAG** | LLM 抽三元組、networkx 多跳查詢、Neo4j Cypher、圖 vs 向量 | 2.0h |
| **M5 Agent** | 手寫 ReAct、function calling 迴圈、LangGraph 審批流程、harness（skills＋subagent） | 5.0h |
| **M6 LoRA** | 20 行手寫 LoRA、PEFT 微調 Qwen2.5-0.5B、合併並匯出給 Ollama | 2.0h |
| **M7 MCP** | 寫一個 MCP server 與 client、Excel 分析 agent | 1.5h |
| **M8 評估與求職** | LLM-as-a-judge、回歸評估集、最小 trace、履歷量化 | 1.5h |

每個模組的 notebook 清單與取材來源見 [modules/README.md](modules/README.md)。

---

## 🛠️ 貫穿式旗艦專案：企業級智能維運與事故處置平台

本倉庫包含一套完整的生產級端到端 Agent 專案：`projects/incident-autonomous-agent`。

- **一個值班 agent**：帶三個 skill（查文件、查資料庫、運維排錯），透過 MCP 呼叫日誌與監控工具。
- **唯讀的事交給 subagent**：平行查日誌、查依賴，結果回報給主 agent。
- **寫入走固定流程**：重啟、改設定一律經過「審批 → 執行 → 驗證」，人點頭才動手。

---

## ⚡ 快速開始 (Quick Start)

```bash
git clone https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026.git
cd awesome-ai-agent-tutorials-2026

uv sync --group m1                 # 安裝模組 1 需要的套件（每個模組一個群組）
cp .env.example .env               # 預設連本機 Ollama，不需要金鑰
ollama pull qwen2.5:3b
uv run jupyter lab modules/module-01-llm-local
```

Ollama、Neo4j 等服務的安裝與 docker compose 一鍵啟動，見 [infra/README.md](infra/README.md)。

沒有 [uv](https://docs.astral.sh/uv/)？`pip install uv` 或參考官方安裝說明。

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 開源授權，歡迎學習、改進與商用參考。
