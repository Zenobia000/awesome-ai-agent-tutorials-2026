# notification：通知延遲

notification 處理非同步通知，不在付款交易路徑上。
先查 notification 的狀態與日誌；只有降級時才建議模擬重啟。
所有重啟都要人工審批，健康服務不應重啟。
恢復需重新確認 p95 < 1000ms、錯誤率 < 0.05 與 healthy。
