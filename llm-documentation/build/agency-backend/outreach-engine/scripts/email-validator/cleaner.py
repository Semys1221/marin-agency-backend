#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_validator import validate_email, ValidationResult
from myemailverifier_client import verify_email as api_verify, check_credits

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("cleaner")


def _merge_api_result(local: ValidationResult, api_data: dict) -> ValidationResult:
    status = api_data.get("Status", "Unknown")

    if api_data.get("catch_all") == "true":
        local.is_catch_all = True
    if api_data.get("Disposable_Domain") == "true":
        local.is_disposable = True
    if api_data.get("Role_Based") == "true":
        local.is_role_based = True

    if status == "Invalid":
        local.valid_format = False
        local.error = "api_invalid"
    elif status == "Catch-all":
        local.is_catch_all = True

    if "error" in api_data:
        local.error = api_data["error"]

    return local


def _demo_result(email: str) -> ValidationResult:
    r = ValidationResult(email)
    r.valid_format = True
    r.has_mx = True
    r.is_role_based = random.random() < 0.05
    r.is_disposable = random.random() < 0.02
    r.is_catch_all = random.random() < 0.1
    return r


async def clean_emails(emails: list[str], use_api: bool = True, api_key: str = "", demo: bool = False) -> list[ValidationResult]:
    local_tasks = [validate_email(e) for e in emails]
    local_results = await asyncio.gather(*local_tasks)

    if demo:
        return [_demo_result(e) for e in emails]

    final = []
    for email, local in zip(emails, local_results):
        if use_api and local.is_valid and api_key:
            api_data = api_verify(email, api_key)
            local = _merge_api_result(local, api_data)
        final.append(local)

    return final


