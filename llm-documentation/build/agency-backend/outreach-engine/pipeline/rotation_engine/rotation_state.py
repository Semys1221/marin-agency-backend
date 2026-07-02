"""
Supabase table:
  create table rotation_state (
    id uuid primary key default gen_random_uuid(),
    tenant_id text not null,
    niche_name text not null,
    status text not null default 'pending',
    leads_pushed int default 0,
    emails_sent int default 0,
    reply_rate numeric default 0,
    positive_reply_rate numeric default 0,
    booking_rate numeric default 0,
    last_message_at timestamptz,
    opened_at timestamptz,
    closed_at timestamptz,
    closed_reason text,
    created_at timestamptz default now()
  );

  create unique index idx_rotation_tenant_niche on rotation_state(tenant_id, niche_name);
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

_script_dir = Path(__file__).resolve().parent
_base = _script_dir.parent
sys.path.insert(0, os.path.join(_base))
sys.path.insert(0, os.path.join(_script_dir))
from cli.db import get_supabase, is_configured

STATUSES = ("pending", "active", "at_target", "scaling", "closed", "paused")


def _now():
    return datetime.now(timezone.utc).isoformat()


def get_state(tenant_id: str, niche_name: str) -> dict | None:
    if not is_configured():
        return None
    result = (
        get_supabase()
        .table("rotation_state")
        .select("*")
        .eq("tenant_id", tenant_id)
        .eq("niche_name", niche_name)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def list_states(tenant_id: str) -> list[dict]:
    if not is_configured():
        return []
    result = (
        get_supabase()
        .table("rotation_state")
        .select("*")
        .eq("tenant_id", tenant_id)
        .order("created_at")
        .execute()
    )
    return result.data


def upsert_state(tenant_id: str, niche_name: str, updates: dict) -> dict | None:
    if not is_configured():
        return None
    existing = get_state(tenant_id, niche_name)
    if existing:
        updated = (
            get_supabase()
            .table("rotation_state")
            .update(updates)
            .eq("id", existing["id"])
            .execute()
        )
        return updated.data[0] if updated.data else None

    payload = {
        "tenant_id": tenant_id,
        "niche_name": niche_name,
        **updates,
    }
    if "created_at" not in payload:
        payload["created_at"] = _now()
    inserted = get_supabase().table("rotation_state").insert(payload).execute()
    return inserted.data[0] if inserted.data else None


def set_status(tenant_id: str, niche_name: str, status: str, reason: str = "") -> dict | None:
    updates = {"status": status}
    if status == "active":
        updates["opened_at"] = _now()
    elif status in ("closed", "at_target"):
        updates["closed_at"] = _now()
        if reason:
            updates["closed_reason"] = reason
    return upsert_state(tenant_id, niche_name, updates)


def init_tenant_niches(tenant_id: str, niches: list[dict]):
    for n in niches:
        existing = get_state(tenant_id, n["name"])
        if not existing:
            upsert_state(tenant_id, n["name"], {"status": "pending"})

    first = find_first_pending(tenant_id, niches)
    if first:
        set_status(tenant_id, first, "active")


def find_first_pending(tenant_id: str, niches: list[dict]) -> str | None:
    for n in niches:
        s = get_state(tenant_id, n["name"])
        if s is None or s["status"] == "pending":
            return n["name"]
    return None


def find_next_active(tenant_id: str, niches: list[dict], current_niche: str) -> str | None:
    found = False
    for n in niches:
        if n["name"] == current_niche:
            found = True
            continue
        if found:
            s = get_state(tenant_id, n["name"])
            if s is None or s["status"] == "pending":
                return n["name"]
    return None
