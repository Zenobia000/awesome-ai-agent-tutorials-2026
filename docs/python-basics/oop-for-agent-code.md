# 讀懂 Agent 程式碼的 OOP 地圖

目標：在本課程看到任何 `class`、`@`、`self`，能在幾秒內說出「它在幹嘛」。

只收**課程程式碼裡真的出現的寫法**。`collections.abc` 與底線命名的細節見 [abc-and-underscores.md](abc-and-underscores.md)。

---

## 0. 知識地圖

由下往上蓋，下一層看不懂就先回上一層。

```text
第 5 層  讀框架程式碼    @tool、@app.get、with、async、yield
           ▲  框架怎麼接上你的函式
第 4 層  資料類別        dataclass、TypedDict、Pydantic、Annotated
           ▲  Agent 的資料長什麼樣
第 3 層  規格與多型      抽象類別、Protocol
           ▲  為什麼可以抽換零件
第 2 層  重用            繼承、super()、組合
           ▲  怎麼站在別人的類別上
第 1 層  封裝            _name、@property、frozen
           ▲  哪些能碰、哪些別碰
第 0 層  物件基礎        class、物件、self、__init__
```

## 五個核心原則

整份文件只在講這五句話：

| # | 原則 | 層 |
|---|---|---|
| 1 | **類別是藍圖，物件是成品**：把資料和操作它的函式綁在一起 | 0 |
| 2 | **封裝**：露出少數入口，藏起細節 | 1 |
| 3 | **繼承是填空，組合是裝零件** | 2 |
| 4 | **認能力，不認身分**：有需要的方法就能用 | 3 |
| 5 | **`@` 是加工**：把函式或類別交給別人包裝、登記 | 5 |

第 4 層是原則 1 的特化：專門裝資料的類別。

---

## 第 0 層：物件基礎

**類別（class）是藍圖，物件（object）是照藍圖做出的成品。**

用深度學習比喻：`nn.Linear` 是類別，`nn.Linear(768, 10)` 建出來的那一層是物件。

```python
class Counter:
    def __init__(self, start):      # 建立物件時自動執行
        self.value = start          # 屬性：這個物件自己記住的資料

    def add(self):                  # 方法：這個物件會做的事
        self.value += 1
        return self.value

a = Counter(0)
b = Counter(100)
print(a.add())      # 1
print(b.add())      # 101    兩個物件各記各的
```

| 詞 | 白話 |
|---|---|
| `self` | 「我自己」，指目前這個物件 |
| `__init__` | 出廠設定 |
| 屬性 `self.x` | 物件記住的東西 |
| 方法 `def f(self)` | 物件會做的動作 |

`a.add()` 等同 `Counter.add(a)`，所以定義時第一個參數是 `self`，呼叫時不用自己傳。

