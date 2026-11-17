# 2026 Agent 架構研究：harness vs supervisor（核實日 2026-11-17）

旗艦專案與模組五改版的依據。三份獨立研究：(A) pi／OpenClaw／Hermes 的架構；(B) Anthropic／OpenAI／LangChain 官方建議；(C) 企業 SRE／值班 agent 產品。每條都附實際開過的連結。

---

## 三個開源 agent 專案的架構現況（查證日 2026-11-17）

> 只寫實際打開過的 URL；查不到的標 UNVERIFIED。星數取自 GitHub API 當日快照（`api.github.com/repos/<owner>/<repo>`），會變動。

### TL;DR

- **共同骨架**：三者核心都是**單一 agent loop**（一個模型 + tools，tool call 有就再跑一輪，沒有就結束），**沒有** supervisor / graph 編排器。擴充靠 **AGENTS.md 類 context 檔 + SKILL.md（Agent Skills 標準、progressive disclosure）+ plugin/extension + lifecycle hooks**，長任務靠 **compaction（摘要取代舊訊息，原始紀錄留在磁碟）**，多 agent 靠「**把自己再 spawn 一份**」（隔離 context，只回傳摘要）。
- **2026 下半年的重大轉向（教材若引用 2025 末的說法會過時）**：
  1. **pi 已不再拒絕 MCP**：v0.99.0（2026-09-29）內建 MCP、`tool_search`、`codemode`；MCP 工具預設不直接宣告給模型，而是透過 codemode 腳本 / tool search 間接取用。2025-11 的「pi does not and will not support MCP」已被推翻。
  2. **OpenClaw 已不再依賴 pi 的 agent core**：現在自有 `@openclaw/agent-core`，文件寫「No external agent framework packages remain」，`pi` 只剩 runtime 別名與 `pi-tui` 依賴。
  3. **pi 易主**：2026-04-08 加入 Earendil（Armin Ronacher 共同創辦），repo 搬到 `earendil-works/pi`，1.0.0 於 2026-10-01 發布。

---

### 1. pi（coding agent）

### 基本資料
| 項目 | 內容 | 來源 |
|---|---|---|
| 名稱 / repo | `pi`；monorepo 原 `badlogic/pi-mono`，現為 `earendil-works/pi`（舊 URL 會轉址） | https://github.com/badlogic/pi-mono（實測轉到 earendil-works/pi）、https://pi.dev/changelog/2026/5/7/pi-has-a-new-home |
| 作者 / 維護 | Mario Zechner 原作；2026-04-08 起由 Earendil Inc. 擁有，決策由 Mario、Armin、Colin 共同負責 | http://mariozechner.at/posts/2026-04-08-ive-sold-out/ 、https://lucumr.pocoo.org/2026/4/8/mario-and-earendil/ |
| License | MIT；Mario 原話「MIT, forever. Non-negotiable.」（加值功能可能採 Fair Source，企業功能專有，當時尚未建置） | http://mariozechner.at/posts/2026-04-08-ive-sold-out/ |
| npm | `@mariozechner/*` → `@earendil-works/*`（0.74.0 起），CLI 仍叫 `pi` | https://pi.dev/changelog/2026/5/7/pi-has-a-new-home |
| 套件 | `pi-ai`（多 provider LLM API）、`pi-agent-core`（agent runtime）、`pi-coding-agent`（CLI）、`pi-tui`、另有 `pi-durable`、`pi-telemetry`、`chord` | https://github.com/earendil-works/pi |
| 活躍度 | ~122k stars；最新 release v1.5.2（2026-11-10）；1.0.0 為 2026-10-01 | GitHub API；https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/CHANGELOG.md |

### 核心 loop
- 單一 loop：送出訊息 → 組 request（system prompt + active branch + tools）→ 串流回應 → 執行每個 tool call 並記錄結果 =「一個 turn」；若有 tool 結果或排隊訊息就再起一個 turn，否則結束。支援 steering（turn 之間插入）與 follow-up 訊息。來源：https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/how-pi-works.md
- **最小 system prompt / tool set**（2025-11-30 原文）：system prompt + tool 定義「below 1000 tokens」；預設只有 `read`、`write`、`edit`、`bash` 四個工具（`grep`/`find`/`ls` 存在但預設關）。https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
- **現況仍是這四個**：「Default enabled tools are `read`, `bash`, `edit`, and `write`」。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/cli.md

### 擴充機制
- **Context files**：只注入 AGENTS.md（全域 → 專案階層載入）。https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
- **Skills**：實作 Agent Skills 規格；啟動時只把每個 skill 的 name/description/path 放進 system prompt，任務需要時模型自己 `read` SKILL.md（progressive disclosure）；`/skill:name` 可強制載入；位置 `~/.agents/skills/`、專案 `.agents/skills/`。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/skills.md
- **Extensions**：TypeScript 模組（jiti 載入免編譯），`pi.registerTool()`（TypeBox schema）、`registerCommand`、`pi.on()` 事件 hook（如 `tool_call` 可 block/改寫 → 可自行做 permission gate；`context`、`before_provider_request`、`session_before_compact` 可自訂 compaction）、`ctx.ui` 自訂 TUI。位置 `~/.pi/agent/extensions/`、`.pi/extensions/`（需 project trust）。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/extensions.md
- 打包成 **pi packages** 經 npm/git 分享。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/README.md
- **MCP — 立場已反轉**：
  - 2025-11-30：「pi does not and will not support MCP」，理由是 MCP server 佔大量 context，偏好「CLI 工具 + README，讓 agent 需要時才讀」。https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
  - 2026-01-31 Armin：MCP 工具需在 session 開始載入 system context，中途重載會破壞 cache；OpenClaw 改用 mcporter 接 MCP。https://lucumr.pocoo.org/2026/1/31/pi/
  - **2026-09-29 v0.99.0**：「Added codemode, tool search, and MCP support as built-in extensions」。MCP 支援 stdio / streamable HTTP（拒絕 SSE），設定 `~/.pi/agent/mcp.json`、`.pi/mcp.json`。**預設 exposure 是 `codemode`**：MCP 工具不宣告給模型，由模型寫 JavaScript（QuickJS sandbox）呼叫；另有 `deferred`（經 `tool_search` 才宣告）、`direct`、`hidden`。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/CHANGELOG.md 、https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/mcp.md
  - 解讀：原本反對的是「工具定義塞爆 context」，新做法以 codemode/延遲宣告避開這點——反對的是**載入方式**，不是 protocol 本身。（此為我的推論，非作者原話。）
- **Sub-agents**：不內建。2025 原文：「If you need pi to spawn itself, just ask it to run itself via bash」。現 README：「skips features like sub-agents and plan mode. Ask Pi to build what you want, or install a package」。extensions 範例目錄有 `subagent/`（`registerTool` + `exec` spawn）。Armin 提到 `/control` extension 讓一個 pi 對另一個 pi 下 prompt，「a simple multi-agent system without complex orchestration」。來源同上 + https://lucumr.pocoo.org/2026/1/31/pi/
- **Plan mode / todos**：不內建，寫在 PLAN.md / TODO.md 檔案裡。**Background bash**：不內建，同步執行，長任務用 tmux。https://mariozechner.at/posts/2025-11-30-pi-coding-agent/

### State、sessions、compaction、權限
- Sessions 是 **JSONL 檔**，每筆 entry 有 id 與 parent → **樹狀**；從舊 entry 繼續即在同檔開新 branch；fork/clone 會複製到新檔。預設位置 `~/.pi/agent/sessions/`（依工作目錄分組）。https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/how-pi-works.md 、.../docs/sessions.md
- Extensions 可用 custom messages 把 state 存進 session 檔，且不進模型 context。https://lucumr.pocoo.org/2026/1/31/pi/
- **Compaction**：`contextTokens > contextWindow - reserveTokens`（預設 reserve 16384）自動觸發或 `/compact`；插入摘要 entry 取代舊訊息，原 entries 保留在樹中；切 branch 時另有 branch summarization。.../docs/compaction.md
- **權限**：2025 原文「pi runs in full YOLO mode」。現況文件：「does not ask for approval before every tool call」，project trust 只管是否載入專案資源、**不是** sandbox；建議跑在 container/VM。要 approval 就自己寫 `tool_call` extension。.../docs/security.md

### 設計哲學引述
- 「Exactly controlling what goes into the model's context yields better outputs」— https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
- 「a minimal, extensible agent harness that you can make your own」— README
- Armin：pi 有「the shortest system prompt of any agent that I'm aware of」；核心理念是讓 agent 自己寫 extension 擴充自己（「I told Pi to make an extension and it did」）。https://lucumr.pocoo.org/2026/1/31/pi/

---

### 2. OpenClaw

### 基本資料
| 項目 | 內容 | 來源 |
|---|---|---|
| Repo | https://github.com/openclaw/openclaw | |
| 名稱沿革 | 「Warelay -> Clawdbot -> Moltbot -> OpenClaw」 | https://raw.githubusercontent.com/openclaw/openclaw/main/VISION.md |
| 作者 / 維護 | Peter Steinberger 與社群建立；現由 **OpenClaw Foundation**（獨立 501(c)(3)）開發，Foundation 雇用核心團隊；「OpenAI is a donor, not an owner」 | https://raw.githubusercontent.com/openclaw/openclaw/main/README.md |
| License | MIT © OpenClaw Foundation | 同上 |
| 活躍度 | ~395k stars；最新 release v2026.11.5（2026-11-17）；CalVer | GitHub API |
| 定位 | 跑在自己機器上的個人助理，透過 WhatsApp/Telegram/Slack/Discord/iMessage 等 20+ channel 對話；一個 **Gateway** 程序是 sessions/tools/events/channels 的本地 control plane | README |

