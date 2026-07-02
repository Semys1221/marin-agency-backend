#!/usr/bin/env python3
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
USERS_DIR = SCRIPT_DIR / "users"


def create_tenant(tenant_id: str, niches: list[dict], target: int = 5000) -> Path:
    config = {
        "tenant_id": tenant_id,
        "niches": niches,
        "target": target,
    }
    tenant_dir = USERS_DIR / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    config_path = tenant_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    return config_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create a new tenant config")
    parser.add_argument("tenant_id", help="Tenant ID (e.g. client-a)")
    parser.add_argument("--target", type=int, default=5000, help="Lead target")
    parser.add_argument("--niche", "-n", action="append", nargs="+",
                        help="Niche with keywords: --niche plombier 'keyword1' 'keyword2'")
    parser.add_argument("--file", "-f", help="JSON file with niches array")

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
        niches = data if isinstance(data, list) else data.get("niches", [])
    elif args.niche:
        niches = []
        for group in args.niche:
            name = group[0]
            keywords = group[1:] if len(group) > 1 else [name]
            niches.append({"name": name, "keywords": keywords})
    else:
        print("Provide --niche or --file", file=sys.stderr)
        sys.exit(1)

    path = create_tenant(args.tenant_id, niches, args.target)
    print(f"Tenant created at: {path}")
    print(json.dumps({"tenant_id": args.tenant_id, "niches": niches, "target": args.target}, indent=2))


if __name__ == "__main__":
    main()
