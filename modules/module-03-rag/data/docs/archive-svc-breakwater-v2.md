# breakwater API 閘道服務說明（v2.5 舊版，已封存）

> 服務：breakwater｜類型：服務說明｜版本：v2.5.0｜負責團隊：平台組｜更新：2025-11-03

本文件已封存。2026 年 6 月事故後多項設定已變更，現行設定請看 breakwater 服務說明。

## 限流規則

- 一般 API 金鑰：每分鐘 300 次請求，超過回 `BW-429`。
- 合作夥伴金鑰：每分鐘 1,000 次。

## 逾時

轉發到上游的預設逾時是 10 秒，設定鍵 `upstream_timeout_ms`。

## JWKS 快取

為了減少對 lighthouse-auth 的請求量，`jwks_cache_ttl` 設為 6 小時。
