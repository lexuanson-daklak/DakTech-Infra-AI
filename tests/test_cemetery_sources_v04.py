from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

overview = pd.read_csv(DATA / "cemetery_collection_overview_v0.4.csv")
status = pd.read_csv(DATA / "cemetery_collection_status_v0.4.csv")

assert len(status) == 36, f"Expected 36 source packages, got {len(status)}"
assert int(overview.loc[overview["chi_tieu"] == "Bản ghi chi tiết đã tách sơ bộ", "gia_tri"].iloc[0]) == 303
assert int(overview.loc[overview["chi_tieu"] == "Bản ghi có cờ chất lượng dữ liệu", "gia_tri"].iloc[0]) == 56
assert (status["data_use_status"] == "EXCLUDED_CANCELLED").sum() == 1
print("test_cemetery_sources_v04: PASS")
