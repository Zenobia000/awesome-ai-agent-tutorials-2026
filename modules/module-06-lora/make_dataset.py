"""產生 Lab 6 的 IT 維運問診資料集（虛構情境，用模板組合）。

用法（在本資料夾執行）：
    uv run python make_dataset.py

輸出：
    data/itops_train.jsonl  訓練用
    data/itops_val.jsonl    驗證用：症狀說法、服務名稱都沒在訓練集出現過，用來挑 checkpoint
    data/itops_test.jsonl   測試用：又換一種說法，只在最後評估時用一次

每筆格式（messages 格式，等同 ShareGPT 的 conversations）：
    {"category": "disk_full",
     "messages": [{"role": "user", "content": "<症狀>"},
                  {"role": "assistant", "content": "可能原因：…\n第一步檢查：`…`"}]}
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

SEED = 6
N_TRAIN = 320
N_VAL = 28
N_TEST = 30


@dataclass(frozen=True)
class Category:
    name: str
    cause: str
    command: str
    train_symptoms: tuple[str, ...]
    val_symptoms: tuple[str, ...]  # 驗證用：訓練集沒出現過的說法
    test_symptoms: tuple[str, ...]  # 測試用：又一種沒出現過的說法


CATEGORIES: tuple[Category, ...] = (
    Category(
        "disk_full", "磁碟空間已滿，無法寫入檔案", "df -h",
        ("{svc} 寫檔失敗，log 一直出現 No space left on device",
         "{host} 上的 {svc} 突然不再寫日誌，重啟也沒用",
         "{svc} 上傳檔案時回 500，錯誤訊息提到 disk full",
         "備份腳本在 {host} 跑到一半就中斷，說沒有空間"),
        ("{svc} 在 {host} 上存不了新資料，錯誤說裝置已無剩餘空間",),
        ("{svc} 的資料目錄寫不進去，系統提示空間不足",),
    ),
    Category(
        "oom", "記憶體不足，{svc} 被 OOM Killer 終止", "dmesg -T | grep -i oom",
        ("{svc} 沒有任何錯誤訊息就自己消失了，程序被殺掉",
         "{host} 上的 {svc} 每隔幾小時就無預警退出",
         "{svc} 處理大批資料時程序直接結束，exit code 137",
         "{svc} 的 Java 程序常常突然不見，log 最後一行很正常"),
        ("{svc} 吃的記憶體一路上升，然後程序就被系統收掉了",),
        ("尖峰時段 {svc} 會莫名其妙掛掉，沒有留下 stack trace",),
    ),
    Category(
        "port_in_use", "埠號 {port} 已被其他程序占用", "ss -lntp | grep :{port}",
        ("{svc} 啟動失敗，訊息是 address already in use，埠號 {port}",
         "部署新版 {svc} 後起不來，說 {port} bind 失敗",
         "在 {host} 上重啟 {svc}，報錯 EADDRINUSE :{port}",
         "{svc} 要聽 {port}，啟動時卻說該埠已被使用"),
        ("{svc} 想監聽 {port}，啟動 log 卻說已經有人用了",),
        ("{svc} 開機自動啟動時卡住，錯誤提到無法綁定 {port}",),
    ),
    Category(
        "dns", "DNS 無法解析 {host}", "nslookup {host}",
        ("{svc} 呼叫外部服務時報錯 Could not resolve host: {host}",
         "{svc} 連 {host} 失敗，但直接用 IP 可以連上",
         "{svc} 的 log 出現 Name or service not known，目標是 {host}",
         "從 {svc} 打 {host} 會出現 getaddrinfo ENOTFOUND"),
        ("{svc} 查不到 {host} 的位址，ping 主機名也失敗",),
        ("{svc} 突然找不到 {host} 這個主機名稱，改填 IP 就正常",),
    ),
    Category(
        "cert_expired", "{host} 的 TLS 憑證已過期",
        "echo | openssl s_client -connect {host}:443 2>/dev/null | openssl x509 -noout -enddate",
        ("{svc} 呼叫 https://{host} 失敗，錯誤是 certificate has expired",
         "使用者反映瀏覽 {host} 時跳出憑證無效的警告",
         "{svc} 的 log 出現 x509: certificate has expired or is not yet valid，對象是 {host}",
         "今天早上開始 {svc} 連 {host} 一直 SSL handshake failed"),
        ("{svc} 對 {host} 發 HTTPS 請求，回報憑證的有效期限已過",),
        ("昨天還好好的，今天 {svc} 連 https://{host} 都被拒絕，說憑證不受信任",),
    ),
    Category(
        "service_down", "{svc} 沒有在執行", "systemctl status {svc}",
        ("nginx 回 502 Bad Gateway，後端是 {svc}",
         "連 {host}:{port} 出現 Connection refused，那是 {svc} 的埠",
         "健康檢查一直失敗，{svc} 的 {port} 埠沒有回應",
         "{svc} 的監控面板整個沒資料，curl 本機 {port} 也被拒絕"),
        ("{svc} 好像停了，{port} 埠完全沒人在聽",),
        ("前端打 API 全部失敗，看起來 {svc} 完全沒有接請求",),
    ),
    Category(
        "cpu_high", "有程序把 CPU 吃滿", "top -o %CPU",
        ("{host} 的 load average 衝到 30，{svc} 回應變得很慢",
         "{svc} 的回應時間從 100ms 變成 5 秒，主機風扇狂轉",
         "SSH 進 {host} 打字都會延遲，{svc} 也跟著變慢",
         "{host} 上的 {svc} 很卡，監控顯示 CPU 使用率 100%"),
        ("{host} 整台變得很慢，{svc} 處理一個請求要等好幾秒",),
        ("{svc} 整體變得遲鈍，{host} 的系統負載異常偏高",),
    ),
    Category(
        "permission", "{svc} 對 {path} 沒有寫入權限", "ls -ld {path}",
        ("{svc} 寫入 {path} 時出現 Permission denied",
         "換了執行帳號之後，{svc} 無法在 {path} 建立檔案",
         "{svc} 啟動失敗，log 寫 EACCES: {path}",
         "{svc} 產生報表時報錯，說不能開啟 {path} 進行寫入"),
        ("{svc} 執行時對 {path} 存取被拒，說權限不足",),
        ("{svc} 想把暫存檔放進 {path}，結果被作業系統拒絕存取",),
    ),
    Category(
        "db_conn", "資料庫連線數已達上限", "psql -c \"select count(*) from pg_stat_activity;\"",
        ("{svc} 連資料庫時報錯 too many connections",
         "{svc} 的 log 出現 remaining connection slots are reserved",
         "尖峰時 {svc} 取不到資料庫連線，一直 timeout 在連線池",
         "{svc} 開始大量回 500，錯誤是 FATAL: sorry, too many clients already"),
        ("{svc} 開不了新的資料庫連線，DB 端說客戶端太多",),
        ("{svc} 等資料庫連線等到逾時，DBA 說連線數爆了",),
    ),
    Category(
        "firewall", "防火牆沒有開放埠號 {port}", "sudo ufw status numbered",
        ("在 {host} 本機 curl localhost:{port} 正常，從外面連 {port} 卻連不上",
         "{svc} 已經在聽 {port}，但其他機器 telnet {host} {port} 一直卡住",
         "新開的 {svc} 服務在 {port}，只有本機能存取",
         "{svc} 本機測試都過，從辦公室網路連 {host}:{port} 逾時"),
        ("{svc} 綁在 {port}，可是別台主機連 {host} 的這個埠會逾時",),
        ("{svc} 在 {host} 上看起來正常運作，但外部請求進不來 {port}",),
    ),
    Category(
        "container_restart", "{svc} 容器啟動後立即崩潰", "docker logs --tail 50 {svc}",
        ("docker ps 看到 {svc} 一直是 Restarting 狀態",
         "{svc} 容器每幾秒就重開一次，服務時有時無",
         "{svc} 容器的 restart count 一直增加",
         "用 docker compose 起 {svc}，它馬上 Exited (1) 又被拉起來"),
        ("{svc} 的容器一直反覆重啟，狀態停不下來",),
        ("{svc} 這個 container 起來沒多久就掛，然後又自己重啟",),
    ),
    Category(
        "clock_skew", "主機的系統時間不同步", "timedatectl status",
        ("{svc} 驗證 JWT 失敗，錯誤是 token used before issued",
         "{host} 上的 {svc} 呼叫雲端 API 一直回 RequestTimeTooSkewed",
         "{svc} 的 log 時間戳比實際時間快了 7 分鐘",
         "只有 {host} 上的 {svc} 會出現簽章過期，其他機器沒事"),
        ("{svc} 驗證簽章時說時間戳不對，這台主機時鐘好像不準",),
        ("{svc} 的 token 驗證時好時壞，懷疑跟主機時鐘有關",),
    ),
    Category(
        "inode_full", "inode 已用完（小檔案太多）", "df -i",
        ("{svc} 無法建立新檔案，但 df -h 顯示還有很多空間",
         "{host} 上的 {svc} 一直寫不進小檔案，磁碟明明還有 60% 空間",
         "{svc} 的 session 目錄有幾百萬個小檔，現在建檔失敗",
         "{svc} 出現 No space left on device，可是容量看起來沒滿"),
        ("{svc} 建檔失敗，容量還夠，但目錄裡的小檔案數量爆多",),
        ("{svc} 開不了新檔，空間還很多，但檔案數量非常大",),
    ),
    Category(
        "packet_loss", "{svc} 到 {host} 的網路有丟包", "ping -c 20 {host}",
        ("{svc} 呼叫 {host} 偶爾 timeout，大部分時候正常",
         "{svc} 連 {host} 時快時慢，重試幾次就會成功",
         "{svc} 到 {host} 的請求有 5% 會逾時，沒有固定規律",
         "{svc} 跟 {host} 的連線時常斷掉又重連"),
        ("{svc} 對 {host} 的請求偶發性失敗，重送通常就好",),
        ("{svc} 和 {host} 之間的通訊不穩，間歇性出現 read timeout",),
    ),
)

TRAIN_SVCS = ("order-api", "payment-svc", "auth-server", "inventory", "report-worker",
              "user-api", "search-svc", "billing", "gateway", "notify-worker")
TEST_SVCS = ("shipping-api", "coupon-svc", "ledger", "media-worker")
TRAIN_HOSTS = ("db01.corp.example", "api.partner.example", "web03.corp.example",
               "cache02.corp.example", "pay.vendor.example")
TEST_HOSTS = ("files.corp.example", "sso.vendor.example")
TRAIN_PORTS = ("8080", "3000", "5432", "9000", "6379")
TEST_PORTS = ("8443", "7000")
PATHS = ("/var/log/app", "/data/uploads", "/srv/reports", "/tmp/cache")


def render(cat: Category, symptom: str, rng: random.Random, test: bool) -> dict:
    """把模板填上服務、主機、埠號，組成一筆對話。"""
    slots = {
        "svc": rng.choice(TEST_SVCS if test else TRAIN_SVCS),
        "host": rng.choice(TEST_HOSTS if test else TRAIN_HOSTS),
        "port": rng.choice(TEST_PORTS if test else TRAIN_PORTS),
        "path": rng.choice(PATHS),
    }
    answer = f"可能原因：{cat.cause.format(**slots)}\n第一步檢查：`{cat.command.format(**slots)}`"
    return {
        "category": cat.name,
        "messages": [
            {"role": "user", "content": symptom.format(**slots)},
            {"role": "assistant", "content": answer},
        ],
    }


def build(n: int, rng: random.Random, split: str) -> list[dict]:
    rows, seen, i = [], set(), 0
    while len(rows) < n:
        cat = CATEGORIES[i % len(CATEGORIES)]  # 類別平均分配
        pool = {"train": cat.train_symptoms, "val": cat.val_symptoms, "test": cat.test_symptoms}[split]
        row = render(cat, rng.choice(pool), rng, test=split != "train")
        key = row["messages"][0]["content"]
        if key not in seen:  # 同一句症狀只留一次
            seen.add(key)
            rows.append(row)
            i += 1
    rng.shuffle(rows)
    return rows


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    rng = random.Random(SEED)
    out = Path(__file__).parent / "data"
    write_jsonl(build(N_TRAIN, rng, "train"), out / "itops_train.jsonl")
    write_jsonl(build(N_VAL, rng, "val"), out / "itops_val.jsonl")
    write_jsonl(build(N_TEST, rng, "test"), out / "itops_test.jsonl")
    print(f"train={N_TRAIN} val={N_VAL} test={N_TEST} → {out}")


if __name__ == "__main__":
    main()
