# 第 8 章　狀態、存檔與人在回路：讓寫入動作只有一條路

**本章結論**：Checkpointer 讓 LangGraph 在每一步之後把整份 state 存檔，於是同一個機制同時撐起三件事：跨回合記憶、從舊存檔分岔的時光旅行，以及在危險操作前暫停等人的人在回路（human-in-the-loop，HITL）。寫入動作的安全不能靠 prompt 拜託模型自律，而要靠程式結構：模型只能提議，固定流程負責審批、執行與驗證，`interrupt()` 暫停、`Command(resume=...)` 恢復。迴圈的保險絲也要自己裝：`recursion_limit` 在現行 langgraph 的預設值是 10,007，等於沒有保險，必須明確設小，再加上呼叫次數上限。旗艦專案把這些規則落成一張「調查 → 計畫 → 審批 → 執行 → 驗證」的固定圖，是本章所有機制的完整示範。

讀完本章，你應該能回答：為什麼正式環境要用 `PostgresSaver` 而不是 `InMemorySaver`；恢復執行時哪段程式會再跑一次、這對副作用意味著什麼；以及一個寫入工具從被模型提議到真正執行之間，要經過哪幾道檢查。

---

## 8.1 Checkpointer 每一步存檔，記憶、時光旅行與人在回路都建立在它上面

**Checkpointer 是 LangGraph 的存檔器：圖每跑完一個 super-step，它就把整份 state 存成一個 checkpoint。** 這個看似單純的功能，是本章三個能力的共同地基。理解了這一點，後面的 API 只是同一件事的三種用法。

你對這個概念再熟悉不過。訓練模型時，每個 epoch 結束呼叫一次 `torch.save(model.state_dict())`，訓練中斷了就從最後一個 checkpoint 接著跑。LangGraph 的 checkpoint 是一模一樣的概念，只是存的是「圖的 state」（messages、證據、待審的操作）而不是權重。不同的 thread 就像不同的實驗 run，各自有自己的一串 checkpoint，互不干擾。

**圖 8-1　一個存檔機制，撐起三種能力**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
flowchart TB
  CK["Checkpointer<br/>每個 super-step 存檔"]
  CK --> MEM["跨回合記憶<br/>同 thread_id 讀回"]
  CK --> TT["時光旅行<br/>從舊存檔分岔"]
  CK --> HITL["人在回路<br/>interrupt 後恢復"]
  CK --> DUR["當機恢復<br/>換行程接著跑"]
  classDef key fill:#051C2C,stroke:#051C2C,color:#FFFFFF
  class CK key
```

<sub>資料來源：本課整理；依 LangGraph 官方文件〈Persistence〉〈Interrupts〉〈Use time-travel〉與投影片「Checkpointer：每一步都存檔」。</sub>

三種能力的關係可以這樣理解。跨回合記憶是「讀最新的存檔」；時光旅行是「讀某個舊存檔，改一點再跑」；人在回路是「主動停在某一步存檔，等外部輸入後從存檔接著跑」。第四格當機恢復是人在回路的推廣：如果存檔放在資料庫裡，連執行的行程都可以換一個。這四件事都不需要你在節點裡多寫任何程式，只要編譯圖時傳入一個 checkpointer。

這也是為什麼本專案的 `AGENTS.md` 把「checkpoint 用 `PostgresSaver` 或 `InMemorySaver`，不准把狀態留在揮發性變數裡」列為架構規則。狀態一旦散落在節點函式的區域變數或全域變數裡，上面四種能力就全部失效。

## 8.2 thread_id 決定讀回哪一份存檔，兩種 Saver 只差在能不能撐過重啟

**同一個 `thread_id` 的呼叫會把上一次的存檔讀回來，換一個 `thread_id` 就是一段全新的對話。** 而存檔放在記憶體還是資料庫，決定了它能不能活過行程重啟。

先看跨回合記憶的最小例子。第二次呼叫沒有再提名字，但因為用了同一個 `thread_id`，模型看得到第一次的對話：

```python
from langgraph.checkpoint.memory import InMemorySaver

app = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "user-42"}}
app.invoke({"messages": "我叫小明"}, cfg)
app.invoke({"messages": "我叫什麼？"}, cfg)   # 讀回存檔，答得出「小明」
```

注意 `thread_id` 放在 `config` 的 `configurable` 鍵底下。回想第 7 章：API 本身沒有記憶，每一輪都要重送整串 messages；checkpointer 就是替你保管這串 messages 的那個人。

**圖 8-2　每個 thread 是一條獨立的存檔鏈，時光旅行可以從任一格分岔**

![checkpoint 每一步一張快照：thread_id ticket-42 有 step 1 到 5 的膠卷，ticket-99 有 step 1 到 2，兩者都存進 InMemorySaver；從 ticket-42 的 step 2 拉出一條紅線標「時光旅行」，指向一格分岔重跑](../../modules/module-05-agent-harness/images/checkpoint.jpg)

<sub>資料來源：模組五 `images/checkpoint.jpg`（本課繪製）。</sub>

兩種 Saver 的取捨很單純：

| | `InMemorySaver` | `PostgresSaver` |
|---|---|---|
| 存在哪 | 行程記憶體 | PostgreSQL 資料表 |
| 行程結束後 | 全部消失 | 還在 |
| 安裝 | 隨 `langgraph` 附帶（`langgraph-checkpoint`） | 另裝 `langgraph-checkpoint-postgres` 與 `psycopg[binary,pool]` |
| 首次使用 | 直接用 | 要呼叫一次 `setup()` 建表 |
| 適合 | 開發、測試、單次示範 | 上線、需要跨重啟恢復的審批 |

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string(DB_URI) as cp:
    cp.setup()                       # 首次使用要建表
    app = g.compile(checkpointer=cp)
```

連線字串 `DB_URI` 要從環境變數讀取，不寫進程式碼。為什麼審批流程一定要 Postgres？因為人的反應時間是分鐘到小時等級。值班主管收到審批通知時，可能服務已經重新部署過、行程已經換了一個。存檔在記憶體裡，審批單就跟著行程一起消失。

**圖 8-3　存檔放在 Postgres，工作行程掛了也能由另一個行程從最後一格接著跑**

![LangChain 文件原圖 Durable Execution: Crash Recovery：Worker A 跑完 c1、c2 後 crash，c1、c2 已存進底部的 Persistence layer (Postgres)；Worker B 從 c2 恢復，再跑出 c3 存回 Postgres](../slides/deck/assets/figures/m5/d-lc-durable-execution.png)

<sub>資料來源：LangChain Docs〈Going to production〉（Deep Agents），MIT License © 2025 LangChain。</sub>

最後區分短期與長期記憶。Checkpointer 管的是**短期記憶**，綁在單一 thread 上，類似 RNN 在單一序列內的 hidden state。跨 thread 的事實（使用者偏好、過去事故的結論）要放在 LangGraph 的 store，或第 4–6 章的向量庫與知識圖譜，那是**長期記憶**，類似外部記憶體。兩者的分工不要混：把所有歷史對話都塞進同一個 thread，context 會越撐越大；第 9 章會講這個成本。

## 8.3 時光旅行不是回滾，而是從舊存檔長出一條新分支

**時光旅行（time travel）讓你從任何一個舊 checkpoint 出發，改一點 state 再跑，長出一條新分支；原本的歷史完整保留。** 它是除錯與做實驗的工具：agent 在第五步走錯了，你可以回到第四步、改掉讓它走錯的那個值，看看結果會不會不同。

用訓練的經驗類比最快：載入第 5 個 epoch 的 checkpoint、改學習率、開一條新的實驗分支。原本那條實驗線還在，你只是多了一條可比較的線。LangGraph 的做法是四步：

```python
history = list(app.get_state_history(cfg))          # 由新到舊
past = next(s for s in history if s.next == ("write_joke",))
fork = app.update_state(past.config, {"topic": "chickens"})
app.invoke(None, fork)                               # 從分岔點續跑
```

`get_state_history` 回傳這個 thread 的所有 checkpoint，順序由新到舊。每個 checkpoint 的 `next` 欄位記錄「下一個要跑的節點」，用它找出你想回到的那一步。`update_state` 會以那個舊 checkpoint 為基礎，寫入一個**新的** checkpoint；`invoke(None, fork)` 傳入 `None` 表示不給新輸入，直接從分岔點續跑。這裡的 `topic`、`write_joke` 取自官方文件的例子。

