import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "dakroad.db"
def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
