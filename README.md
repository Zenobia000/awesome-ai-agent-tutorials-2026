# 🚀 2026 AI Agent & 大模型全棧工程師實戰手冊 (20-Hour Bootcamp)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![LangChain 1.0 / LangGraph](https://img.shields.io/badge/LangChain-1.0%20%2F%20LangGraph-green.svg)
![MCP Ready](https://img.shields.io/badge/MCP-Ready-purple.svg)

> **從 Vibe Coding 到規格驅動（Spec-Driven），從玩具 Demo 到企業級生產上線。**
> 本倉庫為「2026 AI Agent + 大模型全棧工程師」20 小時高強度轉職技術課程配套代碼庫，系統涵蓋 **Transformer 機制、工業級 RAG/GraphRAG 幻覺抑制、LangGraph 狀態工作流、Supervisor 多智能體、MCP 標準協議、LoRA 微調與評測驅動開發（EDD）**。

完整課綱：[curriculum-ai-agent-20h.md](curriculum-ai-agent-20h.md)

---

## 📌 為什麼需要這套手冊？（2026 轉職視角）

在 2026 年，單純呼叫 API 寫 Prompt 的初階「AI 封裝工程師」已被完全淘汰。企業急需能夠解決以下硬核工程問題的 **AI Agent 工程師**：

1. **可靠性與架構收斂**：懂得何時用 Deterministic Workflow、何時用 Single-Agent、何時才需 Supervisor Multi-Agent。
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
├── modules/                            # 各模組代碼與 Hands-on Lab
│   ├── module-01-vibe-to-spec/         # Spec 規範、提示詞與結構化輸出
│   ├── module-02-rag-optimization/     # 分塊、混合檢索 RRF、Reranker、PageIndex
│   ├── module-03-graphrag-neo4j/       # 知識圖譜抽取與 Cypher 混合檢索
│   ├── module-04-langgraph-state/      # 狀態圖、Checkpointer、Human-in-the-Loop
│   ├── module-05-multi-agent-system/   # Supervisor 架構、Tavily、SQL Agent
│   ├── module-06-mcp-ecosystem/        # FastMCP Server / Client 開發
│   ├── module-07-lora-fine-tuning/     # Qwen3 / DeepSeek R1 微調與量化部署
│   └── module-08-eval-and-career/      # EDD 評測鏈、LangSmith 追蹤、履歷模組
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

| 模組 | 核心主題與實戰目標 | 核心技術棧 | 時數 |
| :--- | :--- | :--- | :--- |
| **Module 01** | **底層機制與上下文工程 (Context Engineering)**<br>• 從 Tokenizer 到注意力機制、KV Cache 重用<br>• Spec-Driven Development 規格驅動開發<br>• Pydantic 結構化輸出與 Prompt 攻擊防護 | Transformer, Ollama, Pydantic, Prompt Caching | 2.5h |
| **Module 02** | **工業級 RAG 深度檢索與幻覺抑制**<br>• 父子分塊、語義分塊與 Contextual Retrieval<br>• 稠密+稀疏雙路檢索與 RRF（倒數排名融合）<br>• Cross-Encoder 重排序、無向量 PageIndex | Qwen3-Reranker, ChromaDB, BM25, PageIndex | 3.0h |
| **Module 03** | **拓撲關係與 GraphRAG 實戰**<br>• 非結構化文檔實體/關係抽取<br>• Neo4j 知識圖譜建模與 Cypher 查詢轉換<br>• Text2SQL 企業資料庫查詢與動態元數據注入 | Neo4j, Cypher, GraphRAG, Dify Text2SQL | 2.5h |
| **Module 04** | **LangGraph 循環狀態圖與人機協同 (HITL)**<br>• StateGraph、節點、條件路由與 Checkpointer 持久化<br>• PostgresSaver 會話隔離與狀態時光機（Time Travel）<br>• 人在迴路（Human-in-the-Loop）中斷審批 | LangGraph 1.0, PostgreSQL, PostgresSaver | 2.5h |
| **Module 05** | **多智能體（Multi-Agent）架構與企業級工具協同**<br>• Single-Agent vs. Multi-Agent 邊界評估<br>• Supervisor 主管中樞與專門 Sub-agents 路由<br>• SQL Agent + 搜尋引擎（Tavily）全網自主調研 | LangGraph Supervisor, Tavily Search, SQL Agent | 2.5h |
| **Module 06** | **標準協議（MCP）與跨生態集成**<br>• MCP 架構解析：Host、Client、Server<br>• 基於 FastMCP 開發自定義 Enterprise Server<br>• 串接 Dify / Cherry Studio / Claude Code 開發流 | Model Context Protocol (MCP), FastMCP, Dify | 2.0h |
| **Module 07** | **領域模型微調（LoRA）與邊緣部署**<br>• Qwen3-8B/14B、DeepSeek-R1 領域微調<br>• LoRA / QLoRA 顯存優化與訓練損失可視化<br>• Qwen3-VL 多模態視覺模型本地推理 | Unsloth / LLaMA-Factory, LoRA, Qwen3-VL | 2.5h |
| **Module 08** | **評測驅動開發（EDD）、可觀測性與轉職突破**<br>• 評測集構建（Faithfulness, Answer Relevance）<br>• LangSmith 全鏈路追蹤與 Token/延遲診斷<br>• 轉職履歷改造與架構面試通關 | LangSmith, Ragas, Eval-Driven Development | 2.5h |

---

## 🛠️ 貫穿式旗艦專案：企業級智能維運與事故處置平台

本倉庫包含一套完整的生產級端到端 Agent 專案：`projects/incident-autonomous-agent`。

- **事故自動診斷**：透過 MCP 協議動態接入 Prometheus 監控指標與日誌系統。
- **拓撲關聯分析**：利用 GraphRAG 與 Neo4j 拓撲結構定位微服務雪崩根本原因（Root Cause）。
- **人機協同處置**：具備危險指令審批機制（Human-in-the-Loop），非危險修復自動執行，日誌全程同步至 LangSmith。

---

## ⚡ 快速開始 (Quick Start)

### 1. 環境準備

```bash
git clone https://github.com/Zenobia000/awesome-ai-agent-tutorials-2026.git
cd awesome-ai-agent-tutorials-2026

python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. 配置環境變數

```bash
cp .env.example .env
# 編輯 .env 填入必要的 API 金鑰 (DeepSeek, Qwen, LangSmith, Tavily 等) 與資料庫密碼
```

### 3. 本地啟動基礎服務 (PostgreSQL + Neo4j)

```bash
docker compose --env-file .env -f projects/incident-autonomous-agent/docker-compose.yml up -d
```

### 4. 執行第一個極簡 Agent (50 行代碼體驗)

```bash
python modules/module-04-langgraph-state/minimal_agent.py
```

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 開源授權，歡迎學習、改進與商用參考。
