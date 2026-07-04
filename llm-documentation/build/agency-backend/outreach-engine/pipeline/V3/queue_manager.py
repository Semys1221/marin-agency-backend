#!/usr/bin/env python3
"""Queue manager — 1 fichier, 1 responsabilité : gérer la table campaign_queue."""

import os
import json
import logging
from datetime import datetime, timezone

log = logging.getLogger("v3.queue")

# ── Helpers ──

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def _headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


def _req(method: str, path: str, json_data=None) -> list[dict] | dict:
    """Requête Supabase REST. Retourne [] ou dict selon le path."""
    import httpx
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    try:
        r = httpx.request(method, url, headers={**_headers(), "Prefer": "return=representation"}, json=json_data, timeout=15)
        r.raise_for_status()
        data = r.json() if r.text else []
        return data if isinstance(data, list) else [data]
    except httpx.HTTPStatusError as e:
        log.warning("[queue] HTTP %s: %s", e.response.status_code, e.response.text[:200])
        return []
    except Exception as e:
        log.warning("[queue] erreur: %s", e)
        return []


# ── CRUD campaign_queue ──

def create(niche: str, batch: int = 1) -> dict | None:
    """Crée une nouvelle entrée dans campaign_queue et retourne l'entrée créée."""
    row = {
        "niche": niche,
        "city": "France",
        "status": "created",
        "include_keywords": niche,
        "batch": batch,
        "priority": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    rows = _req("POST", "campaign_queue", json_data=row)
    if rows:
        log.info("[queue] créée: id=%s niche=%s", rows[0].get("id"), niche)
        return rows[0]
    log.warning("[queue] échec création")
    return None


def update_status(queue_id: str, status: str) -> None:
    """Met à jour le status d'une queue et sa date updated_at."""
    _req("PATCH", f"campaign_queue?id=eq.{queue_id}", json_data={
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })


def get_by_id(queue_id: str) -> dict | None:
    """Retourne une queue par son ID."""
    rows = _req("GET", f"campaign_queue?id=eq.{queue_id}&select=*")
    return rows[0] if rows else None


def list_active() -> list[dict]:
    """Liste les queues actives (pas done)."""
    return _req("GET", "campaign_queue?status=neq.done&order=created_at.desc")


def clean() -> int:
    """Supprime toutes les lignes de campaign_queue. Retourne le nombre supprimé."""
    rows = _req("GET", "campaign_queue?select=id")
    if not rows:
        return 0
    ids = [r["id"] for r in rows]
    # Supprimer une par une (PATCH ne supporte pas DELETE batch proprement)
    for qid in ids:
        _req("DELETE", f"campaign_queue?id=eq.{qid}")
    log.info("[queue] nettoyé: %s entrées supprimées", len(ids))
    return len(ids)
