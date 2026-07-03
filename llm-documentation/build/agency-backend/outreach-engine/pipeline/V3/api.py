#!/usr/bin/env python3
"""
Prospection manuelle — API simple pour scraper, valider et pousser des leads.

Usage :
  python api.py
  → Ouvre http://localhost:8000
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("v3")

load_dotenv()

app = FastAPI(title="Prospection Manuelle V3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ──


class ScrapeRequest(BaseModel):
    keywords: list[str]
    limit: int = 20


class PushRequest(BaseModel):
    campaign_id: str
    leads: list[dict]


# ── Helpers ──


def _outscraper_search(keywords: list[str], limit: int) -> list[dict]:
    """Scrape Google Maps via Outscraper."""
    from outscraper import ApiClient

    api_key = os.getenv("OUTSCRAPER_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="OUTSCRAPER_API_KEY non configurée")

    enrichment = os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(",")

    client = ApiClient(api_key=api_key)
    results = client.google_maps_search(
        query=keywords,
        limit=limit,
        language="fr",
        enrichment=enrichment,
    )
    # Outscraper retourne une liste de listes
    if results and isinstance(results[0], list):
        results = results[0]
    return results or []


def _normalize_phone(raw: str) -> str:
    """Normalise un numéro français."""
    if not raw:
        return ""
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 10 and digits.startswith("0"):
        return "+33" + digits[1:]
    if digits.startswith("33"):
        return "+" + digits
    return raw


def _filter_leads(raw: list[dict]) -> list[dict]:
    """Garde uniquement les leads avec email ou téléphone."""
    valid = []
    for entry in raw:
        email = entry.get("email", "")
        phone = entry.get("phone", "")
        if not email and not phone:
            continue
        valid.append({
            "email": email or "",
            "phone": _normalize_phone(phone),
            "company_name": entry.get("name", "") or "",
            "location": entry.get("full_address", "") or entry.get("city", "") or "",
            "website": entry.get("website", "") or "",
        })
    return valid


def _validate_emails(emails: list[str]) -> dict[str, bool]:
    """Valide les emails. Retourne {email: is_valid}."""
    if not emails:
        return {}

    api_key = os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if not api_key:
        # Fallback: DNS MX check basique
        import dns.resolver
        result = {}
        for email in emails:
            domain = email.split("@")[-1] if "@" in email else ""
            try:
                dns.resolver.resolve(domain, "MX")
                result[email] = True
            except Exception:
                result[email] = False
        return result

    # MyEmailVerifier API
    import httpx
    result = {}
    for email in emails:
        try:
            r = httpx.get(
                "https://api.myemailverifier.com/api/verifier/verify",
                params={"email": email},
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )
            data = r.json()
            result[email] = data.get("status") == "valid"
        except Exception:
            result[email] = False
    return result


def _instantly_campaigns() -> list[dict]:
    """Liste les campagnes Instantly."""
    import httpx

    api_key = os.getenv("INSTANTLY_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="INSTANTLY_API_KEY non configurée")

    r = httpx.get(
        "https://api.instantly.ai/api/v1/list_campaigns",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    campaigns = data.get("results", [])
    return [{"id": c["id"], "name": c.get("name", c["id"])} for c in campaigns]


def _instantly_push(campaign_id: str, leads: list[dict]):
    """Push leads vers une campagne Instantly."""
    import httpx

    api_key = os.getenv("INSTANTLY_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="INSTANTLY_API_KEY non configurée")

    # Format Instantly
    payload = {
        "campaign_id": campaign_id,
        "leads": [
            {
                "email": lead["email"],
                "first_name": "",
                "last_name": "",
                "company_name": lead.get("company_name", ""),
                "phone_number": lead.get("phone", ""),
                "location": lead.get("location", ""),
            }
            for lead in leads
            if lead.get("email")
        ],
    }

    r = httpx.post(
        "https://api.instantly.ai/api/v1/add_leads",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


# ── Routes ──


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/api/campaigns")
def get_campaigns():
    """Liste les campagnes Instantly disponibles."""
    try:
        return _instantly_campaigns()
    except Exception as e:
        log.error("Erreur campagnes: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scrape")
def scrape(req: ScrapeRequest):
    """Scrape Google Maps et retourne les leads filtrés."""
    try:
        log.info("[scrape] keywords=%s limit=%d", req.keywords, req.limit)
        raw = _outscraper_search(req.keywords, req.limit)
        log.info("[scrape] %d résultats bruts", len(raw))
        leads = _filter_leads(raw)
        log.info("[scrape] %d leads valides", len(leads))
        return {"count": len(leads), "leads": leads}
    except HTTPException:
        raise
    except Exception as e:
        log.error("Erreur scrape: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/validate")
def validate(req: dict):
    """Valide les emails d'une liste de leads."""
    leads = req.get("leads", [])
    emails = [l["email"] for l in leads if l.get("email")]
    log.info("[validate] %d emails à valider", len(emails))

    try:
        results = _validate_emails(emails)
        valid_leads = [l for l in leads if results.get(l.get("email", ""), False)]
        log.info("[validate] %d/%d valides", len(valid_leads), len(emails))
        return {"total": len(emails), "valid": len(valid_leads), "leads": valid_leads}
    except Exception as e:
        log.error("Erreur validate: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/push")
def push(req: PushRequest):
    """Push les leads vers une campagne Instantly."""
    if not req.leads:
        raise HTTPException(status_code=400, detail="Aucun lead à pusher")

    try:
        log.info("[push] %d leads → campaign %s", len(req.leads), req.campaign_id)
        result = _instantly_push(req.campaign_id, req.leads)
        log.info("[push] OK: %s", result)
        return {"pushed": len(req.leads), "result": result}
    except HTTPException:
        raise
    except Exception as e:
        log.error("Erreur push: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
