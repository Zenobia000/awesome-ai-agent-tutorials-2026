# Runbook：PostgreSQL 主庫切換

> 服務：postgresql｜類型：runbook｜版本：PostgreSQL 15.6｜負責團隊：平台組｜更新：2026-03-28

## 適用範圍

所有用 Patroni 管理的叢集：`pg-auth`、`pg-order`、`pg-stock`、`pg-pay`。

## 自動切換

主庫失聯 30 秒，Patroni 會自動把同步副本升為主庫。因為用同步複寫，RPO 為 0（不掉已確認的交易），
RTO 目標 60 秒內。

## 計畫性切換（例如要更新主機）

1. 只能在部署時段內做，並先在值班頻道公告。
2. 執行 `patronictl -c /etc/patroni.yml switchover <叢集名> --candidate <副本名>`。
3. 確認 `patronictl list` 顯示新主庫為 Leader、舊主庫為 Replica 且 lag 為 0。
4. `pg-pay` 的計畫性切換要避開請款批次 02:30～03:30。

## 常見問題

- 切換後應用程式連不上：檢查應用是否連到 `<叢集名>-rw` 服務名稱，而不是寫死 IP。
