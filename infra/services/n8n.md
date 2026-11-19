# n8n：低代碼自動化（M7，選用）

n8n 用拖拉節點的方式串工作流（定時、Webhook、通訊軟體、資料庫、LLM）。M7 用它對照「固定流程交給低代碼」的那一側。

## 啟動

```bash
cd infra
docker compose up -d n8n
```

打開 <http://localhost:5678>，第一次會要你建立擁有者帳號（只存在本機）。
工作流、帳號、憑證都存在 volume `aiagent_n8n`；裡面也有加密金鑰，**刪了這個 volume，存過的憑證就解不開**。

## 確認活著

```bash
curl http://localhost:5678/healthz          # {"status":"ok"}
```

## 接本機的 Ollama

在 n8n 新增 Ollama 憑證，Base URL 填：

| Ollama 怎麼裝的 | Base URL |
|---|---|
| 本 repo compose（同一個 Docker 網路） | `http://ollama:11434` |
| 原生安裝在本機 | `http://host.docker.internal:11434`（本 repo 已幫 Linux 加上這個名稱） |

Linux 上原生安裝的 Ollama 預設只聽 `127.0.0.1`，容器連不到；要設 `OLLAMA_HOST=0.0.0.0` 再重啟 Ollama，並確認防火牆沒有對外開放 11434。

## 關掉、清掉

```bash
docker compose stop n8n
docker compose rm -sf n8n && docker volume rm aiagent_n8n   # 工作流與憑證一起刪
```

## 注意

- 本 repo 設了 `N8N_SECURE_COOKIE=false`，只為了本機用 http 登入。要放到外網就改走 https 並拿掉這行。
- 映像用 `stable` 標籤；要固定版本，在 `infra/.env` 設 `N8N_TAG=<版本號>`。
