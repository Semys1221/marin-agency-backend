#!/usr/bin/env python3
"""Lead writer — 1 fichier, 1 responsabilité : écrire les leads dans Supabase."""

import os
import logging
from datetime import datetime, timezone

log = logging.getLogger("v3.leads")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def _headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


def write_one(lead: dict) -> bool:
    """Écrit 1 lead dans la table 'leads'. Retourne True si réussi."""
    import httpx
    try:
        r = httpx.post(
            f"{SUPABASE_URL}/rest/v1/leads",
            headers=_headers(),
            json=lead,
            timeout=10,
        )
        r.raise_for_status()
        return True
    except httpx.HTTPStatusError as e:
        # 409 = duplicate (normal)
        if e.response.status_code == 409:
            return False  # doublon, pas grave
        log.warning("[leads] HTTP %s: %s", e.response.status_code, e.response.text[:200])
        return False
    except Exception as e:
        log.warning("[leads] erreur écriture: %s", e)
        return False


def update_status(lead_id: str, status: str, valid: bool = False) -> bool:
    """Met à jour le status d'un lead."""
    import httpx
    try:
        httpx.patch(
            f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}",
            headers=_headers(),
            json={
                "status": status,
                "valid": valid,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            timeout=10,
        )
        return True
    except Exception:
        return False


def get_by_queue(queue_id: str, status: str = None, valid_only: bool = False) -> list[dict]:
    """Récupère les leads d'une queue. Filtrable par status."""
    filters = [f"campaign_queue_id=eq.{queue_id}"]
    if status:
        filters.append(f"status=eq.{status}")
    if valid_only:
        filters.append("valid=eq.true")
    import httpx
    try:
        r = httpx.get(
            f"{SUPABASE_URL}/rest/v1/leads?{'&'.join(filters)}&select=*",
            headers=_headers(),
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def count_by_queue(queue_id: str) -> int:
    """Compte les leads d'une queue."""
    rows = get_by_queue(queue_id)
    return len(rows)