### 核心 loop 與 runtime
- 「OpenClaw ships one **embedded agent runtime**: a built-in agent loop, tool wiring, and prompt assembly」。https://docs.openclaw.ai/concepts/agent.md
- Agent loop 是「the serialized, per-session run」：intake → context assembly → inference → tool execution → streaming → persistence；經 Gateway RPC `agent` / `agent.wait` 進入。https://docs.openclaw.ai/concepts/agent-loop.md
- **與 pi 的關係（已變）**：2026-01 Armin 寫「what's under the hood of OpenClaw is a little coding agent called Pi」（https://lucumr.pocoo.org/2026/1/31/pi/），2026-02-02 仍有 commit「fix: update pi packages to 0.51.0」升級 `@mariozechner/pi-agent-core`、`pi-ai`、`pi-coding-agent`、`pi-tui`（經 GitHub commit search API `repo:openclaw/openclaw remove pi-coding-agent` 查得，commit 雜湊未逐一核對）。**現況**：runtime 由 OpenClaw 自有，`packages/agent-core/`（`@openclaw/agent-core`）含 agent loop、compaction、skills、session storage；「No external agent framework packages remain」；「The legacy alias `pi` normalizes to `openclaw`」；只剩 `@earendil-works/pi-tui` 為依賴（package.json 實查）。https://docs.openclaw.ai/agent-runtime-architecture.md 、https://raw.githubusercontent.com/openclaw/openclaw/main/package.json 。**內化的確切日期 UNVERIFIED。**
- **可插拔 harness**：「Models and agent harnesses (Claude, Codex, local models) are plugins you can swap」；runtime id 有 `openclaw`、`codex`、`copilot`、`claude-cli` 等，`codex` 透過 Codex app-server 跑 turn。README、https://docs.openclaw.ai/concepts/agent-runtimes.md
- Tools：核心 read/exec/edit/write 等永遠存在（受 tool policy 管）；`apply_patch` 對 OpenAI 模型預設開。https://docs.openclaw.ai/concepts/agent.md

### 擴充機制
- **Workspace bootstrap 檔**（首輪注入 system prompt）：`AGENTS.md`、`SOUL.md`（persona）、`IDENTITY.md`、`USER.md`、`BOOTSTRAP.md`（首次儀式後刪除）、`MEMORY.md`。https://docs.openclaw.ai/concepts/agent.md
- **Skills**：workspace `skills/`、`.agents/skills`、`~/.agents/skills`、`~/.openclaw/skills`、bundled；分發走 ClawHub。同上 + VISION.md
- **Plugins**：兩種——code plugins（runtime hooks、providers、channels、tools）與 bundle-style（打包 skills、MCP servers 等，「Prefer bundle-style plugins」）。Memory 是單一 slot plugin。VISION.md
- **Hooks**：internal hooks（HOOK.md metadata）+ automations（cron、webhooks、Gmail PubSub）。https://docs.openclaw.ai/llms.txt 索引
- **MCP**：「OpenClaw supports MCP as both a server and a runtime integration surface」，目標是「pragmatic MCP support」；也有 code mode。VISION.md、https://docs.openclaw.ai/llms.txt

### 多步 / 多 agent
- **Sub-agents（內建）**：`sessions_spawn` 產生背景 run，跑在獨立 session `agent:<agentId>:subagent:<uuid>`，預設把結果 **announce** 回 requester；子 agent 預設拿不到 session/message 工具；可 `context: "fork"` 繼承當前 transcript；「Support configurable nesting depth for orchestrator patterns」。https://docs.openclaw.ai/tools/subagents.md
- **Multi-agent routing**：一個 Gateway 跑多個**隔離** agent（各自 workspace、agentDir、SQLite session history），channel 帳號經 **bindings** 路由到 agent——這是「路由」不是「編排圖」。https://docs.openclaw.ai/concepts/multi-agent.md
- 明確不收：「Heavy orchestration layers that duplicate existing agent and tool infrastructure」。VISION.md
- 也可經 ACP 把任務交給外部 coding agent（Codex 等）。https://docs.openclaw.ai/llms.txt

### State、memory、compaction、權限
- **Memory 是 Markdown 檔**：「there is no hidden state」；`USER.md`、`MEMORY.md`、`memory/YYYY-MM-DD.md` 日記、`DREAMS.md`；預設 workspace `~/.openclaw/workspace`。https://docs.openclaw.ai/concepts/memory.md
- 檢索層：預設 builtin memory engine 為 **SQLite**（keyword/vector/hybrid）；另有 active memory（blocking sub-agent 做 recall）、dreaming（背景整併）。https://docs.openclaw.ai/llms.txt 索引
- **Sessions 與共享狀態在 SQLite**：`~/.openclaw/state/openclaw.sqlite`、per-agent `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`；舊版 JSON 檔要 `openclaw doctor --fix` 匯入。https://docs.openclaw.ai/concepts/agent.md 、.../multi-agent.md
- **Compaction**：舊 turn 摘要成 entry 存回 transcript，近期訊息保留，tool call/result 成對不切；「The full conversation history stays on disk」。https://docs.openclaw.ai/concepts/compaction.md
- **權限**：main session 的 tools 預設在 host 上跑（除非設 sandbox）；陌生 DM 需 pairing 核准；exec approvals 為「policy + allowlist + (optional) user approval all agree」，有 deny/allowlist/ask/auto/full 模式。README、https://docs.openclaw.ai/tools/exec-approvals.md

### 設計哲學引述（VISION.md）
- 「Core stays lean; optional capabilities should usually ship as plugins.」
- 「The core carries a per-call tax: each core tool, prompt line, and config key reaches every operator on every model request」
- 「OpenClaw is primarily an orchestration system: prompts, tools, protocols, and integrations.」（這裡 orchestration 指整合，不是多 agent 編排）

---

### 3. Hermes Agent（Nous Research）

### 基本資料
| 項目 | 內容 | 來源 |
|---|---|---|
| Repo | https://github.com/NousResearch/hermes-agent ；docs https://hermes-agent.nousresearch.com/docs/ | |
| 維護 | Nous Research | README |
| License | MIT | GitHub API |
| 語言 | Python | https://hermes-agent.nousresearch.com/docs/developer-guide/architecture |
| 活躍度 | ~264k stars；最新 v0.23.2（2026-11-16）；GitHub 上最舊可見 release 為 v2026.3.12（2026-03-12）。首次公開日期 UNVERIFIED（二手來源說 2026-02） | GitHub API |
| 定位 | 「The self-improving AI agent」，自稱「the only agent with a built-in learning loop」——從經驗建立 skill、使用中改進、搜尋自己過去的對話 | README |

### 核心 loop
- `AIAgent` =「The synchronous orchestration engine」，一個 class 同時服務 CLI、gateway、ACP、batch、API server；loop 在 `agent/conversation_loop.py`。https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
- 流程：模型回 tool calls → 執行 → append 結果 → 回到重建 messages 再呼叫模型；純文字回應結束 turn。預設上限 `agent.max_turns` = 500 次迭代；多個 tool call 用 ThreadPoolExecutor 並行（互動型工具如 `clarify` 例外）；可中斷；有 fallback providers。https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop
- **非極簡**：tool registry 有 70+ tools、約 28 個 toolsets，`tools/*.py` 自動註冊。設計原則之一「System prompt doesn't change mid-conversation」（保 prompt cache）。architecture 頁

### 擴充機制
- **Skills**：SKILL.md + YAML frontmatter，遵循 agentskills.io；三層 progressive disclosure：`skills_list()`（~3k tokens）→ `skill_view(name)` → `skill_view(name, path)`。**`skill_manage` 讓 agent 自己 create/patch/delete skill**（procedural memory）；system prompt 要求在多步流程、踩坑後找到解法、被使用者糾正時存成 skill。位置 `~/.hermes/skills/`；Skills Hub 可裝 skills.sh、ClawHub 等來源並經安全掃描。https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- **Curator**：背景維護 agent 自建 skill——追蹤使用次數，14 天未用 stale、30 天移到 `.archive/`，「never auto-deletes」；可選 LLM consolidation 合併重疊 skill（預設關）。https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
- **MCP**：完整 client（stdio、HTTP、OAuth），`~/.hermes/config.yaml` 的 `mcp_servers`，`tools.include/exclude` 過濾，命名 `mcp_<server>_<tool>`；可經 `mcp-serve` plugin 當 MCP server。https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- **Plugins / hooks / context files**：plugin 系統（custom tools、hooks）、lifecycle hooks；context files 支援 `.hermes.md`、`AGENTS.md`、`CLAUDE.md`、`SOUL.md`、`.cursorrules`。https://hermes-agent.nousresearch.com/docs/llms.txt 索引

