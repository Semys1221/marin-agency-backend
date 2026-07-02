import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_script_dir = Path(__file__).resolve().parent
_load_dotenv_path = _script_dir
for _ in range(10):
    if (_load_dotenv_path / ".env.local").exists():
        load_dotenv(_load_dotenv_path / ".env.local")
        break
    _load_dotenv_path = _load_dotenv_path.parent

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from supabase_client import get_supabase, is_configured


def save_niche_hunt(tenant_id: str, niches: list[dict]) -> dict | None:
    if not is_configured():
        return {"error": "Supabase non configuré"}

    supabase = get_supabase()
    payload = {
        "tenant_id": tenant_id,
        "niches": niches,
        "active": 0,
        "status": "active"
    }
    result = supabase.table("niche_hunts").insert(payload).execute()
    return result.data[0] if result.data else None


def get_active_niche_hunt(tenant_id: str) -> dict | None:
    if not is_configured():
        return None

    supabase = get_supabase()
    result = supabase.table("niche_hunts") \
        .select("*") \
        .eq("tenant_id", tenant_id) \
        .eq("status", "active") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None


def update_niche_hunt(hunt_id: str, updates: dict) -> dict | None:
    if not is_configured():
        return None

    supabase = get_supabase()
    result = supabase.table("niche_hunts") \
        .update(updates) \
        .eq("id", hunt_id) \
        .execute()
    return result.data[0] if result.data else None


def set_active_niche(hunt_id: str, index: int) -> bool:
    return update_niche_hunt(hunt_id, {"active": index}) is not None


def flag_niche_hunt_exhausted(hunt_id: str) -> bool:
    return update_niche_hunt(hunt_id, {"status": "exhausted"}) is not None


def flag_needs_review(hunt_id: str) -> bool:
    return update_niche_hunt(hunt_id, {"status": "needs_review"}) is not None


def save_niche_variable(niche: str, variables: dict, template: str | None = None) -> dict | None:
    if not is_configured():
        return {"error": "Supabase non configuré"}

    supabase = get_supabase()
    payload = {
        "niche": niche,
        "variables": variables,
        "template": template
    }
    result = supabase.table("niche_variable").upsert(payload, on_conflict="niche").execute()
    return result.data[0] if result.data else None


def get_niche_variable(niche: str) -> dict | None:
    if not is_configured():
        return None

    supabase = get_supabase()
    result = supabase.table("niche_variable") \
        .select("*") \
        .eq("niche", niche) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="marin")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo_niches = [
            {"name": "grossiste_beaute_paris", "keywords": ["grossiste beauté Paris"], "location": "Paris"},
            {"name": "grossiste_beaute_lyon", "keywords": ["grossiste beauté Lyon"], "location": "Lyon"},
        ]
        print(json.dumps({"demo": True, "niches": demo_niches}, indent=2))
        sys.exit(0)
    else:
        active = get_active_niche_hunt(args.tenant)
        print(json.dumps({"active_hunt": active}, indent=2))
