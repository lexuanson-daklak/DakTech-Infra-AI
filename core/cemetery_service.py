from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd

from .config import DATA_DIR

CEMETERY_REQUIRED_FIELDS = [
    "asset_name",
    "locality",
    "management_unit",
    "status",
    "source_id",
]

CEMETERY_CANONICAL_FIELDS = [
    "asset_code",
    "asset_name",
    "locality",
    "ward_code",
    "address",
    "latitude",
    "longitude",
    "cemetery_type",
    "management_unit",
    "management_model",
    "status",
    "total_area_ha",
    "used_area_ha",
    "remaining_area_ha",
    "planned_expansion_area_ha",
    "estimated_graves",
    "occupied_graves",
    "remaining_graves",
    "annual_burials",
    "planning_status",
    "land_status",
    "environmental_status",
    "internal_road_status",
    "drainage_status",
    "water_supply_status",
    "power_status",
    "greenery_status",
    "investment_need",
    "priority",
    "source_id",
    "source_doc_no",
    "source_doc_date",
    "reporting_period",
    "verified_status",
    "updated_at",
    "notes",
]

NUMERIC_FIELDS = [
    "latitude",
    "longitude",
    "total_area_ha",
    "used_area_ha",
    "remaining_area_ha",
    "planned_expansion_area_ha",
    "estimated_graves",
    "occupied_graves",
    "remaining_graves",
    "annual_burials",
]

COLUMN_ALIASES = {
    "asset_code": ["ma nghia trang", "mã nghĩa trang", "ma nt", "mã nt", "asset_code", "ma tai san", "mã tài sản"],
    "asset_name": ["ten nghia trang", "tên nghĩa trang", "ten nt", "tên nt", "nghia trang", "nghĩa trang", "asset_name", "ten"],
    "locality": ["xa phuong", "xã phường", "xa/phuong", "xã/phường", "dia phuong", "địa phương", "locality", "don vi hanh chinh", "đơn vị hành chính"],
    "management_unit": ["don vi quan ly", "đơn vị quản lý", "chu quan ly", "chủ quản lý", "management_unit"],
    "status": ["tinh trang", "tình trạng", "trang thai", "trạng thái", "status", "hien trang", "hiện trạng"],
    "total_area_ha": ["tong dien tich", "tổng diện tích", "dien tich", "diện tích", "dien tich ha", "diện tích ha", "total_area_ha"],
    "used_area_ha": ["dien tich da su dung", "diện tích đã sử dụng", "da su dung", "đã sử dụng", "used_area_ha"],
    "remaining_area_ha": ["dien tich con lai", "diện tích còn lại", "quy dat con lai", "quỹ đất còn lại", "remaining_area_ha"],
    "investment_need": ["nhu cau dau tu", "nhu cầu đầu tư", "kien nghi", "kiến nghị", "de xuat", "đề xuất", "investment_need"],
    "source_id": ["source_id", "ma nguon", "mã nguồn", "nguon du lieu", "nguồn dữ liệu"],
    "source_doc_no": ["so van ban", "số văn bản", "so bao cao", "số báo cáo", "source_doc_no"],
    "reporting_period": ["ky bao cao", "kỳ báo cáo", "thoi diem bao cao", "thời điểm báo cáo", "reporting_period"],
}


def _clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _normalized_label(value: str) -> str:
    import unicodedata

    text = _clean_text(value).lower()
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    for ch in ["_", "-", ".", "/", "(", ")", ":", ";"]:
        text = text.replace(ch, " ")
    return " ".join(text.split())


def suggest_column_mapping(source_columns: list[str]) -> dict[str, str | None]:
    normalized = {_normalized_label(c): c for c in source_columns}
    result: dict[str, str | None] = {}
    for target, aliases in COLUMN_ALIASES.items():
        choice = None
        for alias in aliases:
            key = _normalized_label(alias)
            if key in normalized:
                choice = normalized[key]
                break
        result[target] = choice
    return result