### 多步 / 多 agent
- **`delegate_task`**：子 agent「start with a **completely fresh conversation**」，「only its final summary enters the parent's context」；繼承父 toolsets 但禁用 `clarify`、`memory`、`send_message`、`cronjob`；預設最多 10 個並行；**預設扁平**（子 agent 不能再 delegate），`role="orchestrator"` 需 `max_spawn_depth` > 1（預設 1，等於關閉）。子 agent 迭代上限預設 50。https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation 、.../agent-loop
- 另有 cron 排程、heartbeat、`/loop` 類循環 prompt、可寫 Python 腳本透過 RPC 呼叫工具壓縮多步流程。README、docs 索引

### State、memory、compaction、權限
- **Memory**：`~/.hermes/memories/MEMORY.md`（2,200 字元上限）、`USER.md`（1,375 字元）；session 開始時以**凍結快照**注入 system prompt（中途寫入落盤但下個 session 才進 prompt，保 cache）；`memory` 工具 add/patch/remove；外部 provider（Honcho、Mem0 等）並存。https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- **Sessions 在 SQLite**：`~/.hermes/state.db` + FTS5；舊 JSONL（`~/.hermes/sessions/`）「no longer written or read」；`session_search` 直接回原文不經 LLM 摘要。有 `/branch` 指令但文件只順帶提及（細節 UNVERIFIED）。https://hermes-agent.nousresearch.com/docs/user-guide/sessions
- **Compression**：preflight 在超過 context 50% 時摘要中段 turns；gateway 在 85% 時於 turn 之間壓縮；壓縮會開 continuation session。.../agent-loop、.../sessions
- **權限**：危險指令 pattern 清單 + `approvals.mode`：`smart`（預設，輔助 LLM 判斷風險，不確定才問人）、`manual`、`off`（=`--yolo`）；hardline blocklist 任何模式都擋；逾時 300 秒預設拒絕；container backend 跳過檢查（sandbox 即邊界）；DM pairing。https://hermes-agent.nousresearch.com/docs/user-guide/security

### 設計哲學
- 官方明確的「反框架 / 反 MCP」宣言：**未找到**（UNVERIFIED / 可能不存在）。Hermes 的主張是「learning loop」與「Runs anywhere」，而非極簡。

---

### 4. 相關 essays（含日期）

| 日期 | 作者 / 標題 | 重點 | URL |
|---|---|---|---|
| 2025-08-18 | Armin Ronacher，code MCPs | 提議 MCP server 只暴露一個接受程式碼的工具（codemode 的前身思路） | https://lucumr.pocoo.org/2025/8/18/code-mcps/（僅經搜尋摘要，未打開，UNVERIFIED） |
| 2025-11-30 | Mario Zechner，「What I learned building an opinionated and minimal coding agent」 | <1000 token prompt、4 tools、不做 MCP/sub-agent/plan mode/todos/background bash、YOLO | https://mariozechner.at/posts/2025-11-30-pi-coding-agent/ |
| 2025-12-13 | Armin Ronacher，「Skills vs Dynamic MCP Loadouts」 | 「Skills do not actually load a tool definition into the context」；「MCP servers have no desire to maintain API stability」；偏好 agent 自己維護 skill | https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/ |
| 2026-01-31 | Armin Ronacher，「Pi: The Minimal Agent Within OpenClaw」 | OpenClaw 底層是 pi；session tree；agent 自寫 extension；`/control` 簡易多 agent | https://lucumr.pocoo.org/2026/1/31/pi/ |
| 2026-04-08 | Mario Zechner，「I've sold out」/ Armin，「Mario and Earendil」 | pi 併入 Earendil，core MIT | http://mariozechner.at/posts/2026-04-08-ive-sold-out/ 、https://lucumr.pocoo.org/2026/4/8/mario-and-earendil/ |
| 2026-05-07 | pi.dev，「Pi Has a New Home at Earendil」 | repo/npm scope 搬遷 | https://pi.dev/changelog/2026/5/7/pi-has-a-new-home |
| 2026-09-29 | pi CHANGELOG v0.99.0 | 內建 MCP + codemode + tool_search | https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/CHANGELOG.md |

---

### 5. 對比表

| 面向 | pi | OpenClaw | Hermes Agent |
|---|---|---|---|
| 核心 loop | 單一 loop，<1k token prompt，4 tools | 單一 per-session serialized loop（自有 agent-core，可換 harness） | 單一 `AIAgent` loop，70+ tools |
| 定位 | coding agent harness / SDK | 多 channel 個人助理 + Gateway | 自我改進的通用 agent + gateway |
| Skills | Agent Skills，progressive disclosure | 同上 + ClawHub | agentskills.io + **agent 自建/修改 skill** + curator |
| MCP | 2025 拒絕 → 2026-09 內建（預設 codemode 間接） | client + server | client + server（plugin） |
| Sub-agents | 不內建；extension 或 bash 自我 spawn | 內建 `sessions_spawn`，可設巢狀深度 | 內建 `delegate_task`，預設扁平、可開 orchestrator |
| 多 agent | 無編排；`/control` 互傳 prompt | 多隔離 agent + bindings 路由；拒絕重型編排層 | 子 agent 委派；Bot Mode 多 profile |
| State | JSONL session tree（`~/.pi/agent/sessions/`） | Markdown memory + SQLite sessions/state | Markdown memory + SQLite `state.db` FTS5 |
| Branching | 一級公民（樹狀 session、/tree、fork） | 子 session fork（`context: "fork"`） | `/branch`（細節 UNVERIFIED） |
| Compaction | 門檻觸發摘要 entry，原紀錄保留 | 同上 | 50% preflight / 85% gateway |
| 權限 | 無 approval（YOLO），靠 container；可自寫 gate | exec approvals + allowlist + sandbox + DM pairing | smart（LLM 判風險）/manual/off + hardline blocklist + pairing |
| 語言 | TypeScript | TypeScript | Python |

---

## Arch-B 研究：Supervisor + 專家子代理圖 vs. General Harness + Skills + Subagents（2025–2026 一手來源）

研究日期：2026-11-17。標 [OPENED] 的是本次實際打開過的 URL，標 [UNVERIFIED] 的只看過搜尋摘要或二手報導。
數字一律是原文引述，不是我推算的。

---

### TL;DR（結論先講）

1. **2026 年的共識預設是「單一通用 agent + harness」**：agent loop、內建工具、skills（progressive disclosure）、subagents 當工具、檔案系統當記憶、compaction、hooks/permissions。Anthropic、OpenAI、LangChain 三家的旗艦產品都長這樣：Claude Agent SDK / Managed Agents、Codex + AGENTS.md + Skills、Deep Agents。
2. **多代理沒有消失，只是被降級成「需要時才用的工具」**：subagent 用來隔離 context、平行處理讀取型工作、做驗證，不再當成預設的「依職能切分的組織圖」。Anthropic 明確反對依角色切分。LangChain 自己的 `langgraph-supervisor` README 也寫了 "We now recommend using the supervisor pattern directly via tools rather than this library"。
3. **確定性 workflow/graph 仍然被推薦**的場合：步驟固定且已知、需要可預測的成本與延遲、合規與稽核、高風險不可逆動作要人工核准、有明確驗收標準的 evaluator loop。不過 2026 的趨勢是把這些做成 harness 裡的 **hooks / permissions / HITL middleware / 程式碼編排的 workflow**，而不是把「LLM 路由」寫死成 supervisor graph。
4. 課程設計的意涵：「Supervisor → DocAgent/DBAgent/OpsAgent」依**職能**切分，正好是 Anthropic 2026-01 指南點名的反模式。不過 Ops 的人工核准步驟、Postgres checkpointer、tracing 都還是正確的工程元素，值得保留，只是位置要換。

---

### 1. Anthropic

### 1.1 Building effective agents（2024-12-19，頁面帶 2026 編者註）[OPENED]
https://www.anthropic.com/engineering/building-effective-agents
- 區分 workflows（"orchestrated through predefined code paths"）和 agents（"LLMs dynamically direct their own processes and tool usage"）。
- "workflows offer predictability and consistency for well-defined tasks"，agents 則適用於 "flexibility and model-driven decision-making are needed at scale"。
- 建議 "finding the simplest solution possible, and only increasing complexity when needed"，並建議先直接用 LLM API。對 framework 的評語是它們 "can obscure the underlying prompts and responses"。
- **2026 編者註**："Much of the tooling landscape described in this post has changed since December 2024."，並導向 "how we built Claude Managed Agents" 和 Managed Agents 文件。
- 意涵：workflow 和 agent 的二分法還在，但官方已經說工具層的建議過時了，新的參考點是 harness 和 Managed Agents。

### 1.2 Effective context engineering for AI agents（2025-09-29）[OPENED]
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 三種長任務技術：compaction、structured note-taking（"the agent regularly writes notes persisted to memory outside of the context window"）、sub-agent architectures（"specialized sub-agents can handle focused tasks with clean context windows"，回傳的摘要常在 1,000–2,000 tokens）。
- just-in-time retrieval：只保留檔案路徑、查詢這類輕量參照，到 runtime 才載入內容。
- "One of the most common failure modes we see is bloated tool sets that cover too much functionality."
- 結論："do the simplest thing that works"。
- 意涵：subagent 的價值在於 **context 隔離**，不在於職能分工。工具過多是主要失敗模式，這也是 skills、tool search 出現的原因。

