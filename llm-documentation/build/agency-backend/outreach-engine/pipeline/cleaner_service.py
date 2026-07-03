#!/usr/bin/env python3
"""
Cleaner Service — valide les emails de cold_leads vers clean_leads.

Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   MYEMAILVERIFIER_API_KEY (optionnel),
                   TENANT_ID (optionnel, filtre)
"""

import asyncio
import os
import sys
import time
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("cleaner_service")


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
        return [{"tenant_id": r.get("slug", "")} for r in (result.data or [])]
    except Exception:
        return []


# ── Email validation (simplified, inline from email_validator) ─


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
ROLE_BASED = {"info", "contact", "support", "sales", "admin", "hello", "help",
              "marketing", "billing", "team", "noreply", "no-reply", "dev",
              "webmaster", "postmaster", "abuse", "careers", "jobs"}
DISPOSABLE = {"mailinator.com", "guerrillamail.com", "10minutemail.com",
              "tempmail.com", "throwaway.email", "yopmail.com", "sharklasers.com",
              "maildrop.cc", "inboxbear.com", "temp-mail.org", "trashmail.com"}


class ValidationResult:
    def __init__(self, email: str):
        self.email = email
        self.valid_format = False
        self.has_mx = False
        self.is_disposable = False
        self.is_role_based = False
        self.is_catch_all = False
        self.error = None

    @property
    def is_valid(self) -> bool:
        return self.valid_format and not self.is_disposable and self.has_mx is not False

    @property
    def risk_score(self) -> str:
        if not self.is_valid:
            return "high"
        if self.is_role_based or self.is_catch_all:
            return "medium"
        return "low"


def _check_mx(domain: str) -> bool:
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX", lifetime=5)
        return len(answers) > 0
    except Exception:
        return False


async def _validate_email(email: str) -> ValidationResult:
    r = ValidationResult(email)
    if not EMAIL_REGEX.match(email):
        r.error = "invalid_format"
        return r
    r.valid_format = True
    _, domain = email.split("@")
    domain = domain.lower()
    local_part = email.split("@")[0]
    r.is_role_based = local_part.lower() in ROLE_BASED
    r.is_disposable = domain in DISPOSABLE
    if not _check_mx(domain):
        r.error = "no_mx"
        return r
    r.has_mx = True
    return r


async def _clean_emails(emails: list[str]) -> list[ValidationResult]:
    tasks = [_validate_email(e) for e in emails]
    return await asyncio.gather(*tasks)


# ── Main logic ──────────────────────────────────────────────


def _push_pending(tenant_id: str):
    if not _is_configured():
        log.error("Supabase non configuré")
        return
    sb = _get_supabase()
    data = sb.table("cold_leads").select("*").eq("tenant_id", tenant_id).execute()
    rows = data.data or []
    if not rows:
        log.info("  Aucun lead à cleaner")
        return

    emails = [r["email"] for r in rows]
    log.info("  %d leads à valider", len(emails))
    results = asyncio.run(_clean_emails(emails))
    inserted = 0
    for row, r in zip(rows, results):
        record = {
            "tenant_id": tenant_id, "campaign_id": row.get("campaign_id", ""),
            "email": r.email, "first_name": "", "last_name": "",
            "company_name": row.get("company_name", "") or "",
            "domain": row.get("domain", ""), "phone": row.get("phone", "") or "",
            "location": row.get("location", "") or "",
            "is_role_based": r.is_role_based, "risk_score": r.risk_score,
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
    log.info("  %d/%d écrits dans clean_leads (valid=%d, invalid=%d)", inserted, len(results), valid, invalid)


def run_for_tenant(tenant_id: str):
    log.info("═ %s ═", tenant_id)
    _push_pending(tenant_id)


def run_all():
    log.info("═" * 50)
    log.info("  CLEANER SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
    log.info("═" * 50)
    tenant_filter = os.getenv("TENANT_ID", "")
    for config in _list_tenants():
        tid = config.get("tenant_id", "")
        if tid and (not tenant_filter or tid == tenant_filter):
            run_for_tenant(tid)


def run_survivor():
    try:
        from health import start as start_health
        start_health()
    except Exception:
        pass
    interval = int(os.getenv("CLEANER_INTERVAL_MINUTES", "5"))
    log.info("  Mode survivor (toutes les %d min)", interval)
    while True:
        run_all()
        for _ in range(interval * 60):
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
        run_all()
