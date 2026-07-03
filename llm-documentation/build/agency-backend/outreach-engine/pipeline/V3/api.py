#!/usr/bin/env python3
"""
Prospection V3 — Mass scraping France.

Workflow :
  1. Scrape (Outscraper, ~20 leads/ville, 100 villes)
  2. Clean 1 — DNS MX check (gratuit, rapide)
  3. Clean 2 — MyEmailVerifier API (payant, précis)
  4. Push vers Instantly
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
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("v3")

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

app = FastAPI(title="Prospection Mass Scrape V3")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Top 100 villes françaises ──
FR_CITIES = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
    "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Angers",
    "Grenoble", "Dijon", "Nîmes", "Aix-en-Provence", "Saint-Quentin-en-Yvelines", "Brest",
    "Le Mans", "Amiens", "Tours", "Limoges", "Clermont-Ferrand", "Villeurbanne", "Besançon",
    "Orléans", "Metz", "Rouen", "Caen", "Mulhouse", "Perpignan", "Nancy", "La Rochelle",
    "Fort-de-France", "Saint-Denis", "Argenteuil", "Montreuil", "Dunkerque", "Tourcoing",
    "Avignon", "Nanterre", "Créteil", "Poitiers", "Versailles", "Courbevoie", "Vitry-sur-Seine",
    "Colombes", "Pau", "Aulnay-sous-Bois", "Asnières-sur-Seine", "Rueil-Malmaison", "Saint-Pierre",
    "Champigny-sur-Marne", "La Courneuve", "Saint-Maur-des-Fossés", "Antibes", "Calais", "Béziers",
    "Cannes", "Saint-Nazaire", "Colmar", "Bourges", "Drancy", "Mérignac", "La Seyne-sur-Mer",
    "Noisy-le-Grand", "Issy-les-Moulineaux", "Levallois-Perret", "Quimper", "Ivry-sur-Seine",
    "Vénissieux", "Cergy", "Cayenne", "Pessac", "Troyes", "Niort", "Valence", "Antony",
    "Chambéry", "Montauban", "Sarcelles", "Les Abymes", "Lorient", "Villejuif", "Hyères",
    "Saint-André", "Épinay-sur-Seine", "Pantin", "Maisons-Alfort", "Évreux", "Fontenay-sous-Bois",
    "Bondy", "Chelles", "Clamart", "Cholet", "Vannes", "Arles", "Fréjus", "Sartrouville",
    "Meaux", "Bayonne", "Grasse", "Laval", "Sevran", "Niort", "Albi",
]


# ── Models ──

class ScrapeJobRequest(BaseModel):
    niche: str
    target: int = 5000


class PushRequest(BaseModel):
    queue_id: str
    instantly_campaign_id: str


# ── Supabase helpers ──

def _sb(method: str, path: str, json_data=None):
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


def _sb_patch(path: str, data: dict):
    import httpx
    r = httpx.patch(
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                 "Content-Type": "application/json"},
        json=data,
        timeout=15,
    )
    r.raise_for_status()
    return r.json() if r.text else []


# ── Scraping ──

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


# ── Cleaning 1: DNS MX check (gratuit) ──

def _clean_mx(email: str) -> bool:
    """Vérifie que le domaine a un MX record. Rapide et gratuit."""
    import dns.resolver
    domain = email.split("@")[-1] if "@" in email else ""
    if not domain:
        return False
    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except Exception:
        return False


# ── Cleaning 2: MyEmailVerifier (payant, précis) ──

def _clean_verifier(email: str) -> bool:
    """Valide via MyEmailVerifier API. Précis mais coûteux."""
    import httpx
    api_key = os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "MYEMAILVERIFIER_API_KEY non configurée")
    try:
        r = httpx.get(
            "https://api.myemailverifier.com/api/verifier/verify",
            params={"email": email},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        return r.json().get("status") == "valid"
    except Exception:
        return False


# ── Instantly ──

def _instantly_campaigns() -> list[dict]:
    import httpx
    api_key = os.getenv("INSTANTLY_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "INSTANTLY_API_KEY non configurée")
    r = httpx.get("https://api.instantly.ai/api/v2/campaigns",
                  headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    campaigns = data.get("items", [])
    return [{"id": c["id"], "name": c.get("name", c["id"])} for c in campaigns]


def _instantly_push(campaign_id: str, leads: list[dict]) -> dict:
    import httpx
    api_key = os.getenv("INSTANTLY_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "INSTANTLY_API_KEY non configurée")
    payload = {
        "campaign_id": campaign_id,
        "leads": [
            {
                "email": l["email"],
                "first_name": "",
                "last_name": "",
                "company_name": l.get("company_name", ""),
                "phone_number": l.get("phone", ""),
                "location": l.get("city", ""),
            }
            for l in leads if l.get("email")
        ],
    }
    r = httpx.post("https://api.instantly.ai/api/v2/campaigns/add-leads",
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
    return _instantly_campaigns()


# ── STEP 1: Scrape ──

@app.post("/api/scrape-job")
async def scrape_job(req: ScrapeJobRequest):
    """Mass scraping — streams progress. No validation, just raw scrape."""
    async def generate():
        queue = _sb("POST", "campaign_queue", {
            "niche": req.niche,
            "city": "France",
            "status": "scraping",
            "include_keywords": req.niche,
            "batch": 1,
            "priority": 1,
        })
        queue_id = queue[0]["id"]

        yield f"data: {json.dumps({'type': 'start', 'queue_id': queue_id, 'target': req.target})}\n\n"

        total_scraped = 0
        cities_done = 0

        for city in FR_CITIES:
            if total_scraped >= req.target:
                break

            try:
                keywords = [f"{req.niche} {city}"]
                limit = min(20, req.target - total_scraped)

                raw = _outscraper_search(keywords, limit)
                count = 0

                for entry in raw:
                    email = entry.get("email", "")
                    phone = _normalize_phone(entry.get("phone", ""))
                    if not email and not phone:
                        continue
                    lead = {
                        "campaign_queue_id": queue_id,
                        "place_id": entry.get("place_id", ""),
                        "email": email or f"no-email-{phone}",
                        "first_name": entry.get("first_name", "") or "",
                        "company_name": entry.get("name", "") or "",
                        "domain": email.split("@")[-1] if "@" in email else "",
                        "phone": phone,
                        "location": entry.get("full_address", "") or "",
                        "niche": req.niche,
                        "status": "scraped",
                        "valid": False,
                        "city": city,
                    }
                    try:
                        _sb("POST", "leads", lead)
                        count += 1
                    except Exception:
                        pass  # duplicate

                total_scraped += count
                cities_done += 1
                yield f"data: {json.dumps({'type': 'progress', 'total': total_scraped, 'city': city, 'city_count': count})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'city': city, 'message': str(e)})}\n\n"

        _sb_patch(f"campaign_queue?id=eq.{queue_id}",
                  {"status": "scraped", "updated_at": datetime.now(timezone.utc).isoformat()})

        yield f"data: {json.dumps({'type': 'done', 'total': total_scraped, 'cities': cities_done})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# ── STEP 2: Clean 1 — DNS MX (gratuit, rapide) ──

@app.post("/api/clean-1")
async def clean1(req: dict):
    """DNS MX check sur les leads scraped. Stream progress."""
    queue_id = req["queue_id"]

    async def generate():
        leads = _sb_get(f"leads?campaign_queue_id=eq.{queue_id}&status=eq.scraped&select=*")
        # Filtrer les no-email
        leads = [l for l in leads if l.get("email") and not l["email"].startswith("no-email")]

        total = len(leads)
        valid_count = 0
        invalid_count = 0

        yield f"data: {json.dumps({'type': 'start', 'total': total})}\n\n"

        # Cache MX par domaine (evite de requêter 50x le même domaine)
        mx_cache = {}

        for i, lead in enumerate(leads):
            email = lead["email"]
            domain = email.split("@")[-1]

            if domain in mx_cache:
                has_mx = mx_cache[domain]
            else:
                has_mx = _clean_mx(email)
                mx_cache[domain] = has_mx

            new_status = "cleaned_v1" if has_mx else "invalid"
            try:
                _sb_patch(f"leads?id=eq.{lead['id']}",
                          {"status": new_status, "valid": has_mx,
                           "updated_at": datetime.now(timezone.utc).isoformat()})
            except Exception:
                pass

            if has_mx:
                valid_count += 1
            else:
                invalid_count += 1

            # Progress tous les 50 leads
            if (i + 1) % 50 == 0 or i + 1 == total:
                yield f"data: {json.dumps({'type': 'progress', 'processed': i + 1, 'total': total, 'valid': valid_count, 'invalid': invalid_count})}\n\n"

        _sb_patch(f"campaign_queue?id=eq.{queue_id}",
                  {"status": "cleaned_v1", "updated_at": datetime.now(timezone.utc).isoformat()})

        yield f"data: {json.dumps({'type': 'done', 'total': total, 'valid': valid_count, 'invalid': invalid_count})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# ── STEP 3: Clean 2 — MyEmailVerifier (payant, précis) ──

@app.post("/api/clean-2")
async def clean2(req: dict):
    """MyEmailVerifier API sur les leads cleaned_v1. Stream progress."""
    queue_id = req["queue_id"]

    api_key = os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "MYEMAILVERIFIER_API_KEY non configurée")

    async def generate():
        leads = _sb_get(f"leads?campaign_queue_id=eq.{queue_id}&status=eq.cleaned_v1&valid=eq.true&select=*")

        total = len(leads)
        valid_count = 0
        invalid_count = 0

        yield f"data: {json.dumps({'type': 'start', 'total': total})}\n\n"

        for i, lead in enumerate(leads):
            email = lead["email"]

            is_valid = _clean_verifier(email)

            new_status = "cleaned_v2" if is_valid else "invalid_v2"
            try:
                _sb_patch(f"leads?id=eq.{lead['id']}",
                          {"status": new_status, "valid": is_valid,
                           "updated_at": datetime.now(timezone.utc).isoformat()})
            except Exception:
                pass

            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1

            # Progress tous les 10 leads (API plus lente)
            if (i + 1) % 10 == 0 or i + 1 == total:
                yield f"data: {json.dumps({'type': 'progress', 'processed': i + 1, 'total': total, 'valid': valid_count, 'invalid': invalid_count})}\n\n"

        _sb_patch(f"campaign_queue?id=eq.{queue_id}",
                  {"status": "cleaned_v2", "updated_at": datetime.now(timezone.utc).isoformat()})

        yield f"data: {json.dumps({'type': 'done', 'total': total, 'valid': valid_count, 'invalid': invalid_count})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# ── STEP 4: Push vers Instantly ──

@app.post("/api/push-job")
def push_job(req: PushRequest):
    """Push leads valides vers Instantly. Utilise cleaned_v2 si disponible, sinon cleaned_v1."""
    # Essayer cleaned_v2 d'abord, sinon cleaned_v1
    leads = _sb_get(f"leads?campaign_queue_id=eq.{req.queue_id}&status=eq.cleaned_v2&valid=eq.true&select=*")
    if not leads:
        leads = _sb_get(f"leads?campaign_queue_id=eq.{req.queue_id}&status=eq.cleaned_v1&valid=eq.true&select=*")

    if not leads:
        raise HTTPException(400, "Aucun lead valide à pusher")

    log.info("[push] %d leads → instantly %s", len(leads), req.instantly_campaign_id)
    result = _instantly_push(req.instantly_campaign_id, leads)

    for lead in leads:
        try:
            _sb_patch(f"leads?id=eq.{lead['id']}",
                      {"status": "imported_instantly",
                       "updated_at": datetime.now(timezone.utc).isoformat()})
        except Exception:
            pass

    _sb_patch(f"campaign_queue?id=eq.{req.queue_id}",
              {"status": "done", "updated_at": datetime.now(timezone.utc).isoformat()})

    return {"pushed": len(leads), "result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
