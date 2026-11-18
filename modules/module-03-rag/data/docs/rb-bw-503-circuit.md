# Runbook：breakwater 回 BW-503（熔斷）

> 服務：breakwater｜類型：runbook｜版本：v2.8.3｜負責團隊：平台組｜更新：2026-09-05

## 症狀

前端大量顯示「服務暫時無法使用」，breakwater 日誌出現 `BW-503 circuit open upstream=<服務名>`。

## 先理解

BW-503 不是 breakwater 壞了，而是它在保護後端：某個上游在 20 秒內錯誤率超過 50%，熔斷器打開。
真正要修的是那個上游服務。

## 處理步驟

1. 從日誌的 `upstream=` 欄位找出是哪個服務。
2. 去看那個服務自己的錯誤率與 runbook，例如 tide-pay 就看 TP-5003 runbook。
3. 上游恢復後，熔斷器會在 30 秒後自動半開、試探，不需要手動重置。
4. 確定上游已經好了但熔斷器卡住超過 5 分鐘，才用 `hfctl gw breaker reset --upstream <服務名>`。

## 不要做的事

不要調高錯誤率門檻來「消除」BW-503，這只會把壞掉的流量灌回已經很吃力的上游。