**圖 8-4　update_state 產生新分支，主幹的 c3、c4 都還在**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
flowchart LR
  C1["c1"] --> C2["c2"] --> C3["c3"] --> C4["c4"]
  C2 -->|"update_state<br/>topic 改成 chickens"| C2F["c2'"]
  C2F --> C3F["c3'"] --> C4F["c4'"]
  classDef muted fill:#F0F3F7,stroke:#C5CED6,color:#5B6B79
  classDef accent fill:#2251FF,stroke:#2251FF,color:#FFFFFF
  class C3,C4 muted
  class C2F accent
```

<sub>資料來源：本課整理；改繪自投影片「Time Travel：倒帶、改 state、分岔」與 LangGraph〈Use time-travel〉。灰色為保留的原歷史。</sub>

官方文件區分兩個詞。**Replay（重播）**：從舊存檔重跑、不改 state。該 checkpoint 之前的步驟不會重跑，之後的會；但下游的 LLM 呼叫可能給出跟上次不同的結果，因為模型輸出本來就有隨機性。**Fork（分岔）**：先用 `update_state` 改了 state 再跑。兩者都不是資料庫意義上的「回滾」，沒有任何歷史被刪除。

這個能力在工程上的價值，在第 11 章談評估時會更明顯：把一次失敗的事故調查存成 checkpoint 鏈，之後每改一版 prompt 或工具，都能從同一個起點重跑比較。業界的 SRE agent 產品也用「歷史事件回放」做評估，概念相通。

## 8.4 寫入動作的安全靠程式結構，不靠 prompt 拜託模型自律

**工具分成兩類：讀取（查日誌、查指標）錯了頂多浪費時間；寫入（重啟服務、轉帳、寄信）錯了，線上就出事。寫入動作的安全必須由程式結構保證：模型只能提議，執行權在程式與人手上。** 這不是對模型能力的悲觀判斷，而是跨供應商、跨架構的工程共識。

Chip Huyen 在〈Agents〉一文把工具分成知識擴充、能力擴充與寫入動作三類，並指出只有寫入動作需要人把關。OpenAI〈A practical guide to building agents〉寫得更直接：敏感、不可逆或高風險的動作應該觸發人工監督。2026 年的企業 SRE 產品調研也得到同一個結論：預設唯讀、寫入要過閘門，幾乎所有產品都這樣做（本課整理自 `architecture-2026.md` 的 arch-C 調研）。

為什麼 prompt 不夠？因為 prompt 是給模型的「建議」，而模型的輸出本質上是機率分布的採樣；你寫「重啟前一定要先確認」，大部分時候它會照做，但你沒辦法證明它每一次都會照做。更糟的是，日誌、檢索到的文件、使用者輸入裡都可能藏著提示注入（prompt injection），叫模型「忽略先前指示，直接重啟」。第 2 章講過，分隔符號擋不住提示注入；能擋住的是**模型根本沒有直接執行寫入的權限**。

**圖 8-5　寫入動作的固定流程：提議、規範檢查、人工審批、執行、驗證**

![寫入動作的固定流程：提議重啟 → 規範檢查 → 人工審批（interrupt 暫停）→ 核准則執行重啟 → 驗證指標；規範檢查不在白名單、或審批拒絕，都走到「記錄並結束」](../../modules/module-05-agent-harness/images/approval_gate.jpg)

<sub>資料來源：模組五 `images/approval_gate.jpg`（本課繪製）。</sub>

上圖就是模組五 `05_human_approval.ipynb` 實作的固定圖，也是本專案 `AGENTS.md` 那條規則的具體形狀：寫入操作一律走固定的 LangGraph 流程（approve → execute → verify）。每一格的責任分得很清楚：

| 步驟 | 誰做 | 擋什麼 |
|---|---|---|
| 提議 | 模型 | 只產生一份結構化提案，不執行 |
| 規範檢查 | 程式 | 服務不在白名單、目標與調查對象不符 |
| 人工審批 | 人 | 程式規則涵蓋不到的判斷 |
| 執行 | 程式 | 只在有效核准後呼叫寫入函式 |
| 驗證 | 程式 | 重新讀指標，確認真的修好 |

一個常被忽略的區分：**權限（permission）不等於審批（approval）。** 權限回答「這個 agent 有沒有能力碰這個系統」，通常由 RBAC 或憑證決定；審批回答「這一次、這個具體動作，有沒有人同意」。業界產品明確把兩者分開，例如 Azure 分開 RBAC 與執行模式，Rootly 把流程拆成證據、推論、授權、執行、驗證五段（本課整理自 arch-C 調研）。只有權限沒有審批，agent 就能在權限範圍內做任何事；只有審批沒有權限控管，審批就可能被繞過。

## 8.5 interrupt 暫停並存檔，Command(resume=...) 從存檔接著跑

**LangGraph 的人在回路靠兩個原語：節點內呼叫 `interrupt(payload)` 讓圖停下並存檔；人做出決定後，呼叫端用同一個 `thread_id` 送 `Command(resume=決定)`，圖從存檔讀回，`interrupt()` 的回傳值就是那個決定。** 這兩個原語都從 `langgraph.types` 匯入，而且圖必須以 checkpointer 編譯，否則沒有存檔可以讀回。

課綱原本把恢復寫成「`Command` approve」，這是錯的：`Command` 沒有 approve 這個參數，正確寫法是 `Command(resume=...)`，例如 `Command(resume={"approved": True})`。下面是一個審批閘門節點，根據人的決定，用第 7 章提過的 `Command(goto=...)` 決定下一步：

```python
from langgraph.types import interrupt, Command

