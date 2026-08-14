from __future__ import annotations

import hashlib
from datetime import datetime

import pandas as pd

from .config import ALLOWED_STATUSES, MODULES, REQUIRED_REGISTRY_COLUMNS


def _clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_registry_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lower() for c in out.columns]

    for col in REQUIRED_REGISTRY_COLUMNS:
        if col not in out.columns:
            out[col] = ""

    for col in ["module", "asset_code", "asset_name", "asset_type", "locality", "management_unit", "status", "source_id"]:
        out[col] = out[col].map(_clean_text)

    out["module"] = out["module"].str.lower()
    out["status"] = out["status"].str.upper()
    out["asset_code"] = out["asset_code"].str.upper()
    out["source_id"] = out["source_id"].str.upper()

    if "updated_at" in out.columns:
        parsed = pd.to_datetime(out["updated_at"], errors="coerce")
        out["updated_at"] = parsed.dt.strftime("%Y-%m-%d").fillna("")

    for col in ["latitude", "longitude"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    if "geometry_type" not in out.columns:
        out["geometry_type"] = "POINT"
    out["geometry_type"] = out["geometry_type"].fillna("POINT").astype(str).str.strip().str.upper()

    hash_fields = ["asset_code", "module", "asset_name", "asset_type", "locality", "management_unit", "status", "source_id", "updated_at"]
    out["record_hash"] = out.apply(
        lambda r: hashlib.sha256("|".join(_clean_text(r.get(c, "")) for c in hash_fields).encode("utf-8")).hexdigest(),
        axis=1,
    )
    return out


def validate_registry_frame(df: pd.DataFrame):
    original_columns = {str(c).strip().lower() for c in df.columns}
    normalized = normalize_registry_frame(df)
    errors = []

    missing_columns = [c for c in REQUIRED_REGISTRY_COLUMNS if c not in original_columns]
    for col in missing_columns:
        errors.append({"row": 0, "asset_code": "", "severity": "ERROR", "rule_code": "IMP-001", "message": f"Thiếu cột bắt buộc: {col}"})

    for idx, row in normalized.iterrows():
        excel_row = int(idx) + 2
        asset_code = _clean_text(row.get("asset_code", ""))
        for col in REQUIRED_REGISTRY_COLUMNS:
            if not _clean_text(row.get(col, "")):
                errors.append({"row": excel_row, "asset_code": asset_code, "severity": "ERROR", "rule_code": "IMP-002", "message": f"Thiếu giá trị bắt buộc: {col}"})

        if row.get("module") and row.get("module") not in MODULES:
            errors.append({"row": excel_row, "asset_code": asset_code, "severity": "ERROR", "rule_code": "IMP-003", "message": f"module không hợp lệ: {row.get('module')}"})

        if row.get("status") and row.get("status") not in ALLOWED_STATUSES:
            errors.append({"row": excel_row, "asset_code": asset_code, "severity": "ERROR", "rule_code": "IMP-004", "message": f"status không hợp lệ: {row.get('status')}"})

        lat = row.get("latitude") if "latitude" in normalized.columns else None
        lon = row.get("longitude") if "longitude" in normalized.columns else None
        if pd.notna(lat) and not (-90 <= float(lat) <= 90):
            errors.append({"row": excel_row, "asset_code": asset_code, "severity": "ERROR", "rule_code": "IMP-005", "message": "latitude nằm ngoài khoảng -90 đến 90"})
        if pd.notna(lon) and not (-180 <= float(lon) <= 180):
            errors.append({"row": excel_row, "asset_code": asset_code, "severity": "ERROR", "rule_code": "IMP-006", "message": "longitude nằm ngoài khoảng -180 đến 180"})

    dup_mask = normalized["asset_code"].ne("") & normalized["asset_code"].duplicated(keep=False)
    for idx, row in normalized[dup_mask].iterrows():
        errors.append({"row": int(idx) + 2, "asset_code": row["asset_code"], "severity": "ERROR", "rule_code": "IMP-007", "message": "Trùng asset_code trong tệp nhập"})

    error_df = pd.DataFrame(errors, columns=["row", "asset_code", "severity", "rule_code", "message"])
    valid_codes = set(normalized["asset_code"].astype(str)) - set(error_df.loc[error_df["severity"] == "ERROR", "asset_code"].astype(str)) if not error_df.empty else set(normalized["asset_code"].astype(str))
    summary = {
        "rows": int(len(normalized)),
        "valid_rows_estimate": int(normalized["asset_code"].isin(valid_codes).sum()),
        "errors": int((error_df["severity"] == "ERROR").sum()) if not error_df.empty else 0,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    return normalized, error_df, summary


def registry_completeness(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    cols = [c for c in REQUIRED_REGISTRY_COLUMNS if c in df.columns]
    if not cols:
        return 0.0
    values = df[cols].fillna("").astype(str).apply(lambda s: s.str.strip().ne(""))
    return float(values.to_numpy().mean() * 100)
