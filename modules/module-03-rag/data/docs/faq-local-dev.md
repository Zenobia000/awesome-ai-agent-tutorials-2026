# 本機開發環境 FAQ

> 服務：通用｜類型：FAQ｜版本：-｜負責團隊：平台組｜更新：2026-09-15

## 怎麼把整套服務跑起來

用 `hfdev up` 啟動 docker compose，會起好 PostgreSQL、Redis、Kafka 與各服務的開發版。第一次約需 10 分鐘下載映像檔。

## 各服務本機埠號

| 服務 | 埠號 |
|---|---|
| breakwater | 8080 |
| anchor-order | 8081 |
| harbor-stock | 8082 |
| gull-notify | 8083 |
| lighthouse-auth | 8084 |
| tide-pay（模擬收單行） | 8443 |

## 測試用信用卡

本機與測試環境的 tide-pay 連的是模擬收單行：

- `4000 0000 0000 0002`：永遠授權成功。
- `4000 0000 0000 0010`：觸發 TP-4030 拒絕。
- `4000 0000 0000 0028`：模擬 3D 驗證逾時，觸發 TP-4012。

## 常見問題

- Kafka 起不來：多半是 Docker 記憶體不足，需要至少 8GB。
- 登入一直失敗：本機的 lighthouse-auth 每次重啟會產生新金鑰，執行 `hfdev reset-auth` 清掉舊權杖。