def read_report_table(uploaded_file, sheet_name: str | None = None) -> pd.DataFrame:
    name = Path(uploaded_file.name).name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith(".xlsx"):
        raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
        return pd.read_excel(BytesIO(raw), sheet_name=sheet_name or 0)
    raise ValueError("MVP v0.3 hỗ trợ CSV hoặc XLSX.")


def list_excel_sheets(uploaded_file) -> list[str]:
    raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
    return pd.ExcelFile(BytesIO(raw)).sheet_names


def normalize_cemetery_frame(df: pd.DataFrame, mapping: dict[str, str | None] | None = None) -> pd.DataFrame:
    source = df.copy()
    mapping = mapping or {field: field if field in source.columns else None for field in CEMETERY_CANONICAL_FIELDS}

    out = pd.DataFrame(index=source.index)
    for field in CEMETERY_CANONICAL_FIELDS:
        src = mapping.get(field)
        if src and src in source.columns:
            out[field] = source[src]
        else:
            out[field] = ""

    for field in CEMETERY_CANONICAL_FIELDS:
        if field not in NUMERIC_FIELDS:
            out[field] = out[field].map(_clean_text)

    for field in NUMERIC_FIELDS:
        out[field] = pd.to_numeric(out[field], errors="coerce")

    for date_field in ["source_doc_date", "updated_at"]:
        parsed = pd.to_datetime(out[date_field], errors="coerce")
        out[date_field] = parsed.dt.strftime("%Y-%m-%d").fillna("")

    # Mã tạm để không biến dữ liệu báo cáo thành mã tài sản chính thức một cách im lặng.
    missing_code = out["asset_code"].eq("")
    out.loc[missing_code, "asset_code"] = [f"CEM-TEMP-{i+1:04d}" for i in range(int(missing_code.sum()))]
    if "code_status" in source.columns:
        preserved = source["code_status"].map(_clean_text).str.upper()
        out["code_status"] = np.where(preserved.ne(""), preserved, np.where(missing_code, "TEMPORARY", "SOURCE"))
    else:
        out["code_status"] = np.where(missing_code, "TEMPORARY", "SOURCE")

    # Chỉ tạo các chỉ tiêu tính toán; không ghi đè số liệu nguồn.
    out["computed_remaining_area_ha"] = np.where(
        out["total_area_ha"].notna() & out["used_area_ha"].notna(),
        (out["total_area_ha"] - out["used_area_ha"]).round(4),
        np.nan,
    )
    out["area_usage_pct"] = np.where(
        out["total_area_ha"].gt(0) & out["used_area_ha"].notna(),
        (out["used_area_ha"] / out["total_area_ha"] * 100).round(1),
        np.nan,
    )
    out["remaining_area_pct"] = np.where(
        out["total_area_ha"].gt(0) & out["remaining_area_ha"].notna(),
        (out["remaining_area_ha"] / out["total_area_ha"] * 100).round(1),
        np.nan,
    )
    out["estimated_full_year"] = np.where(
        out["remaining_graves"].notna() & out["annual_burials"].gt(0),
        datetime.now().year + np.ceil(out["remaining_graves"] / out["annual_burials"]),
        np.nan,
    )

    def pressure(row):
        pct = row.get("remaining_area_pct")
        if pd.notna(pct):
            if pct < 10:
                return "RẤT THẤP"
            if pct < 25:
                return "THẤP"
            if pct < 50:
                return "TRUNG BÌNH"
            return "CÒN DƯ ĐỊA"
        return "CHƯA ĐỦ DỮ LIỆU"

    out["capacity_signal"] = out.apply(pressure, axis=1)
    return out


