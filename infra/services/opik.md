# Opik：LLM 追蹤與內建評估指標（M8-04，選用）

Opik 和 Langfuse 是同一類工具：記 trace、跑評估。M8-04 用它看「內建評估指標」怎麼用。

## 先選：雲端免費版，還是自架

| | 雲端（建議上課用） | 自架 |
|---|---|---|
| 要準備什麼 | 到 <https://www.comet.com/opik> 註冊，拿 API key 和 workspace 名稱 | Docker、git |
| `.env` 設定 | 填 `OPIK_API_KEY`、`OPIK_WORKSPACE` | 兩個都留空，改用下面的本機設定 |

## 自架流程

自架版由前端、後端、MySQL、ClickHouse、Redis 等多個容器組成，用官方腳本啟動。

> 依 Opik 官方 local deployment 文件整理（2026-11 最新版 2.2.150），尚未在課程機器上完整實測。官方說明這套只適合本機試用，正式環境要用 Kubernetes。

```bash
# 1. 在 repo 以外的地方取得官方設定
git clone https://github.com/comet-ml/opik.git
cd opik

# 2. 啟動（Windows 用 PowerShell 執行 .\opik.ps1）
./opik.sh
```

3. 打開 <http://localhost:5173>。
4. 讓 Python SDK 連到本機，而不是雲端：

Opik 的 Python 套件裝在**相容環境**（`.venv-compat`，因為它還要求舊版 openai），安裝方式見 [modules/README.md](../../modules/README.md#兩個環境主環境與相容環境)：

```bash
UV_PROJECT_ENVIRONMENT=.venv-compat uv run --no-sync opik configure --use_local
```

或在程式裡：

```python
import opik
opik.configure(use_local=True)
```

## 停止、清除

```bash
./opik.sh --stop      # 停止所有容器
./opik.sh --clean     # 停止並刪除所有 Opik 資料（無法復原）
```
