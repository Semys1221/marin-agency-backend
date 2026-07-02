"""
Tenant management — reads/writes tenants from Supabase `tenants` table.
Falls back to local JSON files if Supabase is not configured.
"""

import json
import os
import sys
from pathlib import Path

_SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_supabase():
    from cli.db import get_supabase, is_configured
    if not is_configured():
        return None
    return get_supabase()


def list_tenants() -> list[dict]:
    sb = get_supabase()
    if sb:
        try:
            result = sb.table("tenants").select("*").execute()
            configs = []
            for row in result.data or []:
                cfg = row.get("config")
                if isinstance(cfg, dict):
                    cfg["tenant_id"] = cfg.get("tenant_id", row.get("slug", ""))
                    configs.append(cfg)
                else:
                    configs.append({"tenant_id": row.get("slug", ""), "niches": []})
            return configs
        except Exception:
            pass

    return _list_local()


def get_tenant(tenant_id: str) -> dict | None:
    sb = get_supabase()
    if sb:
        try:
            result = sb.table("tenants").select("*").eq("slug", tenant_id).limit(1).execute()
            if result.data:
                cfg = result.data[0].get("config")
                if isinstance(cfg, dict):
                    cfg["tenant_id"] = cfg.get("tenant_id", tenant_id)
                    return cfg
                return {"tenant_id": tenant_id, "niches": []}
        except Exception:
            pass

    return _read_local(tenant_id)


def upsert_tenant(tenant_id: str, config: dict) -> bool:
    sb = get_supabase()
    if not sb:
        return False
    try:
        payload = {
            "slug": tenant_id,
            "config": config,
            "name": config.get("name", tenant_id),
        }
        sb.table("tenants").upsert(payload, on_conflict="slug").execute()
        return True
    except Exception:
        return False


def _list_local() -> list[dict]:
    users_dir = Path(_SCRIPT_DIR) / "users"
    if not users_dir.exists():
        return []
    configs = []
    for d in sorted(users_dir.iterdir()):
        if d.is_dir():
            cfg = _read_local(d.name)
            if cfg:
                configs.append(cfg)
    return configs


def _read_local(tenant_id: str) -> dict | None:
    path = Path(_SCRIPT_DIR) / "users" / tenant_id / "config.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", help="Tenant ID")
    args = parser.parse_args()

    if args.tenant:
        cfg = get_tenant(args.tenant)
        if cfg:
            print(json.dumps(cfg, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"error": "not found"}))
            sys.exit(1)
    else:
        tenants = list_tenants()
        print(json.dumps(tenants, indent=2, ensure_ascii=False))