### 1.3 Equipping agents for the real world with Agent Skills（2025-10-16；2025-12-18 更新為開放標準）[OPENED]
https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable."
- 定位："Instead of building fragmented, custom-designed agents for each use case"，用 skills 把 "general-purpose agents into specialized agents"。
- 和 MCP 的關係：MCP 負責接上工具，skills 負責教 agent 怎麼用那些工具（workflow 知識）。
- 2025-12-18 更新：Agent Skills 以開放標準發布，網址 agentskills.io。
- 意涵：**直接反對「每個用例做一個專屬 agent」**。DocAgent/DBAgent/OpsAgent 在 harness 模式下比較自然的形態是 3 個 skill，必要時再加上 subagent 隔離。

### 1.4 How we built our multi-agent research system（2025-06-13）[OPENED]
https://www.anthropic.com/engineering/multi-agent-research-system
- 採用 orchestrator-worker：lead agent 平行派出 subagents。
- 適合 "valuable tasks that involve heavy parallelization"、資訊量超過單一 context、工具很多的情境。
- 不適合所有 agent 都需要 "share the same context" 的領域。coding 的可平行部分較少，比較不適合。
- 原文數字：agents 約用 chat 的 4× tokens，multi-agent 約 15×。在 BrowseComp 上，token 用量解釋約 80% 的表現變異。Opus 4 lead + Sonnet 4 subagents 在內部研究評測上比單一 Opus 4 高 90.2%。
- 限制：subagents 同步執行，lead 無法中途調整方向，subagent 之間也不能互相協調。
- 意涵：多代理在**廣度優先、讀取型、可平行**的任務上確實有效。這是 orchestrator **動態**決定子任務，不是寫死路由的 supervisor。

### 1.5 Effective harnesses for long-running agents（2025-11-26，Justin Young）[OPENED]
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 把 Claude Agent SDK 稱為 "a powerful, general-purpose agent harness adept at coding"。
- initializer agent 和 coding agent 的 system prompt、工具完全相同，只有初始 user prompt 不同。兩者靠 `claude-progress.txt`、`init.sh`、git history 交接。
- "However, compaction isn't sufficient."
- 對專家代理的態度："still unclear whether a single, general-purpose coding agent performs best across contexts"，testing/QA/cleanup 專家代理被列為開放問題。
- 意涵：所謂「多個 agent」其實是**同一個 harness 換不同 prompt**，狀態放在檔案系統，不放在 graph state。

### 1.6 Harness design for long-running application development（2026-03-24，Prithvi Rajasekaran）[OPENED]
https://www.anthropic.com/engineering/harness-design-long-running-apps
- planner / generator / evaluator 三角色。evaluator 透過 Playwright MCP 實際點擊、操作 app。
- 需要獨立 evaluator 的原因：agents "tend to respond by confidently praising the work"；"tuning a standalone evaluator to be skeptical turns out to be far more tractable"。
- 隨模型進步拿掉的元件：Opus 4.5 拿掉 context resets，Opus 4.6 拿掉 sprint 結構，per-sprint 評估改成最後跑一次。planner 保留下來。
- "every component in a harness encodes an assumption about what the model can't do on its own"
- 意涵：**generator-verifier 是 2026 年少數被反覆驗證有效的多代理型態**。harness 元件要定期重新檢驗，該拆就拆。

### 1.7 Scaling Managed Agents: Decoupling the brain from the hands（2026-04-08，Lance Martin 等）[OPENED]
https://www.anthropic.com/engineering/managed-agents
- harness 的定義："the loop that calls Claude and routes Claude's tool calls to the relevant infrastructure"。
- "harnesses encode assumptions about what Claude can't do on its own"，這些假設 "need to be frequently questioned"。舉例：為 Sonnet 4.5 加的 context resets 到 Opus 4.5 已經 "dead weight"。
- 拆成 brain（Claude + harness）、hands（sandbox/tools）、session（"the append-only log of everything that happened"）三個介面。session 是 "a context object that lives outside Claude's context window"。
- 多代理："Scaling to many brains just meant starting many stateless harnesses"。
- 意涵：持久化的單位是 **session event log**，不是 graph checkpoint。這和 LangGraph checkpointer 是同一類需求，抽象層不同。

### 1.8 Building multi-agent systems: When and how to use them（claude.com，2026-01-23）[OPENED]
https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
- "single-agent systems handle most enterprise workflows effectively"
- 多代理勝出的三種情境：context protection、parallelization、specialization（工具太多或行為需求互相衝突）。
- 原文數字：multi-agent "typically use 3-10x more tokens than single-agent approaches for equivalent tasks"。
- **依 context 邊界切分，不要依工作類型或角色切分**。依角色切分 "creates constant coordination overhead"，每次 handoff 都會損失資訊。
- 意涵：**對課程架構最直接的批評**。Doc/DB/Ops 是依職能切分。如果一個使用者問題同時需要文件和 DB（例如「這個 incident 對照 runbook，查一下 DB 指標」），supervisor 就得來回 handoff，每次都丟失 context。

### 1.9 Multi-agent coordination patterns: Five approaches（claude.com，2026-04-10）[OPENED]
https://claude.com/blog/multi-agent-coordination-patterns
- 五種模式：generator-verifier、orchestrator-subagent、agent teams、message bus、shared state。
- "For most use cases, we recommend starting with orchestrator-subagent"
- 警告：不要選 "sound sophisticated" 的模式。sequential subagents 要付多代理的 token 成本，卻拿不到平行帶來的速度。
- 意涵：Anthropic 不反對 orchestrator。它反對的是**預設就用**，以及用錯切分軸。

### 1.10 A harness for every task: dynamic workflows in Claude Code（claude.com，2026-06-02）[OPENED]
https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/
- "Claude can now write its own harness on the fly, custom-built for the task at hand."，模型自己寫 JS workflow，用 `agent()`、`parallel()`、`pipeline()` 編排 subagents。
- 和 static workflow 的對比："because static workflows need to work for all edge cases, they are usually more generic"。
- 確定性仍有角色："the deterministic loop holds the bracket"。
- 要解決的失敗模式：agentic laziness、self-preferential bias、goal drift（"especially after compaction"）。
- 節制："they are not needed for every task and may end up using significantly more tokens"；"parallelism and specialization have to earn their coordination cost"。
- 意涵：2026 的前沿是**模型動態生成編排**，不是人預先畫好 graph。不過「確定性迴圈 + LLM 節點」這個概念仍然成立。

### 1.11 Code execution with MCP（2025-11-04）/ Advanced tool use（2025-11-24）[OPENED]
- https://www.anthropic.com/engineering/code-execution-with-mcp ："Most MCP clients load all tool definitions upfront directly into context"。範例中 token 用量 "from 150,000 tokens to 2,000 tokens"。把工具做成檔案，按需讀取；存下來的程式碼加上 SKILL.md 就成了 skill。
- https://www.anthropic.com/engineering/advanced-tool-use ：Tool Search Tool 的例子是 "~8.7K tokens, preserving 95% of context window"。文中提到 58 個工具約 55K tokens，也見過工具定義達 134K tokens。Programmatic Tool Calling 的例子是 "43,588 to 27,297 tokens, a 37% reduction"。
- 意涵：MCP context 膨脹是官方承認的問題，官方解法是 progressive disclosure（tool search、code execution、skills），不是拆成多個 agent。

### 1.12 Claude Agent SDK 文件（harness 提供什麼）[OPENED]
- https://code.claude.com/docs/en/agent-sdk/overview ：built-in tools、hooks、subagents、MCP、permissions、sessions、skills/commands/memory（`.claude/`）、plugins。Managed Agents 被描述為 "A hosted agent harness"。
- https://code.claude.com/docs/en/agent-sdk/agent-loop ：automatic compaction（`compact_boundary`、`PreCompact` hook）、`max_turns`、`max_budget_usd`、permission modes（default/acceptEdits/plan/dontAsk/auto/bypassPermissions）、hooks（`PreToolUse` 可以擋下工具呼叫）、ToolSearch 預設延遲載入 MCP schemas、sessions 支援 resume/fork 和 `session_store`。
- https://code.claude.com/docs/en/agent-sdk/subagents ：四個好處是 context isolation、parallelization、specialized instructions、tool restrictions。subagent 可以巢狀，預設深度 3、並行 20，可設定預算上限。"Subagents work well for a few delegated tasks per turn"，規模更大時改用 `Workflow` tool。
- 意涵：課程手刻的元件（路由、HITL、checkpoint、tracing、工具權限）在 harness 裡都是**一級功能**。

---

### 2. OpenAI

### 2.1 Agents SDK：Orchestrating multiple agents [OPENED]
https://openai.github.io/openai-agents-python/multi_agent/
- LLM-driven 編排 "uses the intelligence of an LLM to plan, reason, and decide"。code-driven 編排 "makes tasks more deterministic and predictable, in terms of speed, cost and performance"。
- agents-as-tools：manager "keeps control of the conversation"，適用於專家 "should help with a bounded subtask but should not take over"。handoffs：適用於 "routing itself is part of the workflow"。
- code-driven 的手法：structured outputs 做分類路由、chaining、evaluator loops、平行執行。
- 意涵：OpenAI 兩種都支援，明確承認 **code-driven 在成本、延遲、可預測性上的優勢**。課程的 supervisor 屬於 LLM-driven 的 manager/agents-as-tools 型態。

