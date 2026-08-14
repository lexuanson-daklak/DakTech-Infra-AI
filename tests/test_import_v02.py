from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.registry import validate_registry_frame


def test_valid_import_row():
    df = pd.DataFrame([{
        "module": "water",
        "asset_code": "wtr-test-001",
        "asset_name": "Công trình thử",
        "asset_type": "WATER_FACILITY",
        "locality": "Địa bàn thử",
        "latitude": 12.6,
        "longitude": 108.0,
        "management_unit": "Đơn vị thử",
        "status": "active",
        "source_id": "src-test-001",
        "updated_at": "2026-08-14",
    }])
    normalized, errors, summary = validate_registry_frame(df)
    assert errors.empty
    assert normalized.iloc[0]["asset_code"] == "WTR-TEST-001"
    assert normalized.iloc[0]["status"] == "ACTIVE"
    assert summary["errors"] == 0


def test_duplicate_is_rejected():
    base = {
        "module": "road",
        "asset_code": "DUP-001",
        "asset_name": "Tài sản",
        "asset_type": "ROAD_PUBLIC_SPACE_POSITION",
        "locality": "Khu vực",
        "management_unit": "Đơn vị",
        "status": "ACTIVE",
        "source_id": "SRC-X",
        "updated_at": "2026-08-14",
    }
    df = pd.DataFrame([base, base])
    _, errors, _ = validate_registry_frame(df)
    assert (errors["rule_code"] == "IMP-007").any()


if __name__ == "__main__":
    test_valid_import_row()
    test_duplicate_is_rejected()
    print("DakTech Infra AI import v0.2 test: PASS")
