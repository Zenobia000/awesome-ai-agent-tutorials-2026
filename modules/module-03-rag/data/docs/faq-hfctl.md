# hfctl 常用指令速查

> 服務：通用｜類型：FAQ｜版本：hfctl 4.2｜負責團隊：SRE｜更新：2026-10-15

所有正式環境操作都透過 `hfctl`，每個指令都會寫進稽核紀錄。標「需核准」的指令會先發核准請求給第二位值班人員。

## 唯讀（任何人可用）

| 指令 | 用途 |
|---|---|
| `hfctl tidepay acquirer-status` | 看兩家收單行的健康度 |
| `hfctl tidepay stats --code <錯誤碼> --group-by bin --last 1h` | 依卡號前 6 碼統計錯誤 |
| `hfctl mq lag --top 5` | 消費落後最多的 5 個 consumer group |
| `hfctl auth key-history` | 金鑰輪換紀錄 |

## 會改變狀態

| 指令 | 用途 | 需核准 |
|---|---|---|
| `hfctl tidepay failover --to acq-b` | 切換收單行 | 是 |
| `hfctl auth jwks refresh --all` | 強制下游重抓 JWKS | 否 |
| `hfctl auth rotate-key --confirm` | 輪換簽章金鑰 | 是 |
| `hfctl mq skip ... --to-dlq` | 把壞訊息移到死信 topic | 是 |
| `hfctl gw breaker reset --upstream <服務名>` | 手動重置熔斷器 | 否 |
| `hfctl stock queue-mode on --sku <SKU>` | 熱門商品排隊模式 | 否 |
| `hfctl search reindex --full` | 全量重建搜尋索引 | 否 |
| `hfctl deploy rollback <服務名> --to <版本>` | 回滾 | 否 |

## 安裝

`hfctl` 只能在跳板機 `jump-01` 上使用，本機無法連到正式環境。
