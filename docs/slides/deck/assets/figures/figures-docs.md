# 官方文件／部落格架構圖與套件 logo 清單（figures-docs）

核實日期：2026-11-12（所有頁面皆用 WebFetch 實際打開；圖檔皆已下載並用看圖確認內容）。
論文圖不在本檔（另一位同事負責，檔名 `p-*`）。

## 先看這三點

1. **Anthropic 官方部落格的圖一律 `redraw`**：頁面只有「© 2026 Anthropic PBC」，沒有任何開放授權。圖放在 `m<N>/_ref/` 只供參考，不得放進投影片。
2. **LangChain 文件、GraphRAG 文件、MCP 文件的 GitHub repo 有明確開放授權**（見各項），所以其中的圖標 `direct`；`.src` 要寫明授權與版權人。
3. **Host／Client／Server（MCP）、GraphRAG 管線、LangGraph／Deep Agents 的 HITL 流程，官方現行頁面不是圖檔而是 Mermaid 程式碼**，沒有圖可下載；本檔只記錄結構，一律用 rough.js 重畫。

### 配色對照（重畫 Anthropic 圖時）
Anthropic 圖語意：綠框＝LLM 呼叫、粉紅圓角＝輸入／輸出／外部環境、紫框＝非 LLM 的程式邏輯（Gate、Aggregator、Stop、Retrieval、Tools、Memory）、灰實線＝必經路徑、灰虛線＝選擇性／動態路徑。
重畫成本 deck 語意：LLM 呼叫＝圓（靛藍）；Gate／Stop／工具＝三角；In／Out／資料／記憶＝方；虛線箭頭保留「動態決定」的意思。

---

## 一、架構圖

### m5-bea-augmented-llm
- 檔案：assets/figures/m5/_ref/d-bea-augmented-llm.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉（2024-12-19）段落「Building block: The augmented LLM」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 頁面無授權條款，僅 © Anthropic PBC
- 建議用在：502-real-trace 之前或 501-bridge（講「LLM＋檢索＋工具＋記憶」是 agent 的零件）
- 圖的結構：上排 In（粉紅圓角）→ LLM（綠框）→ Out（粉紅圓角），兩段實線箭頭。LLM 正下方三個紫框並排：左 Retrieval、中 Tools（略低）、右 Memory；LLM 與三者之間各有一條雙向虛線箭頭，標籤分別是 Query/Results、Call/Response、Read/Write。
- 給學生的一句話：Agent 的基本零件就是一顆 LLM 加三條雙向線——查資料、呼叫工具、讀寫記憶。

### m5-bea-prompt-chaining
- 檔案：assets/figures/m5/_ref/d-bea-prompt-chaining.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Prompt chaining」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent（workflow 三種寫法之一）
- 圖的結構：由左到右一條線：In → LLM Call 1 →（標籤 Output 1）→ Gate（紫框）。Gate 往右上實線弧到 LLM Call 2（標 Pass），LLM Call 2 →（標 Output 2）→ LLM Call 3 → Out。Gate 往右下虛線弧到 Exit（粉紅圓角，標 Fail）。
- 給學生的一句話：把大任務切成固定的幾步，每步之間放一個檢查閘門，不合格就提早退出。

### m5-bea-routing
- 檔案：assets/figures/m5/_ref/d-bea-routing.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Routing」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；也可呼應 508-conditional-edges（條件邊＝路由）
- 圖的結構：In → LLM Call Router（綠框，兩行字）→ 三個垂直排列的 LLM Call 1／2／3（Call 1 的箭頭是實線、Call 2 與 3 是虛線，表示只走其中一條）→ 三條弧線匯到 Out。
- 給學生的一句話：先讓一個 LLM 判斷「這題該交給誰」，再走對應的那條路——這就是條件邊。

### m5-bea-parallelization
- 檔案：assets/figures/m5/_ref/d-bea-parallelization.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Parallelization」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；509-reducer 的動機（多節點同時寫入要合併）
- 圖的結構：In 扇出三條實線到 LLM Call 1／2／3（垂直排列），三者再扇入同一個 Aggregator（紫框），Aggregator → Out。
- 給學生的一句話：同一件事同時問多個 LLM（或同時處理多段），最後由一個聚合器合併。

### m5-bea-orchestrator-workers
- 檔案：assets/figures/m5/_ref/d-bea-orchestrator-workers.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Orchestrator-workers」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：520-supervisor（Supervisor 拆任務給子 agent 再統整的概念原型）
- 圖的結構：In → Orchestrator（綠框）→ 三條「虛線」弧到 LLM Call 1／2／3（虛線表示 worker 數量與內容由 orchestrator 當場決定）→ 三條虛線匯入 Synthesizer（綠框）→ Out。與 Parallelization 的差別：中間是虛線、前後各有一個 LLM（拆解者與整合者）。
- 給學生的一句話：Supervisor 不是固定流程——拆成幾個子任務、交給誰，是 LLM 當場決定的。

### m5-bea-evaluator-optimizer
- 檔案：assets/figures/m5/_ref/d-bea-evaluator-optimizer.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Workflow: Evaluator-optimizer」— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：504-workflow-vs-agent；315-self-rag-crag 可回頭呼應（檢索後自評再改寫）
- 圖的結構：In → LLM Call Generator → 上方弧線（標 Solution）→ LLM Call Evaluator；Evaluator 下方弧線回到 Generator（標 Rejected + Feedback）；Evaluator → Out（標 Accepted）。形成一個生成／評審的小迴圈。
- 給學生的一句話：一個 LLM 寫、一個 LLM 批改，不過關就帶著意見重寫，直到通過。

### m5-bea-autonomous-agent
- 檔案：assets/figures/m5/_ref/d-bea-autonomous-agent.png（2401×1000）
- 來源：Anthropic〈Building effective agents〉段落「Agents」（圖名 Autonomous agent）— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：503-react-loop（Thought→Action→Observation 的最簡示意）；501-bridge（f(x) 放進迴圈）
- 圖的結構：中間 LLM Call（綠框）。右側 Environment（粉紅圓角）；LLM Call → Environment 上弧線（標 Action），Environment → LLM Call 下弧線（標 Feedback），構成迴圈。左側 Human（粉紅圓角）與 LLM Call 之間一條雙向虛線（隨時可介入）。LLM Call 正下方一條虛線箭頭到 Stop（紫框）。
- 給學生的一句話：Agent 就是把模型放進「行動→環境回饋→再行動」的迴圈，直到自己決定停。