def validate_cemetery_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    out = normalize_cemetery_frame(df)
    issues: list[dict] = []

    for idx, row in out.iterrows():
        row_no = int(idx) + 2
        code = row["asset_code"]
        for field in CEMETERY_REQUIRED_FIELDS:
            if not _clean_text(row.get(field, "")):
                severity = "ERROR" if field in ["asset_name", "source_id"] else "WARNING"
                issues.append({"row": row_no, "asset_code": code, "severity": severity, "rule_code": "CEM-DQ-001", "message": f"Thiếu {field}"})

        total = row.get("total_area_ha")
        used = row.get("used_area_ha")
        remaining = row.get("remaining_area_ha")
        if pd.notna(total) and total <= 0:
            issues.append({"row": row_no, "asset_code": code, "severity": "ERROR", "rule_code": "CEM-DQ-002", "message": "Tổng diện tích phải lớn hơn 0."})
        if pd.notna(total) and pd.notna(used) and used > total + 1e-9:
            issues.append({"row": row_no, "asset_code": code, "severity": "ERROR", "rule_code": "CEM-DQ-003", "message": "Diện tích đã sử dụng lớn hơn tổng diện tích."})
        if pd.notna(total) and pd.notna(used) and pd.notna(remaining):
            expected = total - used
            if abs(expected - remaining) > max(0.05, total * 0.01):
                issues.append({"row": row_no, "asset_code": code, "severity": "WARNING", "rule_code": "CEM-DQ-004", "message": "Diện tích còn lại không khớp tổng diện tích trừ diện tích đã sử dụng; cần đối chiếu nguồn."})
        if row["code_status"] == "TEMPORARY":
            issues.append({"row": row_no, "asset_code": code, "severity": "WARNING", "rule_code": "CEM-DQ-005", "message": "Hệ thống đang dùng mã tạm; cần cấp mã tài sản chính thức sau khi xác minh."})
        pct = row.get("remaining_area_pct")
        if pd.notna(pct) and pct < 10:
            issues.append({"row": row_no, "asset_code": code, "severity": "WARNING", "rule_code": "CEM-MG-001", "message": "Tín hiệu quản lý: quỹ đất còn lại dưới 10%; cần rà soát khả năng đáp ứng, quy hoạch và phương án xử lý. Đây không phải kết luận pháp lý."})

    dup = out["asset_code"].duplicated(keep=False)
    for idx, row in out[dup].iterrows():
        issues.append({"row": int(idx) + 2, "asset_code": row["asset_code"], "severity": "ERROR", "rule_code": "CEM-DQ-006", "message": "Trùng mã nghĩa trang trong tệp."})

    issue_df = pd.DataFrame(issues, columns=["row", "asset_code", "severity", "rule_code", "message"])
    summary = {
        "rows": int(len(out)),
        "errors": int((issue_df["severity"] == "ERROR").sum()) if not issue_df.empty else 0,
        "warnings": int((issue_df["severity"] == "WARNING").sum()) if not issue_df.empty else 0,
        "temporary_codes": int((out["code_status"] == "TEMPORARY").sum()),
    }
    return out, issue_df, summary


def load_cemetery_master() -> pd.DataFrame:
    path = DATA_DIR / "cemetery_master.csv"
    if path.exists():
        df = pd.read_csv(path)
    else:
        df = pd.read_csv(DATA_DIR / "cemetery_assets.csv")
    return normalize_cemetery_frame(df)


def cemetery_kpis(df: pd.DataFrame) -> dict:
    total_area = float(df["total_area_ha"].fillna(0).sum()) if "total_area_ha" in df else 0.0
    used_area = float(df["used_area_ha"].fillna(0).sum()) if "used_area_ha" in df else 0.0
    remaining_area = float(df["remaining_area_ha"].fillna(0).sum()) if "remaining_area_ha" in df else 0.0
    low_land = int(df["capacity_signal"].isin(["RẤT THẤP", "THẤP"]).sum()) if "capacity_signal" in df else 0
    verified = int(df["verified_status"].str.upper().eq("VERIFIED").sum()) if "verified_status" in df else 0
    return {
        "assets": int(len(df)),
        "total_area_ha": total_area,
        "used_area_ha": used_area,
        "remaining_area_ha": remaining_area,
        "low_land": low_land,
        "verified": verified,
    }
