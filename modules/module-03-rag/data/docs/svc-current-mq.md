# current-mq 訊息佇列服務說明

> 服務：current-mq｜類型：服務說明｜版本：Kafka 3.7.1｜負責團隊：平台組｜更新：2026-09-25

## 這個服務做什麼

current-mq 是海風內部的事件匯流排，底層是 Kafka 3.7.1，三台 broker（`mq-b1`～`mq-b3`）。
服務之間的非同步通知都走這裡，例如付款成功、訂單出貨、庫存變動。

## topic 命名規則

格式為 `hf.<領域>.<事件>.v<版本>`，例如：

- `hf.payment.authorized.v1`：付款授權成功（tide-pay 發出）
- `hf.order.shipped.v1`：訂單出貨（anchor-order 發出）
- `hf.notify.request.v2`：要求發送通知（gull-notify 消費）

事件格式要改動時開新版本號的 topic，舊版至少並存 30 天。

## 保存與分區

- 預設保存 72 小時（`retention.ms=259200000`）。
- 一般 topic 12 個分區；`hf.notify.request.v2` 是 24 個分區，因為量最大。
- 複本數 3，`min.insync.replicas=2`。

## 監控

- consumer lag（消費落後筆數）超過 50,000 筆發出 SEV2 警報。
- 單一 broker 磁碟用量超過 80% 發出 SEV2 警報。
- 消費者數量不能超過分區數，多開的消費者會閒置。
