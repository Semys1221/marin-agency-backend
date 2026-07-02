#!/usr/bin/env python3
"""
Pipeline: Outreach Engine — Entry point orchestrator.

Flux : CLI (crée config) → Rotation (décide quelle niche traiter)
     → Outreach Engine (scrape → valide → push)
     → Slack (notifie à chaque étape)
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pipeline")

_script_dir = Path(__file__).resolve().parent
_dotenv_path = _script_dir
for _ in range(10):
    if (_dotenv_path / ".env.local").exists():
        load_dotenv(_dotenv_path / ".env.local")
        break
    _dotenv_path = _dotenv_path.parent

sys.path.insert(0, str(_script_dir))


def phase_create_tenant(demo: bool):
    from cli.setup import main as create_tenant
    log.info("=== Phase: Create Tenant ===")
    if demo:
        log.info("[DEMO] Tenant creation skipped (interactive CLI)")
        return {"tenant_id": "marin", "niches": [{"name": "grossiste_beaute", "target": 1500}]}
    create_tenant()


def phase_rotation(config: dict, demo: bool) -> list[dict]:
    from rotation_engine.rotation_engine import decide
    log.info("=== Phase: Rotation Engine ===")
    decisions = decide(config, demo=demo)
    log.info("Decisions: %s", json.dumps(decisions, indent=2))
    return decisions


def phase_outreach(decision: dict, config: dict, demo: bool):
    import asyncio
    from cli.config import read_config
    from outreach_engine.email_validator.cleaner import clean_emails
    from outreach_engine.push_instantly.push import push_campaign

    niche = decision.get("niche", "")
    tenant_id = config.get("tenant_id", "")

    if not niche:
        log.warning("No niche to process")
        return

    log.info("=== Phase: Outreach Engine [niche=%s] ===", niche)

    cfg = read_config(tenant_id, demo=demo)
    if not cfg:
        log.error("Config not found for tenant %s", tenant_id)
        return

    niche_cfg = next((n for n in cfg.get("niches", []) if n.get("name") == niche), None)
    if not niche_cfg:
        log.error("Niche %s not found in config", niche)
        return

    log.info("Scraping leads for %s...", niche)
    from outreach_engine.scrape.outscraper_scraper import search_maps, extract_email

    if demo:
        leads = [
            {"name": f"Demo {niche} SARL", "email": f"contact@{niche}.fr",
             "phone": "01 23 45 67 89", "site": f"https://{niche}.fr",
             "full_address": "Paris, France"}
        ] * 10
    else:
        keywords = niche_cfg.get("keywords", [niche])
        results = search_maps(keywords, limit=100, api_key=os.getenv("OUTSCRAPER_API_KEY", ""))
        leads = [r for r in results if extract_email(r)]

    log.info("Got %d leads with email", len(leads))

    from outreach_engine.scrape.lead_filter import filter_leads
    valid_leads = filter_leads(leads)
    log.info("After basic filter: %d leads", len(valid_leads))

    emails = [l.get("email", "") for l in valid_leads if l.get("email")]
    clean = asyncio.run(clean_emails(emails, demo=demo))
    log.info("After cleaning: %d valid, %d invalid",
             len([c for c in clean if c.is_valid]),
             len([c for c in clean if not c.is_valid]))

    campaign_name = niche_cfg.get("instantly_campaign_id", f"{niche}-{tenant_id}")
    push_campaign(tenant_id, campaign_name, create_if_missing=True, dry_run=demo)
    log.info("Push phase complete for '%s'", campaign_name)


def phase_slack(message: str, demo: bool):
    if demo:
        log.info("[DEMO] Slack notification: %s", message)
        return
    from slack_notifier.transport.client import send_message
    send_message(message)


def main():
    parser = argparse.ArgumentParser(description="Outreach Engine Pipeline")
    parser.add_argument("--demo", action="store_true", help="Demo mode (no external calls)")
    parser.add_argument("--create-tenant", action="store_true", help="Create a new tenant interactively")
    parser.add_argument("--tenant", default=os.getenv("TENANT_ID", "marin"), help="Tenant ID")
    parser.add_argument("--config", help="Path to config.json (default: auto-detect)")
    parser.add_argument("--once", action="store_true", help="Run one worker cycle and exit")
    parser.add_argument("--mode", choices=["pipeline", "survivor"], help="Runner mode: pipeline or survivor")
    args = parser.parse_args()

    if args.mode == "survivor":
        from survivor_scheduler import run_until_target
        run_until_target(
            tenant_id=args.tenant,
            target=2000,
            max_cycles=20,
            interval_seconds=60,
            dry_run=args.demo,
        )
        return

    if args.mode == "survivor-cleaner":
        import sys
        sys.argv = [sys.argv[0]]
        from outreach_engine.email_validator.cleaner import main as cleaner_main
        cleaner_main()
        return

    if args.create_tenant:
        phase_create_tenant(demo=args.demo)
        return

    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        from cli.config import read_config
        config = read_config(args.tenant, demo=args.demo)
        if not config:
            log.error("No config found for tenant %s. Use --create-tenant first.", args.tenant)
            sys.exit(1)

    phase_slack(f"🚀 Pipeline started for {config.get('tenant_id')}", demo=args.demo)

    decisions = phase_rotation(config, demo=args.demo)
    for d in decisions:
        action = d.get("action")
        if action == "scrape":
            phase_outreach(d, config, demo=args.demo)
        elif action == "close":
            log.info("Closing niche: %s — %s", d.get("niche"), d.get("reason"))
        elif action == "wait":
            log.info("Waiting: %s", d.get("reason"))

    phase_slack(f"✅ Pipeline finished for {config.get('tenant_id')}", demo=args.demo)

    if not args.once:
        log.info("Starting scheduler for continuous rotation...")
        from rotation_engine.cron import run_loop
        run_loop(demo=args.demo)


if __name__ == "__main__":
    main()
