#!/usr/bin/env python3
"""
Push Instantly — CLI entry point.

Usage:
  python push.py --campaign-name "kiné-bordeaux-20260701" --tenant-id "sylk-conseils"
  python push.py --all-campaigns --tenant-id "sylk-conseils" --create-if-missing
  python push.py --campaign-name "..." --tenant-id "..." --dry-run
"""

import argparse
import sys
import time
from datetime import datetime, timezone

from lib import config
from lib.http import log
from lib.accounts import list_active
from lib.campaign import find_by_name, create_with_subsequence
from lib.leads import push as push_leads
from lib.db import fetch_clean_leads, get_distinct_campaigns, mark_leads_contacted, save_instantly_campaign_id


def push_campaign(tenant_id: str, campaign_name: str, create_if_missing: bool = False, dry_run: bool = False):
    log(f"Processing campaign: {campaign_name} (tenant={tenant_id})")

    rows = fetch_clean_leads(tenant_id, campaign_name=campaign_name)
    if not rows:
        log(f"No clean_leads found for campaign_id '{campaign_name}'", "WARN")
        return

    log(f"Found {len(rows)} clean leads for campaign '{campaign_name}'")

    campaign = find_by_name(campaign_name)
    if campaign:
        instantly_id = campaign["id"]
        log(f"Campaign '{campaign_name}' exists → id={instantly_id}")
    elif create_if_missing:
        if dry_run:
            log(f"[DRY-RUN] Would create campaign '{campaign_name}' with settings + subsequence")
            return
        accounts = list_active()
        if not accounts:
            log("No active accounts available — cannot create campaign", "ERROR")
            return
        campaign = create_with_subsequence(campaign_name, accounts)
        if not campaign:
            log(f"Aborting: could not create campaign '{campaign_name}'", "ERROR")
            return
        instantly_id = campaign["id"]
    else:
        log(f"Campaign '{campaign_name}' not found and --create-if-missing not set", "ERROR")
        return

    if dry_run:
        log(f"[DRY-RUN] Would push {len(rows)} leads to campaign {instantly_id}")
        return

    total = push_leads(instantly_id, rows)

    if total > 0:
        mark_leads_contacted(tenant_id, campaign_name)

    save_instantly_campaign_id(tenant_id, campaign_name, instantly_id)
    log(f"Done: {total} leads pushed to campaign '{campaign_name}'")


def push_all(tenant_id: str, create_if_missing: bool = False, dry_run: bool = False):
    campaigns = get_distinct_campaigns(tenant_id)
    if not campaigns:
        log(f"No campaign_ids found in clean_leads for tenant '{tenant_id}'", "WARN")
        return
    log(f"Found {len(campaigns)} campaigns: {campaigns}")
    for name in campaigns:
        push_campaign(tenant_id, name, create_if_missing=create_if_missing, dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(description="Push leads to Instantly with campaign name matching")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--campaign-name", help="Campaign name to match/push to")
    group.add_argument("--all-campaigns", action="store_true", help="Push all niches as individual campaigns")

    parser.add_argument("--tenant-id", default=config.TENANT_ID)
    parser.add_argument("--create-if-missing", action="store_true", help="Create campaign in Instantly if not found")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without API calls")
    parser.add_argument("--limit", type=int, help="Max leads to fetch per campaign")

    args = parser.parse_args()

    if not config.INSTANTLY_API_KEY:
        log("INSTANTLY_API_KEY is not set", "ERROR")
        sys.exit(1)

    if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_ROLE_KEY:
        log("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set", "ERROR")
        sys.exit(1)

    if args.all_campaigns:
        push_all(args.tenant_id, create_if_missing=args.create_if_missing, dry_run=args.dry_run)
    else:
        push_campaign(args.tenant_id, args.campaign_name, create_if_missing=args.create_if_missing, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
