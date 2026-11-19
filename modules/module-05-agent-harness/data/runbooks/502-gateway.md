# Runbook：web-gateway 回 502

適用：使用者下單出現 502 Bad Gateway。

1. 502 代表 gateway 的上游沒回應，問題通常不在 gateway 本身。
2. 先查 order-api 的日誌，看是不是 upstream timeout。
3. 如果 order-api 在等 order-db-proxy，改看資料庫連線池（見 db-connection-pool）。
4. 不要先重啟 web-gateway：重啟只會讓所有連線斷一次，502 不會消失。
