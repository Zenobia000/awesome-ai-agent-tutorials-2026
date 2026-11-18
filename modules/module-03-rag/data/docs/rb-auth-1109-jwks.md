# Runbook：AUTH-1109 簽章驗證失敗

> 服務：lighthouse-auth｜類型：runbook｜版本：v5.1.0｜負責團隊：身分組｜更新：2026-06-12

## 症狀

- 大量使用者被登出，或登入後馬上又跳回登入頁。
- breakwater 回 `BW-401`，下游日誌出現 `AUTH-1109 kid not found`。

## 最常見原因

金鑰剛輪換，下游服務的 JWKS 快取還是舊的，看不懂新金鑰簽的權杖。

## 處理步驟

1. 確認最近 24 小時內是否做過金鑰輪換：`hfctl auth key-history`。
2. 強制所有下游重新抓 JWKS：`hfctl auth jwks refresh --all`。這個動作安全，可以直接做。
3. 檢查 breakwater 的 `jwks_cache_ttl` 是否仍是 10 分鐘，有人改大要改回來。
4. 如果沒有輪換過，卻出現 AUTH-1109，可能是有人偽造權杖，立刻升級 SEV1 並通知資安。

## 不要做的事

不要為了止血把舊金鑰加回去當主要簽章金鑰，這會讓已輪換掉的金鑰重新生效。
