from __future__ import annotations
import csv
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from services.password_utils import hash_password

DB = BASE / "database" / "dakroad.db"

def init_db(reset: bool = False) -> None:
    if reset and DB.exists():
        DB.unlink()

    conn = sqlite3.connect(DB)
    conn.executescript((BASE / "database" / "schema.sql").read_text(encoding="utf-8"))

    users = [
        ("nguoidan_demo", "DakRoad@2026", "Người đề nghị Demo", "APPLICANT"),
        ("canbo_demo", "DakRoad@2026", "Cán bộ xử lý Demo", "OFFICER"),
        ("lanhdao_demo", "DakRoad@2026", "Lãnh đạo Demo", "MANAGER"),
    ]
    for username, password, full_name, role in users:
        conn.execute(
            "INSERT OR IGNORE INTO users(username,password_hash,full_name,role) VALUES(?,?,?,?)",
            (username, hash_password(password), full_name, role),
        )

    with open(BASE / "data" / "assets.csv", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            conn.execute(
                '''INSERT OR REPLACE INTO assets
                (id,asset_code,asset_name,road_name,latitude,longitude,area_zone,
                 sidewalk_width_m,usable_area_m2,management_unit,status,allowed_purposes,notes)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (
                    int(row["id"]), row["asset_code"], row["asset_name"], row["road_name"],
                    float(row["latitude"]), float(row["longitude"]), row["area_zone"],
                    float(row["sidewalk_width_m"]), float(row["usable_area_m2"]),
                    row["management_unit"], row["status"], row["allowed_purposes"], row["notes"],
                ),
            )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB}")
