from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.data import load_asset_registry
from core.rule_engine import evaluate_registry_rules, load_rule_catalog


def test_rule_catalog_has_locked_legal_placeholders():
    catalog = load_rule_catalog()
    legal = [r for r in catalog if r["category"] == "LEGAL_PLACEHOLDER"]
    assert len(legal) == 3
    assert all(r["enabled"] is False for r in legal)


def test_registry_has_no_data_errors():
    df = load_asset_registry()
    results = evaluate_registry_rules(df)
    if not results.empty:
        assert not (results["severity"] == "ERROR").any()


if __name__ == "__main__":
    test_rule_catalog_has_locked_legal_placeholders()
    test_registry_has_no_data_errors()
    print("DakTech Infra AI rules v0.2 test: PASS")
