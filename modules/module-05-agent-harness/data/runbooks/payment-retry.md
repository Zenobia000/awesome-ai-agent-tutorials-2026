# Runbook：payment-api 銀行閘道重試

徵兆：`bank-gateway slow response`，但重試成功。

1. 這是銀行端偶發的慢回應，重試成功就不影響付款。
2. 只有 payment-api 的 error_rate 超過 2% 才需要處理。
3. 不要重啟 payment-api：重啟會中斷進行中的付款。
