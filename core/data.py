from __future__ import annotations

import pandas as pd

from .config import ASSET_LAYER_FILES, DATA_DIR


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def load_assets(module: str) -> pd.DataFrame:
    mapping = {
        "road": "road_assets.csv",
        "cemetery": "cemetery_assets.csv",
        "water": "water_assets.csv",
        "drain": "drain_assets.csv",
    }
    if module not in mapping:
        raise KeyError(f"Unknown module: {module}")
    return load_csv(mapping[module])


def load_asset_registry() -> pd.DataFrame:
    return load_csv("asset_registry.csv")


def get_asset(asset_code: str) -> pd.Series | None:
    df = load_asset_registry()
    hit = df[df["asset_code"].astype(str) == str(asset_code)]
    if hit.empty:
        return None
    return hit.iloc[0]


def load_asset_layer(layer: str, asset_code: str | None = None) -> pd.DataFrame:
    if layer not in ASSET_LAYER_FILES:
        raise KeyError(f"Unknown layer: {layer}")
    df = load_csv(ASSET_LAYER_FILES[layer])
    if asset_code is not None and "asset_code" in df.columns:
        df = df[df["asset_code"].astype(str) == str(asset_code)]
    return df


def asset_summary() -> pd.DataFrame:
    df = load_asset_registry()
    rows = []
    for module, group in df.groupby("module", dropna=False):
        rows.append(
            {
                "module": module,
                "assets": int(len(group)),
                "active": int((group["status"] == "ACTIVE").sum()),
                "attention": int((group["status"] != "ACTIVE").sum()),
                "management_units": int(group["management_unit"].nunique(dropna=True)),
                "localities": int(group["locality"].nunique(dropna=True)),
            }
        )
    return pd.DataFrame(rows)
