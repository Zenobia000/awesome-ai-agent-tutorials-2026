# 模組五 素材地圖

> 對象：懂深度學習（神經網路、softmax、反向傳播、embedding、遷移學習），沒碰過 NLP／生成式 AI／Agent／LangChain。
> 所有 URL 均於 2026-11-12 以 WebFetch 實際開啟核實；版本與 API 事實另以 PyPI、GitHub API、套件 wheel 原始碼交叉確認。
> 注意：WebFetch 只讀得到文字與圖說，讀不到圖片像素。下方「可借的圖解結構」是依原文的段落結構、圖說（caption/alt）與流程文字整理出來的重畫藍圖，不是逐筆描述原圖。

## 論點清單

1. **Tool calling 不是模型去執行函式，而是模型「生成一段符合 JSON schema 的 token」**；你的程式解析它、真的去執行，再把結果當成一則新訊息塞回對話。看懂這三則訊息（assistant 的 tool call → tool result → assistant 的最終回答），agent 就沒有魔法了。
2. **Agent = LLM + 工具 + 記憶 + 迴圈**，四要素用 50 行就寫得完；ReAct 是 Thought → Action → Observation 的迴圈格式。但**先問該不該用 agent**：步驟可預測就用 workflow（寫死的程式路徑），步驟數不可預測才讓 LLM 自己決定流程。
3. **LangGraph 的 StateGraph = 把那個 while 迴圈畫成顯式的狀態機**：State（共享的資料結構）、Node（讀 state、回傳更新的函式）、Edge／Conditional Edge（下一步去哪）、Reducer（多個更新怎麼合併：覆蓋還是追加）。`recursion_limit` 是迴圈的保險絲，但現在的預設值很大，不能指望它自動擋住死循環。
4. **Checkpointer 讓圖在每一步存檔**，於是同一個機制同時撐起三件事：跨回合記憶（thread）、時光旅行（從舊存檔分岔）、人在回路（`interrupt()` 暫停 → `Command(resume=...)` 恢復）。
5. **多智能體的核心是 context engineering（決定每個 agent 看到什麼）**：Supervisor 把子 agent 包成工具來呼叫，子 agent 在乾淨的 context 裡做完、只回傳摘要。代價是 token 成本暴增，只適合可平行、資訊量超過單一 context 的任務。
6. **長任務的答案不是「做更多專用 agent」，而是「通用 agent + 外掛能力」**：Deep Agents 用規劃清單＋子 agent＋虛擬檔案系統撐住長流程；Anthropic Agent Skills 用「漸進式揭露」讓一個通用 agent 按需載入專業流程，避免「智能體動物園」。

## 素材

### 論點 1：Tool calling 的真實長相

- **Tool use（Transformers 文件 chat_extras）** — Hugging Face 官方文件 — https://huggingface.co/docs/transformers/main/en/chat_extras （已核實 2026-11-12）
  - 適合程度：**這群學生最該看的第一份**。它用開源模型（Hermes-2-Pro-Llama-3-8B）+ `apply_chat_template(messages, tools=tools)` + `model.generate()` 示範，學生看到的是 tokenizer、generate、decode——全是 DL 熟悉的東西。輸出直接印出 `<tool_call>{"name": "get_current_temperature", "arguments": {...}}</tool_call>`，一眼看穿「工具呼叫就是模型生成的一段文字」。文中明講「A model cannot actually call the tool itself」。
  - 可借的圖解結構：四格縱向管線——(1) Python 函式 + Google-style docstring → `get_json_schema` 轉成 JSON schema；(2) chat template 把 schema 與對話渲染成一長串 token 餵進模型；(3) 模型 generate 出 `<tool_call>…</tool_call>` token；(4) 你的程式執行函式，把結果以 `{"role": "tool", "content": "22"}` 追加到 messages，再跑一次 generate。每格旁邊標「誰在做事：模型 / 你的程式」。
  - 搭橋：模型最後一層仍是「詞表上的 softmax」，tool call 只是它被微調（遷移學習）成會輸出某種特定格式的 token 序列；就像分類器只輸出 label，**真正「採取行動」的是讀 label 的那段程式**。docstring 的品質直接決定模型能不能選對工具——等於「標籤說明寫錯，模型就學錯」。
- **Tool use with Claude（Overview / How tool use works）** — Anthropic 官方文件 — https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview （已核實 2026-11-12；舊網址 docs.anthropic.com/… 會 301 轉到此）
  - 適合程度：有完整的一來一回範例：第一次請求帶 `tools`（name / description / input_schema）→ 回應 `stop_reason: "tool_use"` 與 `tool_use` block（`id`、`name`、`input`）→ 第二次請求帶 `tool_result` block（`tool_use_id` 對應）→ 最終文字回答。並區分 client tools（你執行）與 server tools（Anthropic 執行），也說明工具定義本身會吃 input token。
  - 可借的圖解結構：泳道圖（sequence diagram），兩條泳道「你的程式」「LLM API」，四支箭頭：①請求（user 訊息＋工具清單）②回應（tool_use，id=toolu_…）③請求（追加 assistant 原訊息＋tool_result，tool_use_id=toolu_…）④回應（文字）。用同一色標出 id 的配對關係。
  - 搭橋：API 是無狀態的，每次都要把「完整歷史」重新送進去——就像 RNN 推論時你得自己把 hidden state 帶到下一步。
