# 白話搞懂 `collections.abc` 與底線命名

範例取自本課程的 `course_utils/llm.py`。

讀完你應該看得懂這兩行在幹嘛：

```text
from collections.abc import Iterator      ← 第一部分
def _endpoints() -> list[Endpoint]:       ← 第二部分
```

---

# 第一部分：`collections.abc`

## 1. 一句話版本

**`collections.abc` 是一本「能力規格清單」：它描述一個東西「會做什麼」，不管它「實際上是什麼」。**

生活比喻：USB-C 插孔。

- 充電器不在乎你插的是手機、耳機還是筆電。
- 它只在乎：**你有沒有符合 USB-C 規格？**

| 比喻 | Python |
|---|---|
| USB-C 規格 | `Iterable`、`Iterator`、`Mapping` …（抽象型別） |
| 手機、耳機、筆電 | `list`、`dict`、你自己寫的類別（具體型別） |
| 充電器 | 使用這些東西的函式 |

## 2. 三個名字先分清楚

| 名字 | 白話 | 例子 |
|---|---|---|
| `collections` | 工具箱：**拿來裝資料**的特製容器 | `Counter`、`deque`、`defaultdict` |
| `collections.abc` | 規格書：**描述容器能力** | `Iterable`、`Iterator`、`Mapping` |
| `abc` | 讓你**自己寫規格書**的工具 | `ABC`、`abstractmethod` |

`abc` = **A**bstract **B**ase **C**lass（抽象基底類別）：

- **Class**：類別。
- **Base**：給別人繼承的底版。
- **Abstract**：只寫「必須有哪些功能」，不能直接拿來建立物件。

## 3. 為什麼需要它？

假設你要寫一個「加總」函式：

```python
def total(nums: list[int]) -> int:
    return sum(nums)
```

標註寫 `list`，意思是「請給我 list」。但 `sum` 其實什麼都能加：

```python
def total(nums) -> int:
    return sum(nums)

total([1, 2, 3])                 # list
total((1, 2, 3))                 # tuple
total({1, 2, 3})                 # set
total(n for n in range(4))       # generator
```

這四種東西型別都不同，共通點只有一個：**可以用 `for` 一個一個拿出來**。

這個能力的名字就叫 `Iterable`：

```python
from collections.abc import Iterable

def total(nums: Iterable[int]) -> int:
    return sum(nums)
```

> **注意**：型別標註只是「說明書」。Python 執行時**不會檢查**，傳錯型別不會在函式入口被擋下。
> 檢查它的是 VS Code（Pylance）、mypy 這類工具。

## 4. 常用的五種能力

| 名稱 | 白話：它能做什麼 | 常見例子 |
|---|---|---|
| `Iterable` | 可以 `for x in 它` | `list`、`str`、`dict`、`set` |
| `Iterator` | 可以 `next(它)` 一次拿一個，**拿完就沒了** | generator、開啟的檔案 |
| `Sequence` | 有順序，可以 `它[0]`、`len(它)` | `list`、`tuple`、`str` |
| `Mapping` | 用 key 查 value：`它["name"]` | `dict` |
| `Callable` | 可以加括號呼叫：`它()` | 函式、類別 |

可以用 `isinstance` 問「你有沒有這個能力？」：

```python
from collections.abc import Iterable, Iterator, Mapping, Sequence

nums = [1, 2, 3]
print(isinstance(nums, Iterable))     # True
print(isinstance(nums, Sequence))     # True
print(isinstance(nums, Mapping))      # False
print(isinstance(nums, Iterator))     # False  ← 下一節解釋
```

## 5. 重點：`Iterable` vs `Iterator`

| | 比喻 | 能重複走訪嗎 |
|---|---|---|
| `Iterable` | **一本書**：可以從頭翻很多次 | `list` 這類容器可以 |
| `Iterator` | **書籤**：記得看到哪，只能往後 | 不行，走完就空了 |

每個 `Iterator` 都是 `Iterable`，反過來不成立。

