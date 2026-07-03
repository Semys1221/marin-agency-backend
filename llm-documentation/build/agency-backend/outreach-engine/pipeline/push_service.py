#!/usr/bin/env python3
"""
Push Service — pousse les leads clean vers Instantly.

Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   INSTANTLY_API_KEY,
                   TENANT_ID (optionnel, filtre)
"""

import os
import sys
import time
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("push_service")

INSTANTLY_BASE = "https://api.instantly.ai/api/v2"
LEAD_BATCH_SIZE = 1000

# ── Shared helpers ──────────────────────────────────────────


def _get_supabase():
    from supabase import create_client
    return create_client(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""))


def _is_configured():
    u = os.getenv("SUPABASE_URL", "")
    k = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    return bool(u and k and u != "..." and k != "...")


def _list_tenants() -> list[dict]:
    if not _is_configured():
        return []
    try:
        result = _get_supabase().table("tenants").select("*").execute()
        configs = []
        for row in result.data or []:
            cfg = row.get("config")
            if isinstance(cfg, dict):
                cfg["tenant_id"] = cfg.get("tenant_id", row.get("slug", ""))
                configs.append(cfg)
            else:
                configs.append({"tenant_id": row.get("slug", ""), "niches": []})
        return configs
    except Exception:
        return []


def _instantly_headers() -> dict:
    return {"Authorization": f"Bearer {os.getenv('INSTANTLY_API_KEY', '')}", "Content-Type": "application/json"}


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ── Instantly Campaign API ──────────────────────────────────


def _find_campaign(name: str) -> dict | None:
    resp = requests.get(f"{INSTANTLY_BASE}/campaigns", headers=_instantly_headers(), params={"search": name, "limit": 20})
    if resp.status_code != 200:
        return None
    for c in resp.json().get("items", []):
        if c.get("name", "").strip().lower() == name.strip().lower():
            return c
    return None


def _list_active_accounts() -> list[str]:
    resp = requests.get(f"{INSTANTLY_BASE}/accounts", headers=_instantly_headers(), params={"limit": 100, "status": 1})
    if resp.status_code != 200:
        log.error("Failed to list accounts: %s", resp.text)
        return []
    return [item["email"] for item in resp.json().get("items", []) if item.get("email")]


def _build_campaign_payload(name: str, emails: list[str]) -> dict:
    schedule = {"schedules": [{"name": "Semaine", "timing": {"from": "09:00", "to": "17:00"},
                               "days": {"0": False, "1": True, "2": True, "3": True, "4": True, "5": True, "6": True},
                               "timezone": "Europe/Belgrade"}]}
    sequences = [{"steps": [{"type": "email", "delay": 0, "variants": [
        {"subject": "Question {niche_keyword_1}", "body": "Bonjour,\n\nNous aidons les {niche} à {objectif} sans {pain_point}.\n\nPuis-je vous envoyer plus d'informations ?\n\n{{gmail_signature}}"},
        {"subject": "Question {niche_keyword_2}", "body": "Bonjour,\n\nJ'allais vous joindre au {{phone_number}}, mais un email me permettait d'être plus clair.\n\nNous aidons les {niche} à {objectif} sans {pain_point} en {timeline}.\n\nSouhaitez-vous en savoir plus ?\n\n{{gmail_signature}}"},
        {"subject": "Question {niche_keyword_3}", "body": "Bonjour à vous,\n\nNous aidons les {niche} à {objectif} sans {pain_point} grâce à {methode}.\n\nSeriez-vous intéressé pour en savoir plus ?\n\n{{gmail_signature}}"},
    ]}, {"type": "email", "delay": 3, "variants": [
        {"subject": "RE: {niche_keyword_1}", "body": "Si nous pouvions vous montrer comment {objectif}, cela vous intéresserait-il ?\n\n{{gmail_signature}}"},
        {"subject": "RE: {niche_keyword_2}", "body": "Vous {pain_point}. Nous pouvons inverser cette tendance en {timeline}. Souhaitez-vous en savoir plus ?\n\n{{gmail_signature}}"},
        {"subject": "RE: {niche_keyword_3}", "body": "Si nous pouvions vous montrer comment {objectif} sans {pain_point}, cela vous intéresserait-il ?\n\n{{gmail_signature}}"},
    ]}]}]
    return {
        "name": name, "campaign_schedule": schedule, "sequences": sequences,
        "email_list": emails, "email_gap": 20, "random_wait_max": 5,
        "daily_limit": 50, "text_only": True, "first_email_text_only": True,
        "stop_on_reply": True, "open_tracking": True, "link_tracking": True,
        "insert_unsubscribe_header": True,
    }