### m5-bea-coding-agent
- 檔案：assets/figures/m5/_ref/d-bea-coding-agent.png（2400×1666）
- 來源：Anthropic〈Building effective agents〉段落「Agents」（圖名 High-level flow of a coding agent）— https://www.anthropic.com/engineering/building-effective-agents（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：502-real-trace 之後（把一段真實 trace 對到時序圖）；505-minimal-agent
- 圖的結構：時序圖，四條垂直生命線：Human（粉紅圓角）、Interface（紫框）、LLM（綠框）、Environment（粉紅圓角）。訊息由上而下：Query（Human→Interface）；虛線框「Until tasks clear」內：Clarify（Human→LLM）、Refine（LLM→Human）；Send context（Interface→LLM）；Search files（LLM→Environment）、Return paths（回）；虛線框「Until tests pass」內：Write code→Status、Test→Results；Complete（LLM→Interface）；Display（Interface→Human）。
- 給學生的一句話：Coding agent 有兩個迴圈——跟人問到需求清楚為止，跟環境測到測試通過為止。

### m5-lc-agent-workflow（direct，可放原圖）
- 檔案：assets/figures/m5/d-lc-agent-workflow.png（4572×2047）
- 來源：LangChain〈Workflows and agents〉— https://docs.langchain.com/oss/python/langgraph/workflows-agents（已核實 2026-11-12）；原檔 https://github.com/langchain-ai/docs/blob/main/src/oss/images/agent_workflow.png
- 授權：direct — langchain-ai/docs repo 的 LICENSE 為 MIT License，Copyright (c) 2025 LangChain。`.src` 寫：「來源：LangChain Docs〈Workflows and agents〉，MIT License © 2025 LangChain」。頁面本身沒有另列授權，以 repo LICENSE 為依據；若要更保守可降為 redraw。
- 建議用在：504-workflow-vs-agent（主圖的對照來源）
- 圖的結構：白底，三欄虛線分隔。左欄「Workflows」：Prompt Chaining、Parallelization 兩個小圖；中欄：Orchestrator-Worker、Evaluator-optimizer、Routing 三個小圖；右欄「Agent」：In → LLM call ⇄ Tool（action／feedback）→ Out。最底下三句說明：左與中欄「LLM is embedded in predefined code paths」／「LLM directs control flow through predefined code paths」，右欄「LLM directs its own actions based on environmental feedback」。手繪（Excalidraw）風、腦袋圖示代表 LLM。
- 給學生的一句話：左邊流程是程式寫死的，右邊流程是模型自己決定——差別只在「誰掌控下一步」。

### m5-lc-workflow-patterns（direct，可放原圖；單一模式的大圖）
- 檔案：assets/figures/m5/d-lc-prompt-chaining.png（1412×444）、d-lc-parallelization.png（1020×684）、d-lc-routing.png（1214×678）、d-lc-orchestrator-worker.png（1486×548）、d-lc-evaluator-optimizer.png（1004×340）、d-lc-agent-loop.png（1732×712）
- 來源：LangChain〈Workflows and agents〉各小節（圖片 alt 依序為 Prompt chaining、parallelization.png、routing.png、worker.png、evaluator_optimizer.png、agent.png）— https://docs.langchain.com/oss/python/langgraph/workflows-agents（已核實 2026-11-12，頁面共 8 張圖含 agent_workflow 與 augmented_llm）
- 授權：direct — 同上，MIT License © 2025 LangChain
- 建議用在：需要「真實出處的單一模式圖」時，放在 504-workflow-vs-agent 之後；其中 d-lc-agent-loop 可放 503-react-loop；d-lc-orchestrator-worker 可放 520-supervisor
- 圖的結構：都是 Excalidraw 手繪風，虛線圓角方框內放腦袋圖示代表 LLM。Prompt chaining：In → 兩個串聯 LLM call → Out；Parallelization：In 分兩路，各自一個 LLM → 各自 Out；Routing：In → Router → 三個 LLM（虛線箭頭）→ 各自 Out；Orchestrator-worker：In → Orchestrator → 三個 worker → Synthesizer → Out；Evaluator-optimizer：Generator → Evaluator → Out，Evaluator 有回箭頭；Agent：In → LLM call → action → Tool → Out，Tool 有 feedback 弧線回 LLM call。
- 給學生的一句話：這幾種模式是 LangGraph 官方範例實際在做的事，後面 Lab 會用狀態圖把它們寫出來。

### m5-lc-checkpoints（direct）
- 檔案：assets/figures/m5/d-lc-checkpoints.jpg（2316×748）、d-lc-get-state.jpg（2692×1056）
- 來源：LangChain〈Checkpointers〉（alt 為 Checkpoints／State）— https://docs.langchain.com/oss/python/langgraph/checkpointers（已核實 2026-11-12；舊的 /persistence 頁面現在沒有任何圖）
- 授權：direct — langchain-ai/docs，MIT License © 2025 LangChain（`.src` 同上）
- 建議用在：511-checkpointer（checkpointer 存什麼、thread 是什麼）
- 圖的結構：由上而下的對照表，左欄名詞、中欄圖示、右欄一句說明。Graph：state "I" → Node 1（粉紅圓）→ Node 2（藍圓）→ state "I heart langgraph"，說明「Control flow of nodes, edges」；Super-steps：每個依序節點是獨立 super-step、平行節點共用同一個；Checkpoints：粉紅與藍色圓角框，內含 state／next／id，說明「State and relevant metadata packaged at every super-step」；Thread：虛線框圈住所有 checkpoint，說明「Collection of checkpoints」；StateSnapshot：checkpoint 的型別。get_state 圖多兩列：Graph.get_state()＝最新一筆、Graph.get_state_history()＝全部清單。
- 給學生的一句話：每走完一個 super-step 就存一份快照，同一個 thread_id 的快照串成一條可回頭看的歷史。

