from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd

from .registry import validate_registry_frame


def read_uploaded_table(uploaded_file) -> pd.DataFrame:
    name = Path(uploaded_file.name).name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    raise ValueError("Chỉ hỗ trợ CSV hoặc XLSX trong MVP v0.2")


def validate_uploaded_table(uploaded_file):
    df = read_uploaded_table(uploaded_file)
    return validate_registry_frame(df)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def dataframe_to_xlsx_bytes(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Asset_Registry")
    return buffer.getvalue()