def approval_gate(state: State) -> Command:
    call = state["messages"][-1].tool_calls[0]
    ok = interrupt({"sql": call["args"]["query"]})     # 暫停、存檔，把 SQL 交給人看
    if ok:
        return Command(goto="execute_sql")
    deny = ToolMessage("管理員拒絕", tool_call_id=call["id"])
    return Command(goto="agent", update={"messages": [deny]})
```

呼叫端的兩次 invoke 長這樣。第一次停在閘門，回傳值裡有 `__interrupt__`；第二次送 resume 接著跑：

```python
cfg = {"configurable": {"thread_id": "ticket-42"}}
out = graph.invoke(inputs, cfg)       # 停在閘門：out["__interrupt__"]
graph.invoke(Command(resume=True), cfg)
```

**圖 8-6　interrupt 的一次完整往返：停下、存檔、交給人、讀回、從頭重跑該節點**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
sequenceDiagram
  participant C as 呼叫端
  participant G as 圖（審批節點）
  participant S as Checkpointer
  participant H as 管理員
  C->>G: invoke(inputs, thread_id)
  G->>S: interrupt(payload)：存檔
  G-->>C: 回傳 __interrupt__
  C->>H: 顯示待審內容
  H-->>C: 核准或拒絕
  C->>G: Command(resume=決定)，同一 thread_id
  S-->>G: 讀回存檔
  Note over G: 節點從頭重跑，interrupt() 直接回傳決定
```

<sub>資料來源：本課整理；依 LangGraph〈Interrupts〉與投影片「HITL：危險操作先停下來」「Lab 5-B：interrupt 暫停，resume 恢復」。</sub>

這個機制有兩個學生幾乎一定會踩的坑，都源自它的實作方式。

**第一，恢復時整個節點從頭重跑。** LangGraph 不會「從 `interrupt()` 那一行繼續」，而是重新執行整個節點函式，這一次 `interrupt()` 直接回傳人給的值。後果是：`interrupt()` **之前**的程式碼會執行兩次。如果你在審批節點裡先寄一封通知信、再呼叫 `interrupt()`，恢復時信會再寄一次。修法是把副作用移到別的節點，審批節點裡只放「準備給人看的內容」和 `interrupt()` 本身。

**第二，不要用裸的 `try/except` 包住 `interrupt()`。** 它靠拋出一個特殊例外來暫停執行；你的 `except Exception` 把它接住了，圖就停不下來，審批形同虛設。

