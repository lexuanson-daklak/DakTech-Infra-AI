from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .config import ALLOWED_STATUSES, CONFIG_DIR, MODULES, REQUIRED_REGISTRY_COLUMNS


def load_rule_catalog() -> list[dict]:
    path = CONFIG_DIR / "data_quality_rules.json"
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_registry_rules(df: pd.DataFrame) -> pd.DataFrame:
    results: list[dict] = []

    for _, row in df.iterrows():
        code = str(row.get("asset_code", ""))
        for col in REQUIRED_REGISTRY_COLUMNS:
            value = row.get(col, "")
            if pd.isna(value) or str(value).strip() == "":
                results.append({"asset_code": code, "rule_code": "DQ-001", "severity": "ERROR", "status": "FAIL", "message": f"Thiếu {col}"})

        module = str(row.get("module", "")).strip().lower()
        if module and module not in MODULES:
            results.append({"asset_code": code, "rule_code": "DQ-002", "severity": "ERROR", "status": "FAIL", "message": f"Module không hợp lệ: {module}"})

        status = str(row.get("status", "")).strip().upper()
        if status and status not in ALLOWED_STATUSES:
            results.append({"asset_code": code, "rule_code": "DQ-003", "severity": "ERROR", "status": "FAIL", "message": f"Trạng thái không hợp lệ: {status}"})
        elif status and status != "ACTIVE":
            results.append({"asset_code": code, "rule_code": "DQ-004", "severity": "INFO", "status": "ATTENTION", "message": f"Tài sản có trạng thái cần theo dõi: {status}"})

        lat = row.get("latitude")
        lon = row.get("longitude")
        if pd.notna(lat) and not (-90 <= float(lat) <= 90):
            results.append({"asset_code": code, "rule_code": "DQ-005", "severity": "ERROR", "status": "FAIL", "message": "Latitude ngoài khoảng hợp lệ"})
        if pd.notna(lon) and not (-180 <= float(lon) <= 180):
            results.append({"asset_code": code, "rule_code": "DQ-005", "severity": "ERROR", "status": "FAIL", "message": "Longitude ngoài khoảng hợp lệ"})

    duplicates = df[df["asset_code"].astype(str).duplicated(keep=False)] if "asset_code" in df.columns else pd.DataFrame()
    for _, row in duplicates.iterrows():
        results.append({"asset_code": str(row.get("asset_code", "")), "rule_code": "DQ-006", "severity": "ERROR", "status": "FAIL", "message": "Trùng mã tài sản"})

    return pd.DataFrame(results, columns=["asset_code", "rule_code", "severity", "status", "message"])
