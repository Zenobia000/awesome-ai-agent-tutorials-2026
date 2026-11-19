# order-db-proxy：連線池耗盡

症狀：DB_POOL_TIMEOUT、pool exhausted、下單 502、p95 超過 1000ms。
先查部署時間、連線池日誌、order-api 的失敗訂單，再確認服務拓撲。
order-api 依賴 order-db-proxy；payment-api 不是本次連線池的修復目標。
若確認 order-db-proxy 降級，提出模擬重啟建議，由人核准後執行。
重啟後必須重新讀取監控，健康狀態、p95 < 1000ms、錯誤率 < 0.05
全部成立才算恢復。重啟無效時升級人工處理，不自動循環重啟。
