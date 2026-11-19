---
name: text2sql
description: 用唯讀 SQL 檢查 orders 的業務影響。
---

資料表只有 orders(id TEXT,status TEXT,service TEXT)。
只使用單一 SELECT，最多回傳100筆。先查失敗訂單統計。
不得讀取其他資料表、執行 PRAGMA、載入擴充或修改資料。
