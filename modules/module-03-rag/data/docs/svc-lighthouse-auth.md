# lighthouse-auth 認證服務說明

> 服務：lighthouse-auth｜類型：服務說明｜版本：v5.1.0｜負責團隊：身分組｜更新：2026-07-15

## 這個服務做什麼

lighthouse-auth 負責會員登入、簽發與驗證存取權杖。所有需要登入的 API 都要帶它簽發的 JWT。

## 權杖規格

- access token：JWT，簽章演算法 ES256，有效期 15 分鐘。
- refresh token：不透明字串，存在 PostgreSQL，有效期 14 天；每次使用都會換發新的（rotation），舊的立即作廢。
- 同一會員最多同時 5 個裝置登入，第 6 個登入會踢掉最舊的裝置。

## 金鑰輪換

簽章私鑰每 90 天輪換一次，固定在季度第一個週三 10:00 執行。輪換時新舊公鑰會同時出現在 JWKS 端點 `/.well-known/jwks.json` 24 小時，
讓下游有時間更新快取。輪換指令：`hfctl auth rotate-key --confirm`，只有身分組值班人員有權限。

## 錯誤碼

| 錯誤碼 | 意思 | 處理方式 |
|---|---|---|
| AUTH-1101 | 帳號或密碼錯誤 | 前端提示，連錯 5 次鎖 15 分鐘 |
| AUTH-1107 | access token 過期 | 客戶端用 refresh token 換新的，屬正常流程 |
| AUTH-1108 | refresh token 已作廢 | 要求使用者重新登入 |
| AUTH-1109 | 簽章驗證失敗（找不到對應的 kid） | 通常是金鑰輪換後下游 JWKS 快取沒更新，見 runbook |
| AUTH-1120 | 帳號被風控鎖定 | 轉客服，不可自行解鎖 |

## 相依

lighthouse-auth 依賴 PostgreSQL 叢集 `pg-auth`（主從架構）與 Redis `rds-auth-01`（存登入失敗計數）。