### m5-lc-time-travel（direct）
- 檔案：assets/figures/m5/d-lc-replay.png（2276×986）、d-lc-checkpoints-fork.jpg（3705×2598）
- 來源：LangChain〈Use time-travel〉（alt 為 Replay／Fork）— https://docs.langchain.com/oss/python/langgraph/use-time-travel（已核實 2026-11-12）；Checkpointers 頁也用同兩張圖
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：512-time-travel
- 圖的結構：延續上一張的表格，往下加列。Replay 圖多一列 `Graph.stream(None,{checkpoint_id, thread_id})`：從指定 checkpoint 重播，「該 checkpoint 之前的步驟不重跑、之後的步驟會重跑」。Fork 圖（完整版）再加：`Graph.update_state({thread_id},{state:"I like cold brew"})` 從目前 checkpoint 分叉出新 checkpoint（綠色）；`update_state({checkpoint_id,thread_id},{state:"I like"})` 從指定舊 checkpoint 分叉（紫色）；最後 `Graph.stream(None,{checkpoint_id,thread_id})` 從分叉點繼續跑，「因為該 checkpoint 沒被執行過」。
- 給學生的一句話：拿舊快照可以重播，改過狀態再存就是分叉出一條新時間線。
- 注意：Fork 圖有 3705×2598、文字很小，上課前要裁切成「分叉那兩列」再放大。

### m5-lc-durable-execution（direct）
- 檔案：assets/figures/m5/d-lc-durable-execution.png（962×545，深色底）
- 來源：LangChain〈Going to production〉（Deep Agents）alt「Durable execution: when a worker crashes mid-run, another worker picks the run up from the latest checkpoint」— https://docs.langchain.com/oss/python/deepagents/going-to-production（已核實 2026-11-12）；原檔 src/oss/images/deepagents/production/durable-execution.png
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：511-checkpointer（為什麼正式環境要 PostgresSaver）；552-lab5b-code
- 圖的結構：標題「Durable Execution: Crash Recovery」。左上方框 Worker A：c1 → c2 → 打叉的圓「crash」；右上方框 Worker B：c2 → c3；下方長條「Persistence layer (Postgres)」內 c1、c2、c3 三個圓；Worker A 的 c1、c2 以虛線存入 Postgres，由 c2 一條實線標「resume from c2」指向 Worker B 的 c2，Worker B 的 c3 再存回 Postgres。
- 給學生的一句話：Worker 掛了沒關係，換一台從最後一個 checkpoint 接著跑——前提是 checkpoint 存在 Postgres 而不是記憶體。
- 注意：深色底，放進紙色底 deck 要放在 `.fig` 白底卡片外再加深色邊框，或直接重畫。

### m5-lc-hitl-interrupt（direct，但目前線上頁面沒有引用）
- 檔案：assets/figures/m5/d-lc-hitl-interrupt.png（1160×792，深色底）
- 來源：langchain-ai/docs repo 的檔案 https://github.com/langchain-ai/docs/blob/main/src/oss/images/deepagents/hitl.png（已核實檔案存在，2026-11-12）。**線上現行頁面沒有任何一頁引用這張圖**：Deep Agents〈Human-in-the-loop〉頁（https://docs.langchain.com/oss/python/deepagents/human-in-the-loop）只有 Mermaid 流程圖；LangGraph〈Interrupts〉頁只有 Studio 表單截圖；LangChain〈Human-in-the-loop〉頁完全沒有圖。
- 授權：direct — 檔案在 MIT repo 內；`.src` 請引用 repo 檔案路徑而非某個網頁。
- 建議用在：513-hitl（`interrupt()` 暫停 → 人工決定 → `Command(resume=...)` 恢復的完整往返）；514-hitl-code
- 圖的結構：左右兩個大框：左框 Human（內有 Review）、右框 Agent（內有 Draft Action → interrupt() → continue）。interrupt() 以粉紅線標「Surface Payload」指向 Human 的 Review；interrupt() 另一條虛線標「Save」指向中間的圓柱 checkpointer；Review 以藍線標「Command(resume=decision)」指向 Agent 的 continue；checkpointer 以虛線標「Load」指向 continue。
- 給學生的一句話：interrupt() 把現場存進 checkpointer 然後停下，人給了決定後再讀回來接著跑。
- 風險：因為官方網站目前沒有放這張圖，日後 repo 可能刪檔。建議本地備份（已存），並以重畫為主、原圖為輔。

### m5-lc-hitl-flow-mermaid（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼，沒有圖檔）
- 來源：LangChain Deep Agents〈Human-in-the-loop〉— https://docs.langchain.com/oss/python/deepagents/human-in-the-loop（已核實 2026-11-12；原始碼 src/oss/deepagents/human-in-the-loop.mdx）
- 授權：redraw — 文字與結構取自 MIT repo，但沒有圖檔可放，直接用 rough.js 重畫
- 建議用在：513-hitl
- 圖的結構：由左到右：Agent → 菱形「Interrupt?」。no → Execute；yes → 菱形 Human。Human 四條出路：approve → Execute、edit → Execute、reject → ToolMessage、respond → ToolMessage（LangChain 頁面版本只有 approve／edit／reject 三條）。Execute → Agent、ToolMessage → Agent（回到 Agent 迴圈）。
- 給學生的一句話：人有四種回應——放行、改了再放行、拒絕、用文字回覆；後兩種會變成一則 ToolMessage 回到 agent。

### m5-lc-pattern-subagents（direct）
- 檔案：assets/figures/m5/d-lc-pattern-subagents.png（1020×734）
- 來源：LangChain〈Multi-agent〉段落「Visual overview」（alt「Subagents pattern: main agent coordinates subagents as tools」）— https://docs.langchain.com/oss/python/langchain/multi-agent（已核實 2026-11-12）
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：520-supervisor、521-subagent-as-tool（「子 agent 包成工具」）
- 圖的結構：Mermaid 渲染圖。User request（圓角）→ Main Agent（方框）；Main Agent 與 Subagent A／B／C（右側三個方框）各有雙向箭頭（呼叫與回傳）；Main Agent 另一條箭頭 → Response（圓角）。
- 給學生的一句話：所有路由都經過主 agent，子 agent 就像主 agent 手上的三個工具。
- 注意：頁面沒有 supervisor 一詞，也沒有 supervisor 專用圖；課程用詞「Supervisor」與此圖的「Main Agent」對應。

### m5-lc-patterns-others（direct）
- 檔案：assets/figures/m5/d-lc-pattern-handoffs.png（1568×464）、d-lc-pattern-router.png（1560×556）、d-lc-pattern-skills.png（874×734）
- 來源：LangChain〈Multi-agent〉段落「Visual overview」— https://docs.langchain.com/oss/python/langchain/multi-agent（已核實 2026-11-12）
- 授權：direct — MIT License © 2025 LangChain
- 建議用在：524-agent-zoo（多 agent 四種模式比較）；d-lc-pattern-skills 放 525-skills
- 圖的結構：Handoffs：User request → 框「Agents」內 Agent A ⇄ Agent B ⇄ Agent C（彼此雙向、A↔C 也有）；A、B、C 各有一條箭頭到 Response。Router：User request → Router → Agent A／B／C（三路）→ Synthesize → Response。Skills：User request → Agent → Skill A／B／C（三條單向箭頭）；Agent → Response。
- 給學生的一句話：多 agent 不只 Supervisor 一種——交棒、分流、載入技能各有取捨。