- **Function calling** — OpenAI 官方指南 — https://developers.openai.com/api/docs/guides/function-calling （已核實 2026-11-12；舊網址 platform.openai.com/docs/guides/function-calling 會 301 轉到此）
  - 適合程度：五步驟流程寫得非常乾淨（送工具 → 收到 tool call → 執行 → 帶結果再送 → 收到答案或更多 tool call），並特別提醒 `arguments` 是 **JSON 字串**，要 `json.loads`。
  - 可借的圖解結構：五步驟環狀圖，步驟 3–4 畫成可重複的小迴圈（「可以重複多次」），這個小迴圈就是下一個論點的 agent loop 雛形。
  - 搭橋：同上；另可點出「模型輸出是字串、要 parse、可能 parse 失敗」→ 呼應 Module 2 的結構化輸出與錯誤處理。
  - 注意：此頁主推 Responses API（`function_call` / `function_call_output` + `call_id`）。課綱 Lab 5-A 用的「OpenAI 相容 SDK」多半是 Chat Completions 格式（`message.tool_calls[].function.arguments` + `role: "tool"` + `tool_call_id`），vLLM 文件 https://docs.vllm.ai/en/latest/features/tool_calling.html （已核實 2026-11-12）就是這個格式。投影片要選定一種格式講到底，別混用。

### 論點 2：Agent 四要素、ReAct、手寫迴圈、workflow vs agent

- **How to Build an Agent（or: The Emperor Has No Clothes）** — Thorsten Ball（Amp），2025-04-15 — https://ampcode.com/how-to-build-an-agent （已核實 2026-11-12）
  - 適合程度：核心主張一句話：agent 就是「an LLM, a loop, and enough tokens」，不到 400 行（多為樣板）。逐步從聊天迴圈 → 假工具 → `read_file` → 工具執行迴圈 → `list_files` → `edit_file` 長出來，正是 Lab 5-A 的敘事節奏。程式是 Go，但每步都有文字解釋，不懂 Go 也看得懂結構。
  - 可借的圖解結構：「逐步長大」的五格演進圖：第 1 格只有 user ↔ LLM 的聊天迴圈；第 2 格在迴圈裡插入「回應裡有 tool_use 嗎？」菱形判斷；第 3–5 格依次往工具箱加 read_file / list_files / edit_file。每格標程式行數增量，強化「agent 很小」的印象。
  - 搭橋：迴圈＝訓練迴圈的 `for step in range(...)`；messages 清單＝在迴圈中累積的狀態。
- **LLM Powered Autonomous Agents** — Lilian Weng（Lil'Log），2023-06-23 — https://lilianweng.github.io/posts/2023-06-23-agent/ （已核實 2026-11-12）
  - 適合程度：Agent 領域最常被引用的入門綜述。LLM 當大腦，三個元件 Planning / Memory / Tool Use。ReAct 放在 Planning 的 Self-Reflection 小節。**對 DL 學生最有價值的是記憶分類**：把人類的感官記憶、短期記憶、長期記憶分別對應到 embedding 表示、in-context learning、外部向量資料庫。
  - 可借的圖解結構：(a) 中心放「LLM（大腦）」，三條輻射線連到 Planning（子目標拆解、反思）、Memory（短期／長期）、Tools（API、搜尋、程式執行），右側一個 Action 方塊——這就是課綱的「四要素」圖，把第四要素「迴圈」畫成 Action 回到 LLM 的回饋箭頭。(b) 記憶對照表三列：人類記憶 → 機器對應 → 本課哪個模組（短期＝messages/checkpointer，長期＝RAG/向量庫，模組三）。
  - 搭橋：「感官記憶 ≈ embedding」直接接學生熟悉的 embedding 層；「長期記憶 ≈ 向量庫 + 最近鄰搜尋」接 Module 3。
- **A Visual Guide to LLM Agents** — Maarten Grootendorst，2025-03-17 — https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-llm-agents （已核實 2026-11-12，全文免費可讀）
  - 適合程度：整篇以插圖為主、文字為輔，正是「有圖解、給入門者」的典型。從 Augmented LLM（計算機例子）→ 短期／長期記憶 → function calling（模型生成 JSON）→ ReAct → Reflexion → 多智能體，順序和本模組幾乎一致。
  - 可借的圖解結構：ReAct 迴圈圖：一個循環三站「Thought（我要查什麼）→ Action（呼叫 search 工具）→ Observation（工具回傳）」再回到 Thought，直到出現「Final Answer」出口。短期記憶圖：context window 畫成固定長度的格子，舊對話被壓縮成摘要格。
  - 搭橋：context window 是固定長度的輸入張量；超過就得截斷或摘要——跟固定輸入尺寸的 CNN 要 resize/crop 同一個道理。
