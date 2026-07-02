"""
Rotation Engine — décide quelle niche scraper et quand.

ZÉRO IA. Règles if/else basées sur les métriques.
Décisions retournées :
  - {"action": "scrape", "niche": "..."}         → lancer le scraping
  - {"action": "close", "niche": "...", "reason": "..."}  → fermer la niche
  - {"action": "wait", "reason": "..."}            → rien à faire
"""

import json
import os
import sys
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
_base = _script_dir.parent
sys.path.insert(0, os.path.join(_base))
sys.path.insert(0, os.path.join(_script_dir))

from supabase_client import get_supabase, is_configured
from rotation_state import get_state, upsert_state, set_status, list_states, init_tenant_niches, find_next_active
from metrics import get_niche_metrics, get_all_metrics

# Seuils
MIN_SENT_FOR_EVAL = 1000
REPLY_RATE_FLOOR = 2.0
POSITIVE_REPLY_RATE_FLOOR = 5.0
BOOKING_RATE_FLOOR = 2.0
HOURS_SINCE_LAST_MSG = 24


def decide(tenant_config: dict, demo: bool = False) -> list[dict]:
    decisions = []

    if demo:
        return _demo_decisions()

    tenant_id = tenant_config.get("tenant_id", "")
    niches = tenant_config.get("niches", [])

    if not tenant_id or not niches:
        return [{"action": "wait", "reason": "No tenant_id or niches in config"}]

    # Init rotation_state for any new niches not yet in DB
    init_tenant_niches(tenant_id, niches)

    # Load all metrics once
    all_metrics = get_all_metrics(tenant_id)
    states = list_states(tenant_id)
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
                set_status(tenant_id, name, "scaling", "At target but performing well")
                decisions.append({"action": "scrape", "niche": name, "reason": "At target, scaling (good metrics)"})
            else:
                set_status(tenant_id, name, "at_target", "Target reached")
                decisions.append({"action": "close", "niche": name, "reason": "Target reached, metrics below thresholds"})
            continue

        if rr < REPLY_RATE_FLOOR and lma is not None and lma >= HOURS_SINCE_LAST_MSG:
            if prr < POSITIVE_REPLY_RATE_FLOOR and br < BOOKING_RATE_FLOOR:
                set_status(tenant_id, name, "closed", f"Reply rate {rr}% < {REPLY_RATE_FLOOR}% + {HOURS_SINCE_LAST_MSG}h idle")
                next_niche = find_next_active(tenant_id, niches, name)
                if next_niche:
                    set_status(tenant_id, next_niche, "active", "Activated by rotation")
                    decisions.append({"action": "scrape", "niche": next_niche, "reason": "Closing underperformer, activating next"})
                else:
                    decisions.append({"action": "wait", "reason": "All niches closed or pending"})
                continue

        decisions.append({"action": "scrape", "niche": name, "reason": "Continuing"})

    if not decisions:
        decisions.append({"action": "wait", "reason": "No actionable niches"})

    _log_decisions(tenant_id, decisions)
    return decisions


def _hours_since(ts_str: str | None) -> int | None:
    if not ts_str:
        return None
    try:
        from datetime import datetime, timezone
        if isinstance(ts_str, str):
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        else:
            ts = ts_str
        now = datetime.now(timezone.utc)
        delta = now - ts
        return int(delta.total_seconds() / 3600)
    except Exception:
        return None


def _log_decisions(tenant_id: str, decisions: list[dict]):
    if not is_configured():
        return
    try:
        supabase = get_supabase()
        for d in decisions:
            supabase.table("rotation_decisions").insert({
                "tenant_id": tenant_id,
                "action": d.get("action", "unknown"),
                "niche": d.get("niche", ""),
                "reason": d.get("reason", ""),
            }).execute()
    except Exception:
        pass


def _demo_decisions() -> list[dict]:
    return [
        {"action": "scrape", "niche": "grossiste_beaute", "reason": "Demo mode"},
    ]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    elif args.demo:
        config = {"tenant_id": "marin", "niches": [{"name": "grossiste_beaute", "target": 1500}]}
    else:
        print("Provide --config or --demo")
        sys.exit(1)

    result = decide(config, demo=args.demo)
    print(json.dumps(result, indent=2, ensure_ascii=False))
