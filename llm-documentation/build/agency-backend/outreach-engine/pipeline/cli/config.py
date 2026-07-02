import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEMO_CONFIG = {
    "tenant_id": "marin",
    "niches": [
        {
            "name": "grossiste_beaute",
            "keywords": ["grossiste beauté", "grossiste cosmétique"]
        }
    ],
    "target": 10000
}


def read_config(tenant_id: str, demo: bool = False) -> dict | None:
    if demo:
        return {**_DEMO_CONFIG, "tenant_id": tenant_id}

    config_path = Path(f"/users/{tenant_id}/config.json")
    if not config_path.exists():
        config_path = Path(SCRIPT_DIR) / "users" / tenant_id / "config.json"
        if not config_path.exists():
            return None

    try:
        with open(config_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def validate_config(config: dict) -> list[str]:
    errors = []
    niches = config.get("niches")
    if not niches or not isinstance(niches, list):
        errors.append("niches array is required")
    else:
        for i, n in enumerate(niches):
            if not n.get("name"):
                errors.append(f"niches[{i}].name is required")
            if not n.get("keywords"):
                errors.append(f"niches[{i}].keywords is required")
    return errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="marin")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    config = read_config(args.tenant, demo=args.demo)
    if config is None:
        print(json.dumps({"error": "config not found"}))
        sys.exit(1)

    errors = validate_config(config)
    if errors:
        print(json.dumps({"error": "invalid config", "details": errors}))
        sys.exit(1)

    print(json.dumps(config, indent=2))