- **Building effective agents** — Erik Schluntz、Barry Zhang（Anthropic），2024-12-19 — https://www.anthropic.com/engineering/building-effective-agents （已核實 2026-11-12；頁面自註部分工具描述已過時，但概念部分仍是業界標準說法）
  - 適合程度：workflow vs agent 的定義來源：workflow 是「LLM 與工具透過預先定義的程式路徑編排」，agent 是「LLM 動態主導自己的流程與工具使用」。核心建議：先找最簡單的方案，必要時才增加複雜度。
  - 可借的圖解結構：七張遞進小圖排成一頁「光譜」：最左 Augmented LLM（LLM 方塊外掛 retrieval / tools / memory 三個小方塊）→ Prompt chaining（串列方塊，中間插 Gate 檢查點）→ Routing（一進多出的分類器）→ Parallelization（扇出再彙總）→ Orchestrator-workers（中央 LLM 動態派工）→ Evaluator-optimizer（生成器與評審器兩方塊互相回饋）→ 最右 Autonomous agent（LLM ↔ 環境的閉環）。橫軸標「可預測性 高 → 低」「成本/延遲 低 → 高」。
  - 搭橋：workflow ≈ 靜態計算圖（每次 forward 走固定路徑），agent ≈ 動態控制流（PyTorch eager 模式下由資料決定 if/while 走向）。Routing ≈ Mixture-of-Experts 的 gating network。
- **Workflows and agents** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/workflows-agents （已核實 2026-11-12）
  - 適合程度：把上一篇的六種模式逐一配上 LangGraph 程式碼與 mermaid 圖（`draw_mermaid_png()`），是「從概念到 LangGraph」最順的橋。
  - 可借的圖解結構：同一頁左「概念圖」右「LangGraph 節點圖」對照，讓學生看到每種模式都只是 node + edge 的不同接法——順勢帶入論點 3。
  - 搭橋：同上。
- **Agents（AI Engineering 第六章改寫）** — Chip Huyen，2025-01-07 — https://huyenchip.com/2025/01/07/agents.html （已核實 2026-11-12）
  - 適合程度：工具三分類（知識擴充／能力擴充／寫入動作）對「為什麼要 HITL」是很好的鋪陳：寫入動作（寄信、轉帳）才需要人把關。也講失敗模式（選錯工具、參數錯、誤報完成、步驟太多）。
  - 可借的圖解結構：Figure 6-9 的「計畫 → 驗證 → 執行」三段分離圖（只有驗證過的計畫才執行），以及 Figure 6-11 的四種控制流（循序／平行／if／for）——後者可直接當 LangGraph edge 種類的預告。
  - 搭橋：「錯誤會逐步累積（compound）」＝序列模型 exposure bias／誤差累積。
- **ReAct Prompting** — Prompting Guide（DAIR.AI）— https://www.promptingguide.ai/techniques/react （已核實 2026-11-12）
  - 適合程度：用 HotpotQA 的實際 Thought/Action/Observation 逐步軌跡示範，適合貼一段真實 trace 到投影片上。
  - 可借的圖解結構：把一條 ReAct 軌跡畫成「對話氣泡 + 工具卡片」交錯的時間軸。
  - 搭橋：與 Chain-of-Thought 對比：CoT 只在腦中推理（封閉系統），ReAct 會跟環境互動取得新觀測（像 RL 的 agent–environment loop）。

### 論點 3：StateGraph（state / node / conditional edge / reducer）與 recursion_limit

- **Graph API overview** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/graph-api （已核實 2026-11-12）
  - 適合程度：定義最權威。明講「預設 reducer 用右值覆蓋左值」、`Annotated[list[str], operator.add]` 改為追加、`messages` 應用 `add_messages`（因為 `operator.add` 只能追加、不能就地更新同 id 訊息）；`add_conditional_edges` 的路由函式讀當前 state 回傳節點名；`Command(update=..., goto=...)` 一步同時更新狀態與路由；執行以 super-step 為單位，平行節點共用一個 super-step。
  - 可借的圖解結構：(a) 「State 是一張白板」圖：中央一個 TypedDict 方塊（messages, foo, bar），三個 node 箭頭讀白板、回傳「部分更新」，箭頭進白板時經過一個標著 reducer 的閘門（foo：覆蓋；bar：+=）。(b) super-step 時間軸：兩個平行 node 在同一格，循序 node 各占一格；平行兩格同時寫 `bar` 時，沒 reducer 就只剩一個值（課綱「並發覆蓋」踩坑的視覺化）。
  - 搭橋：State ≈ 在網路中流動的 tensor；Node ≈ layer（輸入 state、輸出更新）；**Reducer ≈ 梯度累加：`.grad` 預設是累加（`+=`）而不是覆蓋**，所以 PyTorch 每步要 `zero_grad()`；LangGraph 剛好相反，預設覆蓋、要累加得明講。Conditional edge ≈ early-exit 網路或 MoE 的路由。
