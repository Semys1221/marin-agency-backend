#!/usr/bin/env python3
"""
Prospection manuelle V3 — Supabase + Smartlead.

Flow :
  1. Créer une entrée campaign_queue (niche + city + keywords)  → status: pending
  2. Scraper (Outscraper)                                       → leads status: scraped
  3. Valider emails                                             → leads status: cleaned
  4. Push Smartlead                                             → leads status: imported_smartlead
                                                                  campaign_queue status: done

Usage :
  python api.py
  → http://localhost:8000
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("v3")

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

app = FastAPI(title="Prospection Manuelle V3")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ── Models ──

class CreateQueueRequest(BaseModel):
    niche: str
    city: str
    include_keywords: Optional[str] = None
    exclude_keywords: Optional[str] = None
    smartlead_campaign_id: Optional[int] = None
    priority: int = 1


class ScrapeRequest(BaseModel):
    queue_id: str
    limit: int = 20


class PushRequest(BaseModel):
    queue_id: str
    smartlead_campaign_id: int


# ── Supabase helpers ──

def _sb(method: str, path: str, json_data=None):
    """Simple Supabase REST helper."""
    import httpx
    r = httpx.request(
        method,
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                 "Content-Type": "application/json", "Prefer": "return=representation"},
        json=json_data,
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _sb_get(path: str):
    import httpx
    r = httpx.get(
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _update_queue_status(queue_id: str, status: str):
    _sb("PATCH", f"campaign_queue?id=eq.{queue_id}",
        {"status": status, "updated_at": datetime.now(timezone.utc).isoformat()})


# ── Scrape ──

def _outscraper_search(keywords: list[str], limit: int) -> list[dict]:
    from outscraper import ApiClient
    api_key = os.getenv("OUTSCRAPER_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "OUTSCRAPER_API_KEY non configurée")
    enrichment = os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(",")
    client = ApiClient(api_key=api_key)
    results = client.google_maps_search(query=keywords, limit=limit, language="fr", enrichment=enrichment)
    if results and isinstance(results[0], list):
        results = results[0]
    return results or []


def _normalize_phone(raw: str) -> str:
    if not raw:
        return ""
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 10 and digits.startswith("0"):
        return "+33" + digits[1:]
    if digits.startswith("33"):
        return "+" + digits
    return raw


# ── Validate ──

def _validate_emails(emails: list[str]) -> dict[str, bool]:
    if not emails:
        return {}
    import dns.resolver
    api_key = os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if api_key:
        import httpx
        result = {}
        for email in emails:
            try:
                r = httpx.get("https://api.myemailverifier.com/api/verifier/verify",
                              params={"email": email},
                              headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
                result[email] = r.json().get("status") == "valid"
            except Exception:
                result[email] = False
        return result
    # Fallback: MX check
    result = {}
    for email in emails:
        domain = email.split("@")[-1] if "@" in email else ""
        try:
            dns.resolver.resolve(domain, "MX")
            result[email] = True
        except Exception:
            result[email] = False
    return result


# ── Smartlead ──

def _smartlead_campaigns() -> list[dict]:
    import httpx
    api_key = os.getenv("SMARTLEAD_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "SMARTLEAD_API_KEY non configurée")
    r = httpx.get("https://api.smartlead.ai/v1/campaigns",
                  headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    campaigns = data.get("campaigns", [])
    return [{"id": c["id"], "name": c.get("name", str(c["id"]))} for c in campaigns]


def _smartlead_push(campaign_id: int, leads: list[dict]) -> dict:
    import httpx
    api_key = os.getenv("SMARTLEAD_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "SMARTLEAD_API_KEY non configurée")
    payload = {
        "campaign_id": campaign_id,
        "lead_list": [
            {
                "email": l["email"],
                "first_name": l.get("first_name", ""),
                "last_name": "",
                "company_name": l.get("company_name", ""),
                "phone_number": l.get("phone", ""),
                "location": l.get("city", ""),
            }
            for l in leads if l.get("email")
        ],
    }
    r = httpx.post("https://api.smartlead.ai/v1/campaigns/add-leads",
                   json=payload,
                   headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
    r.raise_for_status()
    return r.json()


# ── Routes ──

@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/api/campaigns")
def get_campaigns():
    """Smartlead campaigns."""
    return _smartlead_campaigns()


@app.get("/api/queue")
def list_queue():
    """Liste les campaign_queue entries."""
    return _sb_get("campaign_queue?select=*&order=created_at.desc&limit=50")


@app.post("/api/queue")
def create_queue(req: CreateQueueRequest):
    """Crée une entrée campaign_queue (pending)."""
    data = {
        "niche": req.niche,
        "city": req.city,
        "status": "pending",
        "smartlead_campaign_id": req.smartlead_campaign_id,
        "batch": 1,
        "priority": req.priority,
        "include_keywords": req.include_keywords,
        "exclude_keywords": req.exclude_keywords,
    }
    result = _sb("POST", "campaign_queue", data)
    log.info("[queue] Créé: %s", result[0]["id"])
    return result[0]


@app.post("/api/scrape")
def scrape(req: ScrapeRequest):
    """Scrape pour un campaign_queue → insère leads."""
    # Fetch queue entry
    queue = _sb_get(f"campaign_queue?id=eq.{req.queue_id}")
    if not queue:
        raise HTTPException(404, "Queue entry introuvable")
    q = queue[0]

    _update_queue_status(req.queue_id, "scraping")

    # Build keywords
    keywords = []
    if q.get("include_keywords"):
        keywords = [k.strip() for k in q["include_keywords"].split(",") if k.strip()]
    if not keywords:
        niche_city = f"{q['niche']} {q['city']}"
        keywords = [niche_city]

    log.info("[scrape] queue=%s keywords=%s limit=%d", req.queue_id, keywords, req.limit)
    raw = _outscraper_search(keywords, req.limit)
    log.info("[scrape] %d résultats bruts", len(raw))

    # Insert leads
    count = 0
    for entry in raw:
        email = entry.get("email", "")
        phone = _normalize_phone(entry.get("phone", ""))
        if not email and not phone:
            continue
        lead = {
            "campaign_queue_id": req.queue_id,
            "place_id": entry.get("place_id", ""),
            "email": email or f"no-email-{phone}",
            "first_name": entry.get("first_name", "") or "",
            "company_name": entry.get("name", "") or "",
            "domain": email.split("@")[-1] if "@" in email else "",
            "phone": phone,
            "location": entry.get("full_address", "") or "",
            "niche": q["niche"],
            "status": "scraped",
            "valid": False,
            "city": q["city"],
        }
        try:
            _sb("POST", "leads", lead)
            count += 1
        except Exception:
            pass  # duplicate

    log.info("[scrape] %d leads insérés", count)
    _update_queue_status(req.queue_id, "scraped")
    return {"scraped": count, "queue_id": req.queue_id}


@app.post("/api/validate")
def validate(req: dict):
    """Valide les emails scraped pour un queue_id."""
    queue_id = req["queue_id"]
    leads = _sb_get(f"leads?campaign_queue_id=eq.{queue_id}&status=eq.scraped&select=*")
    if not leads:
        return {"validated": 0, "valid": 0}

    emails = [l["email"] for l in leads if l.get("email") and not l["email"].startswith("no-email")]
    results = _validate_emails(emails)

    valid_count = 0
    for lead in leads:
        email = lead.get("email", "")
        if email.startswith("no-email"):
            continue
        is_valid = results.get(email, False)
        try:
            _sb("PATCH", f"leads?id=eq.{lead['id']}",
                {"valid": is_valid, "status": "cleaned" if is_valid else "invalid",
                 "updated_at": datetime.now(timezone.utc).isoformat()})
            if is_valid:
                valid_count += 1
        except Exception:
            pass

    log.info("[validate] %d/%d valides", valid_count, len(emails))
    return {"total": len(emails), "valid": valid_count, "queue_id": queue_id}


@app.get("/api/leads")
def list_leads(queue_id: str, status: Optional[str] = None):
    """Liste les leads pour un queue_id."""
    query = f"leads?campaign_queue_id=eq.{queue_id}&select=*&order=created_at.desc"
    if status:
        query += f"&status=eq.{status}"
    return _sb_get(query)


@app.post("/api/push")
def push(req: PushRequest):
    """Push leads cleaned vers Smartlead."""
    leads = _sb_get(f"leads?campaign_queue_id=eq.{req.queue_id}&status=eq.cleaned&valid=eq.true&select=*")
    if not leads:
        raise HTTPException(400, "Aucun lead cleaned à pusher")

    log.info("[push] %d leads → smartlead campaign %d", len(leads), req.smartlead_campaign_id)
    result = _smartlead_push(req.smartlead_campaign_id, leads)

    # Update leads status
    for lead in leads:
        try:
            _sb("PATCH", f"leads?id=eq.{lead['id']}",
                {"status": "imported_smartlead",
                 "updated_at": datetime.now(timezone.utc).isoformat()})
        except Exception:
            pass

    # Update queue
    _sb("PATCH", f"campaign_queue?id=eq.{req.queue_id}",
        {"status": "done", "smartlead_campaign_id": req.smartlead_campaign_id,
         "updated_at": datetime.now(timezone.utc).isoformat()})

    log.info("[push] OK: %d leads pushés", len(leads))
    return {"pushed": len(leads), "result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
