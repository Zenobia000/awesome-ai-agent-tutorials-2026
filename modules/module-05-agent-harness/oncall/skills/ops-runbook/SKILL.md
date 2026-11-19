---
name: ops-runbook
description: 線上事故（502、逾時、連線池用盡）的排查步驟。使用者回報服務出錯時使用。
---

# ops-runbook：線上事故排查

1. 用 read_logs(level="ERROR") 看最近的錯誤，找出最下游、最先出錯的服務。
2. 用 query_metrics 查那個服務的 error_rate；order-db-proxy 另外查 pool_used。
3. pool_used 到 50 代表連線池用盡：根因是 order-db-proxy，短期處理是重啟它。
4. 重啟前先說明證據，等人核准；重啟後再查一次 error_rate，低於 1% 才算恢復。