還有兩個細節。`interrupt()` 的 payload 必須可以 JSON 序列化，因為它要被存進 checkpoint。langgraph 1.2.12 起另有 `response_schema` 參數，可以驗證 resume 回來的值；旗艦專案則在節點內用 Pydantic 的 `Decision.model_validate(...)` 自己驗證，效果相同。

可以把 `interrupt()` 想成除錯器的 breakpoint 加上「從 checkpoint 重啟」：程式停在某一行、狀態全部存好，你看完之後按繼續。如果你寫過 Python generator，`yield` 出一個值、外面用 `send()` 送回一個值，也是同樣的形狀。

## 8.6 HumanInTheLoopMiddleware 把審批閘門搬到工具層

**如果你用的是 `create_agent` 而不是自己接圖，審批不必手刻：掛上 `HumanInTheLoopMiddleware`，指定哪些工具要攔下，它會在模型要呼叫那些工具時替你 `interrupt()`。** 沒列入的工具自動放行，所以唯讀查詢照跑，只有寫入動作會停下。

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

agent = create_agent(model, tools=[run_query, execute_sql],
    middleware=[HumanInTheLoopMiddleware(
        interrupt_on={"execute_sql": {"allowed_decisions": ["approve", "reject"]}})],
    checkpointer=InMemorySaver())
# 恢復：
agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), cfg)
```

恢復時的格式和手刻版不同：`Command(resume={"decisions": [...]})`，每個決定有一個 `type`。LangChain 文件列出四種：approve（照原參數放行）、edit（改了參數再放行）、reject（拒絕，把理由回給模型）、respond（不執行，直接用文字回覆模型）。官方文件也明說：人在回路需要 checkpointer 才能處理中斷。

**圖 8-7　middleware 在「模型 → 工具」那條邊上設一個收費站**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
flowchart LR
  A["agent"] --> I{"在 interrupt_on<br/>名單內？"}
  I -->|"否"| EX["執行工具"]
  I -->|"是"| H{"人的決定"}
  H -->|"approve"| EX
  H -->|"edit"| EX
  H -->|"reject"| TM["ToolMessage<br/>理由回給 agent"]
  H -->|"respond"| TM
  EX --> A
  TM --> A
  classDef accent fill:#2251FF,stroke:#2251FF,color:#FFFFFF
  class H accent
```

<sub>資料來源：本課整理；依 LangChain〈Human-in-the-loop〉與 Deep Agents〈Human-in-the-loop〉的流程結構重繪。</sub>

高階框架都有同一個東西，只是名字不同：Deep Agents 的 `interrupt_on`、OpenAI Agents SDK 的 `needs_approval`、Claude Agent SDK 的 `can_use_tool` 回呼與 `PreToolUse` hook。底層概念完全相同：**模型只能提議，執行權在程式與人手上。**

那什麼時候該用 middleware、什麼時候該自己接固定圖？判準是「審批之後還有沒有確定性的步驟」。Middleware 版的閘門只管「這次工具呼叫放不放行」，放行後就回到 agent 迴圈，由模型決定下一步。如果你的流程要求核准後一定執行、執行後一定驗證、驗證失敗一定停止自動操作，這些「一定」就不該交給模型，而要寫成固定圖。8.8 節的旗艦專案就是這種情況。

## 8.7 recursion_limit 的預設值擋不住死循環，要明確設小並加呼叫上限

**`recursion_limit` 是 LangGraph 迴圈的保險絲，但 langgraph 1.1.4 起預設值是 10,007 個 super-step，等於沒有保險。** 網路上多數教材寫的是 25，那是 1.0.5 以前的舊預設值。學生若以為「有預設上限、會自己停」，就可能在死循環時燒掉上萬次 LLM 呼叫。本專案的規則是：agent 迴圈一律明確設定 `recursion_limit`。

設定位置是 config 的**頂層鍵**，不是放在 `configurable` 裡；超過時拋出 `GraphRecursionError`：

```python
cfg = {
    "configurable": {"thread_id": "ticket-42"},
    "recursion_limit": 25,            # 頂層鍵，明確設小值
}
graph.invoke(inputs, cfg)             # 超過則拋 GraphRecursionError
```

