from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd

from core.cemetery_service import load_cemetery_master, normalize_cemetery_frame, validate_cemetery_frame


def main():
    df = load_cemetery_master()
    assert len(df) >= 8
    assert {"capacity_signal", "area_usage_pct", "source_id"}.issubset(df.columns)

    raw = pd.DataFrame({
        "TÊN NGHĨA TRANG": ["A"],
        "XÃ/PHƯỜNG": ["X"],
        "ĐƠN VỊ QUẢN LÝ": ["UBND X"],
        "TỔNG DIỆN TÍCH": [10],
        "ĐÃ SỬ DỤNG": [9.5],
        "NGUỒN DỮ LIỆU": ["BC-01"],
        "TRẠNG THÁI": ["ACTIVE"],
    })
    mapping = {
        "asset_name": "TÊN NGHĨA TRANG",
        "locality": "XÃ/PHƯỜNG",
        "management_unit": "ĐƠN VỊ QUẢN LÝ",
        "total_area_ha": "TỔNG DIỆN TÍCH",
        "used_area_ha": "ĐÃ SỬ DỤNG",
        "source_id": "NGUỒN DỮ LIỆU",
        "status": "TRẠNG THÁI",
    }
    normalized = normalize_cemetery_frame(raw, mapping)
    assert normalized.iloc[0]["asset_code"].startswith("CEM-TEMP-")
    checked, issues, summary = validate_cemetery_frame(normalized)
    assert summary["rows"] == 1
    assert "capacity_signal" in checked.columns
    print("test_cemetery_v03: PASS")


if __name__ == "__main__":
    main()
