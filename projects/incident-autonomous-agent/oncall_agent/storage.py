"""SQLite 教學服務；操作收據與狀態更新使用同一個交易。"""

import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path

import sqlglot
from sqlglot import exp

from .models import RESTARTABLE, RestartArgs, SQLArgs

INITIAL = {
    "order-api": ("degraded", 1500, 0.12),
    "order-db-proxy": ("degraded", 2300, 0.18),
    "payment-api": ("healthy", 160, 0.001),
    "notification": ("healthy", 100, 0.001),
}


class Operations:
    def __init__(self, data_dir):
        self.path = Path(data_dir).resolve() / "operations.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS services (
                    service TEXT PRIMARY KEY, state TEXT, p95_ms INTEGER,
                    error_rate REAL, revision INTEGER DEFAULT 0,
                    restart_count INTEGER DEFAULT 0,
                    recover_on_restart INTEGER DEFAULT 1
                );
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY, service TEXT, message TEXT
                );
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY, status TEXT, service TEXT
                );
                CREATE TABLE IF NOT EXISTS actions (
                    action_id TEXT PRIMARY KEY, receipt TEXT NOT NULL
                );
            """)
            for name, (state, latency, rate) in INITIAL.items():
                conn.execute(
                    "INSERT OR IGNORE INTO services "
                    "(service,state,p95_ms,error_rate) VALUES (?,?,?,?)",
                    (name, state, latency, rate),
                )
            if not conn.execute("SELECT 1 FROM logs LIMIT 1").fetchone():
                conn.executemany(
                    "INSERT INTO logs (service,message) VALUES (?,?)",
                    [
                        (
                            "order-db-proxy",
                            "14:00 deployment v2; pool exhausted",
                        ),
                        (
                            "order-db-proxy",
                            "14:01 DB_POOL_TIMEOUT waiting 2000ms",
                        ),
                        (
                            "order-api",
                            "14:01 upstream order-db-proxy returned 502",
                        ),
                    ],
                )
                conn.executemany(
                    "INSERT INTO orders VALUES (?,?,?)",
                    [
                        ("A-101", "failed", "order-api"),
                        ("A-102", "failed", "order-api"),
                        ("A-103", "paid", "payment-api"),
                    ],
                )

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.path, timeout=15)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def status(self, service):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM services WHERE service=?", (service,)
            ).fetchone()
        if row is None:
            raise ValueError("未知服務")
        return dict(row)

    def logs(self, service, limit=10):
        with self.connect() as conn:
            return [
                dict(row)
                for row in conn.execute(
                    "SELECT service,message FROM logs WHERE service=? "
                    "ORDER BY id DESC LIMIT ?",
                    (service, limit),
                )
            ]

    def query(self, sql):
        SQLArgs(sql=sql)
        statements = sqlglot.parse(sql, read="sqlite")
        if len(statements) != 1 or not isinstance(statements[0], exp.Select):
            raise ValueError("只接受單一 SELECT")
        tree = statements[0]
        if any(table.name != "orders" for table in tree.find_all(exp.Table)):
            raise ValueError("只允許查詢 orders")
        uri = f"{self.path.as_uri()}?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            conn.enable_load_extension(False)

            def authorize(action, table, column, database, trigger):
                if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_FUNCTION):
                    # No extension loading, file access or arbitrary UDFs.
                    allowed = {
                        "count",
                        "sum",
                        "avg",
                        "min",
                        "max",
                        "coalesce",
                        "lower",
                        "upper",
                        "like",
                    }
                    if action == sqlite3.SQLITE_FUNCTION:
                        return (
                            sqlite3.SQLITE_OK
                            if column in allowed
                            else sqlite3.SQLITE_DENY
                        )
                    return sqlite3.SQLITE_OK
                if action == sqlite3.SQLITE_READ and table == "orders":
                    return sqlite3.SQLITE_OK
                return sqlite3.SQLITE_DENY

            conn.set_authorizer(authorize)
            budget = 0

            def progress():
                nonlocal budget
                budget += 1
                return int(budget > 100)

            conn.set_progress_handler(progress, 1000)
            return [dict(row) for row in conn.execute(sql).fetchmany(100)]

    def restart(self, args: RestartArgs):
        """Only the fixed graph calls this adapter after validated approval."""
        if args.service not in RESTARTABLE:
            raise ValueError("服務不在重啟白名單")
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            previous = conn.execute(
                "SELECT receipt FROM actions WHERE action_id=?",
                (args.action_id,),
            ).fetchone()
            if previous:
                receipt = json.loads(previous[0])
                if receipt["service"] != args.service:
                    raise ValueError("操作識別碼與服務不符")
                return receipt
            current = conn.execute(
                "SELECT * FROM services WHERE service=?", (args.service,)
            ).fetchone()
            if current["revision"] != args.expected_revision:
                raise ValueError("服務已變更，請重新調查與審批")
            recovered = bool(current["recover_on_restart"])
            conn.execute(
                "UPDATE services SET revision=revision+1, "
                "restart_count=restart_count+1,state=?,p95_ms=?,error_rate=? "
                "WHERE service=?",
                (
                    "healthy" if recovered else "degraded",
                    90 if recovered else 2300,
                    0.001 if recovered else 0.18,
                    args.service,
                ),
            )
            receipt = {
                "action_id": args.action_id,
                "service": args.service,
                "revision": args.expected_revision + 1,
                "operation": "simulated_restart",
            }
            conn.execute(
                "INSERT INTO actions VALUES (?,?)",
                (args.action_id, json.dumps(receipt)),
            )
            return receipt
