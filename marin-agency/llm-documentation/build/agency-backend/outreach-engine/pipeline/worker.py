"""
Worker — orchestrateur autonome du pipeline.

Exécute toutes les 6h (via cron) :
1. Push les leads non envoyés vers Instantly
2. Vérifie la rotation → décide quelles niches scraper
3. Scrape → valide → sauvegarde en clean_leads
4. Notifie Slack

Usage :
  python3 worker.py                  # cycle complet
  python3 worker.py --tenant X       # un seul tenant
  python3 worker.py --dry-run        # sans effets de bord
  python3 worker.py --once           # alias de la valeur par défaut
"""

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [worker] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("worker")

_script_dir = Path(__file__).resolve().parent
_dotenv_path = _script_dir
for _ in range(10):
    if (_dotenv_path / ".env.local").exists():
        load_dotenv(_dotenv_path / ".env.local")
        break
    _dotenv_path = _dotenv_path.parent


def _push_pending_leads(tenant_id: str, dry_run: bool = False):
    """Push tout les clean_leads non encore envoyés vers Instantly."""
    from outreach_engine.push_instantly.push import push_campaign
    from outreach_engine.push_instantly.lib.db import get_distinct_campaigns, fetch_clean_leads

    campaign_names = get_distinct_campaigns(tenant_id)
    if not campaign_names:
        log.info("  [push] Aucune campagne à pousser pour %s", tenant_id)
        return

    log.info("  [push] %d campagne(s) à traiter: %s", len(campaign_names), campaign_names)
    for name in campaign_names:
        rows = fetch_clean_leads(tenant_id, campaign_name=name)
        if not rows:
            continue
        log.info("  [push] %d leads pour %s → push...", len(rows), name)
        push_campaign(tenant_id, name, create_if_missing=True, dry_run=dry_run)


MAX_VALIDATE_PER_CYCLE = 20


def _scrape_niche(tenant_id: str, niche: dict, campaign_id: str, dry_run: bool = False):
    """Scrape → filtre → sauvegarde en cold_leads → valide batch → clean_leads."""
    from outreach_engine.scrape.outscraper_scraper import search_maps
    from outreach_engine.scrape.lead_filter import filter_leads

    name = niche.get("name", "")
    keywords = niche.get("keywords", [name])
    target = niche.get("target", 1000)

    log.info("  [scrape] Niche=%s keywords=%s target=%d", name, keywords, target)

    if dry_run:
        log.info("  [scrape] [DRY-RUN] Would scrape %s", name)
        return

    results = search_maps(keywords, limit=20, language="fr",
                          enrichment=os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(","),
                          api_key=os.getenv("OUTSCRAPER_API_KEY", ""))
    log.info("  [scrape] %d résultats bruts", len(results))

    valid = filter_leads(results)
    log.info("  [scrape] %d leads valides (email ou téléphone)", len(valid))

    emails = [l.get("email", "") for l in valid if l.get("email")]
    log.info("  [scrape] %d leads avec email", len(emails))

    _save_cold_leads(tenant_id, valid, campaign_id)

    if not emails:
        log.info("  [scrape] Aucun email à valider")
        _notify_scrape(tenant_id, name, len(results), len(valid), 0)
        return

    batch = emails[:MAX_VALIDATE_PER_CYCLE]
    log.info("  [scrape] Validation de %d/%d emails", len(batch), len(emails))

    from outreach_engine.email_validator.cleaner import clean_emails
    clean = asyncio.run(clean_emails(batch, use_api=bool(os.getenv("MYEMAILVERIFIER_API_KEY")),
                                     api_key=os.getenv("MYEMAILVERIFIER_API_KEY", ""),
                                     demo=False))
    valid_emails = {r.email for r in clean if r.is_valid}
    log.info("  [scrape] %d/%d emails valides", len(valid_emails), len(batch))

    _save_to_clean_leads(tenant_id, valid, clean, campaign_id, name)
    _notify_scrape(tenant_id, name, len(results), len(valid), len(valid_emails))


def _save_cold_leads(tenant_id: str, leads: list[dict], campaign_id: str):
    from cli.db import get_supabase
    from outreach_engine.scrape.outscraper_scraper import normalize_phone

    sb = get_supabase()
    if not sb:
        return
    count = 0
    for entry in leads:
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
                row_id = data[0]["id"]
                sb.table("cold_leads").update(record).eq("id", row_id).execute()
            else:
                sb.table("cold_leads").insert(record).execute()
            count += 1
        except Exception:
            pass
    log.info("  [save] %d leads → cold_leads", count)


