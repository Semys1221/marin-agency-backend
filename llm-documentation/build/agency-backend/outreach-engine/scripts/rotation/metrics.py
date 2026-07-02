"""
Lit les métriques des campagnes Instantly depuis Supabase (campaign_analytics).

campaign_analytics est alimenté par push-instantly après chaque envoi.
Si la table n'existe pas ou est vide, retourne des defaults à 0.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

_script_dir = Path(__file__).resolve().parent
_base = _script_dir.parent
sys.path.insert(0, os.path.join(_base))
sys.path.insert(0, os.path.join(_script_dir))

from supabase_client import get_supabase, is_configured


def get_niche_metrics(tenant_id: str, niche_name: str) -> dict:
    if not is_configured():
        return _empty()

    try:
        result = (
            get_supabase()
            .table("campaign_analytics")
            .select("*")
            .eq("tenant_id", tenant_id)
            .eq("niche_name", niche_name)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if result.data:
            return _parse(result.data[0])
        return _empty()
    except Exception:
        return _empty()


def get_all_metrics(tenant_id: str) -> dict[str, dict]:
    if not is_configured():
        return {}

    try:
        result = (
            get_supabase()
            .table("campaign_analytics")
            .select("*")
            .eq("tenant_id", tenant_id)
            .execute()
        )
        if not result.data:
            return {}

        latest: dict[str, dict] = {}
        for row in result.data:
            name = row.get("niche_name", "")
            ts = row.get("created_at", "")
            if name not in latest or ts > latest[name].get("_ts", ""):
                latest[name] = {**row, "_ts": ts}

        return {k: _parse(v) for k, v in latest.items()}
    except Exception:
        return {}


def _empty() -> dict:
    return {
        "emails_sent": 0,
        "leads_pushed": 0,
        "reply_rate": 0.0,
        "positive_reply_rate": 0.0,
        "booking_rate": 0.0,
        "last_message_at": None,
    }


def _parse(row: dict) -> dict:
    def f(v, default=0):
        return v if v is not None else default

    def parse_ts(v):
        if v is None:
            return None
        if isinstance(v, str):
            return v
        return v.isoformat() if hasattr(v, "isoformat") else str(v)

    return {
        "emails_sent": f(row.get("emails_sent"), 0),
        "leads_pushed": f(row.get("leads_pushed"), 0),
        "reply_rate": float(f(row.get("reply_rate"), 0.0)),
        "positive_reply_rate": float(f(row.get("positive_reply_rate"), 0.0)),
        "booking_rate": float(f(row.get("booking_rate"), 0.0)),
        "last_message_at": parse_ts(row.get("last_message_at")),
    }