- **Thinking in LangGraph** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph （已核實 2026-11-12）
  - 適合程度：用「客服信件 agent」走完五步設計法（拆步驟 → 判斷每步類型 → 設計 state → 寫 node → 接線），適合當 Lab 5-B 前的設計練習。
  - 可借的圖解結構：START → classify → draft → (human review | send) → END；實線＝固定 edge，虛線＝node 內以 `Command` 在執行期決定的路線。直接沿用「實線/虛線」圖例區分靜態與動態路由。
  - 搭橋：先畫計算圖再寫 `forward()`——跟設計網路架構圖再實作同一個習慣。
- **AI Agents in LangGraph** — DeepLearning.AI 短課程（Harrison Chase、Rotem Weiss）— https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/ （已核實 2026-11-12；可免費旁聽，評量需 Pro）
  - 適合程度：1 小時 47 分，第 2 課「Build an Agent from Scratch」先手寫、第 3 課再用 LangGraph 重寫，和本模組「先手寫、再上框架」同構；後面還有 Persistence and Streaming、Human in the Loop。影片節奏適合學生課前預習。
  - 可借的圖解結構：「手寫版 ↔ LangGraph 版」左右對照：左邊 while 迴圈的每一段程式碼，用色塊對應到右邊的 node / edge。
  - 搭橋：手寫訓練迴圈 → 換成 PyTorch Lightning 的 `training_step`；框架只是把你本來就在寫的迴圈結構化。
  - 注意：課程錄製於 LangGraph 1.0 之前，個別 import 路徑可能已變，講概念可、照抄程式碼不行。
- **Introduction to LangGraph** — LangChain Academy — https://academy.langchain.com/courses/intro-to-langgraph （已核實 2026-11-12；免費，約 6 小時影片，報名需註冊帳號）
  - 適合程度：官方完整課程，Module 1 Introduction → 2 State and Memory → 3 UX and Human-in-the-Loop → 4 Building Your Assistant → 5 Long-Term Memory → 6 Deployment，可作為學生課後延伸。
  - 可借的圖解結構：課程目錄本身就是本模組論點 3–4 的順序，可直接借它的章節切法安排投影片段落。
  - 搭橋：—
  - 注意：頁面未標明 LangGraph 版本，不保證符合 1.x API。

### 論點 4：Checkpointer → 記憶、時光旅行、人在回路

- **Persistence** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/persistence （已核實 2026-11-12）
  - 適合程度：說明 checkpointer 以 thread 為單位存 checkpoint，config 帶 `{"configurable": {"thread_id": ...}}`；`InMemorySaver` 與 `PostgresSaver` 的 import 路徑，`PostgresSaver` 首次要 `checkpointer.setup()` 建表。
  - 可借的圖解結構：橫向時間軸，每個 super-step 結束掉下一顆「存檔點」膠囊（checkpoint 1, 2, 3…），整條軸標 `thread_id = "user-42"`；另起一條軸是另一個 thread，彼此獨立。下方畫兩種儲存後端：記憶體（程式結束就消失）vs Postgres（重啟仍在）。
  - 搭橋：**`torch.save(model.state_dict())` 每個 epoch 存一次 checkpoint，訓練中斷可以從最後一個 checkpoint 接著跑**——一模一樣的概念，只是存的是「圖的 state」而不是權重。thread ≈ 不同的實驗 run。
- **Memory（Add memory）** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/add-memory （已核實 2026-11-12）
  - 適合程度：短期記憶（checkpointer，綁 thread）vs 長期記憶（store，跨 thread）的分工講得清楚，並給 `pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres` 與 `PostgresSaver.from_conn_string(...)` 完整範例。
  - 可借的圖解結構：兩層方塊：上層「Store（使用者偏好、跨對話事實）」被多個 thread 共用；下層每個 thread 自己一條 checkpoint 鏈。
  - 搭橋：短期 ≈ RNN 的 hidden state（單一序列內）；長期 ≈ 外部記憶體／向量庫（跨序列）。
- **Time travel** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/use-time-travel （已核實 2026-11-12）
  - 適合程度：四步驟具體可教：`get_state_history(config)`（新到舊）→ 挑 `s.next == ("write_joke",)` 的 checkpoint → `update_state(cfg, values={...})` 產生分岔 → `invoke(None, fork_config)` 從分岔點續跑。明講 **update_state 不是回滾，原歷史保留**；並區分 Replay（不改 state 重跑，但下游 LLM 呼叫可能給出不同結果）與 Fork（改 state 再跑）。
  - 可借的圖解結構：git 分支圖：主幹 c1 → c2 → c3 → c4；從 c2 拉出一條分支 c2' → c3' → c4'（標 topic="chickens"），主幹保持原樣。Replay 畫成從 c2 再走一次同一路徑但虛線。
  - 搭橋：從第 5 個 epoch 的 checkpoint 載入、改學習率、開一條新的實驗分支——學生做過超參數調整就懂。
