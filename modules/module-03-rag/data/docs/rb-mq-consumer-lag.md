# Runbook：current-mq 消費落後（consumer lag）

> 服務：current-mq｜類型：runbook｜版本：Kafka 3.7.1｜負責團隊：平台組｜更新：2026-09-30

## 症狀

- 警報：某個 consumer group 的 lag 超過 50,000 筆。
- 使用者抱怨通知很慢、出貨狀態沒更新。

## 處理步驟

1. 找出是哪個 consumer group：`hfctl mq lag --top 5`。
2. 看消費者是否還活著：pod 數量、最近一次 commit offset 的時間。
3. 消費者都活著只是太慢：擴充消費者數量，但**上限是分區數**。`hf.notify.request.v2` 是 24 個分區，最多開 24 個消費者。
   指令：`hfctl scale gull-notify-consumer --replicas 24`。
4. 消費者卡在某一筆壞訊息（poison message）：日誌會一直重試同一個 offset。把那筆移到死信 topic：
   `hfctl mq skip --group <group> --partition <p> --offset <o> --to-dlq`。需要第二人核准。
5. lag 超過 100 萬筆，或保存期限 72 小時內消化不完，升級 SEV1，否則會掉資料。

## 參考

2026 年 9 月壓測事故 INC-2026-0921。
