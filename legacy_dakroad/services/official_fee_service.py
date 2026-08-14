from __future__ import annotations
from pathlib import Path
import pandas as pd

FILE = Path(__file__).resolve().parents[1] / "data" / "official_fee_rates.csv"

def load_rates() -> pd.DataFrame:
    return pd.read_csv(FILE)

def calculate_nq24(purpose_code: str, quantity: float = 1, periods: float = 1,
                   condition_code: str = "", locality: str = "") -> dict:
    df = load_rates()
    q = df[(df.policy_code == "NQ24_2024_DAKLAK_FORMER") & (df.purpose_code == purpose_code)]
    if condition_code:
        q = q[q.condition_code == condition_code]
    if locality:
        q = q[q.locality == locality]
    if q.empty:
        return {"ok": False, "message": "Không tìm thấy mức thu phù hợp."}
    row = q.iloc[0]
    total = float(row.rate_vnd) * float(quantity) * float(periods)
    return {"ok": True, "rate": int(row.rate_vnd), "unit": row.unit, "total": total,
            "source_id": row.source_id, "notes": row.notes}

def calculate_nq35(locality: str, position: str, purpose_code: str,
                   area_m2: float, months: float) -> dict:
    df = load_rates()
    q = df[(df.policy_code == "NQ35_2022_PHUYEN_FORMER") &
           (df.locality == locality) & (df.position == position) &
           (df.purpose_code == purpose_code)]
    if q.empty:
        return {"ok": False, "message": "Không tìm thấy mức thu phù hợp."}
    row = q.iloc[0]
    total = float(row.rate_vnd) * float(area_m2) * float(months)
    return {"ok": True, "rate": int(row.rate_vnd), "unit": row.unit, "total": total,
            "source_id": row.source_id, "notes": row.notes}
