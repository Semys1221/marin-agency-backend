#!/usr/bin/env python3
"""
Service de Nettoyage — valide les emails de cold_leads vers clean_leads.

Dépendances : supabase, dnspython, httpx
Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   MYEMAILVERIFIER_API_KEY (optionnel),
                   TENANT_ID (optionnel, filtre)

Mode Render cron (--once) :
  python cleaner_service.py --once

Lit cold_leads (non encore traité), valide les emails, écrit dans clean_leads.
"""

import asyncio
import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("cleaner_service")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _push_pending(tenant_id: str):
    """Pousse les leads depuis cold_leads vers clean_leads."""
    from cli.db import get_supabase, is_configured
    from outreach_engine.email_validator.cleaner import clean_emails

    if not is_configured():
        log.error("Supabase non configuré")
        return

    sb = get_supabase()

    # Lit les cold_leads non encore dans clean_leads
    q = sb.table("cold_leads").select("*").eq("tenant_id", tenant_id)
    data = q.execute()
    rows = data.data or []
    if not rows:
        log.info("  Aucun lead à cleaner dans cold_leads")
        return

    emails = [r["email"] for r in rows]
    log.info("  %d leads à valider", len(emails))

    api_key = os.getenv("MYEMAILVERIFIER_API_KEY", "")
    use_api = bool(api_key)

    results = asyncio.run(clean_emails(emails, use_api=use_api, api_key=api_key, demo=False))

    inserted = 0
    for row, r in zip(rows, results):
        record = {
            "tenant_id": tenant_id,
            "campaign_id": row.get("campaign_id", ""),
            "email": r.email,
            "first_name": "",
            "last_name": "",
            "company_name": row.get("company_name", "") or "",
            "domain": row.get("domain", ""),
            "phone": row.get("phone", "") or "",
            "location": row.get("location", "") or "",
            "is_role_based": r.is_role_based,
            "risk_score": r.risk_score,
            "status": "fresh" if r.is_valid else "invalid",
            "metadata": row.get("metadata", {}),
        }
        try:
            existing = sb.table("clean_leads").select("id") \
                .eq("tenant_id", tenant_id) \
                .eq("campaign_id", record["campaign_id"]) \
                .eq("email", r.email).execute()
            if existing.data:
                sb.table("clean_leads").update(record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("clean_leads").insert(record).execute()
            inserted += 1
        except Exception as e:
            log.warning("  Upsert error %s: %s", r.email, e)

    valid = sum(1 for r in results if r.is_valid)
    invalid = sum(1 for r in results if not r.is_valid)
    log.info("  %d/%d écrits dans clean_leads (valid=%d, invalid=%d)",
             inserted, len(results), valid, invalid)


def run_for_tenant(tenant_id: str):
    log.info("═ %s ═", tenant_id)
    _push_pending(tenant_id)


def run_all():
    from cli.scraping.tenant import list_tenants

    log.info("═" * 50)
    log.info("  CLEANER SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
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

    interval_minutes = int(os.getenv("CLEANER_INTERVAL_MINUTES", "5"))
    log.info("  [cleaner] Mode survivor démarré (toutes les %d min)", interval_minutes)
    while True:
        run_all()
        for _ in range(interval_minutes * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cleaner Service")
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