- **Interrupts** — LangGraph 官方文件 — https://docs.langchain.com/oss/python/langgraph/interrupts （已核實 2026-11-12）
  - 適合程度：`from langgraph.types import interrupt, Command`；在 node 內 `approved = interrupt("Do you approve?")` 暫停；以同一 `thread_id` 呼叫 `Command(resume=True)` 恢復，resume 的值就是 `interrupt()` 的回傳值。列出六條規則，其中兩條是學生必踩坑：**恢復時整個 node 從頭重跑**（interrupt 之前的副作用會再發生一次）、**不能用裸 `try/except` 包住 interrupt**（它靠拋例外實作）。
  - 可借的圖解結構：三格時序：①node 執行到 interrupt → 存檔 → 回傳 `__interrupt__` 給呼叫端（畫成暫停鍵）；②人類在 UI 看到待審內容；③呼叫端送 `Command(resume=...)` → 從存檔讀回 → node「從頭」重跑，這次 `interrupt()` 直接回傳人類給的值。第③格特別用紅框標「node 從頭重跑」。
  - 搭橋：除錯器的 breakpoint（pdb）+ 從 checkpoint 重啟；或「generator 的 yield / send」。
- **Human-in-the-loop（LangChain 高階版）** — LangChain 官方文件 — https://docs.langchain.com/oss/python/langchain/human-in-the-loop （已核實 2026-11-12）
  - 適合程度：`HumanInTheLoopMiddleware(interrupt_on={"execute_sql": {"allowed_decisions": ["approve", "reject"]}})`，決策有 approve / edit / reject / respond 四種，恢復用 `Command(resume={"decisions": [...]})`。這正是 Lab 5-B「SQL 審批」的現成寫法。
  - 可借的圖解結構：agent 迴圈圖中，在「model → tools」的箭頭上插一個收費站：approve 放行、edit 改參數放行、reject 把拒絕訊息回送 model。
  - 搭橋：同上。課堂可先用 `interrupt()` 手刻一次，再展示 middleware 一行搞定，對比底層 vs 高階 API。

### 論點 5：多智能體＝context engineering；Supervisor 與子 agent 包成工具

- **Multi-agent** — LangChain 官方文件 — https://docs.langchain.com/oss/python/langchain/multi-agent （已核實 2026-11-12）
  - 適合程度：列出五種模式（Subagents、Handoffs、Skills、Router、Custom workflow），並一句話點出主軸：「At the center of multi-agent design is context engineering—deciding what information each agent sees.」說明 subagents 模式中子 agent 無狀態、每次呼叫都從乾淨 context 開始。
  - 可借的圖解結構：四格分頁圖（Subagents / Handoffs / Skills / Router）。Subagents 格：主 agent 在中間，子 agent 以「工具」形狀掛在旁邊，箭頭是「請求字串進、摘要字串出」。
  - 搭橋：MoE：router/gating 決定哪個 expert 處理；context 隔離 ≈ 每個 expert 只看到自己那份輸入。
- **Build a supervisor agent（Supervisor 教學）** — LangChain 官方文件 — https://docs.langchain.com/oss/python/langchain/supervisor （已核實 2026-11-12）
  - 適合程度：**和 Lab 5-C 幾乎一模一樣**：Calendar agent（`get_available_time_slots`、`create_calendar_event`）+ Email agent（`send_email`），各用 `create_agent` 建；以 `@tool` 包成 `schedule_event`、`manage_email`，內部 `calendar_agent.invoke(...)` 後只回傳 `result["messages"][-1].text`；子 agent 掛 `HumanInTheLoopMiddleware`，只有頂層 supervisor 掛 checkpointer。
  - 可借的圖解結構：三層樹：使用者 → Supervisor（工具：schedule_event、manage_email）→ 兩個子 agent（各自的低階 API 工具）。在 supervisor 與子 agent 之間的箭頭標「只傳一句自然語言請求／只回最後一則訊息」，視覺化「上層看不到下層的細節」。
  - 搭橋：模組化封裝：子網路包成一個 `nn.Module`，外層只看它的 forward 介面。
- **How we built our multi-agent research system** — Anthropic，2025-06-13 — https://www.anthropic.com/engineering/multi-agent-research-system （已核實 2026-11-12）
  - 適合程度：提供「多智能體值不值得」的數據：agent 約用聊天的 4 倍 token、多智能體約 15 倍；BrowseComp 上 token 用量單獨解釋約 80% 的效能差異。明講適合廣度優先、可平行的研究任務，不適合需共享 context 或大多數寫程式任務。
  - 可借的圖解結構：Lead agent 扇出多個平行 subagent（像漏斗的濾網），各自搜尋後回收到 lead，最後經 CitationAgent 再交給使用者；旁邊一條長條圖：聊天 1× / 單 agent 4× / 多 agent 15× token。
  - 搭橋：多智能體 ≈ 用更多算力（更多 token）換表現，跟 scaling law「更多 compute → 更好」同一條邏輯；也是 ensemble/資料平行的直覺。

### 論點 6：Deep Agents 與「通用 Agent + Agent Skills」

