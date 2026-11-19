# 沒有 GPU：租雲端算力

**先講結論：大部分學員不用租。** 只有「跑模型」和「微調」吃 GPU；Neo4j、PostgreSQL、Chroma、n8n 這些服務用筆電 CPU 就夠。
真的要租，建議只把 Ollama 搬到雲端，其他服務留在筆電，用 SSH 通道把雲端的 Ollama 接回 `localhost:11434`。這樣 notebook 一行程式都不用改。

## 哪些實作需要 GPU

| 實作 | 沒 GPU 能跑嗎 | 建議 |
|---|---|---|
| M1-03 看 logits（Qwen2.5-0.5B） | 能，慢一點 | 筆電 CPU |
| 全課對話（`qwen2.5:3b`） | 能，一次回答約數秒到十幾秒 | 筆電 CPU；嫌慢再租 |
| M3 embedding（`bge-m3`） | 能，建索引時較慢 | 筆電 CPU |
| M6 LoRA 微調（Qwen2.5-0.5B） | 很慢，不建議 | Colab／Kaggle 免費 GPU，或租 |
| 想換 7B 以上的模型 | 不實際 | 租 24 GB 顯卡 |

## 推薦順序

價格是 2026-11 查詢的隨選（on-demand）價，會浮動，**下單前以官網為準**。

| 順位 | 平台 | 適合 | 參考價格 | 注意 |
|---|---|---|---|---|
| 1 | **Google Colab**／**Kaggle**（免費） | M6 微調、M1-03 這類單一 notebook | 免費。Kaggle 一般回報每週約 30 小時 T4／P100；Colab 免費版通常是 T4 | 官方不公布額度；單次工作階段最長約 12 小時；**不能跑 Docker**，關掉就重置 |
| 2 | **RunPod**（主推） | 整門課要一張穩定的 24 GB 顯卡 | RTX 4090：Community US$0.34／時、Secure US$0.89／時；A100 80GB：US$1.19～2.09／時 | 按秒計費；有官方 Ollama 教學；pod 本身是容器，**裡面不能再跑 Docker** |
| 3 | **Vast.ai** | 預算最緊 | RTX 4090 約 US$0.27／時起（市集價） | 個人出租的機器，可能中途斷線，沒有 SLA |
| — | TWCC（國網中心台灣 AI 雲） | 有研究計畫的學校單位 | 需申請 | 偏研究用途，個人臨時要用不方便 |
| — | AutoDL | 在中國大陸的學員 | 人民幣計價 | 註冊實名可能需要中國大陸手機號，台灣學員先確認 |

粗估：整門課真正用到 GPU 的時間約 10 小時，用 RunPod Community 的 RTX 4090 大約 US$3～4（以上述時價估算，不含儲存）。

## RunPod 流程：只把 Ollama 搬上雲

### 1. 開機

1. 註冊 RunPod、儲值（建議先設消費上限）。
2. 在 Settings 加入你的 SSH 公鑰（`~/.ssh/id_ed25519.pub`；沒有就先 `ssh-keygen -t ed25519`）。
3. Deploy 一個 Pod：GPU 選 RTX 4090（24 GB），範本選官方 PyTorch，Volume 給 30 GB 放模型；勾選 **SSH over exposed TCP**（要用它開通道）。

### 2. 在 Pod 裡裝 Ollama

Pod 是容器，沒有 systemd，也不能再跑 Docker，所以直接裝原生版並手動啟動：

```bash
curl -fsSL https://ollama.com/install.sh | sh
export OLLAMA_MODELS=/workspace/ollama          # 放在 Volume，關機後模型還在
nohup ollama serve > /workspace/ollama.log 2>&1 &
ollama pull qwen2.5:3b
ollama pull bge-m3
```

Ollama 只聽 Pod 內的 127.0.0.1，**不要**把 11434 埠公開到網路上：Ollama 沒有帳號密碼，公開了任何人都能用你的 GPU。

### 3. 從筆電開 SSH 通道

在 Pod 的 Connect 頁面找到公開 IP 和 SSH 埠號，然後在筆電上：

```bash
ssh -N -L 11434:localhost:11434 root@<Pod 公開 IP> -p <SSH 埠號> -i ~/.ssh/id_ed25519
```

這個指令會一直掛著，不要關。開著的時候，筆電的 `localhost:11434` 就是雲端那台的 Ollama。

> 筆電上原本有在跑 Ollama 的話，先關掉（或改用 `-L 11435:localhost:11434`，再把 `.env` 的 `LOCAL_BASE_URL` 改成 `http://localhost:11435/v1`）。

### 4. 確認接上了

```bash
curl http://localhost:11434/api/version
```

接著照常跑 notebook。Neo4j、PostgreSQL 這些容器照樣在筆電用 `infra/compose.yml` 開。

### 5. 用完一定要關

| 動作 | 計費 |
|---|---|
| Stop（停止） | GPU 停止計費；Volume 仍按月計費（閒置時 US$0.20／GB／月） |
| Terminate（終止） | 全部停止計費，**Volume 和模型一起刪除** |

下課就 Stop；整門課結束就 Terminate。

## 用 Colab／Kaggle 做 M6 微調

微調只需要一本 notebook 和一張 GPU，不需要任何容器服務：

1. 把 `modules/module-06-lora/` 的 `01_peft_finetune.ipynb` 上傳到 Colab 或 Kaggle，並把同資料夾的 `lab6_utils.py` 和 `data/` 一起上傳到 notebook 的工作目錄（notebook 會 import 前者、讀後者的 jsonl）。
2. 執行階段（Runtime）選 GPU（T4 即可，Qwen2.5-0.5B 放得下）。
3. 第一格先裝套件：`!pip install -q "peft>=0.13" "transformers>=4.45" "datasets>=3.0" "accelerate>=1.0"`（和本 repo `m6` 群組一致；Colab 已內建 torch）。
4. 訓練完把 LoRA 權重下載回筆電，再照 M6-02 合併、匯出給本機 Ollama。

免費額度用完或被斷線時，改用上面的 RunPod 流程。
