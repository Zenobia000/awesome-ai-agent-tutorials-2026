# PostgreSQL：Agent 的持久狀態（M5、旗艦專案）

LangGraph 的 checkpointer 把每一步的狀態存下來，才能暫停、恢復、跨會話接續。
`InMemorySaver` 存在記憶體，程式一關就沒了；`PostgresSaver` 存進 PostgreSQL，重開機也還在。M5-B 的「審批暫停後恢復」要用後者。

## 啟動

```bash
cd infra
cp .env.example .env              # 第一次才要；填 POSTGRES_PASSWORD
docker compose up -d postgres
docker compose ps postgres        # 等到 (healthy)
```

## 確認活著

```bash
docker compose exec postgres psql -U agent -d agent -c "select version();"
```

## 接上 LangGraph

需要套件 `langgraph-checkpoint-postgres` 和 `psycopg[binary]`，主環境的 `m5` 群組沒有預裝，臨時加上即可：

```bash
uv run --with langgraph-checkpoint-postgres --with "psycopg[binary]" jupyter lab
```

連線字串格式：
`postgresql://<使用者>:<密碼>@localhost:5432/<資料庫>`。

```python
import os
from langgraph.checkpoint.postgres import PostgresSaver

url = f"postgresql://agent:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/agent"
with PostgresSaver.from_conn_string(url) as saver:
    saver.setup()                       # 第一次建表，之後重跑也安全
    graph = builder.compile(checkpointer=saver)
    graph.invoke(inputs, {"configurable": {"thread_id": "demo-1"}})
```

`thread_id` 區分不同會話；同一個 `thread_id` 再呼叫會接著上次的狀態。

看存了什麼：

```bash
docker compose exec postgres psql -U agent -d agent -c "select thread_id, checkpoint_id from checkpoints limit 5;"
```

## 關掉、清掉

```bash
docker compose stop postgres
docker compose rm -sf postgres && docker volume rm aiagent_postgres   # 連資料一起刪
```

## 常見問題

| 症狀 | 修法 |
|---|---|
| `port 5432 is already allocated` | 本機已裝了 PostgreSQL。改 `infra/.env` 的 `POSTGRES_PORT`（例如 5433），連線字串一起改 |
| 改了密碼登不進去 | 和 Neo4j 一樣，密碼只在第一次建資料庫時生效；刪 volume 重建，或進去用 `ALTER USER` 改 |
| `password authentication failed` | 確認 notebook 讀到的 `.env` 和 `infra/.env` 是同一組密碼 |