- **Deep Agents** — Harrison Chase（LangChain blog），2025-07-30 — https://www.langchain.com/blog/deep-agents （已核實 2026-11-12）
  - 適合程度：定義「淺 agent」（簡單 LLM 呼叫工具迴圈，撐不了長任務）vs「深 agent」四件套：規劃工具（Claude Code 的 todo 清單其實是個 no-op，只是幫模型保持方向）、子 agent、檔案系統、詳細的 system prompt。明講主要靈感來自 Claude Code，也提到 Deep Research、Manus。
  - 可借的圖解結構：中央一個 agent 迴圈，四周四個外掛：左上 Todo 清單（☐☑）、右上子 agent（小 agent 圖示）、左下檔案櫃（虛擬檔案系統）、右下長卷軸（system prompt）。標題「同一個迴圈，加四個外掛就變深」。
  - 搭橋：todo 清單 ≈ 把中間狀態寫到外部（像把 activation 存到 CPU 記憶體的 offloading）；檔案系統 ≈ 外部記憶體。
- **Deep Agents overview** — LangChain 官方文件 — https://docs.langchain.com/oss/python/deepagents/overview （已核實 2026-11-12）
  - 適合程度：`from deepagents import create_deep_agent`；內建檔案工具 ls / read_file / write_file / edit_file（加 glob、grep、delete），`task` 工具產生隔離 context 的子 agent，後端可選 in-memory state、本地磁碟、LangGraph store 等。**v0.7 起規劃（`write_todos`）改為 opt-in**，需加 `TodoListMiddleware`。
  - 可借的圖解結構：分層堆疊圖：底層 LangGraph runtime → 中層 LangChain `create_agent` + middleware → 頂層 deepagents（檔案系統 middleware、子 agent、可選規劃）。讓學生看清三個套件的上下關係。
  - 搭橋：框架堆疊 ≈ CUDA → PyTorch → Lightning/HF Trainer。
- **Effective context engineering for AI agents** — Anthropic，2025-09-29 — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents （已核實 2026-11-12）
  - 適合程度：解釋「為什麼需要子 agent／檔案系統」的理論根據：context rot（token 越多回想越差）、attention budget、compaction（摘要後重開）、structured note-taking（筆記寫到 context 外）、sub-agent（乾淨 context、回傳濃縮摘要）。
  - 可借的圖解結構：一條「system prompt 高度」光譜：左端寫死 if-else 的脆弱提示、右端空泛提示、中間「right altitude」。另畫一個逐漸被填滿的 context 水槽，滿到某線就觸發 compaction。
  - 搭橋：attention 計算量隨序列長度平方成長、長序列注意力被稀釋——學生學過 attention/softmax 就能理解「token 越多，每個 token 分到的注意力越少」。
- **Equipping agents for the real world with Agent Skills** — Barry Zhang、Keith Lazuka、Mahesh Murag（Anthropic），2025-10-16 — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills （已核實 2026-11-12）
  - 適合程度：Skill 是一個資料夾（`SKILL.md` + 腳本 + 參考檔），讓通用 agent 按需變成專家，取代「每個場景做一個專用 agent」。核心設計是三層漸進式揭露：L1 啟動時只載 name/description；L2 判斷相關才讀整份 SKILL.md；L3 需要時才讀附檔（PDF skill 的 reference.md / forms.md）。用「新人入職手冊」比喻。
  - 可借的圖解結構：(a) context window 時序圖：system prompt + 所有 skill 的一行描述 → 使用者訊息 → agent 用 bash 讀 `pdf/SKILL.md` → 再讀 `forms.md` → 完成任務；每讀一層，context 長條就多一段。(b) 「目錄 → 章節 → 附錄」的書本比喻三層塔。
  - 搭橋：**一個通用 backbone + 可插拔的 task head**（遷移學習）；或 LoRA adapter 按任務熱插拔（呼應模組六）。漸進式揭露 ≈ lazy loading。
- **Agent Skills（開放規格站）** — agentskills.io — https://agentskills.io （已核實 2026-11-12）
  - 適合程度：說明 Agent Skills 由 Anthropic 發起、已釋出為開放標準並被多家 agent 產品採用；資料夾結構（SKILL.md / scripts / references / assets）與 Discovery → Activation → Execution 三階段寫得很短很清楚。
  - 可借的圖解結構：資料夾樹狀圖（直接用它的 `my-skill/` 結構）＋三階段箭頭。
  - 搭橋：同上。
- **Agent Skills with Anthropic** — DeepLearning.AI 短課程（Elie Schoppik，Anthropic）— https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic/ （已核實 2026-11-12；2 小時 19 分、初學者等級；頁面未標價，評量與證書屬 Pro）
  - 適合程度：課綱「通用 Agent + Skills」的影片版：Why Use Skills（兩部）→ Skills vs Tools, MCP, and Subagents → 預建 Skills → 自製 Skills → 在 Claude API / Claude Code / Claude Agent SDK 中使用。「Skills vs Tools, MCP, and Subagents」那一課（7 分鐘）正好回答學生最常問的「這跟工具有什麼不同」。
  - 可借的圖解結構：四欄比較表「Tools / MCP / Subagents / Skills」×「它提供什麼（動作／連線／隔離的 context／流程知識）、何時載入、佔多少 context」。（依課程大綱整理，未觀看影片內容）
  - 搭橋：Tools ≈ 可呼叫的函式庫；Skills ≈ 附帶 SOP 的訓練手冊——一個給能力、一個給做法。