```python
nums = [1, 2, 3]          # Iterable
it = iter(nums)           # 向它要一個 Iterator

print(next(it))           # 1
print(next(it))           # 2
print(list(it))           # [3]   只剩沒拿過的
print(list(it))           # []    空了
print(list(nums))         # [1, 2, 3]  原本的 list 不受影響
```

## 6. 回到本課程：`stream()`

函式裡只要出現 `yield`，呼叫它就會得到一個 **generator**（`Iterator` 的一種）。

| | `return` | `yield` |
|---|---|---|
| 行為 | 交出結果，函式**結束** | 交出一個值，函式**暫停**，下次從這裡繼續 |
| 比喻 | 整桌菜一次上齊 | 做好一道上一道 |

簡化版的 `stream()`：

```python
from collections.abc import Iterator

def stream() -> Iterator[str]:
    yield "你"
    yield "好"
    yield "！"

for piece in stream():
    print(piece, end="")      # 你好！
```

真正的 `course_utils/llm.py` 一樣，只是文字片段來自模型。所以聊天畫面能一個字一個字跳出來。

`-> Iterator[str]` 讀作：「我會**一段一段**給你字串。」因此：

```python
# result = stream()
# result[0]       ← TypeError：Iterator 不能用編號取值
# len(result)     ← TypeError：Iterator 不知道總共有幾個

full_text = "".join(stream())   # 想要完整字串就全部接起來
```

## 7. 進階：自己做一個容器

繼承規格、補上必要功能，就會**免費得到其他功能**：

```python
from collections.abc import Sequence

class Deck(Sequence):
    def __init__(self, cards):
        self.cards = cards

    def __getitem__(self, i):     # 必寫：怎麼用編號取值
        return self.cards[i]

    def __len__(self):            # 必寫：有幾個
        return len(self.cards)

d = Deck(["A", "K", "Q"])
print("K" in d)                   # True            免費
print(list(reversed(d)))          # ['Q', 'K', 'A'] 免費
print(d.index("Q"))               # 2               免費
```

少寫 `__len__`，執行 `Deck(...)` 時就會立刻 `TypeError`。

## 8. 進階：自己寫規格（`abc` 模組）

想規定「所有模型客戶端都必須有 `chat`」：

```python
from abc import ABC, abstractmethod

class ChatModel(ABC):
    @abstractmethod
    def chat(self, text: str) -> str:
        """子類別一定要實作。"""

class EchoModel(ChatModel):
    def chat(self, text: str) -> str:
        return f"你說：{text}"

print(EchoModel().chat("嗨"))     # 你說：嗨
# ChatModel()                     ← TypeError：抽象類別不能直接建立
```

---

# 第二部分：底線命名

## 1. 總表

| 寫法 | 白話意思 | Python 會強制嗎 | 常見程度 |
|---|---|---|---|
| `name` | 公開，大家都能用 | — | 天天見 |
| `_name` | 「內部用的，外面別碰」 | 否，只是約定 | 很常見 |
| `__name` | 類別內避免子類別撞名 | 會改名 | 少見 |
| `__name__` | Python 規定的特殊名稱 | Python 會自動使用 | 很常見 |
| `name_` | 避開保留字 | 否 | 偶爾 |
| `_` | 「這個值我不要」 | 否 | 常見 |

底線數量看**前後**：只有前面一個、前面兩個、前後各兩個，意思完全不同。

## 2. `_name`：員工專用門

比喻：門上貼「員工專用」。**門沒上鎖**，但你知道不該進去。

`course_utils/llm.py` 裡：

```text
def _endpoints()    ← 內部零件
def _client(ep)     ← 內部零件

def chat(...)       ← 給你用的
def stream(...)     ← 給你用的
def embed(...)      ← 給你用的
```

作者的意思是：「你用 `chat`、`stream`、`embed` 就好。底線開頭那兩個我之後可能改掉，別依賴它。」

實際效果：

- `from course_utils.llm import _client` **照樣可以**，Python 不擋。
- `from course_utils.llm import *` 預設**不會帶入**底線開頭的名稱（模組若有定義 `__all__`，以它列出的為準）。
- 編輯器自動完成通常把它排在後面。

