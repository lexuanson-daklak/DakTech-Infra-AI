from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.data import asset_summary, load_assets


def test_modules_have_data():
    for module in ["road", "cemetery", "water", "drain"]:
        df = load_assets(module)
        assert not df.empty
        assert {"asset_code", "asset_name", "latitude", "longitude", "status"}.issubset(df.columns)


def test_summary_counts():
    summary = asset_summary()
    assert int(summary["assets"].sum()) == 36


if __name__ == "__main__":
    test_modules_have_data()
    test_summary_counts()
    print("DakTech Infra AI data smoke test: PASS")