### 2.2 A practical guide to building agents（PDF，2025；確切日期在擷取文字中未見，[UNVERIFIED] 日期）[OPENED]
https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- "Our general recommendation is to maximize a single agent's capabilities first."
- 拆分時機：Complex logic（prompt 裡 if-then-else 太多）、Tool overload（"Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools"）。
- 人工介入："High-risk actions: Actions that are sensitive, irreversible, or have high stakes should trigger human oversight"。
- 結語："starting with a single agent and evolving to multi-agent systems only when needed"。
- 意涵：單一 agent 優先。高風險動作要人工核准，這是**跨架構的不變量**。

### 2.3 Harness engineering: leveraging Codex in an agent-first world（2026-02-11 [UNVERIFIED 日期，取自二手報導]；作者 Ryan Lopopolo [UNVERIFIED]）[OPENED 經 r.jina.ai 代理]
https://openai.com/index/harness-engineering/ （直連 403，內容透過 r.jina.ai 讀取）
- AGENTS.md："give Codex a map, not a 1,000-page instruction manual"；當作 "the table of contents"，指向結構化的 `docs/`。
- 架構約束 "enforced mechanically via custom linters ... and structural tests"。
- "Humans steer. Agents execute."；"Humans always remain in the loop, but work at a different layer of abstraction"。
- 單一 Codex run 可以連續做一個任務 6 小時以上。review 大多改成 agent-to-agent。
- 意涵：OpenAI 的 harness 核心是**環境、約束、回饋迴路**，不是多代理拓撲。確定性放在 linter 和測試，不放在 agent 路由。

### 2.4 AGENTS.md / Skills in Codex [OPENED]
- https://learn.chatgpt.com/docs/build-skills ：ChatGPT 和 Codex 的 skills "build on the open agent skills standard"（agentskills.io）；"Skills use progressive disclosure to manage context efficiently"。
- 意涵：Skills 已經跨廠商。Anthropic 和 OpenAI 都用 SKILL.md。

---

### 3. LangChain

### 3.1 Agent frameworks, runtimes, and harnesses — oh my!（2025-10-25，Harrison Chase）[OPENED]
https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my
- LangChain = framework，LangGraph = runtime（durable execution、streaming、HITL、persistence），DeepAgents = harness（"batteries included"：prompts、planning、filesystem）。
- 意涵：LangChain 官方把 LangGraph 重新定位成**底層 runtime**。直接用 StateGraph 寫 agent 拓撲成了「要客製時才下探」的層級。

### 3.2 Deep Agents overview（docs）[OPENED]
https://docs.langchain.com/oss/python/deepagents/overview
- "the agent harness for complex, multi-step work"
- 內建：`write_todos`、虛擬檔案系統、`task` tool（隔離的 subagents，可 async）、SKILL.md progressive disclosure、AGENTS.md 記憶、summarization/offloading、`interrupt_on` HITL。底層是 LangGraph（durable execution）。
- 選型：複雜長任務用 Deep Agents，不需要這些內建能力就用 `create_agent`，要從頭打造客製 workflow 才用 LangGraph。
- 意涵：**LangChain 自家的 2026 旗艦就是 harness 模式**，幾乎是 Claude Code 的開源翻版。

### 3.3 Improving Deep Agents with harness engineering（2026-02-17，Vivek Trivedy）[OPENED]
https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- harness 的目標是 "mold the inherently spiky intelligence of a model for tasks we care about"。
- 調整的旋鈕：system prompt、tools、middleware（`PreCompletionChecklistMiddleware`、`LocalContextMiddleware`、`LoopDetectionMiddleware`、time budget）。
- 原文數字：Terminal Bench 2.0（模型固定為 gpt-5.2-codex），52.8% → 66.5%（"13.7 points"），"Top 30 to Top 5"。
- 意涵：**只改 harness、不換模型就有大幅提升**。教學重點應該放在 harness 工程。

### 3.4 LangChain multi-agent docs（v1）[OPENED]
- https://docs.langchain.com/oss/python/langchain/multi-agent ：五種模式是 subagents、handoffs、skills、router、custom workflow。原文 "not every complex task requires this approach"。多代理的時機是 "a single agent has too many tools and makes poor decisions"、需要大量專門 context、要強制順序約束。頁面完全沒用 "supervisor" 這個詞。
- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ："coordinates subagents by calling them as tools"、"each subagent invocation works in a clean context window"。適用於 "multiple distinct domains (e.g., calendar, email, CRM, database)"。subagent 內可以用 interrupts 做 HITL。
- https://docs.langchain.com/oss/python/langchain/multi-agent/skills ："Use the skills pattern when you want a single agent with many possible specializations"、"Skills are simpler than full sub-agents"。
- https://docs.langchain.com/oss/python/langchain/human-in-the-loop ：`HumanInTheLoopMiddleware`、`interrupt_on`，決策有 approve/edit/reject。"Human-in-the-loop requires checkpointing to handle interrupts."
- https://docs.langchain.com/oss/python/langgraph/workflows-agents ："Workflows have predetermined code paths"；prompt chaining 用於 "well-defined tasks that can be broken down into smaller, verifiable steps"。
- 意涵：LangChain 也承認「多個 distinct domains」可以用 subagents（課程的 Doc/DB/Ops 勉強符合這一點）。但推薦的實作是 **subagents-as-tools**，不是 supervisor library。

### 3.5 langgraph-supervisor README [OPENED]
https://github.com/langchain-ai/langgraph-supervisor-py
- "We now recommend using the supervisor pattern directly via tools rather than this library for most use cases."，原因是 tool-calling 方式 "gives you more control over context engineering"。
- 意涵：**連 LangChain 都不再推薦專用的 supervisor library。** supervisor 的概念還在，但實作形態已經變成「主 agent 把子 agent 當工具呼叫」。

### 3.6 How and when to build multi-agent systems（2025-06-16，Harrison Chase）[OPENED]
https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems
- "read actions are inherently more parallelizable than write actions"
- "Context engineering is critical to making agentic systems work reliably."
- 調和 Cognition 和 Anthropic 的立場：沒有一體適用的架構。不論哪種，都需要 durable execution、observability、eval。（作者是 LangChain 的人，立場有利益相關。）

---

### 4. Cognition / Manus / 辯論

### 4.1 Cognition: Don't Build Multi-Agents（2025-06-12，Walden Yan）[OPENED]
https://cognition.com/blog/dont-build-multi-agents
- 原則 1："Share context, and share full agent traces, not just individual messages"
- 原則 2："Actions carry implicit decisions, and conflicting decisions carry bad results"
- 建議單執行緒的線性 agent，長任務再加一個壓縮歷史的模型。

### 4.2 Cognition: Multi-Agents: What's Actually Working（2026-04-22，Walden Yan）[OPENED]
https://cognition.com/blog/multi-agents-working
- 有效的型態：多代理只負責讀取或提供意見，"writes stay single-threaded"。乾淨 context 的 reviewer（"clean context leads to a notable improvement ... generator-verifier loop"）。smart friend（兩邊都是強模型時）。manager + child agents（"map-reduce-and-manage"）。
- 無效的型態：parallel-writer swarms（"most of the sexy ideas in that space still don't see meaningful adoption"）、非結構化的 agent 網路。
- "the open problems are all communication problems"
- 意涵：2026 的修正版共識是**單一寫入者 + 唯讀或審查型 subagents**。課程的 OpsAgent 會執行寫入動作，DB/Doc 是唯讀，這個切法剛好可以對應「單一寫入者」原則，只是需要主 agent 保有完整 context。

### 4.3 Manus: Context Engineering for AI Agents（2025-07-18，Yichao "Peak" Ji）[OPENED]
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- "the KV-cache hit rate is the single most important metric for a production-stage AI agent"
- mask, don't remove：避免在迭代中途增刪工具。
- 檔案系統是 "the ultimate context ... unlimited in size, persistent by nature"。
- todo.md 複誦、保留錯誤（"leave the wrong turns in the context"）、避免被 few-shot 帶偏。
- 意涵：單一 agent 長迴圈 + 檔案系統記憶的實戰證據。動態切換 agent 或工具會破壞 KV-cache。

---

### 5. 標準層

### 5.1 Agent Skills open standard [OPENED]
- https://agentskills.io ："originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products"。三階段：discovery、activation、execution。
- client 展示頁 https://agentskills.io/clients 是動態渲染，擷取不到名單 [UNVERIFIED 名單]。已確認支援的有 Claude（Agent SDK）、OpenAI ChatGPT/Codex（見 2.4）、LangChain Deep Agents（見 3.2）。

### 5.2 MCP / AAIF [OPENED]
- https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation ：2025-12-09 成立 AAIF，創始專案是 MCP（Anthropic）、goose（Block）、AGENTS.md（OpenAI）。原文："more than 10,000 published MCP servers"；AGENTS.md 被 "more than 60,000 open source projects and agent frameworks" 採用。

### 5.3 MCP context 膨脹 vs skills/CLI 辯論（2026）
- 一手來源：Anthropic 的 code-execution-with-mcp 和 advanced-tool-use（見 1.11）承認問題，並提出 tool search、程式化工具呼叫。Claude Agent SDK 現在預設延遲載入 MCP schemas（見 1.12）。
- 二手來源 [UNVERIFIED，只看過搜尋摘要]：OpenRouter "MCP vs CLI vs Skills"（https://openrouter.ai/blog/insights/mcp-vs-cli-vs-skills ）、Quandri "MCP is dead"（https://www.quandri.io/engineering-blog/mcp-is-dead ，據報後來承認 tool search 已大致解決膨脹問題）、Firecrawl、PubNub 等。大致的趨勢是：爭論主軸從「MCP 還是 CLI」轉向「eager 還是 lazy loading」。MCP 在企業稽核和多使用者情境仍有價值。
- 意涵：MCP 現在是連接層的標準。context 膨脹靠 progressive disclosure 解決，不靠拆 agent。