def _clean_db(use_api: bool, api_key: str, tenant: str, campaign_id: str, demo: bool):
    from supabase_client import get_supabase, is_configured

    if not is_configured():
        log.error("Supabase non configuré (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY)")
        sys.exit(1)

    sb = get_supabase()
    q = sb.table("cold_leads").select("*").eq("tenant_id", tenant)
    if campaign_id:
        q = q.eq("campaign_id", campaign_id)
    data = q.execute()
    rows = data.data or []
    if not rows:
        log.info("Aucun lead à cleaner dans cold_leads")
        return

    emails = [r["email"] for r in rows]
    log.info("Lecture de %d leads depuis cold_leads", len(emails))

    results = asyncio.run(clean_emails(emails, use_api=use_api, api_key=api_key, demo=demo))

    inserted = 0
    for row, r in zip(rows, results):
        record = {
            "tenant_id": tenant,
            "campaign_id": campaign_id or row.get("campaign_id", ""),
            "email": r.email,
            "first_name": "",
            "last_name": "",
            "company_name": row.get("company_name", "") or "",
            "domain": row.get("domain", ""),
            "phone": row.get("phone", "") or "",
            "location": row.get("location", "") or "",
            "profession": (row.get("metadata") or {}).get("category") or (row.get("metadata") or {}).get("type") or "",
            "is_role_based": r.is_role_based,
            "risk_score": r.risk_score,
            "status": "fresh" if r.is_valid else "invalid",
            "metadata": row.get("metadata", {}),
        }
        try:
            existing = sb.table("clean_leads").select("id").eq("tenant_id", tenant).eq("campaign_id", record["campaign_id"]).eq("email", r.email).execute()
            if existing.data:
                sb.table("clean_leads").update(record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("clean_leads").insert(record).execute()
            inserted += 1
        except Exception as e:
            log.warning("Upsert error %s: %s", r.email, e)

    log.info("Écriture: %d/%d dans clean_leads", inserted, len(results))


def _insert_to_db(tenant: str, campaign_id: str, results: list[ValidationResult]):
    from supabase_client import get_supabase, is_configured

    if not is_configured():
        log.error("Supabase non configuré (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY)")
        return

    sb = get_supabase()
    cold_ok = clean_ok = 0

    for r in results:
        domain = r.email.split("@")[-1] if "@" in r.email else ""

        cold_record = {
            "tenant_id": tenant,
            "email": r.email,
            "domain": domain,
            "source": "manual",
            "campaign_id": campaign_id,
        }
        try:
            existing = sb.table("cold_leads").select("id").eq("tenant_id", tenant).eq("email", r.email).execute()
            if existing.data:
                sb.table("cold_leads").update(cold_record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("cold_leads").insert(cold_record).execute()
            cold_ok += 1
        except Exception as e:
            log.warning("cold_leads error %s: %s", r.email, e)

        clean_record = {
            "tenant_id": tenant,
            "campaign_id": campaign_id,
            "email": r.email,
            "domain": domain,
            "is_role_based": r.is_role_based,
            "risk_score": r.risk_score,
            "status": "fresh" if r.is_valid else "invalid",
        }
        try:
            existing = sb.table("clean_leads").select("id").eq("tenant_id", tenant).eq("campaign_id", campaign_id).eq("email", r.email).execute()
            if existing.data:
                sb.table("clean_leads").update(clean_record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("clean_leads").insert(clean_record).execute()
            clean_ok += 1
        except Exception as e:
            log.warning("clean_leads error %s: %s", r.email, e)

    log.info("DB: %d/%d cold_leads, %d/%d clean_leads", cold_ok, len(results), clean_ok, len(results))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Email cleaner — 2-stage pipeline")
    parser.add_argument("--local", action="store_true", help="Skip API call")
    parser.add_argument("--demo", action="store_true", help="Random results, no API")
    parser.add_argument("--api-key", help="Override MYEMAILVERIFIER_API_KEY")
    parser.add_argument("--credits", action="store_true", help="Check remaining credits")
    parser.add_argument("--db", action="store_true", help="Read from cold_leads, write to clean_leads")
    parser.add_argument("--to-db", action="store_true", help="Insert stdin-validated results into cold_leads + clean_leads")
    parser.add_argument("--tenant-id", default=os.getenv("TENANT_ID", "sylk-conseils"))
    parser.add_argument("--campaign-id", default="", help="Filter by campaign")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("MYEMAILVERIFIER_API_KEY", "")

    if args.credits:
        credits = check_credits(api_key)
        print(f"Credits restants : {credits}")
        sys.exit(0)

    if args.db:
        _clean_db(use_api=not args.local, api_key=api_key,
                  tenant=args.tenant_id, campaign_id=args.campaign_id, demo=args.demo)
        return

    emails = [e.strip() for e in sys.stdin.read().splitlines() if e.strip()]
    if not emails:
        log.error("Usage: cat emails.txt | python cleaner.py [--local] [--demo] [--api-key KEY] [--credits]")
        log.error("   or: python cleaner.py --db [--campaign-id X]")
        sys.exit(1)

    results = asyncio.run(clean_emails(emails, use_api=not args.local, api_key=api_key, demo=args.demo))

    valid = [r for r in results if r.is_valid]
    invalid = [r for r in results if not r.is_valid]

    log.info(f"\nChecked: {len(results)}, Valid: {len(valid)}, Invalid: {len(invalid)}")
    log.info(f"Risk breakdown: low={sum(1 for r in valid if r.risk_score == 'low')} "
             f"medium={sum(1 for r in valid if r.risk_score == 'medium')} "
             f"high={sum(1 for r in invalid if r.risk_score == 'high')}")

    print(json.dumps({"results": [r.to_dict() for r in results]}, indent=2))

    with open("valid_emails.txt", "w") as f:
        for r in valid:
            f.write(f"{r.email}\n")

    with open("invalid_emails.txt", "w") as f:
        for r in invalid:
            f.write(f"{r.email} | {r.error or r.risk_score}\n")

    if args.to_db:
        _insert_to_db(args.tenant_id, args.campaign_id, results)


if __name__ == "__main__":
    main()
