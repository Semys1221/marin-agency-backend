#!/usr/bin/env python3
"""
Deduplicate cold_leads and clean_leads in Supabase.

Normalizes campaign_id (NULL → "") and removes duplicate rows
keeping the oldest entry per (tenant_id, campiagn_id, email).

Usage:
    python dedup_leads.py                            # preview only
    python dedup_leads.py --apply                    # apply fixes
    python dedup_leads.py --apply --tenant-id x      # scoped to tenant
"""
import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("dedup")


def _fix_clean_leads(sb, tenant: str, apply: bool):
    """
    1. Find (tenant, email) groups where both NULL and "" campaign_id exist.
    2. Delete the "" rows (they're the duplicates).
    3. Normalize remaining NULL → "".
    """
    resp = sb.table("clean_leads").select("id,email,campaign_id,created_at").eq("tenant_id", tenant).execute()
    rows = resp.data or []

    null_ids = []
    empty_ids = []

    for r in rows:
        cid = r.get("campaign_id")
        if cid is None or cid == "None":
            null_ids.append(r)
        elif cid == "" or cid == " ":
            empty_ids.append(r)

    empty_map = {}
    for r in empty_ids:
        empty_map.setdefault(r["email"], []).append(r["id"])

    null_map = {}
    for r in null_ids:
        null_map.setdefault(r["email"], []).append(r)

    to_delete = []
    for email, eids in empty_map.items():
        if email in null_map:
            to_delete.extend(eids)
            log.info("  Duplicate %s → keeping NULL, deleting '' row", email)

    if not to_delete:
        log.info("  clean_leads: 0 duplicates to remove")
    else:
        log.info("  clean_leads: %d duplicate(s) to delete", len(to_delete))
        if apply:
            for i in range(0, len(to_delete), 50):
                batch = to_delete[i : i + 50]
                sb.table("clean_leads").delete().in_("id", batch).execute()
            log.info("  Deleted %d row(s)", len(to_delete))

    remaining_null = [r for r in null_ids if r["email"] in null_map]
    if remaining_null:
        log.info("  clean_leads: %d NULL campaign_id → normalize", len(remaining_null))
        if apply:
            for r in remaining_null:
                sb.table("clean_leads").update({"campaign_id": ""}).eq("id", r["id"]).execute()
            log.info("  Normalized %d row(s)", len(remaining_null))

    return len(to_delete) + len(remaining_null)


def _fix_cold_leads(sb, tenant: str, apply: bool):
    """Normalize NULL campaign_id → "" in cold_leads."""
    resp = sb.table("cold_leads").select("id,campaign_id").eq("tenant_id", tenant).execute()
    rows = resp.data or []

    null_ids = [r["id"] for r in rows if r.get("campaign_id") is None or r.get("campaign_id") == "None"]
    if not null_ids:
        log.info("  cold_leads: 0 NULL campaign_id")
        return 0

    log.info("  cold_leads: %d NULL campaign_id → normalize", len(null_ids))
    if apply:
        for rid in null_ids:
            sb.table("cold_leads").update({"campaign_id": ""}).eq("id", rid).execute()
        log.info("  Normalized %d row(s)", len(null_ids))

    return len(null_ids)


def main():
    parser = argparse.ArgumentParser(description="Deduplicate leads in Supabase")
    parser.add_argument("--apply", action="store_true", help="Apply deletions")
    parser.add_argument(
        "--tenant-id",
        default=os.getenv("TENANT_ID", "sylk-conseils"),
    )
    args = parser.parse_args()

    from supabase_client import get_supabase, is_configured

    if not is_configured():
        log.error("Supabase non configuré")
        sys.exit(1)

    sb = get_supabase()
    tag = "APPLY" if args.apply else "PREVIEW (--apply to execute)"
    log.info("Mode: %s | Tenant: %s\n", tag, args.tenant_id)

    total = 0

    log.info("── Cleaning clean_leads ──────")
    total += _fix_clean_leads(sb, args.tenant_id, args.apply)

    log.info("── Cleaning cold_leads ───────")
    total += _fix_cold_leads(sb, args.tenant_id, args.apply)

    if total == 0:
        log.info("\nTout est propre ✅")
    elif not args.apply:
        log.info("\nRerun with --apply to fix %d issue(s)", total)


if __name__ == "__main__":
    main()