---

### 6. 確定性 graph / workflow 仍被推薦的地方（平衡面）

| 場合 | 來源依據 |
|---|---|
| 步驟固定、已知的任務（ETL、表單審批、分類後分派） | Anthropic BEA："workflows offer predictability and consistency for well-defined tasks"；LangGraph docs 的 prompt chaining |
| 需要可預測的成本、延遲、表現 | OpenAI Agents SDK："code-driven ... more deterministic and predictable, in terms of speed, cost and performance" |
| 高風險、不可逆動作的人工核准 | OpenAI practical guide 的 "High-risk actions"；LangChain `HumanInTheLoopMiddleware` + checkpointer；Claude Agent SDK permissions/`canUseTool`/`PreToolUse` hook；Deep Agents `interrupt_on` |
| 強制順序約束 | LangChain multi-agent docs："enforce sequential constraints" 是多代理或 custom workflow 的理由之一 |
| 有明確驗收標準的 generator-verifier loop | Anthropic coordination patterns；harness-design-long-running-apps；Cognition 2026；OpenAI evaluator loops |
| 大規模 fan-out 的編排（迴圈、bracket、pipeline） | Anthropic dynamic workflows："the deterministic loop holds the bracket"，但 2026 的做法是由模型生成這段程式碼 |
| 架構約束、品質閘門 | OpenAI harness engineering：custom linters + structural tests 機械化執行 |
| durable execution、persistence | LangChain 把 LangGraph 定位為 runtime；Deep Agents 本身就跑在 LangGraph 上 |

重點：2026 年**沒有人說確定性控制不重要**。爭議點在確定性該放在哪一層。
- 舊做法：把「哪個 agent 處理」寫成 graph 邊（LLM supervisor 路由），確定性和 agent 拓撲綁在一起。
- 新做法：agent 拓撲交給模型或 harness，確定性放在**護欄層**（hooks、permissions、HITL interrupt、linter/測試、budget/turn 上限），或放在由程式碼驅動的外層 workflow。

---

### 7. 爭議點（還沒定論的）

1. **專家 agent 有沒有用**：Anthropic 2025-11 說 "still unclear"，2026-03 的 planner/generator/evaluator 證明角色分工在長任務上有效，2026-01 又反對依角色切分。我的調和讀法是：依「需要獨立 context 或懷疑立場」切分（evaluator）可以，依「業務職能」切分（Doc/DB/Ops）通常不行。
2. **多代理的成本**：15×（2025-06 研究系統）、3–10×（2026-01 指南）。換到的品質是否值得，取決於任務價值。
3. **supervisor 是不是反模式**：Anthropic 推薦以 orchestrator-subagent 起步，LangChain docs 列出 subagents 模式並說適用於 "multiple distinct domains"。所以 supervisor **概念**沒被否定，被淘汰的是「專用 supervisor graph library」和「依職能硬切的拓撲」。
4. **MCP vs skills/CLI**：二手來源吵得很兇，一手來源（Anthropic）的態度是兩者互補，並用 lazy loading 解決膨脹。
5. **harness 元件的壽命**：Anthropic 兩篇都強調 harness 假設會隨模型過時。這會讓任何寫死的架構（包括 5 層 graph）都有折舊風險。

---

### 8. 對課程的具體意涵（給設計者）

- 保留：Postgres checkpointer（對應 session 或 durable execution）、LangSmith tracing（observability，各家都說必要）、Ops 的人工核准（跨架構不變量）、Text2SQL 和 RAG 的技術內容（變成 skills 或 tools）。
- 調整：
  - 主軸從「Supervisor 路由到 3 個職能 agent」改成「1 個通用 agent + 3 個 skills（doc-rag、text2sql、ops-runbook）+ MCP tools + 按需的 subagent」，subagent 用在大量文件檢索的 context 隔離或平行查詢。
  - Ops 的核准改用 `HumanInTheLoopMiddleware` / `interrupt_on`（LangChain）或 `PreToolUse`/`canUseTool`（Claude SDK），做成**工具層的確定性閘門**。
  - 加入 generator-verifier（例如 SQL 結果驗證、RCA 報告審查），這是 2026 年證據最強的多代理型態。
  - 加入 compaction、檔案系統記憶（progress file / AGENTS.md）、budget/turn 上限。
- 教學上可以把 Supervisor graph 當成**對照組**來教：示範它在跨領域問題上的 handoff 資訊損失，再對比 harness 版本。這樣學生兩種都學到，也知道 2026 年的預設選擇是哪個。

---

## 2025–2026 Incident-response / SRE Agent 架構調研（arch-C）

調研日：2026-11-17。標「OPENED」= 我實際用 WebFetch 打開過；標「UNVERIFIED」= 只看過搜尋摘要或第三方轉述。
數字只引用原文出現者，並標明是廠商自述。

---

### TL;DR

2026 的主流不是「Supervisor 固定路由到 DocAgent / DBAgent / OpsAgent」，而是：

**一個 investigation agent（假設驅動迴圈）+ tools（愈來愈多走 MCP）+ runbook 寫成 skills / 知識檔 + 依「假設」動態開平行 subagent + 寫入動作走 policy/approval gate。**

subagent 依**假設**切（每個候選根因一個），不依**資料源**切（Doc/DB/Ops）。
例外：AWS DevOps Agent 用固定**生命週期階段**的 agent type（Triage → RCA → Mitigation）；Azure SRE Agent 有可選的 custom agent handoff chain（最接近 supervisor 模式），但它自己的工程文章說 generalist agent 表現更好。

---

### 一、廠商產品

### 1. Datadog Bits AI SRE（Bits Investigation）
- 連結：https://www.datadoghq.com/blog/building-bits-ai-sre/ （OPENED，2026-01-12）；https://docs.datadoghq.com/bits_ai/bits_remediation/ （OPENED）
- 架構：單一 agent，**假設樹**迴圈：formulate hypotheses → 用 targeted queries validate/reject → 被支持的假設再拆 sub-hypotheses 往下挖，"recursively generates deeper root cause hypotheses until it exhausts the search space"。每個假設結論為 validated / invalidated / inconclusive。文章沒說有平行 subagent，只說未來會有 "more expert investigator and optimization agents"。
- 知識：以即時 telemetry 為主；文章未談 runbook。
- 工具：內部 tool call 查 logs/traces/metrics；文章沒提 MCP。（Datadog MCP server 2026-03 GA — UNVERIFIED，搜尋摘要）
- 安全：remediation 由 Guardrails 管："Admins govern which actions Bits can take and who must approve them"；一鍵動作需 guardrail 涵蓋該動作與目標資源；Action History 記錄由哪個 guardrail 放行、誰觸發；Preview。Ask/Deny 模式細節 UNVERIFIED。
- 教訓：早期版本「summarize 全部資料」會讓 input token 線性膨脹、被無關錯誤帶偏；改成每個假設綁定特定 telemetry 的因果鏈。
- Evals：用數百個團隊標註的真實事件 + 封存 telemetry 回放，LLM judge 打 pass/fail。

### 2. Microsoft Azure SRE Agent
- 連結：overview https://learn.microsoft.com/en-us/azure/sre-agent/overview （OPENED，ms.date 2026-10-28）；custom agents https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents （OPENED，2026-03-18）；run modes https://learn.microsoft.com/en-us/azure/sre-agent/run-modes （OPENED，2026-06-02）；工程文章 "The agent that investigates itself" https://techcommunity.microsoft.com/blog/appsonazureblog/the-agent-that-investigates-itself/4500073 （OPENED，2026-03-10）
- 架構（產品面）：主 agent + 五個擴充點：Skills、Custom agents、Python tools、MCP servers、Agent hooks。Custom agent 以 YAML 定義（system_prompt、handoff_description、tools、connectors、enable_skills），用 `/agent` 顯式叫用，或由 incident/scheduled task 觸發；可串 handoff chain，且**共享同一 conversation context**（"Custom agents don't get a clean slate"）。官方表格：「Read-only queries → No（主 agent 自己處理即可）」。
- 架構（工程面）：團隊轉向**單一 generalist agent**，工作區是 filesystem（source code、runbooks、query schemas、notes），用 read_file/grep/shell 而非客製 API："a generally capable agent in the right execution environment outperforms a specialized agent with bespoke tooling."；有獨立子任務時開**平行 subagent**（各自 context window）再合併，避免一個假設污染另一個。早期高分情境靠「hand-built subagents、pre-written log queries」等重度人工鷹架，後來移除。
- 知識：產品面 Knowledge base（md/txt runbook、postmortem、架構文件，自動索引）+ Skills（"Team-wide procedure with optional execution"）。工程面用**可瀏覽的結構化 Markdown memory 取代 RAG**："let the model navigate memory, not retrieve it through query matching"；memory staleness 仍未解。
- 工具：MCP server（Datadog、Splunk、New Relic、Dynatrace、Elasticsearch 等 partner connector，或任何自訂 MCP）+ Azure CLI/ARM + Kusto。
- 安全：Run mode（Review / Autonomous）與 permission（RBAC/managed identity）分離，兩者都要滿足；Review 模式下只有 SRE Agent Administrator 能按 Approve；Review 的 Approve/Deny 按鈕**只覆蓋 Azure infra 寫入**，其他動作（寄信、發 Teams）要靠 hooks 或 tool access policy（每個 tool allow/ask/deny）。注意：response plan / scheduled task 預設是 Autonomous，agent 層預設 Review；官方建議先 Review 2–4 週再逐 trigger 放權。缺權限時走 Entra OBO 臨時授權。
- 工程文章數字（廠商自述）：Intent Met 在 novel incidents 由 45% → 75%。

