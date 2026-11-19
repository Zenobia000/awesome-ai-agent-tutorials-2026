# Neo4j：圖資料庫（M4、旗艦專案）

Neo4j 把資料存成「節點＋關係」，用 Cypher 查多跳關係（例如「魯夫的船員的師父是誰」）。
M4-01、02 用 networkx 在記憶體裡做，M4-03 起換成 Neo4j。

## 啟動

```bash
cd infra
cp .env.example .env              # 第一次才要；填 NEO4J_PASSWORD（至少 8 字元）
docker compose up -d neo4j
docker compose ps neo4j           # 等到 (healthy)，第一次要下載 APOC 外掛，約 30 秒
```

本 repo 的設定已經裝好 **APOC** 外掛：`langchain_neo4j` 讀圖的 schema 會用到它，沒裝會報 `apoc.meta` 找不到。

## 兩個入口

| 入口 | 網址 | 誰用 |
|---|---|---|
| 瀏覽器介面 | <http://localhost:7474> | 你，用來看圖、手打 Cypher。帳號 `neo4j`，密碼是 `.env` 裡的 `NEO4J_PASSWORD` |
| Bolt 協定 | `bolt://localhost:7687` | Python driver（notebook、旗艦專案） |

## 確認活著

```bash
docker compose exec neo4j cypher-shell -u neo4j -p <你的密碼> "RETURN apoc.version();"
```

Python 端（notebook、旗艦專案）一律從 repo 根目錄 `.env` 讀這三個變數，值要和 `infra/.env` 一致：

```dotenv
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=<和 infra/.env 相同>
```

```python
import os
from neo4j import GraphDatabase
with GraphDatabase.driver(os.environ["NEO4J_URI"],
                          auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])) as d:
    print(d.execute_query("RETURN 1 AS ok").records[0]["ok"])   # 1
```

改了 `NEO4J_BOLT_PORT` 的話，`NEO4J_URI` 的埠號要一起改。

## 清空圖（重做實驗時）

```cypher
MATCH (n) DETACH DELETE n
```

## 關掉、清掉

```bash
docker compose stop neo4j
docker compose rm -sf neo4j && docker volume rm aiagent_neo4j   # 連資料一起刪
```

## 常見問題

| 症狀 | 修法 |
|---|---|
| 改了 `.env` 的密碼，還是登不進去 | 密碼只在**第一次建資料庫**時生效。要嘛用舊密碼登入後改，要嘛刪掉 volume 重建 |
| 啟動後馬上退出，log 有 `password too short` | 密碼至少 8 字元 |
| 記憶體不夠、容器被殺 | 調小 `infra/.env` 的 `NEO4J_HEAP`（預設 1G）；教學資料量 512M 也夠 |
| 下載 APOC 失敗（沒有外網） | 外掛是啟動時從網路下載的。離線環境要先在有網路的地方建好映像 |