## 3. `__name`：自動加上類別名稱

只在 **class 裡面**有作用。Python 會把 `__secret` 改名成 `_類別名__secret`。這叫 **name mangling**（名稱改編）。

用途：避免子類別不小心蓋掉父類別的變數。

```python
class Parent:
    def __init__(self):
        self.__token = "parent"      # 實際名稱：_Parent__token

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__token = "child"       # 實際名稱：_Child__token

c = Child()
print(c.__dict__)
# {'_Parent__token': 'parent', '_Child__token': 'child'}  兩個並存
print(c._Parent__token)              # parent  ← 仍拿得到，所以不是安全機制
```

日常寫程式用 `_name` 就夠了。

## 4. `__name__`：Python 的暗號（dunder）

前後各兩個底線，唸作 **dunder**（**d**ouble **under**score）。

這些名稱由 Python 定好意義，**你寫它、Python 在適當時機呼叫它**：

| 你寫的 | 實際觸發的是 |
|---|---|
| `Deck([...])` | `__init__`（物件建立後做初始化） |
| `len(d)` | `d.__len__()` |
| `d[0]` | `d.__getitem__(0)` |
| `for x in d` | `d.__iter__()`（`Sequence` 已幫你寫好） |
| `"K" in d` | `d.__contains__("K")` |
| `next(it)` | `it.__next__()` |
| `print(d)` | `d.__str__()` |

這就接回第一部分：**`collections.abc` 的「能力」，就是看你有沒有實作對應的 dunder 方法。**

| 能力 | 必須實作 |
|---|---|
| `Iterable` | `__iter__` |
| `Iterator` | `__iter__`、`__next__` |
| `Callable` | `__call__` |
| `Sequence` | `__getitem__`、`__len__`（並且要繼承 `Sequence`） |
| `Mapping` | `__getitem__`、`__len__`、`__iter__`（並且要繼承 `Mapping`） |

前三種只要方法存在，`isinstance` 就回 `True`；`Sequence`、`Mapping` 要明確繼承（或註冊）才算。

```python
from collections.abc import Iterator

class CountDown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 0:
            raise StopIteration      # 告訴 for：沒有下一個了
        self.n -= 1
        return self.n + 1

print(isinstance(CountDown(3), Iterator))   # True，即使沒有繼承
print(list(CountDown(3)))                   # [3, 2, 1]
```

另外幾個不是方法、但常看到的：

| 名稱 | 意思 |
|---|---|
| `__name__` | 目前模組的名字。直接執行該檔案時是 `"__main__"` |
| `__file__` | 目前這個檔案的路徑 |
| `__dict__` | 物件身上的屬性清單 |

```python
if __name__ == "__main__":
    print("只有直接執行這個檔案才會跑；被 import 時不會")
```

`from __future__ import annotations`（`llm.py` 也有）：讓型別標註延後解讀，不在定義函式的當下就計算。

> **規則**：不要自己發明 `__xxx__` 名稱，這個格式保留給 Python。
> 有些套件也借用此格式當特殊標記，例如本專案 LangGraph 流程裡的字串 `"__interrupt__"`，那是套件的約定。

## 5. `name_` 與 `_`

```python
class_ = "A 班"                 # class 是保留字，後面加底線避開

for _ in range(3):              # 不需要迴圈編號
    print("hi")

name, _ = ("qwen", "3b")        # 第二個值不要
print(name)                     # qwen
```

---

# 自我檢查

1. `def f(x: Iterable[str])` 可以傳 `set` 嗎？
2. 同一個 generator 跑兩次 `for`，第二次會看到什麼？
3. `_client` 可以被別的檔案 import 嗎？應該這樣做嗎？
4. `len(obj)` 背後呼叫哪個方法？

<details>
<summary>答案</summary>

1. 可以，`set` 能用 `for` 走訪。
2. 什麼都沒有，第一次已經拿完。
3. 技術上可以；不應該，它是內部零件。
4. `obj.__len__()`。

</details>