也可以用環境變數 `LANGGRAPH_DEFAULT_RECURSION_LIMIT` 改預設值。另外要知道，`create_agent` 內部另設了 `recursion_limit: 9_999`，同樣不能指望它擋住失控的迴圈。

**圖 8-8　兩層保險：recursion_limit 限制步數，呼叫上限 middleware 限制成本**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
flowchart LR
  L["工具回傳格式<br/>不符預期"] --> R["模型反覆<br/>呼叫同一工具"]
  R --> D{"預設 10,007"}
  D -->|"沒設上限"| B["帳單一直跳"]
  D -->|"明確設 25"| E["GraphRecursionError"]
  R --> M["ToolCallLimit<br/>ModelCallLimit"]
  M --> E2["提早停止"]
  classDef muted fill:#F0F3F7,stroke:#C5CED6,color:#5B6B79
  classDef accent fill:#2251FF,stroke:#2251FF,color:#FFFFFF
  class B muted
  class E accent
```

<sub>資料來源：本課整理；依 `product-facts.md` 第 5 列勘誤、`M5-agent-langgraph.md` 事實核實，與投影片「踩坑：死循環燒 token、並發寫入出錯」。</sub>

步數上限和呼叫次數上限要搭配使用，因為它們量的東西不同。`recursion_limit` 算的是 super-step，一個 super-step 裡可能有好幾個平行節點、好幾次工具呼叫；`ModelCallLimitMiddleware` 和 `ToolCallLimitMiddleware` 直接算模型與工具的呼叫次數，比較接近你的帳單。至於設多小，素材給的參考是 25 到 50，依流程的實際深度決定；原則是「略大於正常流程需要的步數」，讓正常情況永遠碰不到、失控時很快就停。

第 7 章的兩個常見事故放在一起看，兩者都是「看到什麼 → 為什麼 → 改哪一行」：

| 症狀 | 原因 | 修法 |
|---|---|---|
| 同一個工具被反覆呼叫，帳單一直跳 | 工具回傳格式不是模型預期的，它不斷重試；預設上限 10,007 | config 頂層設 `{"recursion_limit": 25}`，再加 `ToolCallLimitMiddleware` |
| 兩個平行節點寫同一欄位，拋 `InvalidUpdateError` | 沒有 reducer 的欄位，同一步只能有一個寫入者 | `Annotated[list, operator.add]`；`messages` 用 `add_messages` |
| 審批後副作用發生兩次 | 恢復時節點從頭重跑 | 副作用移到審批之後的節點 |
| 回答說「已重啟」，其實沒有呼叫工具 | 小模型編造執行結果 | 看 trace 驗收；寫入走固定流程，回報以執行收據為準 |

最後一列是把第 7 章的教訓和本章串起來：當寫入只能經由固定圖執行，「是否真的重啟了」就不再取決於模型怎麼說，而是看 state 裡有沒有執行收據。

## 8.8 旗艦專案：寫入只有一條路，調查 → 計畫 → 審批 → 執行 → 驗證

**旗艦專案 `projects/incident-autonomous-agent/` 把本章所有規則落成一張固定的 LangGraph 圖：唯一能改動服務狀態的路徑是「調查 → 計畫 → 審批 → 執行 → 驗證」，模型無法繞過。** 它的 `workflow.py` 開頭第一行 docstring 就寫著「唯一寫入路徑」。所有重啟都作用於 SQLite 模擬服務，不會呼叫 Docker、shell 或真實線上服務。

先看圖的形狀。五個節點、一條固定主線，每個關卡都有一條提早結束的出口：

**圖 8-9　旗艦專案的固定圖：每一關都有出口，只有全部通過才會執行與驗證**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
stateDiagram-v2
  state "investigate 唯讀調查" as investigate
  state "plan 白名單與目標檢查" as plan
  state "approve interrupt 等人" as approve
  state "execute 版本檢查與收據" as execute
  state "verify 重讀指標" as verify
  [*] --> investigate
  investigate --> plan
  plan --> approve: awaiting_approval
  plan --> [*]: resolved / blocked / manual_review
  approve --> execute: approved
  approve --> [*]: denied
  execute --> verify: executed
  execute --> [*]: execution_failed
  verify --> [*]: verified / verification_failed
```