## 事實核實

- **LangChain 1.0 是否已正式發布與日期**：是。LangChain 1.0 與 LangGraph 1.0 於 **2025-10-22** 同日發布，承諾「2.0 之前不做破壞性變更」。出處：https://www.langchain.com/blog/langchain-langgraph-1dot0 。截至 2026-11-12，PyPI 最新為 `langchain 1.5.0`（2026-11-11）、`langgraph 1.2.20`（2026-11-05）（https://pypi.org/project/langchain/ 、https://pypi.org/project/langgraph/ ）。**課綱寫「LangChain 1.0」沒錯，但實作時應寫「LangChain 1.x」並鎖定實際版本。**
- **AgentExecutor 狀態**：已移出主套件。`langchain 1.5.0` wheel 中找不到 AgentExecutor；它只存在於舊功能相容套件 `langchain-classic`（`langchain_classic/agents/agent.py`，最新 1.0.8），套件內的棄用訊息為「Use `langchain.agents.create_agent` for new applications」。出處：https://docs.langchain.com/oss/python/releases/langchain-v1 （「Legacy functionality has moved to `langchain-classic`」）＋本次下載 wheel 原始碼確認。**課綱「徹底廢棄 AgentExecutor」方向對；「LangGraph 確立為底層唯一執行中樞」的說法要修正**：正確說法是「`create_agent` 建在 LangGraph runtime 上」，LangChain 1.0 的新主角是 `create_agent` + middleware，課綱完全沒提 middleware。
- **create_agent 的位置**：`from langchain.agents import create_agent`。它取代 `langgraph.prebuilt.create_react_agent`；後者在 `langgraph-prebuilt` 內已標 `@deprecated("create_react_agent has been moved to langchain.agents ...")`。出處：https://docs.langchain.com/oss/python/releases/langchain-v1 、https://docs.langchain.com/oss/python/langchain/agents 。
- **InMemorySaver / PostgresSaver 套件名**：`from langgraph.checkpoint.memory import InMemorySaver`（隨 langgraph 安裝的 `langgraph-checkpoint`，最新 4.3.1）；`from langgraph.checkpoint.postgres import PostgresSaver` 需另裝 `langgraph-checkpoint-postgres`（最新 3.2.0，2026-10-14）並安裝 `psycopg[binary,pool]`，首次使用要呼叫 `checkpointer.setup()`。出處：https://docs.langchain.com/oss/python/langgraph/persistence 、https://docs.langchain.com/oss/python/langgraph/add-memory 。與課綱一致。
- **interrupt() 與 Command(resume=...) 用法**：`from langgraph.types import interrupt, Command`；node 內 `value = interrupt(payload)`，payload 需可 JSON 序列化；圖必須以 checkpointer 編譯，恢復時用**同一個 thread_id** 呼叫 `graph.invoke(Command(resume=...), config)`，resume 值成為 `interrupt()` 回傳值；恢復時 node 從頭重跑。langgraph ≥ 1.2.12 另有 `response_schema` 參數驗證 resume 值。出處：https://docs.langchain.com/oss/python/langgraph/interrupts 。課綱 Lab 5-B 寫「`Command` approve」——正確寫法是 `Command(resume=...)`（例如 `Command(resume={"approved": True})`），沒有 approve 這個參數；若改用 `HumanInTheLoopMiddleware`，則是 `Command(resume={"decisions": [{"type": "approve"}]})`（https://docs.langchain.com/oss/python/langchain/human-in-the-loop ）。
- **recursion_limit 預設值**：**langgraph ≥ 1.1.4 預設 10,007 個 super-step**（1.0.6–1.1.3 為 10,000；1.0.5 以前為 25，已以 langgraph 1.0.5 wheel 原始碼確認）。以 config 頂層鍵 `{"recursion_limit": N}` 設定（不放在 `configurable` 裡），或用環境變數 `LANGGRAPH_DEFAULT_RECURSION_LIMIT`；超過時拋 `GraphRecursionError`。`create_agent` 內部另設 `recursion_limit: 9_999`。出處：https://docs.langchain.com/oss/python/langgraph/graph-api ＋ langgraph 1.2.20 wheel 原始碼（`DEFAULT_RECURSION_LIMIT = ... "10007"`）。**和課綱有落差**：課綱說「必須設定 recursion_limit 以強制終止」本身沒錯，但學生若以為有預設上限就安全，會在死循環時燒掉上萬次 LLM 呼叫。應改教「明確設小值（如 25–50）」，並搭配 LangChain 的 `ModelCallLimitMiddleware` / `ToolCallLimitMiddleware`（langchain 1.5.0 wheel 內有）。
- **Annotated[list, operator.add] 的 reducer 寫法**：正確，但對 `messages` 欄位官方建議用 `add_messages`（能依 id 更新既有訊息）。出處：https://docs.langchain.com/oss/python/langgraph/graph-api 。
- **langgraph-supervisor 現況**：GitHub repo `langchain-ai/langgraph-supervisor-py` **已封存（archived）**，PyPI 最後版本 0.0.31（2025-11-19）。README 明寫「We now recommend using the supervisor pattern directly via tools rather than this library for most use cases」，並導向 https://docs.langchain.com/oss/python/langchain/supervisor 。出處：https://github.com/langchain-ai/langgraph-supervisor-py 。課綱 Lab 5-C 寫「將子 Agent 封裝為工具集」正好是官方現行推薦做法；**不要在課程中 `pip install langgraph-supervisor`**。
- **deepagents 現況**：活躍維護中。PyPI `deepagents 0.7.35`（2026-11-09），GitHub `langchain-ai/deepagents` 未封存，描述為「The batteries-included agent harness」。`from deepagents import create_deep_agent`；內建虛擬檔案系統工具與 `task` 子 agent；**v0.7 起任務規劃（write_todos）改為 opt-in**。另有 LangSmith 託管版 Managed Deep Agents。出處：https://docs.langchain.com/oss/python/deepagents/overview 。課綱寫「DeepAgent」應改為正式名稱 **Deep Agents / `deepagents`**；「自主規劃」需註明要手動開啟。
- **LangChain Chat-UI 名稱（模組八 Lab 8 引用）**：正式名稱是 **Agent Chat UI**（repo `langchain-ai/agent-chat-ui`，`npx create-agent-chat-app`）。**該 repo 已於 2026-11-03 封存為唯讀**（GitHub API `archived: true`），但官方文件 https://docs.langchain.com/oss/python/langchain/ui 目前仍推薦它，且有託管版 agentchat.vercel.app。截至今日未見官方公布的後繼專案。出處：https://github.com/langchain-ai/agent-chat-ui 。
- **WorkBuddy 是否真實存在（模組八引用）**：存在，見 M8 檔案的事實核實。
- **Anthropic「通用 Agent + Skills」**：Agent Skills 出自 Anthropic 2025-10-16 工程文章，現已以開放標準形式由 agentskills.io 維護。課綱的「智能體動物園」一詞不是原文用語（原文說的是取代「為每個用例建專用 agent」），引用時要標明是我們的轉述。
- **Tool calling 訊息格式**：OpenAI 官方指南已改以 Responses API 為主（`function_call` / `function_call_output` / `call_id`）；OpenAI 相容端點（vLLM 等）仍是 Chat Completions 的 `tool_calls` + `role: "tool"` + `tool_call_id`；`arguments` 都是 JSON 字串。Anthropic 則是 `tool_use` / `tool_result` block。出處見論點 1。

