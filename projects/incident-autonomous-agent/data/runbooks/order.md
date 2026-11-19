# order-api：下單 502 調查

order-api 依賴 order-db-proxy 與 payment-api。
下單 502 可能來自上游連線池耗盡，必須先查依賴狀態。
orders 資料表欄位：id TEXT、status TEXT、service TEXT。
唯讀查詢範例：SELECT status, COUNT(*) AS count FROM orders GROUP BY status。
order-api 不在可重啟白名單，調查結果應交由人工確認修復目標。