### m5-mars-orchestrator-worker
- 檔案：assets/figures/m5/_ref/d-mars-orchestrator-worker.png（4584×2579）、d-mars-process.png（4584×4584）
- 來源：Anthropic〈How we built our multi-agent research system〉（2025-06-13）— https://www.anthropic.com/engineering/multi-agent-research-system（已核實 2026-11-12，頁面共 3 張圖，兩張為架構圖）
- 授權：redraw — 無授權條款
- 建議用在：520-supervisor（真實系統的 Supervisor 長相）；522-context-passing（Memory 與只回報結果）
- 圖的結構：架構圖標題「High-level Architecture of Advanced Research」。左側灰色區「Claude.ai chat」（使用者提問）；右側灰色區「Multi-agent research system」：中央大藍框「Lead agent (orchestrator)」，框內寫 Tools: search tools + MCP tools + memory + run_subagent + complete_task；左邊 Citations subagent（單向箭頭出去）、右邊 Memory（雙向箭頭）、下方三個 Search subagent（各與 Lead 雙向箭頭、各自有自我迴圈箭頭）。左右之間兩條箭頭：User request →、← Final report。時序圖標題「Multi-agent System Process Diagram」：七條生命線 User、System、LeadResearcher、Subagent1、Subagent2、Memory、CitationAgent；LeadResearcher 在「Iterative Research Process」框內 think（plan approach）→ save plan 到 Memory → retrieve context → create subagent for aspect A／B → 子 agent 各自 web_search、think（evaluate）→ complete_task 回報 → think（synthesize）→ 判斷「More research needed?」（Exit loop／Continue loop）；結束後 complete_task 把結果交給 System，CitationAgent 處理文件與報告插入引用，System 持久化並回傳帶引用的結果。
- 給學生的一句話：真實的 Supervisor 會先把計畫存進記憶、並行派出多個子 agent，最後由專門的 agent 補上引用。

### m5-skills-progressive-disclosure
- 檔案：assets/figures/m5/_ref/d-skills-progressive-disclosure.jpg（2292×673）、d-skills-context-window.jpg（1650×929）、d-skills-bundle-files.jpg（1650×1069）
- 來源：Anthropic〈Equipping agents for the real world with Agent Skills〉（2025-10-16，2025-12-18 更新）— https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills（已核實 2026-11-12，頁面共 6 張圖）
- 授權：redraw — 無授權條款
- 建議用在：525-skills
- 圖的結構：progressive disclosure 是一張表（直接重畫成三層階梯即可）：Level 1「SKILL.md Metadata (YAML)」— Always loaded — 約 100 tokens；Level 2「SKILL.md Body (Markdown)」— Loaded when Skill triggers — 少於 5k tokens；Level 3+「Bundled files (text files, scripts, data)」— Loaded as-needed by Claude — unlimited*（以上數字是圖上寫的，要放進投影片須標「依 Anthropic 部落格」）。context-window 圖標題「Skills and the Context Window」：大框 Context Window，上半是 Agent's System Prompt 與一排技能名稱小標籤（bigquery、docx、nda-review、pdf、pptx、…、xlsx），左側註解「Short snippets from each Skill appended to the system prompt」；下半依序是 User 訊息、Claude 決定觸發 PDF Skill、Tool use: Bash("cat /mnt/skills/pdf/SKILL.md")、Tool result、再 cat forms.md 與其結果，右側註解標出「Claude decides to trigger」「follow the reference to forms.md」。
- 給學生的一句話：技能平常只佔幾十個 token 的說明，真的要用時才把正文和附檔讀進 context。

### m3-cr-standard-rag
- 檔案：assets/figures/m3/_ref/d-cr-standard-rag.png（3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉（2024-09-19）圖「A Standard Retrieval-Augmented Generation (RAG) system that uses both embeddings and Best Match 25 (BM25) to retrieve information」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：303-two-pipelines（離線 vs 在線的真實例子）；309-hybrid-rrf 之後
- 圖的結構：標題「Standard RAG」，兩個大底板：左「PREPROCESSING」、右「RUNTIME」。左：Corpus（文件堆疊）→（標 Chunks）→ 分兩路：Embedding model →（Embeddings）→ Vector database；TF-IDF →（TF-IDF encodings）→ TF-IDF index。右：Query（人像）分別連到 Vector database 與 TF-IDF index；兩者輸出匯入 Rank fusion →（Top K chunks）→ Generative model（右上角有 Claude 圖示）→ Response。
- 給學生的一句話：向量與關鍵字兩路各自索引，查詢時兩路一起找，再用排名融合合併。
- 注意：圖上框裡寫的是「TF-IDF」，但文章標題與說明寫 BM25。重畫時請標 BM25，並加註「原圖標示 TF-IDF，BM25 為其改良版」避免學生比對時困惑。

### m3-cr-contextual-preprocess
- 檔案：assets/figures/m3/_ref/d-cr-contextual-preprocess.png（3840×2160；右側被裁切，只有前處理部分完整）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖「Contextual Retrieval is a preprocessing technique that improves retrieval accuracy」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：302-three-pains（上下文斷裂的解法）；313-doc-to-qa（同屬「入庫前先用 LLM 加工」）
- 圖的結構：標題「Contextual Retrieval Preprocessing」，底板「PREPROCESSING (new)」，藍色表示新增步驟。Corpus 中取出一份文件 → 切成 Chunk 1、Chunk 2、…、Chunk X（藍色小框）→ 一個大藍框「Run prompt for every chunk to situate it within the document」（Claude 圖示）；整份文件另有一條藍線也送進這個大藍框。輸出 Context 1 + Chunk 1、Context 2 + Chunk 2、…、Context X + Chunk X，旁註「For every prompt, Claude responds with 50–100 tokens of context, which is then prepended to the corresponding chunk」。之後接回原有的 Embedding model → Vector database、TF-IDF → TF-IDF index（灰色）。
- 給學生的一句話：入庫前，先讓 LLM 讀整份文件，替每個 chunk 補一小段「你在文件的哪裡」再去做向量與關鍵字索引。
- 注意：「50–100 tokens」是圖上旁註的原文，放進投影片時標明出處。

