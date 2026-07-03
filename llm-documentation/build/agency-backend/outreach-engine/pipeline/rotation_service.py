#!/usr/bin/env python3
"""
Rotation Service — décide quelle niche scraper et quand.

Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, TENANT_ID (optionnel)

Mode Render web service (--survivor) :
  python rotation_service.py --survivor

Mode debug (--once) :
  python rotation_service.py --once
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("rotation_service")

INTERVAL = int(os.getenv("ROTATION_INTERVAL_MINUTES", "15"))

# ── Shared helpers (no external imports) ──────────────────────


def _get_supabase():
    from supabase import create_client
    return create_client(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""))


def _is_configured():
    u = os.getenv("SUPABASE_URL", "")
    k = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    return bool(u and k and u != "..." and k != "...")


def _list_tenants() -> list[dict]:
    if not _is_configured():
        return []
    try:
        result = _get_supabase().table("tenants").select("*").execute()
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
        return []


def _get_tenant(tenant_id: str) -> dict | None:
    if not _is_configured():
        return None
    try:
        result = _get_supabase().table("tenants").select("*").eq("slug", tenant_id).limit(1).execute()
        if result.data:
            cfg = result.data[0].get("config")
            if isinstance(cfg, dict):
                cfg["tenant_id"] = cfg.get("tenant_id", tenant_id)
                return cfg
            return {"tenant_id": tenant_id, "niches": []}
    except Exception:
        pass
    return None


# ── Rotation state helpers (Supabase rotation_state table) ────


def _state_get(tenant_id: str, niche_name: str) -> dict | None:
    if not _is_configured():
        return None
    r = _get_supabase().table("rotation_state").select("*").eq("tenant_id", tenant_id).eq("niche_name", niche_name).limit(1).execute()
    return r.data[0] if r.data else None


def _state_list(tenant_id: str) -> list[dict]:
    if not _is_configured():
        return []
    r = _get_supabase().table("rotation_state").select("*").eq("tenant_id", tenant_id).order("created_at").execute()
    return r.data


def _state_upsert(tenant_id: str, niche_name: str, updates: dict):
    if not _is_configured():
        return
    existing = _state_get(tenant_id, niche_name)
    if existing:
        _get_supabase().table("rotation_state").update(updates).eq("id", existing["id"]).execute()
    else:
        _get_supabase().table("rotation_state").insert({"tenant_id": tenant_id, "niche_name": niche_name, **updates}).execute()


def _state_set_status(tenant_id: str, niche_name: str, status: str, reason: str = ""):
    updates = {"status": status}
    now = datetime.now(timezone.utc).isoformat()
    if status == "active":
        updates["opened_at"] = now
    elif status in ("closed", "at_target"):
        updates["closed_at"] = now
        if reason:
            updates["closed_reason"] = reason
    _state_upsert(tenant_id, niche_name, updates)


def _state_init_niches(tenant_id: str, niches: list[dict]):
    for n in niches:
        if not _state_get(tenant_id, n["name"]):
            _state_upsert(tenant_id, n["name"], {"status": "pending"})
    first = _find_first_pending(tenant_id, niches)
    if first:
        _state_set_status(tenant_id, first, "active")


def _find_first_pending(tenant_id: str, niches: list[dict]) -> str | None:
    for n in niches:
        s = _state_get(tenant_id, n["name"])
        if s is None or s["status"] == "pending":
            return n["name"]
    return None


def _find_next_active(tenant_id: str, niches: list[dict], current_niche: str) -> str | None:
    found = False
    for n in niches:
        if n["name"] == current_niche:
            found = True
            continue
        if found:
            s = _state_get(tenant_id, n["name"])
            if s is None or s["status"] == "pending":
                return n["name"]
    return None


# ── Metrics helpers (Supabase campaign_analytics) ─────────────


def _metrics_empty() -> dict:
    return {"emails_sent": 0, "leads_pushed": 0, "reply_rate": 0.0,
            "positive_reply_rate": 0.0, "booking_rate": 0.0, "last_message_at": None}


def _get_niche_metrics(tenant_id: str, niche_name: str) -> dict:
    if not _is_configured():
        return _metrics_empty()
    try:
        r = _get_supabase().table("campaign_analytics").select("*").eq("tenant_id", tenant_id).eq("niche_name", niche_name).order("created_at", desc=True).limit(1).execute()
        if r.data:
            row = r.data[0]
            return {
                "emails_sent": row.get("emails_sent") or 0,
                "leads_pushed": row.get("leads_pushed") or 0,
                "reply_rate": float(row.get("reply_rate") or 0.0),
                "positive_reply_rate": float(row.get("positive_reply_rate") or 0.0),
                "booking_rate": float(row.get("booking_rate") or 0.0),
                "last_message_at": row.get("last_message_at"),
            }
    except Exception:
        pass
    return _metrics_empty()


def _get_all_metrics(tenant_id: str) -> dict[str, dict]:
    if not _is_configured():
        return {}
    try:
        r = _get_supabase().table("campaign_analytics").select("*").eq("tenant_id", tenant_id).execute()
        if not r.data:
            return {}
        latest = {}
        for row in r.data:
            name = row.get("niche_name", "")
            ts = row.get("created_at", "")
            if name not in latest or ts > latest[name].get("_ts", ""):
                latest[name] = {**row, "_ts": ts}
        return {k: {
            "emails_sent": v.get("emails_sent") or 0,
            "leads_pushed": v.get("leads_pushed") or 0,
            "reply_rate": float(v.get("reply_rate") or 0.0),
            "positive_reply_rate": float(v.get("positive_reply_rate") or 0.0),
            "booking_rate": float(v.get("booking_rate") or 0.0),
            "last_message_at": v.get("last_message_at"),
        } for k, v in latest.items()}
    except Exception:
        return {}


# ── Rotation engine logic ────────────────────────────────────

MIN_SENT_FOR_EVAL = 1000
REPLY_RATE_FLOOR = 2.0
POSITIVE_REPLY_RATE_FLOOR = 5.0
BOOKING_RATE_FLOOR = 2.0
HOURS_SINCE_LAST_MSG = 24


def _hours_since(ts_str: str | None) -> int | None:
    if not ts_str:
        return None
    try:
        if isinstance(ts_str, str):
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        else:
            ts = ts_str
        return int((datetime.now(timezone.utc) - ts).total_seconds() / 3600)
    except Exception:
        return None


def decide(tenant_config: dict) -> list[dict]:
    decisions = []
    tenant_id = tenant_config.get("tenant_id", "")
    niches = tenant_config.get("niches", [])
    if not tenant_id or not niches:
        return [{"action": "wait", "reason": "No tenant_id or niches in config"}]

    _state_init_niches(tenant_id, niches)
    all_metrics = _get_all_metrics(tenant_id)
    states = _state_list(tenant_id)
    state_map = {s["niche_name"]: s for s in states}

    for n in niches:
        name = n["name"]
        target = n.get("target", 1500)
        s = state_map.get(name, {})
        status = s.get("status", "pending")
        metrics = all_metrics.get(name, {})
        msent = metrics.get("emails_sent", 0)
        pushed = metrics.get("leads_pushed", 0)

        if status == "closed":
            continue
        if status == "pending":
            decisions.append({"action": "scrape", "niche": name})
            continue
        if msent < MIN_SENT_FOR_EVAL:
            decisions.append({"action": "scrape", "niche": name, "reason": f"Only {msent} sent, need {MIN_SENT_FOR_EVAL}"})
            continue

        rr = metrics.get("reply_rate", 0.0)
        prr = metrics.get("positive_reply_rate", 0.0)
        br = metrics.get("booking_rate", 0.0)
        lma = _hours_since(metrics.get("last_message_at"))

        if pushed >= target:
            if rr >= REPLY_RATE_FLOOR or prr >= POSITIVE_REPLY_RATE_FLOOR or br >= BOOKING_RATE_FLOOR:
                _state_set_status(tenant_id, name, "scaling", "At target but performing well")
                decisions.append({"action": "scrape", "niche": name, "reason": "At target, scaling (good metrics)"})
            else:
                _state_set_status(tenant_id, name, "at_target", "Target reached")
                decisions.append({"action": "close", "niche": name, "reason": "Target reached, metrics below thresholds"})
            continue

        if rr < REPLY_RATE_FLOOR and lma is not None and lma >= HOURS_SINCE_LAST_MSG:
            if prr < POSITIVE_REPLY_RATE_FLOOR and br < BOOKING_RATE_FLOOR:
                _state_set_status(tenant_id, name, "closed", f"Reply rate {rr}% < {REPLY_RATE_FLOOR}% + {HOURS_SINCE_LAST_MSG}h idle")
                next_niche = _find_next_active(tenant_id, niches, name)
                if next_niche:
                    _state_set_status(tenant_id, next_niche, "active", "Activated by rotation")
                    decisions.append({"action": "scrape", "niche": next_niche, "reason": "Closing underperformer, activating next"})
                else:
                    decisions.append({"action": "wait", "reason": "All niches closed or pending"})
                continue

        decisions.append({"action": "scrape", "niche": name, "reason": "Continuing"})

    if not decisions:
        decisions.append({"action": "wait", "reason": "No actionable niches"})

    for d in decisions:
        log.info("    → %s: %s", d.get("action", "?"), d.get("niche", d.get("reason", "")))
    return decisions


# ── Entry points ─────────────────────────────────────────────


def run_for_tenant(tenant_id: str):
    config = _get_tenant(tenant_id)
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return
    log.info("  Décision pour %s...", tenant_id)
    decide(config)


def run_all():
    log.info("═" * 50)
    log.info("  ROTATION SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("═" * 50)
    tenant_filter = os.getenv("TENANT_ID", "")
    tenants = _list_tenants()
    for config in tenants:
        tid = config.get("tenant_id", "")
        if tid and (not tenant_filter or tid == tenant_filter):
            run_for_tenant(tid)


def run_survivor():
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass
    log.info("  Mode survivor démarré (toutes les %d min)", INTERVAL)
    while True:
        run_all()
        for _ in range(INTERVAL * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rotation Service")
    parser.add_argument("--once", action="store_true", help="Execute once and exit")
    parser.add_argument("--survivor", action="store_true", help="Survivor loop (Render)")
    args = parser.parse_args()
    if args.survivor:
        run_survivor()
    else:
        run_all()