def _save_to_clean_leads(tenant_id: str, raw_leads: list[dict],
                          clean_results: list, campaign_id: str, niche_name: str):
    from cli.db import get_supabase
    from outreach_engine.scrape.outscraper_scraper import normalize_phone

    sb = get_supabase()
    if not sb:
        return

    valid_emails_map = {}
    for r in clean_results:
        if r.is_valid:
            valid_emails_map[r.email] = r

    count = 0
    for entry in raw_leads:
        email = entry.get("email", "")
        if not email or email not in valid_emails_map:
            continue
        cr = valid_emails_map[email]

        raw_phone = entry.get("phone", "")
        address = entry.get("full_address", "") or ""
        if not address:
            parts = [entry.get("city", ""), entry.get("postal_code", ""), entry.get("country_code", "")]
            address = ", ".join(p for p in parts if p)

        record = {
            "tenant_id": tenant_id,
            "campaign_id": campaign_id,
            "email": cr.email,
            "first_name": "",
            "last_name": "",
            "company_name": entry.get("name", "") or "",
            "domain": cr.email.split("@")[-1] if "@" in cr.email else "",
            "phone": normalize_phone(raw_phone),
            "location": address,
            "country_code": entry.get("country_code", ""),
            "is_role_based": cr.is_role_based,
            "risk_score": cr.risk_score,
            "status": "fresh",
            "niche": niche_name,
        }
        try:
            existing = sb.table("clean_leads").select("id").eq("tenant_id", tenant_id).eq("campaign_id", campaign_id).eq("email", cr.email).execute()
            if existing.data:
                sb.table("clean_leads").update(record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("clean_leads").insert(record).execute()
            count += 1
        except Exception as e:
            log.warning("  [save] Erreur upsert %s: %s", cr.email, e)
    log.info("  [save] %d leads → clean_leads (campaign=%s)", count, campaign_id)


def _notify_scrape(tenant_id: str, niche: str, total: int, valid: int, valid_emails: int):
    try:
        from slack_notifier.data.notifier import announce_scrape_complete
        announce_scrape_complete(tenant_id, niche, total, valid, valid_emails)
    except Exception:
        pass


def _notify_worker_start(tenant_id: str):
    try:
        from slack_notifier.transport.client import send_message
        send_message(f"⏰ *Worker* — Démarrage pour `{tenant_id}`")
    except Exception:
        pass


def _notify_worker_done(tenant_id: str, decisions: list[dict], pushed: int):
    try:
        from slack_notifier.transport.client import send_message
        actions = ", ".join(f"{d.get('action')}({d.get('niche','?')})" for d in decisions)
        extra = f" + {pushed} leads poussés" if pushed else ""
        send_message(f"✅ *Worker* — `{tenant_id}` terminé : {actions}{extra}")
    except Exception:
        pass


def run_for_tenant(tenant_id: str, dry_run: bool = False):
    from cli.scraping.tenant import get_tenant
    from rotation_engine.rotation_engine import decide

    config = get_tenant(tenant_id)
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return

    log.info("═ %s ═", tenant_id)
    _notify_worker_start(tenant_id)

    total_pushed = 0

    if not dry_run:
        _push_pending_leads(tenant_id, dry_run=dry_run)

    decisions = decide(config, demo=False)
    log.info("  Décisions: %s", json.dumps(decisions, indent=2))

    for d in decisions:
        action = d.get("action")
        niche_name = d.get("niche", "")
        if not niche_name:
            log.info("  Décision: %s (pas de niche)", d.get("reason", ""))
            continue

        niche_cfg = next((n for n in config.get("niches", []) if n.get("name") == niche_name), None)
        if not niche_cfg:
            log.warning("  Niche %s introuvable dans la config", niche_name)
            continue

        if action == "scrape":
            campaign_id = niche_cfg.get("instantly_campaign_id") or f"{niche_name}-{tenant_id}"
            _scrape_niche(tenant_id, niche_cfg, campaign_id, dry_run=dry_run)
        elif action == "close":
            log.info("  Fermeture niche: %s — %s", niche_name, d.get("reason", ""))

    _notify_worker_done(tenant_id, decisions, total_pushed)


def run_all(dry_run: bool = False, tenant_filter: str | None = None):
    from cli.scraping.tenant import list_tenants

    log.info("=" * 50)
    log.info("  WORKER — %s", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("=" * 50)

    tenants = list_tenants()
    if not tenants:
        log.warning("Aucun tenant trouvé")
        return

    for cfg in tenants:
        tid = cfg.get("tenant_id", "")
        if not tid:
            continue
        if tenant_filter and tid != tenant_filter:
            continue
        t0 = time.time()
        run_for_tenant(tid, dry_run=dry_run)
        elapsed = time.time() - t0
        log.info("  ⏱  %s en %.1fs", tid, elapsed)

    log.info("=" * 50)
    log.info("  WORKER TERMINÉ")
    log.info("=" * 50)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Worker — Pipeline autonome")
    parser.add_argument("--tenant", help="Tenant ID (default: tous)")
    parser.add_argument("--dry-run", action="store_true", help="Simule sans appels externes")
    args = parser.parse_args()

    run_all(dry_run=args.dry_run, tenant_filter=args.tenant)


if __name__ == "__main__":
    main()
