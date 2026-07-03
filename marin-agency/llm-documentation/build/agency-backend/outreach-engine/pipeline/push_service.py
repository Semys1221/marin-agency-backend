#!/usr/bin/env python3
"""
Service de Push — pousse les leads clean vers Instantly.

Dépendances : supabase, httpx, requests
Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   INSTANTLY_API_KEY,
                   TENANT_ID (optionnel, filtre)

Mode Render cron (--once) :
  python push_service.py --once

Lit les clean_leads (status='fresh') et les push vers les campagnes Instantly.
Crée les campagnes si elles n'existent pas (create_if_missing=true).
"""

import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("push_service")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def push_for_tenant(tenant_id: str):
    """Pousse toutes les campagnes d'un tenant."""
    from cli.scraping.tenant import get_tenant
    from outreach_engine.push_instantly.push import push_campaign, push_all

    config = get_tenant(tenant_id)
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return

    # D'abord les campagnes configurées dans le tenant
    for niche in config.get("niches", []):
        campaign_name = niche.get("instantly_campaign_id") or f"{niche['name']}-{tenant_id}"
        log.info("  [push] Campagne: %s", campaign_name)
        push_campaign(tenant_id, campaign_name, create_if_missing=True, dry_run=False)

    # Ensuite les campagnes orphelines (sans niche config)
    from outreach_engine.push_instantly.lib.db import get_distinct_campaigns
    extra = get_distinct_campaigns(tenant_id)
    configured = {n.get("instantly_campaign_id") or f"{n['name']}-{tenant_id}"
                  for n in config.get("niches", [])}
    for name in extra:
        if name not in configured:
            log.info("  [push] Campagne orpheline: %s", name)
            push_campaign(tenant_id, name, create_if_missing=True, dry_run=False)


def run_all():
    from cli.scraping.tenant import list_tenants

    log.info("═" * 50)
    log.info("  PUSH SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("═" * 50)

    if not os.getenv("INSTANTLY_API_KEY"):
        log.error("INSTANTLY_API_KEY non définie")
        return

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
        push_for_tenant(tid)


def run_once():
    run_all()


def run_survivor():
    """Mode Render Web Service : health endpoint + boucle."""
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass

    interval_minutes = int(os.getenv("PUSH_INTERVAL_MINUTES", "30"))
    log.info("  [push] Mode survivor démarré (toutes les %d min)", interval_minutes)
    while True:
        run_all()
        for _ in range(interval_minutes * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Push Service")
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