### m3-cr-rerank-pipeline
- 檔案：assets/figures/m3/_ref/d-cr-rerank-pipeline.png（3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖「Combine Contextual Retrieval and Reranking to maximize retrieval accuracy」（原標題有 Retrieva 拼字錯誤）— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 無授權條款
- 建議用在：311-rerank（粗篩再精排的完整管線）；303-two-pipelines
- 圖的結構：標題「Combined」。左底板「PREPROCESSING (with Contextual Retrieval)」，內容同上一張（縮小）；右底板「RUNTIME (with Reranking)」：Query 連到 Vector database 與 TF-IDF index，兩者 → Rank fusion →（Top N chunks）→ Reranker →（Top K chunks）→ Generative model → Response。
- 給學生的一句話：先多撈一些（Top N），再讓重排器精選少數幾個（Top K）交給模型。
- 注意：圖上只寫 Top N／Top K，沒有數字。文章內文提到的具體數字（先撈 150、重排後取 20）是從頁面摘要得到，放進投影片前請回原文逐字核對。

### m3-cr-results（數據，供 X65–X69 數據比較頁）
- 檔案：assets/figures/m3/_ref/d-cr-results-contextual.png（4 根長條）、d-cr-results-rerank.png（6 根長條）（皆 3840×2160）
- 來源：Anthropic〈Introducing Contextual Retrieval〉圖說「Combining Contextual Embedding and Contextual BM25 reduce the top-20-chunk retrieval failure rate by 49%」與「Reranked Contextual Embedding and Contextual BM25 reduces the top-20-chunk retrieval failure rate by 67%」— https://www.anthropic.com/news/contextual-retrieval（已核實 2026-11-12）
- 授權：redraw — 圖不能放；**數字可以用乾淨圖表重畫**，`.src` 寫「依 Anthropic〈Introducing Contextual Retrieval〉(2024) 圖重繪」
- 建議用在：311-rerank 之後的數據頁
- 圖的結構：縱軸「Average % Failed Retrievals @20」（top-20 檢索失敗率）。左組 Standard Retrieval：Embedding 5.7%、Embedding + BM25 5.0%、Reranked embedding + BM25 3.5%；右組 Contextual Retrieval：Contextual embedding 3.7%、Contextual embedding + contextual BM25 2.9%、Reranked contextual embedding + contextual BM25 1.9%。圖說的相對降幅：5.7%→2.9% 為 49%、5.7%→1.9% 為 67%（5.7%→3.7% 約 35%，是由圖上數字算出，不是圖說寫的）。
- 給學生的一句話：補上下文、加關鍵字、再重排，失敗率從 5.7% 一路降到 1.9%。

### m4-graphrag-kg-viz（direct）
- 檔案：assets/figures/m4/d-graphrag-kg-viz.jpg（600×611）
- 來源：Microsoft GraphRAG 文件首頁 Figure 1「An LLM-generated knowledge graph built using GPT-4 Turbo」— https://microsoft.github.io/graphrag/（已核實 2026-11-12）；原檔 https://github.com/microsoft/graphrag/blob/main/docs/img/GraphRag-Figure1.jpg
- 授權：direct — microsoft/graphrag repo 為 MIT License，Copyright (c) Microsoft Corporation。`.src` 寫「來源：Microsoft GraphRAG 文件 Figure 1，MIT License © Microsoft」。網站頁尾只有「© 2025 Microsoft」，授權依據是 repo LICENSE。
- 建議用在：402-why-graph 或 410-query-modes（「大規模圖譜長這樣」）；與論文 Fig. 1（`m4/p-graphrag-fig1.png`）內容相近，擇一即可
- 圖的結構：白底散點圖，無框線無箭頭：大量圓點（疏密不一），顏色代表社群、圓大小代表實體的度（連線數），彼此疏密不同形成團塊。
- 給學生的一句話：每個圓是一個實體，同顏色是同一個社群——全局檢索就是讀這些社群的摘要。
- 注意：Microsoft Research 部落格〈GraphRAG: Unlocking LLM discovery on narrative private data〉（https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/）的 Figure 3 是同一張圖，但部落格沒有授權條款，所以不要從部落格取圖，用 repo 版。

### m4-graphrag-drift（direct）
- 檔案：assets/figures/m4/d-graphrag-drift.png（2048×339，很扁）
- 來源：Microsoft GraphRAG〈DRIFT Search〉Figure 1 — https://microsoft.github.io/graphrag/query/drift_search/（已核實 2026-11-12）；原檔 docs/img/drift-search-diagram.png
- 授權：direct — 同上 MIT License © Microsoft Corporation
- 建議用在：410-query-modes（Global／Local／DRIFT／Basic 的 DRIFT 一格）
- 圖的結構：一棵由上往下展開的大樹，樹根標 A，第二層節點裡標 B，第三層標 C；節點是帶缺口的藍色圓（缺口大小表示「是否繼續展開」的信心），葉端是許多細小紅點。圖說（頁面）：三個階段是 Primer（拿查詢對最相關的 top-K 社群報告，產生初步答案與追問）、Follow-Up（用 local search 細化追問，每個節點帶信心分數決定是否繼續展開）、Output Hierarchy（輸出一棵依相關度排序的問答階層）。
- 給學生的一句話：DRIFT 先用社群報告給一個粗答案和追問，再一層層用局部檢索追下去。
- 注意：圖很扁、無文字，只有 A／B／C 三個標記，建議裁出左半或重畫成簡化樹。

### m4-graphrag-index-dataflow（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼）
- 來源：Microsoft GraphRAG〈Indexing Dataflow〉— https://microsoft.github.io/graphrag/index/default_dataflow/（已核實 2026-11-12）；原始碼 docs/index/default_dataflow.md
- 授權：redraw — 內容在 MIT repo 內，但沒有圖檔可放；用 rough.js 重畫
- 建議用在：407-two-schools（Microsoft 派的離線建圖流程）；408-global-search 之前
- 圖的結構：標題「Dataflow Overview」，由上而下六個階段（方框分組）。Phase 1 Compose TextUnits：Documents → Chunk → Text Units（預設 chunk 大小 1200 tokens，依該頁原始碼 default_dataflow.md 的文字）。Phase 2 Document Processing：Documents 與 Text Units → Link to TextUnits → Documents Table。Phase 3 Graph Extraction：Text Units → Entity & Relationship Extraction → Entity & Relationship Summarization → Claim Extraction → Graph Tables。Phase 4 Graph Augmentation：Graph Tables → Community Detection → Communities Table。Phase 5 Community Summarization：Communities Table → Community Summarization → Community Reports Table。Phase 6 Text Embeddings：Text Units → Text Embedding、Graph Tables → Description Embedding、Community Reports → Content Embedding。
- 給學生的一句話：先把文件切成 TextUnit，抽實體關係、分社群、寫社群報告，最後三種東西各做一份 embedding。