<sub>資料來源：本課整理；依 `projects/incident-autonomous-agent/oncall_agent/workflow.py` 的 `build_graph` 繪製。</sub>

逐一看每個節點怎麼把本章的原則寫成程式。

**investigate：唯讀調查。** 這一格平行收集五種證據：指標、日誌、runbook 檢索、服務拓撲、訂單統計。在 `demo` 模式下由固定規則產生診斷；在 `live` 模式下交給一個 Deep Agents 調查 agent（第 9 章細講），它只拿得到唯讀工具，最後必須交出一份 Pydantic 定義的 `Diagnosis`，內容包括摘要、證據、建議動作（`restart` 或 `none`）與目標服務。不管哪種模式，這一格的輸出都只是「提案」，沒有任何寫入能力。

**plan：程式做規範檢查。** 模型的建議先被 `Diagnosis.model_validate` 驗證，再過三道確定性的檢查：建議的目標必須和調查的服務相符，否則 `blocked`；服務不在重啟白名單（只允許 `order-db-proxy`、`notification`），就轉 `manual_review` 交給人；服務已經健康或模型建議不動作，就 `resolved` 結束。全部通過才產生一份 `RestartArgs` 提案，其中綁定事件的 `action_id` 和當下的服務版本號 `expected_revision`。

**approve：interrupt 等人。** 節點呼叫 `interrupt()`，把提案和摘要交給頁面顯示，並附一句「只會修改教學模擬服務」。恢復時，回傳值經 `Decision.model_validate` 驗證（`approved` 用 `StrictBool`，不接受 "yes" 之類的字串），而且決定裡的 `action_id` 必須和提案相符，否則直接報錯。注意這個節點完全沒有副作用，正好避開 8.5 節的第一個坑。

**execute：再驗一次，然後才寫入。** 執行節點不信任前一步的 status，自己重新驗證「有核准、`action_id` 相符」才呼叫 `operations.restart`。寫入函式本身再做三件事：服務必須在白名單內；同一個 `action_id` 若已有收據就直接回傳舊收據（冪等，checkpoint 重試也不會重複重啟）；服務版本號若已改變（例如另一事件已修復），就拒絕執行並要求重新調查與審批。狀態更新與操作收據寫在同一個 SQLite 交易裡。

**verify：用指標驗收，不用模型的話。** 重新讀取指標，必須同時滿足 `healthy`、`p95_ms < 1000`、`error_rate < 0.05` 才算通過；任何一項不符就標記 `verification_failed`，停止自動操作。

這五格合起來，回答了 8.4 節表格的每一列：提議歸模型，規範檢查、執行、驗證歸程式，判斷歸人。

存檔與恢復的部分在 `runtime.py`。設定 `ONCALL_CHECKPOINT=postgres` 時用 `PostgresSaver.from_conn_string(...)` 並呼叫 `setup()`，否則用 `InMemorySaver`；README 的教學流程是：開始一個事件、停在待審狀態、**關掉整個程序再重啟**，然後用事件 ID 恢復，照樣可以核准或拒絕。這就是 8.2 節「審批單要活過行程重啟」的實際示範。每次呼叫圖的 config 都同時帶 `thread_id`（就是事件 ID）與頂層的 `recursion_limit`；`Settings` 把它的預設值設為 40，並用 Pydantic 限制在 10 到 100 之間，杜絕有人把它設成上萬。

```python
def config(self, incident_id):
    return {"configurable": {"thread_id": incident_id},
            "recursion_limit": self.settings.recursion_limit}
```

人的決定進來時，`decide()` 也先做檢查才呼叫 `Command(resume=...)`：事件必須真的處於待審狀態，`action_id` 必須相符，否則回傳衝突錯誤。這擋掉了重複審批與過期審批。

