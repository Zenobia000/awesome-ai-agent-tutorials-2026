# Ollama：本地模型服務（M1 起全課）

Ollama 是一個在本機跑開放權重模型的服務，對外提供 OpenAI 相容的 API（`http://localhost:11434/v1`）。
課程程式碼只認這個網址（repo 根目錄 `.env` 的 `LOCAL_BASE_URL`），所以你用哪一種方式部署都可以。

## 選一種部署方式

| 你的環境 | 建議 | 原因 |
|---|---|---|
| macOS | **原生安裝** | Docker 在 macOS 拿不到 GPU，容器版只能用 CPU |
| Windows | 原生安裝（最簡單）或 Docker Desktop＋WSL2 | 兩種都吃得到 NVIDIA 卡 |
| Linux＋NVIDIA | Docker（本 repo compose） | 版本好控制、刪掉不留痕跡 |
| 沒有 GPU | 原生或 Docker 都行，選 3B 以下的小模型 | 或租雲端 GPU，見 [../cloud-gpu.md](../cloud-gpu.md) |

## A. 原生安裝

到 <https://ollama.com/download> 下載安裝檔（macOS、Windows），Linux 用：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

裝好後 Ollama 會在背景常駐。

## B. Docker 部署

### Linux 先裝 NVIDIA Container Toolkit（一次）

讓容器能用 GPU。Ubuntu／Debian：

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

> `systemctl restart docker` 會**重啟這台機器上所有容器**。共用機器先跟其他使用者講好。

確認容器看得到顯卡：

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

### 啟動

```bash
cd infra
docker compose -f compose.yml -f compose.gpu.yml up -d ollama   # 有 NVIDIA 卡
docker compose up -d ollama                                      # 只用 CPU
```

## 下載課程用的模型

| 模型 | 用途 | 大小 |
|---|---|---|
| `qwen2.5:3b` | 全課預設對話模型 | 約 1.9 GB |
| `bge-m3` | M3 起的 embedding 模型（中英文都能檢索） | 約 1.2 GB |

```bash
# 原生安裝
ollama pull qwen2.5:3b
ollama pull bge-m3

# Docker
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull bge-m3
```

顯存 16 GB 可以換更大的模型（例如 7B／8B 的 4-bit 量化版），改 repo 根目錄 `.env` 的 `LOCAL_MODEL` 就好。

## 確認活著

```bash
curl http://localhost:11434/api/version
curl http://localhost:11434/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"qwen2.5:3b","messages":[{"role":"user","content":"用一句話打招呼"}]}'
```

確認有用到 GPU：

```bash
ollama ps                                   # 原生；PROCESSOR 欄要是 100% GPU
docker compose exec ollama ollama ps        # Docker
docker compose logs ollama | grep "inference compute"   # 要看到 library=CUDA 和你的顯卡名稱
```

## 設定

| 變數 | 作用 | 本 repo 預設 |
|---|---|---|
| `OLLAMA_CONTEXT_LENGTH` | context 長度；Ollama 原廠預設 4096，超過會被**靜默截斷** | 8192 |
| `OLLAMA_KEEP_ALIVE` | 模型閒置多久後從顯存卸載 | 10m |
| `OLLAMA_HOST` | 監聽位址；要讓別台機器連進來才設 `0.0.0.0` | 只聽本機 |

Docker 版改 `infra/.env`；原生版在系統環境變數裡設，然後重啟 Ollama。

## 關掉、清掉

```bash
docker compose stop ollama                  # 暫停，模型保留
docker compose exec ollama ollama rm qwen2.5:3b   # 刪單一模型
docker compose down -v                      # 連同所有已下載模型一起刪
```

## 常見問題

| 症狀 | 修法 |
|---|---|
| `CUDA out of memory` 或載入就崩潰 | 換小一號的模型或 4-bit 量化版；`ollama ps` 看是否有別的模型還佔著顯存 |
| 回答忽略了長文件的後半段 | context 被截斷：調大 `OLLAMA_CONTEXT_LENGTH` |
| 本機已有一個 Ollama，又起了 Docker 版 | 兩個都搶 11434 埠和顯存；只留一個，或把 Docker 版改 `OLLAMA_PORT` |
| n8n 容器連不到 Ollama | 在容器裡要填 `http://host.docker.internal:11434`，不是 `localhost` |
