#!/usr/bin/env python3
"""
Service de Scraping — scrape Google Maps via Outscraper pour les niches actives.

Dépendances : outscraper, supabase
Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   OUTSCRAPER_API_KEY, OUTSCRAPER_ENRICHMENT,
                   TENANT_ID (optionnel, filtre)

Mode Render cron (--once) :
  python scraper_service.py --once

Lit rotation_state dans Supabase pour savoir quelle niche scraper.
Sauvegarde les résultats dans cold_leads.
"""

import asyncio
import json
import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("scraper_service")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MAX_SCRAPE_PER_CYCLE = 3
MAX_VALIDATE_PER_CYCLE = 20


def _scrape_niche(tenant_id: str, niche_name: str, keywords: list[str],
                  target: int, campaign_id: str):
    """Scrape → filtre → sauvegarde en cold_leads. Pas de validation email ici."""
    from outreach_engine.scrape.outscraper_scraper import search_maps, normalize_phone
    from outreach_engine.scrape.lead_filter import filter_leads
    from cli.db import get_supabase

    log.info("  [scraper] Niche=%s keywords=%s target=%d", niche_name, keywords, target)

    enrichment = os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(",")
    results = search_maps(keywords, limit=20, language="fr",
                          enrichment=enrichment,
                          api_key=os.getenv("OUTSCRAPER_API_KEY", ""))
    log.info("  [scraper] %d résultats bruts", len(results))

    valid = filter_leads(results)
    log.info("  [scraper] %d leads valides (email ou téléphone)", len(valid))

    # Sauvegarde dans cold_leads
    sb = get_supabase()
    if not sb:
        log.error("  [scraper] Supabase non configuré")
        return

    count = 0
    for entry in valid:
        email = entry.get("email", "")
        raw_phone = entry.get("phone", "")
        address = entry.get("full_address", "") or ""
        if not address:
            parts = [entry.get("city", ""), entry.get("postal_code", ""), entry.get("country_code", "")]
            address = ", ".join(p for p in parts if p)

        record = {
            "tenant_id": tenant_id,
            "email": email or f"no-email-{raw_phone}",
            "company_name": entry.get("name", "") or "",
            "phone": normalize_phone(raw_phone),
            "location": address,
            "country_code": entry.get("country_code", ""),
            "source": "outscraper",
            "campaign_id": campaign_id,
            "metadata": entry,
        }
        try:
            existing = sb.table("cold_leads").select("id").eq("tenant_id", tenant_id).eq("email", email).execute()
            data = getattr(existing, "data", None) or []
            if data:
                sb.table("cold_leads").update(record).eq("id", data[0]["id"]).execute()
            else:
                sb.table("cold_leads").insert(record).execute()
            count += 1
        except Exception:
            pass
    log.info("  [scraper] %d leads → cold_leads", count)


def run_for_tenant(tenant_id: str):
    """Scrape les niches actives pour un tenant."""
    from cli.scraping.tenant import get_tenant
    from rotation_engine.rotation_state import list_states

    config = get_tenant(tenant_id)
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return

    states = list_states(tenant_id)
    state_map = {s["niche_name"]: s for s in states}

    scraped = 0
    for n in config.get("niches", []):
        if scraped >= MAX_SCRAPE_PER_CYCLE:
            break

        name = n.get("name", "")
        s = state_map.get(name, {})
        status = s.get("status", "pending")

        # Ne scrape que les niches actives ou pending
        if status not in ("active", "pending"):
            continue

        campaign_id = n.get("instantly_campaign_id") or f"{name}-{tenant_id}"
        keywords = n.get("keywords", [name])
        target = n.get("target", 1000)

        _scrape_niche(tenant_id, name, keywords, target, campaign_id)
        scraped += 1


def run_all():
    from cli.scraping.tenant import list_tenants

    log.info("═" * 50)
    log.info("  SCRAPER SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("═" * 50)

    tenant_filter = os.getenv("TENANT_ID", "")
    tenants = list_tenants()
    if not tenants:
        log.info("  Aucun tenant trouvé")
        return

    for config in tenants:
        tid = config.get("tenant_id", "")
        if not tid:
            continue
        if tenant_filter and tid != tenant_filter:
            continue
        run_for_tenant(tid)


def run_once():
    run_all()


def run_survivor():
    """Mode Render Web Service : health endpoint + boucle."""
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass

    interval_minutes = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "15"))
    log.info("  [scraper] Mode survivor démarré (toutes les %d min)", interval_minutes)
    while True:
        run_all()
        for _ in range(interval_minutes * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scraper Service")
    parser.add_argument("--once", action="store_true", help="Execute once and exit")
    parser.add_argument("--survivor", action="store_true", help="Survivor loop (Render)")
    parser.add_argument("--tenant", help="Tenant ID (override env)")
    args = parser.parse_args()

    if args.tenant:
        os.environ["TENANT_ID"] = args.tenant
    if args.survivor:
        run_survivor()
    else:
        run_once()