def _create_campaign(name: str, emails: list[str]) -> dict | None:
    payload = _build_campaign_payload(name, emails)
    resp = requests.post(f"{INSTANTLY_BASE}/campaigns", json=payload, headers=_instantly_headers())
    if resp.status_code not in (200, 201):
        log.error("Failed to create campaign: %s %s", resp.status_code, resp.text)
        return None
    campaign = resp.json()
    log.info("Created campaign '%s' → id=%s (%d accounts)", name, campaign.get("id"), len(emails))
    return campaign


def _activate_campaign(campaign_id: str) -> bool:
    resp = requests.post(f"{INSTANTLY_BASE}/campaigns/{campaign_id}/activate", headers=_instantly_headers())
    if resp.status_code != 200:
        log.error("Failed to activate campaign %s: %s", campaign_id, resp.status_code)
        return False
    log.info("Activated campaign %s", campaign_id)
    return True


def _create_subsequence(campaign_id: str):
    payload = {
        "parent_campaign": campaign_id, "name": "Interested Follow-up",
        "conditions": {"lead_activity": [4]},
        "subsequence_schedule": {"schedules": [{"name": "Semaine", "timing": {"from": "09:00", "to": "17:00"},
                                                 "days": {"0": False, "1": True, "2": True, "3": True, "4": True, "5": True, "6": True},
                                                 "timezone": "Europe/Belgrade"}]},
        "sequences": [{"steps": [
            {"type": "email", "delay": 1, "variants": [{"subject": "RE: {sujet_step_1}",
                "body": "Bonjour {{first_name}},\n\nMerci pour votre retour. Le plus simple pour vous présenter la solution est de réserver 15 min.\n\nQuand seriez-vous disponible ?\n\n{{gmail_signature}}"}]},
            {"type": "email", "delay": 3, "variants": [{"subject": "Suite de notre échange",
                "body": "Bonjour {{first_name}},\n\nUn {niche_member} comme vous a atteint {objectif} en {timeline} grâce à notre accompagnement.\n\nJe reste à votre disposition.\n\n{{gmail_signature}}"}]},
            {"type": "email", "delay": 3, "variants": [{"subject": "Pour donner suite",
                "body": "Bonjour {{first_name}},\n\nN'ayant pas eu de suite, je passe la main à notre équipe qui pourra échanger avec vous par téléphone.\n\nBonne journée,\n\n{{gmail_signature}}"}]},
        ]}], "daily_limit_mode": "inherit",
    }
    resp = requests.post(f"{INSTANTLY_BASE}/subsequences", json=payload, headers=_instantly_headers())
    if resp.status_code not in (200, 201):
        log.error("Failed to create subsequence: %s %s", resp.status_code, resp.text)
    else:
        log.info("Created subsequence → id=%s", resp.json().get("id"))


def _create_campaign_full(name: str, emails: list[str]) -> dict | None:
    campaign = _create_campaign(name, emails)
    if not campaign:
        return None
    cid = campaign["id"]
    time.sleep(1)
    _activate_campaign(cid)
    time.sleep(1)
    _create_subsequence(cid)
    return campaign