## 投影片建議

1. **論點 1 改用開源模型 + chat template 開場，再進 API。** 對 DL 學生最有說服力的是看到 `model.generate()` 吐出 `<tool_call>{...}</tool_call>`（HF chat_extras 範例），立刻理解「tool calling = 被微調過的 token 生成」。之後再展示 API 版的三則訊息。課綱目前直接從「解析 `tool_calls`」切入，會讓學生以為 API 有魔法。
2. **把「LangChain 1.0 架構巨變」從「AgentExecutor → LangGraph」改寫成「AgentExecutor → `create_agent` + middleware（底層跑在 LangGraph 上）」。** 學生從沒用過舊 LangChain，花時間比較 AgentExecutor 只是在解釋歷史包袱；面試題可保留，但投影片只需一張「舊 → 新」對照表。Middleware（HITL、摘要、PII、呼叫次數上限）應該補進課綱，它是 1.0 的核心新概念，也讓 Lab 5-B / 5-C 少寫很多樣板。
3. **recursion_limit 那一格踩坑要改寫。** 預設值已是 10,007（langgraph 1.0.5 以前是 25，網路上多數教材寫的是 25），所以「有預設上限、會自己停」是錯的安全感。投影片建議：明確設 `recursion_limit=25` 示範 `GraphRecursionError`，再介紹 `ModelCallLimitMiddleware` / `ToolCallLimitMiddleware` 作為成本保險。
4. **Reducer 用「梯度累加」搭橋，並修正課綱措辭。** 「並發狀態覆蓋與資料競爭」聽起來像多執行緒 race condition，實際是「同一 super-step 兩個 node 寫同一欄位、預設 reducer 是覆蓋」。用「PyTorch `.grad` 預設累加、LangGraph state 預設覆蓋」對照，學生一秒懂；`messages` 欄位改教 `add_messages`。
5. **Lab 5-C 不要用 `langgraph-supervisor` 套件，直接照官方 Supervisor 教學（子 agent 包成 `@tool`）。** 套件已封存，而官方教學的 Calendar/Email 範例跟課綱完全一致。多智能體段落開頭加一張 Anthropic「4× / 15× token」長條圖，先講「什麼時候不該用多智能體」，比直接教 Supervisor 更像工程師的思維。