### 3. AWS DevOps Agent
- 連結：多 agent 推理 https://aws.amazon.com/blogs/devops/how-aws-devops-agent-uses-multi-agent-reasoning-to-find-root-causes/ （OPENED，2026-05-27，內容截斷）；Skills 文件 https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html （OPENED）；擴充文章 https://aws.amazon.com/blogs/mt/extending-aws-devops-agent-with-skills-model-context-protocol-mcp-servers-custom-agents-and-connectors/ （OPENED，2026-11-02，內容截斷）
- 架構：明說 "multi-agent architecture that decomposes incident operations into specialized capabilities"——**按生命週期階段**切：Triage、Investigation(RCA)、Mitigation、Prevention/Learning；Skills 文件列出 agent types：Generic、On-demand、Incident Triage、Incident RCA、Incident Mitigation、Incident UI、Evaluation、Release testing。RCA 階段 "generates multiple competing root-cause theories simultaneously"，用正反證據檢驗。
- 知識：**Application Topology Graph**（由 CloudFormation/CDK、tag、runtime observability、CI/CD 學出的依賴圖；Investigation 沿邊追溯、Mitigation 用來估 blast radius）+ Investigation Journal（稽核軌跡）+ **Skills**（Agent Skills 規範子集，SKILL.md + references/ + assets/，依 frontmatter description 自動載入，可指定給特定 agent type 以省 context；舊 Runbooks 已**自動遷移為 Skills**；腳本預設不支援，開 Sandbox preview 才能放可執行碼）。另有自動生成的 learned skills（如 Agent Space Understanding）。
- 工具：內建唯讀 AWS API tool；自訂 MCP server（帳號層註冊、每個 Agent Space allowlist 個別 tool）；partner connector = 對方託管的 MCP。"A Skill (reasoning) plus an MCP server (data access) is the gold standard."
- 安全："generates mitigation plans but does not execute remediation actions"；寫入能力限於建 ticket / support case。文件警告自訂 MCP server 增加 prompt injection 風險（搜尋摘要轉述，UNVERIFIED 原句）。

### 4. PagerDuty SRE Agent（Paige）
- 連結：工程文章 https://www.pagerduty.com/eng/inside-pagerdutys-sre-agent-how-we-built-deep-incident-investigation/ （OPENED，2026-06-24）；產品更新 https://www.pagerduty.com/blog/ai/sre-agent-enhancements-faster-triage-greater-access-controls-deeper-system-connectivity/ （OPENED，2026-08-05）
- 架構：v1 是單一大 context agent → context rot、instruction overload → 改為 **coordinator 依每個候選根因 spawn 一個 subagent**，每個只拿必要 context，平行跑，fan-out + 並行 fan-in（結果到一個處理一個，使用者可中途插話）。**明確試過 LangChain Deep Agents 與 LangGraph，因 superstep 模型會讓 orchestrator 卡到整批平行完成而放棄**，自寫 reactive loop（asyncio.Queue mailbox、resume lock、使用者輸入優先的 priority queue）；supervisor 可 checkpoint、subagent 無狀態、死了就重 spawn。教訓："Build the hard version to understand the problem; ship the simple one."
- 知識：Incident Context document（alerts、相關歷史事件、change events、runbook 內容、notes）+ service topology/dependency graph + 跨事件 memory。Skills（Early Access）。
- 工具：Connectors 經 "MCP or API" 接 Grafana、New Relic、Datadog；另有 Confluence、GitHub。
- 安全：team-level 權限控管 AI 使用；responder 在執行前審閱 agent 推薦的 workflow。完整 approval 矩陣文章未寫。

### 5. incident.io AI SRE / Investigations（Nexus）
- 連結：https://incident.io/blog/introducing-investigations-powered-by-nexus （OPENED，2026-08-05）；技術細節來自 ZenML 對其演講的摘要 https://www.zenml.io/llmops-database/ai-powered-incident-response-system-with-multi-agent-investigation （OPENED，二手；原演講 https://www.youtube.com/watch?v=NeOpqXwh9mk 未開）
- 架構：每個 incident 自動生一個 investigation，作為 ambient agent 持續監看 Slack 與系統變化；工作切成平行/序列的 "checks"；先 gate 到 context 足夠才搜 code changes、歷史事件、Slack、observability；假設產生 → 自我批判；**假設檢驗問題各 spawn 專門 subagent 回報主推理迴圈**（二手來源）。
- 知識：Nexus = 組織系統、流程、失敗模式、修復歷史的知識層。檢索從純向量轉為**以 Postgres 摘要 + keyword tags 為主、embedding 為輔、LLM batch rerank**，理由之一是可除錯性（二手）。
- 工具：產品文對外提供 MCP 給 coding agents；內部接法未寫。
- 安全/評估：明確 checkpoint 對抗 positivity bias；"time travel" eval（事件結案後有 ground truth，自動 grader + component grader）（二手）。Approval 未寫。

### 6. Google Cloud Gemini Cloud Assist Investigations
- 連結：https://docs.cloud.google.com/cloud-assist/investigations （OPENED，Preview；2026-04-10 起限 Premium Support）
- 架構：輸出為 Observations（logs/config/metrics，排序、附來源連結）→ Hypotheses（不確定時多個並列）→ 建議步驟；可 revision 深挖、轉 support case。內部 agent 結構未公開。
- 知識："procedural runbooks, broad signal analysis, or tools"。
- 安全：以執行者身分的權限跑；OAuth token "is never used for mutating data"——**唯讀、只建議**。MCP 未提。

### 7. Rootly AI SRE
- 連結：https://rootly.com/ai-sre-guide/architecture （OPENED，2026-07-24）
- 架構（參考架構文，非產品內部）：context builder（telemetry、changes、topology、ownership、runbooks、incident history）→ reasoning layer 測競爭假設 → **policy gateway** → deterministic workflow 執行 → 用獨立訊號 verify。"The model proposes actions. Identity, policy, approvals, and workflow systems decide what happens next." "An AI SRE agent should never turn its own recommendation directly into a production command."
- 知識：依資料型態選檢索：telemetry 用時間範圍查詢、changes 精確查詢、dependencies 圖遍歷、runbooks 文件搜尋；檢索文字以「evidence + 來源 + 信任等級」進推理層。
- 自治分三級：Read-only investigator → Assisted operator（逐動作 policy + 人工核准 + 短效 scoped credential + verify）→ Narrow autonomy（已知故障模式的預核准修復 + canary + 自動 rollback）。"Earn autonomy per workflow and failure mode."
- MCP：本文未提；Rootly MCP server 2026-03-12 GA、之後推 CLI 稱比 MCP 省 token — UNVERIFIED（搜尋摘要）。

### 8. Traversal
- 連結：https://www.traversal.com/blog/why-an-ai-sre-that-requires-thousands-of-markdown-files-isnt-a-real-ai-sre （OPENED，無日期）；https://www.traversal.com/blog/sre-claude-code-moment （OPENED，約 2026-07）
- 架構：Agentless capture → Causal Indexer → **Production World Model**（持續更新的因果模型）→ Causal Search Engine（跨 10+ dependency hops）；Knowledge Bank 以既有 runbook/postmortem 起步再自動擴充。"orchestrator spawns a swarm of agents in parallel" 來自 AI Engineer 2025 演講摘要 — UNVERIFIED。
- 立場（反例觀點）：批評「需要上千份 markdown 檔的 AI SRE」——runbook 會過期、tribal knowledge 寫不下來；主張系統應自己建環境理解。MCP 只當對外介面。Approval 未提。

### 9. Resolve AI
- 連結：https://resolve.ai/blog/knowledge-graph-agentic-ai-incident-response （OPENED，無日期）
- 架構：自動建/維護的**知識圖譜**（服務、依賴、logs/metrics 位置；廠商稱企業環境可達 50,000 nodes / 500,000 edges），用自家 DSL "Gragg" 安全查圖，事件時遍歷依賴找根因。「多個專門、可組合 agent」的說法來自搜尋摘要 — UNVERIFIED。Approval 未提。

### 10. Cleric
- 全部 UNVERIFIED（只看到 LangChain case study / ZenML 摘要的搜尋片段）：平行調查、先產生多個假設、知識圖譜、跨 session 學習。

---

### 二、開源 / 參考實作