### m4-graphrag-global-local-search（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼）
- 來源：Microsoft GraphRAG〈Global Search〉https://microsoft.github.io/graphrag/query/global_search/ 與〈Local Search〉https://microsoft.github.io/graphrag/query/local_search/（皆已核實 2026-11-12）
- 授權：redraw — 同上
- 建議用在：408-global-search、409-local-search
- 圖的結構：**Global Search Dataflow**（由左到右）：User Query 與 Conversation History 匯成一個點，把「打亂的社群報告批次 1…N」各送進一個方塊，每批產生一則「Rated Intermediate Response」（附重要性評分）→ Ranking + Filtering → Aggregated Intermediate Responses → Response（map 平行、reduce 合併）。**Local Search Dataflow**：User Query 與 Conversation History →（實體描述 embedding）→ Extracted Entities；由實體展開五路候選：Entity-Text Unit Mapping → Candidate Text Units、Entity-Report Mapping → Candidate Community Reports、Entity-Entity Relationships → Candidate Entities、同一關係 → Candidate Relationships、Entity-Covariate Mappings → Candidate Covariates；每路各自 Ranking + Filtering 成 Prioritized 版本，與 Conversation History 一起匯入 Response。
- 給學生的一句話：全局檢索是「每批社群報告各答一次、再合併」，局部檢索是「先找實體，再往外抓相關資料」。

### m7-mcp-simple-diagram（direct）
- 檔案：assets/figures/m7/d-mcp-simple-diagram.png（3840×1500）
- 來源：Model Context Protocol〈What is the Model Context Protocol (MCP)?〉— https://modelcontextprotocol.io/docs/getting-started/intro（已核實 2026-11-12，會轉址到 /docs/2026-07-28/getting-started/intro）；原檔 https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/images/mcp-simple-diagram.png
- 授權：direct — repo LICENSE 寫明「專案正由 MIT 轉換到 Apache-2.0；新的程式碼與規格貢獻為 Apache-2.0；文件貢獻（不含規格）為 CC-BY-4.0；尚未取得重新授權同意的貢獻維持 MIT」。三種授權都允許轉載，都要求保留出處／授權聲明。這張圖 2025-04 由 Alex Isken 取代、2025-10 有錯字修正（Koichi ITO），無法確定適用哪一種，`.src` 寫「來源：Model Context Protocol 文件，MIT／Apache-2.0／CC BY 4.0（見 repo LICENSE）」。
- 建議用在：702-nxm（N×M 整合爆炸 → 一個協定）
- 圖的結構：白底。中央藍色方塊「MCP — Standardized protocol」。左側三個黑框（欄底標「AI applications」）：Chat interface（Claude Desktop, LibreChat）、IDEs and code editors（Claude Code, Goose）、Other AI applications（5ire, Superinterface）。右側三個黑框（欄底標「Data sources and tools」）：Data and file systems（PostgreSQL, SQLite, GDrive）、Development tools（Git, Sentry, etc.）、Productivity tools（Slack, Google Maps, etc.）。六個框各用一條雙向箭頭接到中央方塊，兩側各標「Bidirectional data flow」。
- 給學生的一句話：左邊的 AI 應用和右邊的資料／工具都只對 MCP 說話，不用每對組合各寫一套整合。
- 注意：圖上的案例（Claude Desktop、LibreChat、5ire…）是官方的舉例，不是完整清單。

### m7-mcp-host-client-server（結構記錄，無圖檔）
- 檔案：無（官方是 Mermaid 程式碼，網頁上沒有 img）
- 來源：Model Context Protocol〈Architecture overview〉段落「Participants」— https://modelcontextprotocol.io/docs/learn/architecture（已核實 2026-11-12）；另有規格頁〈Architecture〉https://modelcontextprotocol.io/specification/latest/architecture（已核實 2026-11-12）
- 授權：redraw — 文件為 CC BY 4.0／Apache-2.0／MIT 混合（見上），但沒有圖檔可放；用 rough.js 重畫，`.src` 同上寫出處
- 建議用在：703-host-client-server
- 圖的結構：**Learn 版**：一個大框「MCP Host (AI Application)」內有四個 MCP Client（Client 1–4）。框外三個 Server：Server A「Local（例：Filesystem）」、Server B「Local（例：Database）」、Server C「Remote（例：Sentry）」。連線：Client 1–Server A、Client 2–Server B、Client 3–Server C、Client 4–Server C，每條標「Dedicated connection」（Server C 同時被兩個 client 連線，表示遠端 server 可服務多個 client）。**規格版**（多一層邊界）：「Application Host Process」框內 Host → Client 1／2／3；「Local machine」框內 Server 1（Files & Git）、Server 2（Database）與各自雙向連到的 Local Resource A／B（圓柱）；「Internet」框內 Server 3（External APIs）雙向連到 Remote Resource C。Client 1→Server 1、Client 2→Server 2、Client 3→Server 3。
- 給學生的一句話：一個 Host 為每個 Server 各開一個 Client，一對一連線；Server 可以在本機也可以在遠端。
- 文字重點（頁面原文）：Host＝協調並管理多個 client 的 AI 應用；Client＝維持與一個 server 的連線並取得 context；Server＝提供 context 的程式。

---

## 二、找不到或不適用的項目

