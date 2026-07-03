#!/usr/bin/env python3
"""
Service de Rotation — décide quelle niche scraper et quand.

Dépendances : APScheduler, supabase
Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, TENANT_ID (optionnel)

Mode Render cron (--once) :
  python rotation_service.py --once

Mode développement (loop) :
  python rotation_service.py
"""

import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("rotation_service")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

INTERVAL = int(os.getenv("ROTATION_INTERVAL_MINUTES", "15"))

# ── Imports paresseux (evite les circular imports) ──


def _run_for_tenant(tenant_id: str) -> list[dict]:
    from cli.scraping.tenant import get_tenant
    from rotation_engine.rotation_engine import decide

    config = get_tenant(tenant_id)
    if not config:
        log.warning("  [rotation] Tenant %s introuvable", tenant_id)
        return []

    log.info("  [rotation] Décision pour %s...", tenant_id)
    result = decide(config, demo=False)
    for d in result:
        log.info("    → %s: %s", d.get("action", "?"), d.get("niche", d.get("reason", "")))
    return result


def run_all():
    from cli.scraping.tenant import list_tenants

    log.info("═" * 50)
    log.info("  ROTATION SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
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
        _run_for_tenant(tid)


def run_once():
    run_all()


def run_loop():
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except ImportError:
        log.warning("APScheduler non installé. Exécution unique puis sortie.")
        run_once()
        return

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all, "interval", minutes=INTERVAL,
                      id="rotation", replace_existing=True)
    scheduler.start()
    log.info("  [rotation] Scheduler démarré (toutes les %d min)", INTERVAL)

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info("  [rotation] Arrêt demandé...")
        scheduler.shutdown(wait=False)


def run_survivor():
    """Mode Render Web Service : health endpoint + boucle."""
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass

    log.info("  [rotation] Mode survivor démarré (toutes les %d min)", INTERVAL)
    while True:
        run_all()
        for _ in range(INTERVAL * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rotation Service")
    parser.add_argument("--once", action="store_true", help="Execute once and exit")
    parser.add_argument("--survivor", action="store_true", help="Survivor loop (Render)")
    args = parser.parse_args()

    if args.survivor:
        run_survivor()
    elif args.once:
        run_once()
    else:
        run_loop()
