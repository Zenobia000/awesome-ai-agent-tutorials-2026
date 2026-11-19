# Langfuse：LLM 追蹤與評估（M8-03，選用）

Langfuse 記錄每次 LLM 呼叫的 trace（輸入、輸出、耗時、token、成本），還能把評分寫回去。

## 先選：雲端免費版，還是自架

| | 雲端（建議上課用） | 自架 |
|---|---|---|
| 要準備什麼 | 到 <https://cloud.langfuse.com> 註冊，建專案拿金鑰 | Docker，約 4 核、16 GB 記憶體 |
| `.env` 設定 | `LANGFUSE_HOST=https://cloud.langfuse.com` | `LANGFUSE_HOST=http://localhost:3000` |
| 資料在哪 | Langfuse 的伺服器 | 你自己的機器 |

公司資料不能出去、或想學整套怎麼架，才選自架。repo 根目錄 `.env.example` 預設就是雲端。

## 自架流程

自架版由 web、worker、PostgreSQL、ClickHouse、Redis、MinIO 六個容器組成，用官方 compose 檔，不放進本 repo 的 `compose.yml`。

> 依 Langfuse v4 官方文件整理（2026-11 最新版 v4.82.0），尚未在課程機器上完整實測。官方說明 Docker Compose 只適合試用，沒有高可用與備份。

```bash
# 1. 在 repo 以外的地方取得官方設定
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

2. 打開 `docker-compose.yml`，每一行標了 `# CHANGEME` 的密碼和金鑰都換成隨機長字串（可用 `openssl rand -hex 32` 產生）。

```bash
# 3. 啟動，約 2～3 分鐘後 langfuse-web 的 log 會出現 Ready
docker compose up -d
docker compose logs -f langfuse-web
```

4. 打開 <http://localhost:3000>，按 Sign up 建立第一個帳號（沒有預設帳號），再建組織與專案。
5. 到專案設定建立 API key，填進 repo 根目錄 `.env`：

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000
```

## 埠號衝突

官方 compose 會佔用 3000（網頁）和 9090（MinIO）等埠號。和本機其他服務撞埠時，改 `docker-compose.yml` 裡 `ports:` 冒號**左邊**的數字。

## 停止、清除

```bash
docker compose down        # 移除容器，trace 資料保留
docker compose down -v     # 連所有 trace、帳號一起刪
```
