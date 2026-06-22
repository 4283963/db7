import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "checkin.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checkin_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            activity_name TEXT NOT NULL,
            checkin_time DATETIME NOT NULL
        )
    """)
    conn.commit()

    cursor = conn.execute("SELECT COUNT(*) FROM checkin_records")
    if cursor.fetchone()[0] == 0:
        _seed_data(conn)

    conn.close()


def _seed_data(conn):
    activities = [
        "周末读书会", "社区晨跑", "亲子手工坊",
        "英语角", "瑜伽课", "编程沙龙",
    ]
    names = [
        "张伟", "王芳", "李娜", "刘洋", "陈磊",
        "杨静", "赵敏", "黄强", "周婷", "吴刚",
        "徐丽", "孙涛", "马超", "朱红", "胡明",
        "郭亮", "何欢", "林峰", "罗敏", "梁宇",
    ]

    records = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    current = start_date

    while current <= end_date:
        num_checkins = random.randint(3, 15)
        for _ in range(num_checkins):
            hour = random.randint(8, 20)
            minute = random.randint(0, 59)
            checkin_time = current.replace(hour=hour, minute=minute)
            user = random.choice(names)
            activity = random.choice(activities)
            records.append((user, activity, checkin_time.strftime("%Y-%m-%d %H:%M:%S")))
        current += timedelta(days=1)

    conn.executemany(
        "INSERT INTO checkin_records (user_name, activity_name, checkin_time) VALUES (?, ?, ?)",
        records,
    )
    conn.commit()


def get_monthly_stats():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            strftime('%Y-%m', checkin_time) AS month,
            COUNT(*) AS total
        FROM checkin_records
        GROUP BY month
        ORDER BY month
    """).fetchall()
    conn.close()
    return [
        {"month": r["month"], "total": int(r["total"]) if r["total"] is not None else 0}
        for r in rows
    ]


def get_weekday_stats():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            strftime('%w', checkin_time) AS weekday,
            COUNT(*) AS total
        FROM checkin_records
        GROUP BY weekday
        ORDER BY weekday
    """).fetchall()
    conn.close()

    weekday_names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    ordered = [0, 1, 2, 3, 4, 5, 6]

    row_map = {}
    for r in rows:
        wd = int(r["weekday"]) if r["weekday"] is not None else 0
        total = int(r["total"]) if r["total"] is not None else 0
        row_map[wd] = total

    result = []
    for wd in ordered:
        result.append({
            "weekday": wd,
            "weekday_name": weekday_names[wd],
            "total": row_map.get(wd, 0),
        })
    return result