| 項目 | 結果 |
|---|---|
| LangGraph HITL 流程圖 | 現行 LangGraph〈Interrupts〉、LangChain〈Human-in-the-loop〉頁**沒有流程圖**（前者只有兩張 LangSmith Studio 截圖，後者零圖）。唯一的圖檔 `hitl.png` 只存在於 repo、網站未引用（見 m5-lc-hitl-interrupt）；Deep Agents 頁只有 Mermaid（見 m5-lc-hitl-flow-mermaid） |
| LangGraph supervisor 圖 | 現行〈Multi-agent〉頁**沒有 supervisor 圖**，頁面也不使用該詞。repo 內有 `supervisor.png`，但沒有任何頁面引用，且 `langgraph-supervisor` 已封存，所以未下載，改用 d-lc-pattern-subagents |
| LangGraph〈Persistence〉頁 | 該頁已無圖；圖搬到〈Checkpointers〉頁 |
| MCP Host／Client／Server 圖檔 | 官方頁面是 Mermaid，沒有圖檔（見 m7-mcp-host-client-server） |
| Microsoft GraphRAG 管線圖 | 官方文件首頁、Indexing Overview、Microsoft Research 部落格與專案頁**都沒有管線示意圖**（只有 Mermaid 與一張知識圖譜視覺化）。管線圖只在論文 *From Local to Global* 裡，那是論文同事的範圍；部落格圖沒有授權條款，不可直接放 |
| Anthropic〈Contextual Retrieval〉圖的授權 | 無任何開放授權，全部 redraw；只有圖上的數字（5.7／5.0／3.5／3.7／2.9／1.9）可以拿來重畫 |

## 三、logo（存放於 assets/figures/logos/）

通則：
- 所有檔案**未改形狀**；只有兩種修改：（1）simple-icons 的單色 SVG 在 `<svg>` 標籤加上 `fill="#官方色碼"`（simple-icons 預設無填色，會顯示成黑色），色碼取自 simple-icons 的 `data/simple-icons.json`；（2）`openai.svg` 的填色由白改黑。其餘（Python、Docker、PostgreSQL、LangChain 三件、ChromaDB、LLaMA-Factory、Cherry Studio）都是官方原檔。
- simple-icons 整個專案是 CC0，但它的 DISCLAIMER 明說「CC0 不代表每個 icon 本身都是 CC0；logo 是各品牌的商標」。所以 CC0 只解決「檔案能不能散布」，**商標使用仍受品牌條款約束**；下表第四欄寫的是品牌條款。
- 使用規則（BRIEF）：高度 ≤ 48px、不改形狀與顏色、只用來指稱「這是哪個套件」。
- 19 個全部都找到檔案。其中 **4 個的條款有風險或未能直接核實**（Docker、Anthropic、OpenAI、Neo4j），另有 7 個找不到品牌條款（見第四節）。

