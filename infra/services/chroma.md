# Chroma：向量資料庫（M3）

Chroma 存 embedding 向量，用「意思相近」找文件片段。它有兩種用法：

| 模式 | 怎麼連 | 什麼時候用 |
|---|---|---|
| 內嵌（notebook 預設） | `chromadb.PersistentClient(path="./chroma_db")` | 自己一個人做實驗。資料是本機一個資料夾，**不用開任何服務** |
| 伺服器 | `chromadb.HttpClient(host="localhost", port=8000)` | 多個程式要共用同一份資料（例如旗艦專案的 agent 和建索引腳本） |

M3 的 notebook 用內嵌模式就能跑完。下面是伺服器模式的部署流程。

## 啟動

```bash
cd infra
docker compose up -d chroma
```

資料存在 Docker volume `aiagent_chroma`（容器內 `/data`），關掉容器不會遺失。

## 確認活著

```bash
curl http://localhost:8000/api/v2/heartbeat
```

用 Python 寫入再讀回：

```python
import chromadb
client = chromadb.HttpClient(host="localhost", port=8000)
col = client.get_or_create_collection("smoke")
col.add(ids=["a"], documents=["魯夫是草帽海賊團船長"], embeddings=[[0.1, 0.2, 0.3]])
print(col.count())          # 1
client.delete_collection("smoke")
```

## 版本要對齊

伺服器映像（`CHROMA_TAG`，預設 1.5.9）和 Python 套件 `chromadb` 要用同一個版本，差太多會連線失敗或 API 不符。
查 Python 端版本：`uv run python -c "import chromadb; print(chromadb.__version__)"`。

## 關掉、清掉

```bash
docker compose stop chroma        # 暫停
docker compose rm -sf chroma      # 移除容器，資料保留
docker volume rm aiagent_chroma   # 刪資料（要先移除容器）
```

## 常見問題

| 症狀 | 修法 |
|---|---|
| 網路上的範例設了 `IS_PERSISTENT`、`PERSIST_DIRECTORY`，掛載 `/chroma/chroma` | 那是 0.x 舊版設定。1.x 映像預設就持久化，資料在 `/data` |
| 8000 埠被佔用 | 改 `infra/.env` 的 `CHROMA_PORT`，程式裡的 `port=` 一起改 |
