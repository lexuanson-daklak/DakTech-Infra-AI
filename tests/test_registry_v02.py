from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.data import load_asset_registry, load_asset_layer
from core.registry import registry_completeness


def test_registry_common_fields():
    df = load_asset_registry()
    required = {"asset_code", "module", "asset_name", "asset_type", "locality", "management_unit", "status", "source_id", "updated_at", "record_hash"}
    assert required.issubset(df.columns)
    assert len(df) == 36
    assert df["asset_code"].is_unique
    assert set(df["module"]) == {"road", "cemetery", "water", "drain"}
    assert registry_completeness(df) == 100.0


def test_asset_360_layers_link_to_registry():
    registry = load_asset_registry()
    codes = set(registry["asset_code"].astype(str))
    for layer in ["legal", "planning", "investment", "operations", "maintenance", "incidents", "history"]:
        df = load_asset_layer(layer)
        if not df.empty:
            assert set(df["asset_code"].astype(str)).issubset(codes)


if __name__ == "__main__":
    test_registry_common_fields()
    test_asset_360_layers_link_to_registry()
    print("DakTech Infra AI registry v0.2 test: PASS")
