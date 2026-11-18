# Runbook：order-db-proxy 連線池用盡

徵兆：日誌出現 `connection pool exhausted`，指標 pool_used 到 50（上限 50）。

1. 先確認是不是慢查詢把連線卡住：搜尋日誌裡的 `slow query`。
2. 短期處理：重啟 order-db-proxy，可以清掉卡住的連線，大約 30 秒恢復。
3. 重啟屬於寫入動作，必須依「重啟規範」取得值班主管核准。
4. 長期處理：替慢查詢補索引（例如 orders.status），並開事故單追蹤。