**讀程式碼的技巧**：先看 `__init__`，它列出這個物件手上有哪些東西。
例如 [`Runtime.__init__`](../../projects/incident-autonomous-agent/oncall_agent/runtime.py#L22)。

---

## 第 1 層：封裝

**封裝 = 外面只需要知道「按哪個鈕」，不需要知道裡面怎麼接線。**

就像呼叫 `chat(messages)`，你不必知道它怎麼在本地和雲端模型之間切換。

三種工具，由寬到嚴：

| 寫法 | 效果 | 課程例子 |
|---|---|---|
| `_name` | 約定「別從外面碰」，不強制 | [`_client`](../../course_utils/llm.py#L50)、[`_mcp`](../../projects/incident-autonomous-agent/oncall_agent/tools.py#L23) |
| `@property` | 方法偽裝成屬性；沒寫 setter 就唯讀 | `BudgetTracker.spent`（Lab 1-08） |
| `@dataclass(frozen=True)` | 建立後不能改欄位 | [`Endpoint`](../../course_utils/llm.py#L23) |

```python
class Budget:
    def __init__(self, costs):
        self._costs = tuple(costs)      # 內部資料

    @property
    def spent(self):                    # 每次讀取時即時計算
        return sum(self._costs)

b = Budget([1, 2, 3])
print(b.spent)        # 6     不用加括號
# b.spent = 0         ← AttributeError：唯讀
```

---

## 第 2 層：重用（繼承與組合）

| | 關係 | 比喻 | 寫法 |
|---|---|---|---|
| 繼承 | A **是一種** B | 填寫公版表格 | `class A(B):` |
| 組合 | A **擁有** B | 把零件裝進機器 | `self.b = b` |

### 繼承

子類別拿到父類別的全部功能，再**新增**或**覆寫**（同名方法蓋掉原本的）。

```python
class Model:
    def __init__(self, name):
        self.name = name

    def reply(self, text):
        return f"{self.name}: {self._generate(text)}"   # 固定流程

    def _generate(self, text):
        raise NotImplementedError                       # 留給子類別填

class Echo(Model):
    def __init__(self):
        super().__init__("echo")      # 先跑父類別的出廠設定

    def _generate(self, text):        # 填空
        return text

print(Echo().reply("嗨"))             # echo: 嗨
```

這是框架最常見的模式：**框架寫好流程，你只填空，框架回頭呼叫你。**

| 你寫的類別 | 繼承自 | 你填的空 |
|---|---|---|
| `ChromaRetriever`（Lab 3-04） | `BaseRetriever` | `_retrieve` |
| `RequestSpy`（Lab 5-06） | `BaseCallbackHandler` | `on_chat_model_start` |

所以你找不到誰呼叫 `_retrieve` 是正常的：呼叫它的是套件內部的程式。
在這個情境，`_` 的意思是「給子類別填、一般使用者別直接呼叫」。

一行就結束的繼承，只是為了**取一個專屬名字**：

```python
class ConflictError(ValueError):     # 一種特殊的 ValueError
    pass
```

[API 層](../../projects/incident-autonomous-agent/oncall_agent/api.py#L39)靠這個名字認出它，回傳 HTTP 409。

### 組合

```python
class ReadTools:
    def __init__(self, operations, runbooks):
        self.operations = operations     # 零件從外面傳進來
        self.runbooks = runbooks
```

[`ReadTools`](../../projects/incident-autonomous-agent/oncall_agent/tools.py#L16) 不是一種資料庫，它**拿著**資料庫來用。
零件從外面傳入（依賴注入），測試時就能換成假零件。

看到 `self.operations.status(...)`，讀作：「我的零件 operations，請做 status。」

---

## 第 3 層：規格與多型

**多型 = 同一行呼叫，換不同物件就有不同行為。**

```python
class Qwen:
    def chat(self, text):
        return "qwen: " + text

class DeepSeek:
    def chat(self, text):
        return "deepseek: " + text

for model in [Qwen(), DeepSeek()]:
    print(model.chat("hi"))          # 這一行不用知道是誰
```

只要有 `chat` 就能用，這叫 **duck typing**（走路像鴨子就當它是鴨子）。

想把規格寫清楚有兩種方式：

| | 要繼承嗎 | 附共用程式碼 | 何時檢查 |
|---|---|---|---|
| 抽象類別 `ABC` | 要 | 可以 | 建立物件時 |
| `Protocol` | 不用 | 通常不放 | 由 Pylance、mypy 檢查 |

```python
from typing import Protocol

class ChatModel(Protocol):
    def chat(self, text: str) -> str: ...     # ... 代表「這裡不實作」

def ask(model: ChatModel) -> str:
    return model.chat("hi")
```

`Iterator`、`Iterable` 就是 Python 內建的規格。

---

## 第 4 層：資料類別

Agent 程式大半在傳資料。四種寫法**長得像，執行時行為差很多**：

| 寫法 | 白話 | 執行時驗證 | 取值 | 課程用途 |
|---|---|---|---|---|
| `@dataclass` | 省掉手寫 `__init__` 的類別 | 否 | `x.name` | 內部設定 |
| `TypedDict` | 有欄位說明的 dict | 否 | `x["name"]` | LangGraph state |
| Pydantic `BaseModel` | 有門口警衛的類別 | **是** | `x.name` | 工具參數、模型輸出 |
| `Literal[...]` | 只准這幾個值（標註） | 在 Pydantic 裡才會擋 | — | 列舉選項 |

判斷方法：**資料來自外部（使用者、模型）→ Pydantic。**

### dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Endpoint:
    name: str
    model: str

ep = Endpoint("local", "qwen2.5:3b")    # __init__ 自動產生
print(ep)                               # Endpoint(name='local', model='qwen2.5:3b')
# ep.model = "x"                        ← FrozenInstanceError
```

### TypedDict

```python
from typing import TypedDict

class State(TypedDict):
    service: str

s: State = {"service": "order-api"}
print(type(s))              # <class 'dict'>   它就是普通 dict
```

[`IncidentState`](../../projects/incident-autonomous-agent/oncall_agent/workflow.py#L18) 的 `total=False` 表示這一層宣告的欄位可以缺；從 `IncidentInput` 繼承來的仍是必填。

### Pydantic

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class Arguments(BaseModel):
    model_config = ConfigDict(extra="forbid")     # 多給欄位就拒絕

class LogArgs(Arguments):                         # 繼承上面的規矩
    service: Literal["order-api", "payment-api"]
    limit: int = Field(default=10, ge=1, le=50)   # 範圍 1～50

print(LogArgs(service="order-api").limit)         # 10
try:
    LogArgs(service="order-api", limit=999)
except ValidationError as exc:
    print("擋下：", exc.errors()[0]["msg"])
```

為什麼 Agent 到處用它：模型給的工具參數可能亂寫，Pydantic 在執行前擋下。
完整版見 [models.py](../../projects/incident-autonomous-agent/oncall_agent/models.py#L11)。

### Annotated

`Annotated[型別, 附註]`：Python 本身忽略附註，**框架會讀它**。

```text
class Demo(TypedDict):
    overwrite: list                              # 新值蓋掉舊值
    appended: Annotated[list, operator.add]      # LangGraph：新值接在舊值後面
```

---

## 第 5 層：讀框架程式碼

### `@` 裝飾器

**`@deco` 放在函式上方，等同定義完後執行 `f = deco(f)`。**

```python
registry = {}

def tool(func):
    registry[func.__name__] = func     # 登記
    return func

@tool
def read_logs(service):
    """讀某個服務的日誌。"""
    return f"{service} 的日誌"

print(list(registry))        # ['read_logs']
print(read_logs.__doc__)     # 讀某個服務的日誌。
```

看到 `@xxx` 就問：**它把我的函式登記到哪，或加了什麼功能？**

| 看到 | 意思 |
|---|---|
| `@tool`、`@function_tool`、`@mcp.tool` | 把函式變成模型可呼叫的工具；docstring 是給模型看的說明 |
| `@app.get("/health")` | 這個網址交給這個函式處理 |
| `@dataclass` | 幫類別自動產生 `__init__` 等方法 |
| `@property` | 呼叫時不用括號 |
| `@classmethod` | 收到的是類別 `cls`，常用來提供另一種建立方式 |
| `@field_validator("service")` | Pydantic 驗證該欄位時多跑這段 |
| `@contextmanager`、`@asynccontextmanager` | 讓函式能搭配 `with`／`async with` |
| `@observe`、`@opik.track` | 記錄呼叫過程（追蹤） |
| `@lru_cache` | 相同參數直接回傳上次結果 |
| `@pytest.fixture` | 測試的準備材料 |

`@classmethod` 例子是 [`Settings.from_env()`](../../projects/incident-autonomous-agent/oncall_agent/models.py#L71)：不先建物件，直接「從環境變數建一個」。

注意：LangChain 的 `@tool` 會把函式換成**工具物件**，要用 `read_logs.invoke({...})` 呼叫。

### `with`：借了一定歸還

`yield` 之前是借，之後是還。中途出錯也會歸還。

```python
from contextlib import contextmanager

@contextmanager
def connect():
    print("開連線")
    try:
        yield "conn"          # 交給 with 區塊使用
    finally:
        print("關連線")

with connect() as conn:
    print("使用", conn)
```

真實版本：[`Operations.connect`](../../projects/incident-autonomous-agent/oncall_agent/storage.py#L77)。

### `async` / `await`：等待時先做別的事

```python
import asyncio

async def fetch():
    await asyncio.sleep(0.1)     # 等待期間讓出控制權
    return "ok"

print(asyncio.run(fetch()))      # 一般程式的進入方式
```

只寫 `fetch()` 不會執行，只拿到一個待執行的 coroutine。
在 notebook 裡直接寫 `await fetch()`（那裡不能用 `asyncio.run`）。

### 另外兩個高頻寫法

```python
jobs = {"a": lambda: 1 + 1}          # lambda：沒名字的小函式，先存起來不執行
print(jobs["a"]())                   # 2    加括號才執行

def call(model, temperature):
    return f"{model} {temperature}"

config = {"model": "qwen", "temperature": 0}
print(call(**config))                # qwen 0    把 dict 攤開成具名參數
```

---

## 讀碼速查：四個問題

打開一個陌生的類別，依序問：

1. **括號裡繼承誰？** → 決定它是資料類別、框架填空，還是專屬名稱。
2. **`__init__` 收了什麼？** → 它手上有哪些零件。
3. **哪些方法沒有 `_`？** → 外面能按的按鈕。
4. **方法上面有 `@` 嗎？** → 誰會來呼叫它。

| 第 1 題看到 | 直接判斷 |
|---|---|
| `(BaseModel)` | 會驗證的資料 |
| `(TypedDict)` | 有欄位說明的 dict |
| `(BaseXxx)` | 框架填空，找被覆寫的方法 |
| `(XxxError)` | 自訂例外 |
| 沒有括號 | 一般類別，看 `__init__` |

---

## 自我檢查

```text
class SearchTool(BaseTool):
    def __init__(self, index):
        super().__init__()
        self._index = index

    @property
    def size(self):
        return len(self._index)

    def _run(self, query):
        return self._index.search(query)
```

（虛構範例）

1. `SearchTool` 和 `BaseTool` 是什麼關係？`SearchTool` 和 `index` 呢？
2. `size` 怎麼讀取？能直接指派嗎？
3. `_run` 大概誰在呼叫？
4. 工具參數要檢查範圍，該用 `TypedDict` 還是 `BaseModel`？

<details>
<summary>答案</summary>

1. 繼承（是一種）；組合（擁有）。
2. `tool.size`，不加括號；沒有 setter，不能指派。
3. 框架（父類別裡的固定流程）。
4. `BaseModel`，`TypedDict` 執行時不驗證。

</details>
