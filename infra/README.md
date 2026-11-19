# 部署：課程用到的容器服務

本課所有「要另外開一個服務」的東西都在這裡：怎麼裝、怎麼開、怎麼確認活著、怎麼關、怎麼清。
notebook 本身不在容器裡跑，它用 `localhost:<埠號>` 連這些服務。

## 先看你需要哪些

| 服務 | 用在 | 一定要開？ | 怎麼部署 | 埠號 | 流程 |
|---|---|---|---|---|---|
| Ollama | M1 起全課 | 是 | 本 repo `compose.yml`，或原生安裝 | 11434 | [services/ollama.md](services/ollama.md) |
| Chroma | M3-02 起 | 否（notebook 預設內嵌模式） | 本 repo `compose.yml` | 8000 | [services/chroma.md](services/chroma.md) |
| Neo4j | M4、旗艦專案 | M4-03 起要 | 本 repo `compose.yml` | 7474、7687 | [services/neo4j.md](services/neo4j.md) |
| PostgreSQL | M5（選做）、旗艦專案 | 否（M5 notebook 用記憶體 checkpointer；換成 PostgresSaver 時才要） | 本 repo `compose.yml` | 5432 | [services/postgres.md](services/postgres.md) |
| n8n | M7 | 否（低代碼示範） | 本 repo `compose.yml` | 5678 | [services/n8n.md](services/n8n.md) |
| Langfuse | M8-03 | 否（可用雲端免費版） | 官方 compose（多容器） | 3000 | [services/langfuse.md](services/langfuse.md) |
| Opik | M8-04 | 否（可用雲端免費版） | 官方腳本（多容器） | 5173 | [services/opik.md](services/opik.md) |

沒有 GPU、或顯卡太小：看 [cloud-gpu.md](cloud-gpu.md)。只有模型推論和微調需要 GPU，其他服務都在筆電上用 CPU 跑。

## 第 0 步：裝 Docker（一次）

| 系統 | 安裝 | GPU |
|---|---|---|
| Windows | Docker Desktop，啟用 WSL2 後端 | NVIDIA 卡在 WSL2 可用，要先裝最新的 Windows 版 NVIDIA 驅動 |
| macOS | Docker Desktop | **容器拿不到 GPU**。Ollama 改用原生安裝才吃得到 Apple 晶片的加速 |
| Linux | Docker Engine ＋ Compose plugin | 要另裝 NVIDIA Container Toolkit（見 [services/ollama.md](services/ollama.md)） |

確認版本（Compose 2.x 即可）：

```bash
docker --version
docker compose version
```

## 第 1 步：設定

```bash
cd infra
cp .env.example .env      # 填 NEO4J_PASSWORD、POSTGRES_PASSWORD；.env 不要 commit
```

`infra/.env` 只給容器用；repo 根目錄的 `.env` 給 notebook 用，兩邊的密碼和埠號要一致。

## 第 2 步：開服務

每個服務屬於它用到的模組的 profile，`--profile mN` 會一次開好那一章需要的全部服務：

```bash
docker compose --profile m1 up -d          # Ollama
docker compose --profile m3 up -d          # Ollama ＋ Chroma
docker compose --profile m4 up -d          # Ollama ＋ Neo4j
docker compose --profile m5 up -d          # Ollama ＋ PostgreSQL
docker compose --profile m7 up -d          # Ollama ＋ n8n
docker compose up -d neo4j                 # 只開單一服務
```

Linux／WSL2 有 NVIDIA 卡，Ollama 要吃 GPU 就多疊一個檔：

```bash
docker compose -f compose.yml -f compose.gpu.yml --profile m1 up -d
```

## 第 3 步：確認活著

```bash
docker compose ps                          # STATUS 要是 Up，有 healthcheck 的要 (healthy)
docker compose logs -f neo4j               # 起不來時看 log
```

各服務的連線測試指令在各自的流程檔。

## 第 4 步：關掉、清掉

| 想做的事 | 指令 | 資料 |
|---|---|---|
| 暫停，下次接著用 | `docker compose --profile all stop` | 保留 |
| 移除容器 | `docker compose --profile all down` | 保留（在 volume 裡） |
| 連資料一起砍掉重來 | `docker compose --profile all down -v` | **全部刪除，含已下載的模型** |

`down -v` 只會刪本專案（project 名稱 `aiagent`）的 volume，不會動到你機器上別的容器。

## 常見問題

| 症狀 | 原因 | 修法 |
|---|---|---|
| `port is already allocated` | 本機已有服務佔用同一埠號（例如自己裝過 Postgres） | 改 `infra/.env` 的 `*_PORT`，再同步改 repo 根目錄 `.env` 的連線網址 |
| `set NEO4J_PASSWORD in infra/.env` | 沒設密碼 | 照提示填 `.env`；Neo4j 密碼至少 8 字元 |
| 容器裡連不到本機的 Ollama | 容器裡的 `localhost` 是容器自己 | 用 `http://host.docker.internal:11434`；同一個 compose 裡的服務直接用服務名，例如 `http://ollama:11434` |
| 模型跑得很慢，`nvidia-smi` 沒有 ollama | 容器沒拿到 GPU | Linux 確認裝了 NVIDIA Container Toolkit 並疊了 `compose.gpu.yml`；macOS 改原生安裝 |
| 磁碟被吃光 | 模型和映像檔累積 | `docker system df` 看用量；`docker exec aiagent-ollama-1 ollama rm <模型>` 刪不用的模型 |

## 版本

`compose.yml` 釘住了映像版本（2026-11 驗證過）：Ollama 0.40.16、Chroma 1.5.9、Neo4j 2026.10.2 community、PostgreSQL 17、n8n stable。
要升級就改 `infra/.env` 裡對應的 `*_TAG`，再 `docker compose pull && docker compose up -d`。
Chroma 伺服器和 Python 套件 `chromadb` 的版本要對得上，升級時兩邊一起升。