| 名稱 | 檔案 | 來源 URL | 授權／品牌條款 |
|---|---|---|---|
| Python | logos/python.svg | https://www.python.org/static/community_logos/python-logo-generic.svg（官方，頁面 https://www.python.org/community/logos/） | 官方雙色版（含 python 字樣）。PSF 頁面：鼓勵使用 Python 的專案與公司在網站、手冊等處放此 logo；商標屬 Python Software Foundation，細節見 PSF Trademark Usage Policy；**使用衍生版本或有疑慮請先詢問**（所以未採用 simple-icons 的單色衍生版）。原樣使用，無修改 |
| Ollama | logos/ollama.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/ollama.svg（simple-icons 登錄的來源是 Ollama 維護者在 https://github.com/ollama/ollama/issues/2152 提供的 logo.svg） | 檔案 CC0；Ollama 沒有品牌使用頁（程式碼 repo 為 MIT，不含商標）。色碼 #000000。注意：找不到官方品牌條款 |
| Docker | logos/docker.svg | 官方 Logo Kit https://www.docker.com/static/Docker-Logos-1.zip 內 `docker-logo-ocean-blue.svg`（頁面 https://www.docker.com/company/newsroom/media-resources/） | 官方 Ocean Blue 版（符合「只能用 Ocean Blue／Light Blue／Deep Blue／白色」）。**注意：條款偏嚴**。品牌頁：不得翻轉、傾斜、擠壓、拉伸、裁切、去色、單獨用字標；至少 24px。商標指引（https://www.docker.com/legal/trademark-guidelines/）：教育／說明用途只開放「字標」（文字 Docker），**logo 圖形需 Docker 事先授權**，且 logo「只能取自 Docker 的產品頁並經授權」。建議：工具頁先用文字「Docker」；要放 logo 請先寄 trademark@docker.com 確認 |
| PostgreSQL | logos/postgresql.svg | https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg（頁面 https://wiki.postgresql.org/wiki/Logo） | 官方 Slonik 全彩版。商標政策（https://www.postgresql.org/about/policies/trademarks/）：可在不暗示背書的前提下，用來指稱 PostgreSQL（例如文件、文章、活動）；**不得修改、不得與其他商標或 logo 並排呈現**；商業用途建議加 ®；建議附註「Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.」。注意：「不得與其他 logo 並排」對「工具頁一排 logo」的版面有影響，Lab 架構圖旁各放各的、不要排成一列 |
| Neo4j | logos/neo4j.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/neo4j.svg（simple-icons 註記來源與指引 https://neo4j.com/brand/#logo） | 檔案 CC0，色碼 #4581C3。**注意：品牌條款未能核實**：neo4j.com/brand 現在轉址到 Needle 設計系統站 https://www.neo4j.design/（抓到的只有站名，沒有條款文字），商標指引頁（neo4j.com 法務條款）也沒找到；simple-icons 的色碼可能是改版前的顏色。使用前請到 neo4j.design 確認現行 logo 與規定 |
| ChromaDB | logos/chromadb.svg | https://github.com/chroma-core/chroma/blob/main/docs/mintlify/images/light-logo.svg（Chroma 官方 repo 的文件 logo，淺色底版） | 檔案在 Apache-2.0 repo 內（Apache-2.0 第 6 條不授予商標權）。官網 https://www.trychroma.com/brand 是登入頁，沒有品牌頁。注意：找不到品牌條款。這是「圖形＋Chroma 字樣」的橫式 logo，寬高比約 4:1，高 48px 時寬約 190px。repo 內另有 favicon.svg 但內含第三方圖庫（Streamline）標記，未採用 |
| LangChain | logos/langchain.svg | https://www.langchain.com/brand-assets 的 `LangChain_Lockup_Black.svg`（官方 zip：https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a9998494f7b532d49a38525_langchain-brand-assets.zip） | 官方：「approved for use in documentation, presentations, press coverage, and community content, subject to the usage guidelines」。規定：維持原比例與間距、使用提供的淺／深色版本不要自行換色、不拉伸、不加特效、背景對比要夠、不用 Community logo 取代官方 logo。本檔用黑色版，放在白底或紙色底 |
| LangGraph | logos/langgraph.svg | 同上官方 zip 內 `LangGraph_OSS Lockup_light.svg` | 同 LangChain 的規定。深藍圓角底＋淺藍圖示＋「langgraph」字樣的淺色版 lockup |
| LangSmith | logos/langsmith.svg | https://www.langchain.com/brand-assets 頁面上的 `LangSmith_Wordmark_Black 1.svg`（https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a9936e524dccd963978bf0f_LangSmith_Wordmark_Black%201.svg） | 同 LangChain 的規定。只有字標（官方未提供 LangSmith 圖形符號）；官方 zip 內沒有 LangSmith 的 SVG，所以 SVG 是從頁面連結單獨取得 |
| Hugging Face | logos/huggingface.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/huggingface.svg（指引 https://huggingface.co/brand） | 檔案 CC0，色碼 #FFD21E（與官方品牌頁的 #FFD21E 一致）。官方品牌頁只提供下載（hf-logo 等 svg／png／ai），**沒有寫使用條款**，頁面僅寫「Download the official Hugging Face brand assets to use in your projects」。注意：條款未明示，只能視為允許指稱用途 |
| Qwen | logos/qwen.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/qwen.svg（來源 https://qwen.ai） | 檔案 CC0，色碼 #6950EF。注意：找不到官方品牌條款 |
| DeepSeek | logos/deepseek.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/deepseek.svg（來源 https://www.deepseek.com） | 檔案 CC0，色碼 #5786FE。注意：找不到官方品牌條款 |
| LLaMA-Factory | logos/llama-factory.png（1400×400，白底不透明） | https://github.com/hiyouga/LLaMA-Factory/blob/main/assets/logo.png（專案 README 首圖） | repo 為 Apache-2.0（不含商標授權）；專案沒有品牌頁，simple-icons 也沒收錄。注意：找不到品牌條款。圖內含標語「Easy and Efficient LLM Fine-Tuning」，需放在白底上 |
| MCP | logos/mcp.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/modelcontextprotocol.svg（來源是 MCP 文件的 logo/light.svg，https://github.com/modelcontextprotocol/docs/blob/573dc60c2e7aab2605b29d0bf27194aa7b02e4fb/logo/light.svg） | 檔案 CC0；MCP repo LICENSE 為 MIT／Apache-2.0／CC-BY-4.0 過渡（見 m7-mcp-simple-diagram）。色碼 #000000。沒有獨立的 logo 使用規範 |
| Dify | logos/dify.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/dify.svg（來源 https://github.com/langgenius/dify/blob/48f6b2e885eb40230dfe318fe4d3fb71b50dbc02/web/public/logo/logo.svg） | simple-icons 登錄授權為自訂：https://dify.ai/end-user-license-agreement；品牌條款 https://dify.ai/dify-brand-usage-terms：可在部落格、文件、簡報、教學影片、演講中**不需事先核准**用來指稱 Dify；不得改色、字型、比例、效果，不得與其他 logo 組合成新標誌，不得暗示背書；**付費訓練／課程若暗示官方背書需書面核准**；商業廣告與周邊需書面核准（marketing@dify.ai）。色碼 #0033FF 為官方色。注意：本課若是收費課程，頁面不可寫成「官方合作」 |
| n8n | logos/n8n.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/n8n.svg（來源 https://guidelines.n8n.design/logo） | 檔案 CC0，色碼 #FF91AC（官方粉）。官方 logo 頁：符號版提供粉／黑／白三色；留白＝符號高度；與夥伴 logo 並排時用加號連接、n8n 在左或上。頁面沒有寫誤用規則與最小尺寸。這是符號版，不含 n8n 字樣 |
| Cherry Studio | logos/cherry-studio.png（512×512） | https://github.com/CherryHQ/cherry-studio/blob/main/build/icons/512x512.png（官方 repo 的應用圖示） | repo 為 AGPL-3.0（Community Edition，另有商業授權可洽 bd@cherry-ai.com）；README 沒有 logo 或商標條款。注意：AGPL 管的是程式碼，圖示的商標與著作權使用條款找不到 |
| Anthropic | logos/anthropic.svg | simple-icons https://github.com/simple-icons/simple-icons/blob/develop/icons/anthropic.svg（來源 https://www.anthropic.com） | 檔案 CC0，色碼 #191919。**注意：條款最嚴**。Anthropic 商標指引（https://www.anthropic.com/legal/trademark-guidelines）寫「You may only use our trademarks as specifically permitted by us and only in materials we approve beforehand」，禁止任何改色、字型、比例變更，也不提供公開 logo 下載；教育性指稱的用法在指引中沒有明文開放。建議：用文字「Anthropic」，要放 logo 先寄 marketing@anthropic.com |
| OpenAI | logos/openai.svg | https://github.com/openai/openai-agents-python/blob/main/docs/assets/logo.svg（OpenAI 官方 repo，MIT；原檔是白色填色，本檔只把填色改成 #000000 以便放在淺色底） | **注意：條款未能直接核實**。官方品牌頁 https://openai.com/brand/ 與 https://openai.com/design 對自動化存取回 403，讀不到原文；simple-icons 已不收錄 OpenAI；GitHub 組織頭像只有 200×200，不符 ≥256px，所以沒用。依搜尋結果摘要與第三方整理（非官方原文）：第三方可依品牌指引使用，不得改動、需有足夠留白與對比、用黑或白色、不得暗示背書、不得用在周邊，OpenAI 可隨時要求停用。建議：放之前在瀏覽器打開 openai.com/brand 讀一次原文 |

## 四、風險彙整

- **條款需要先確認才能放 logo**：Docker（logo 圖形需授權）、Anthropic（需事先核准）、OpenAI（原文未能讀取）、Neo4j（品牌站改版，條款未能讀取）。這四個建議工具頁先用文字，確認後再放圖。
- **找不到品牌條款但風險低**（僅用來指稱）：Ollama、Qwen、DeepSeek、ChromaDB、LLaMA-Factory、Cherry Studio、Hugging Face（有下載頁但沒寫條款）。
- **條款明確且允許**：Python、PostgreSQL（但不得與其他 logo 並排）、LangChain／LangGraph／LangSmith、Dify（收費課程不得暗示官方背書）、MCP、n8n。
- 所有檔案都只是存檔，沒有執行；zip 檔（LangChain 品牌包、Docker logo kit）解壓在 scratchpad，只取出需要的 SVG，並確認 SVG 內沒有 script 或外部連結。
- 授權是否足以支撐「公開散布這份 deck」超出技術判斷，最後由課程方決定；本檔只記錄事實與條款原文要點。