**圖 8-10　一次核准從頁面到寫入，中間要過四道獨立的檢查**

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Noto Sans TC, Helvetica, Arial, sans-serif','fontSize':'15px','primaryColor':'#FFFFFF','primaryTextColor':'#051C2C','primaryBorderColor':'#051C2C','lineColor':'#7A8B99','secondaryColor':'#F0F3F7','tertiaryColor':'#F0F3F7','clusterBkg':'#F7F9FB','clusterBorder':'#C5CED6','edgeLabelBackground':'#FFFFFF','actorBkg':'#FFFFFF','actorBorder':'#051C2C','noteBkgColor':'#F0F3F7','noteBorderColor':'#C5CED6'}}}%%
flowchart LR
  UI["審批頁面"] --> K1["decide()<br/>待審中？ID 相符？"]
  K1 --> K2["approve 節點<br/>Decision 驗證"]
  K2 --> K3["execute 節點<br/>核准且 ID 相符"]
  K3 --> K4["restart()<br/>白名單、版本、冪等"]
  K4 --> DB[("SQLite 交易<br/>狀態＋收據")]
  classDef accent fill:#2251FF,stroke:#2251FF,color:#FFFFFF
  class K4 accent
```

<sub>資料來源：本課整理；依 `oncall_agent/runtime.py`、`workflow.py`、`storage.py`。</sub>

看起來重複檢查了好幾次，這是刻意的。每一層都假設上一層可能被繞過或出錯：API 可能被直接呼叫、checkpoint 可能被重試、兩個事件可能同時修同一個服務。工具參數的驗證也遵守同一原則，`models.py` 裡每個工具參數模型都設了 `extra="forbid"`，模型多塞一個欄位就驗證失敗；SQL 查詢工具只接受單一 `SELECT`、只查 `orders` 表、用唯讀連線和執行步數上限。

最後，專案 README 對自己的邊界寫得很誠實，值得照抄這種習慣：預設只綁 `127.0.0.1`、單程序單 worker；`reviewer` 只是示範用的審批標籤，不是企業身分驗證；尚未接企業 SSO／RBAC 與真實監控；接入真實寫入前，應改用具授權檢查與冪等機制的受控執行端。

## 本章重點

Checkpointer 在每個 super-step 存檔，同一機制撐起跨回合記憶（同 `thread_id` 讀回）、時光旅行（`update_state` 從舊存檔分岔，原歷史保留）與人在回路；需要活過行程重啟的審批一定要用 `PostgresSaver`。寫入動作的安全靠結構不靠 prompt：模型只提議，程式做規範檢查，人審批，程式執行並用指標驗證。`interrupt()` 暫停、`Command(resume=...)` 恢復，恢復時節點從頭重跑，所以副作用不能放在 `interrupt()` 之前，也不能用裸 `try/except` 包住它；用 `create_agent` 時可改掛 `HumanInTheLoopMiddleware`。`recursion_limit` 預設 10,007 不是保險，要在 config 頂層明確設小，再加呼叫次數上限。旗艦專案的五節點固定圖示範了這些規則如何層層疊加成「寫入只有一條路」。

## 對應實作與延伸閱讀

- 原理紀要：[模組五 `00_concepts.md`](../../modules/module-05-agent-harness/00_concepts.md) 第 4–5 節
- checkpoint、thread、時光旅行、`recursion_limit`：[`04_state_checkpoint.ipynb`](../../modules/module-05-agent-harness/04_state_checkpoint.ipynb)
- 固定審批圖（核准／拒絕／規範擋下三條路）：[`05_human_approval.ipynb`](../../modules/module-05-agent-harness/05_human_approval.ipynb)
- 旗艦專案：[`projects/incident-autonomous-agent/README.md`](../../projects/incident-autonomous-agent/README.md)、[`oncall_agent/workflow.py`](../../projects/incident-autonomous-agent/oncall_agent/workflow.py)、[`oncall_agent/runtime.py`](../../projects/incident-autonomous-agent/oncall_agent/runtime.py)、[`oncall_agent/models.py`](../../projects/incident-autonomous-agent/oncall_agent/models.py)
- 投影片 PDF：[`deck.pdf`](../slides/deck/deck.pdf)（模組五 511–513、551–552、580 頁）
- LangGraph 官方文件〈Persistence〉〈Add memory〉〈Use time-travel〉〈Interrupts〉
- LangChain 官方文件〈Human-in-the-loop〉（`HumanInTheLoopMiddleware`）
- OpenAI〈A practical guide to building agents〉：高風險動作要觸發人工監督
- Chip Huyen〈Agents〉（2025-01-07）：工具三分類與失敗模式