def _fetch_clean_leads(tenant_id: str, campaign_name: str | None = None) -> list[dict]:
    q = _get_supabase().table("clean_leads").select("*").eq("tenant_id", tenant_id)
    if campaign_name:
        q = q.eq("campaign_id", campaign_name)
    return q.execute().data


def _push_leads(campaign_id: str, rows: list[dict]) -> int:
    total = 0
    import math
    for i in range(0, len(rows), LEAD_BATCH_SIZE):
        batch = rows[i:i + LEAD_BATCH_SIZE]
        leads = []
        for row in batch:
            lead = {"email": row.get("email", "")}
            for k in ("first_name", "last_name", "company_name", "phone"):
                if row.get(k):
                    lead[k] = row[k]
            leads.append(lead)
        payload = {"campaign_id": campaign_id, "leads": leads, "skip_if_in_workspace": True, "verify_leads_on_import": False}
        resp = requests.post(f"{INSTANTLY_BASE}/leads/add", json=payload, headers=_instantly_headers())
        if resp.status_code not in (200, 201):
            log.error("Failed to push leads: %s %s", resp.status_code, resp.text)
            continue
        result = resp.json()
        uploaded = result.get("leads_uploaded", 0)
        total += uploaded
        log.info("  Pushed %d/%d (dups=%d)", uploaded, len(batch), result.get("duplicated_leads", 0))
    return total


# ── Main logic ──────────────────────────────────────────────


def push_campaign(tenant_id: str, campaign_name: str, create_if_missing: bool = True):
    log.info("  Processing campaign: %s (tenant=%s)", campaign_name, tenant_id)
    rows = _fetch_clean_leads(tenant_id, campaign_name)
    if not rows:
        log.info("  No clean_leads for '%s'", campaign_name)
        return

    campaign = _find_campaign(campaign_name)
    if campaign:
        instantly_id = campaign["id"]
        log.info("  Campaign '%s' exists → id=%s", campaign_name, instantly_id)
    elif create_if_missing:
        accounts = _list_active_accounts()
        if not accounts:
            log.error("  No active accounts")
            return
        campaign = _create_campaign_full(campaign_name, accounts)
        if not campaign:
            log.error("  Aborting: could not create campaign")
            return
        instantly_id = campaign["id"]
    else:
        log.error("  Campaign '%s' not found and create_if_missing=False", campaign_name)
        return

    total = _push_leads(instantly_id, rows)
    if total > 0:
        _get_supabase().table("clean_leads").update({"status": "contacted"}).eq("tenant_id", tenant_id).eq("campaign_id", campaign_name).execute()
        _get_supabase().table("campaign_settings").upsert({
            "tenant_id": tenant_id, "campaign_id": campaign_name,
            "instantly_campaign_id": instantly_id, "niche": "", "status": "running",
        }, on_conflict="tenant_id,campaign_id").execute()
    log.info("  Done: %d leads pushed", total)


def push_for_tenant(tenant_id: str):
    config = None
    for t in _list_tenants():
        if t.get("tenant_id") == tenant_id:
            config = t
            break
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return

    for niche in config.get("niches", []):
        campaign_name = niche.get("instantly_campaign_id") or f"{niche['name']}-{tenant_id}"
        push_campaign(tenant_id, campaign_name)


def run_all():
    log.info("═" * 50)
    log.info("  PUSH SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("═" * 50)
    if not os.getenv("INSTANTLY_API_KEY"):
        log.error("INSTANTLY_API_KEY non définie")
        return
    tenant_filter = os.getenv("TENANT_ID", "")
    for config in _list_tenants():
        tid = config.get("tenant_id", "")
        if tid and (not tenant_filter or tid == tenant_filter):
            push_for_tenant(tid)


def run_survivor():
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass
    interval = int(os.getenv("PUSH_INTERVAL_MINUTES", "30"))
    log.info("  Mode survivor (toutes les %d min)", interval)
    while True:
        run_all()
        for _ in range(interval * 60):
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
        run_all()
