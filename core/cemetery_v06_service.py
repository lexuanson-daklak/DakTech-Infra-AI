from __future__ import annotations
import pandas as pd
from .config import DATA_DIR


def _read(name: str) -> pd.DataFrame:
    p = DATA_DIR / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()


def load_v06_progress() -> pd.DataFrame:
    return _read('cemetery_v06_progress.csv')


def load_v06_priority() -> pd.DataFrame:
    return _read('cemetery_v06_review_priority.csv')


def load_v06_type_summary() -> pd.DataFrame:
    return _read('cemetery_v06_type_summary.csv')


def load_v06_status_summary() -> pd.DataFrame:
    return _read('cemetery_v06_status_summary.csv')


def load_v06_quality_summary() -> pd.DataFrame:
    return _read('cemetery_v06_quality_summary.csv')


def metric(label: str, default=0):
    df = load_v06_progress()
    if df.empty:
        return default
    hit = df[df['chi_tieu'] == label]
    if hit.empty:
        return default
    return hit.iloc[0]['gia_tri']