### 11. HolmesGPT（Robusta → CNCF Sandbox，2025-10）
- 連結：https://github.com/HolmesGPT/holmesgpt （OPENED）；https://www.cncf.io/blog/2026/01/07/holmesgpt-agentic-troubleshooting-built-for-the-cloud-native-era/ （OPENED，2026-01-07）
- 架構：**單一 agentic loop**——"actively decides what data to fetch, runs targeted queries, and iteratively refines its hypotheses"；未提 subagent。
- 知識：runbooks（CLI `-r` 指定或寫進 config — 此細節來自搜尋摘要；CNCF 文說 runbook 用來 "Encode operational expertise for others to reuse"）；Confluence/Slab 等作為 runbook 資料源。
- 工具：**toolsets**（YAML 包裝指令，如模板化 `kubectl get pod`）+ 大量 MCP 整合（AWS、Azure、GCP、GitHub、Sentry、Splunk…）。
- 安全："By design, HolmesGPT has read-only access and respects RBAC permissions."；但 README 同時列出 Kubernetes Remediation (MCP) 可 scaling/rollback、GitHub 可開 PR——唯讀是預設核心，寫入透過可選 MCP 擴充（README 未說明如何調和）。
- Evals：pytest-based eval 套件（CNCF 文 / 搜尋摘要）。

### 12. k8sgpt
- 連結：https://github.com/k8sgpt-ai/k8sgpt （OPENED）
- 架構：**確定性 analyzers 先跑**（"SRE experience codified into its analyzers"），LLM 只在 `--explain` 時解釋結果——不是 agent loop，是「規則掃描 + LLM 解說」。另提供 MCP server（`k8sgpt serve --mcp`，stdio/HTTP，README 列 12 tools）讓外部 agent 呼叫；operator 做持續監控。auto-remediation：README 未描述（第三方說法互相矛盾，UNVERIFIED）。

### 13. Anthropic Claude Agent SDK cookbook — The Site Reliability Agent
- 連結：https://platform.claude.com/cookbook/claude-agent-sdk-03-the-site-reliability-agent （OPENED，2026-02-16）
- 架構：**單一 agent**（`query()` loop），**MCP server 跑在獨立 subprocess（stdio）**以隔離 tool crash；12 個 tools 分 Prometheus / Infrastructure / Diagnostics / Documentation。"Tool descriptions drove tool selection."；system prompt 刻意短。
- 知識：runbook 寫成 `SKILL.md`（觸發條件如 `db_connections_active > 90`，workflow 先 `execute_runbook(phase="investigate")` 再 `remediate`，"Present remediation options before taking action"）——頁面註明 skills 設定片段為示意。
- 安全：寫入走**窄 MCP tool + handler 內建檢查**（只能改 `config/`、shell 只允許 docker/docker-compose、container allowlist）："through narrow MCP tools with built-in safety checks, not through broad shell access"；`PreToolUse` hooks 驗證參數範圍；investigate / remediate 分兩個 prompt 階段（但這個分隔靠 prompt，不是撤掉寫入工具——生產環境應改成工具層強制）。

### 14. Anthropic cookbook — SRE incident responder with Claude Managed Agents
- 連結：https://platform.claude.com/cookbook/managed-agents-sre-incident-responder （OPENED，2026-04-10）
- 架構：單一 agent、每個 incident 一個 session；PagerDuty webhook → session。
- 知識：runbook 規範放在 **Skill**（progressive disclosure：先看一行 description，相關才讀本文），runbook 依 failure signature 組織（`oom.md`、`5xx.md`、`latency.md`）；"Do not patch live resources directly"，修改一律開 PR 並引用 runbook。
- 工具：內建 sandbox toolset（bash/read/grep/edit）+ custom tools（open_pull_request、request_approval、merge_pull_request）；生產可換 GitHub MCP。
- 安全：**approval 是一個 custom tool**——agent 呼叫 `request_approval` 後 session 進 `requires_action` idle，由應用程式回傳人類決策；sandbox networking `limited`；所有步驟成為可稽核 session events。

### 15. AWS tools-for-devops-agent（官方社群 skills / MCP repo）
- 連結：在 AWS Skills 文件內引用 https://github.com/aws/tools-for-devops-agent （repo 本身未開，存在性由 OPENED 的 AWS 文件佐證）。內容：AWS Health、VPC DNS、MSK、EKS/RDS operational review 等 skills + custom agents + MCP servers。

### 16. 社群 "SRE skills" repos
- greyhaven-ai/claude-code-config、davila7/claude-code-templates、jeffallan/claude-skills 等有 incident-response / sre-engineer SKILL.md — 全部 UNVERIFIED（只看到 skills 聚合站搜尋結果，star 數不引用）。

---

### 三、跨來源的工程教訓（只列 OPENED 來源中明確出現者）

1. **單一大 context agent 會劣化** → 依假設開小 context subagent（PagerDuty、Azure 工程文）。
2. **subagent 依假設切而非依資料源切**：PagerDuty "one sub-agent per candidate root cause"；Azure "stops one hypothesis from biasing another"；incident.io 每個檢驗問題一個 subagent（二手）。
3. **少一點預先寫死的鷹架**：Azure 移除 hand-built subagents / pre-written queries 後表現更好；Anthropic cookbook 也主張短 prompt、靠 tool description。反方：AWS 仍用固定階段 agent type；Rootly 主張執行層要 deterministic workflow。兩者不矛盾——**調查要開放、執行要確定**。
4. **Runbook → Skills 是明確趨勢**：AWS 把 Runbooks 自動遷移成 Skills；Azure、PagerDuty、Anthropic 都有 Skills；反方 Traversal 認為依賴人工 markdown 不可持續，要自動建 world model/知識圖譜。
5. **知識圖譜/拓撲是一等公民**：AWS Topology Graph（也用於 blast radius）、Resolve KG、Traversal World Model、PagerDuty dependency graph、Rootly 用圖遍歷查 dependency。
6. **純向量 RAG 不是主力**：Azure 用可瀏覽 markdown 取代 RAG；incident.io 改 tags + Postgres + rerank（二手）；Rootly 依資料型態選檢索方式。
7. **唯讀預設、寫入要閘門**：HolmesGPT、Gemini Cloud Assist、AWS DevOps Agent（不執行 remediation）預設唯讀；Azure Review mode + tool allow/ask/deny + hooks；Datadog Guardrails；Rootly policy gateway + 短效憑證 + verify + rollback；Anthropic 窄工具 + PreToolUse hook + approval tool。
8. **Permission ≠ approval**：Azure 明確分開 RBAC 與 run mode；Rootly 分 evidence / inference / authorization / execution / verification。
9. **Evals 用歷史事件回放**：Datadog（標註事件 + 封存 telemetry + LLM judge）、incident.io "time travel"（二手）、HolmesGPT pytest evals。
10. **框架選擇**：PagerDuty 明確因 LangGraph superstep 阻塞而改自寫 reactive loop——對以 LangGraph 為教學框架的課程是值得點出的實務 trade-off。

---

### 四、綜合判斷

**問題：2026 常見模式是「one investigation agent + tools/MCP + runbooks as skills + 可選平行假設 subagent + approval gates」，還是「supervisor 路由到固定 specialist agents」？**

答：**前者是主流**，但要加兩個修正：

- 支持前者：Datadog（單 agent 假設樹）、HolmesGPT（單 loop + toolsets/MCP + runbooks + 唯讀）、Anthropic 兩個 cookbook（單 agent + MCP/skills + hooks/approval tool）、PagerDuty（coordinator + 每假設一個動態 subagent）、Azure 工程文（generalist + 平行 subagent）、incident.io（主推理迴圈 + 問題級 subagent，二手）。
- 例外 / 部分支持後者：
  - **AWS DevOps Agent**：固定 agent types（Triage / RCA / Mitigation / Evaluation…），是**按生命週期階段**的 specialist pipeline，不是按資料源；RCA 內部仍是多假設並行。
  - **Azure SRE Agent 產品面**：有 orchestrator 依 `handoff_description` 交給 custom agent（DB Expert、Network Expert）與 handoff chain——這最像「supervisor → specialist」，但它是可選擴充，官方表格說唯讀查詢主 agent 自己做即可，工程文章更明說 generalist 勝過 bespoke specialist。
  - **k8sgpt**：根本不是 agent loop，是確定性 analyzers + LLM 解說。
  - **Traversal / Resolve**：重心在自動建的因果模型/知識圖譜，反對以人工 markdown runbook 為核心。

**對本課程 Supervisor → DocAgent / DBAgent / OpsAgent 的含意**（調研者意見）：
1. 「依資料源切 specialist」在一手來源裡幾乎找不到；真實系統切法是**依假設**（調查期）或**依階段**（triage / RCA / mitigation）。
2. Doc/DB/Ops 比較像 **tool groups / MCP servers / skills**，而不是 agent。
3. OpsAgent 的寫入要放在**確定性 workflow + approval node + 窄工具**（對應 LangGraph `interrupt()` + checkpointer），這點與 AGENTS.md 的 deterministic state transition 規則一致，也與 Rootly / Azure / Anthropic 的做法一致。
4. 若保留 Supervisor 作教學鷹架，建議明說它是「教學用的顯式路由」，並加一個進階版：Investigator（假設迴圈）→ fan-out 每假設 subagent → Approval gate → Ops workflow → Verify。同時可引 PagerDuty 的 LangGraph superstep 教訓作為框架取捨討論。

會改變結論的未知：Cleric、Resolve 的多 agent 細節、incident.io 的一手技術文件都沒能打開；若它們公開的是固定 specialist 路由，主流判斷的比例會變，但不會推翻「依假設切 subagent + approval gate」在一手來源中佔多數。
