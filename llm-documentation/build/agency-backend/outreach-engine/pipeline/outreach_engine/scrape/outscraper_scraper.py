#!/usr/bin/env python3
import argparse
import csv
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outscraper import OutscraperClient

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("outscraper_scraper")

API_KEY = os.getenv("OUTSCRAPER_API_KEY", "")

FIELDS = [
    "name", "site", "phone", "email", "email_1", "email_2", "email_3",
    "full_address", "city", "postal_code", "country_code",
    "place_id", "google_id", "latitude", "longitude",
    "category", "type", "rating", "reviews", "reviews_per_score",
    "working_hours", "business_status", "about", "range",
    "photo", "time_zone", "verified",
]


def search_maps(query: str | list[str], limit: int = 100, language: str = "fr",
                enrichment: list[str] | None = None, api_key: str = "") -> list[dict]:
    key = api_key or API_KEY
    if not key:
        log.error("OUTSCRAPER_API_KEY not set")
        return []

    client = OutscraperClient(api_key=key)
    results = client.google_maps_search(
        query if isinstance(query, list) else [query],
        limit=limit,
        language=language,
        enrichment=enrichment or [],
    )
    items = []
    for page in results:
        if isinstance(page, list):
            items.extend(page)
    return items


def extract_email(entry: dict) -> str:
    for k in ("email", "email_1", "email_2", "email_3"):
        v = entry.get(k, "")
        if v:
            return v.strip().lower()
    return ""


def to_flat(entry: dict) -> dict:
    return {k: entry.get(k, "") for k in FIELDS}


def _domain(site: str) -> str:
    if not site:
        return ""
    site = site.strip().lower()
    for p in ("https://", "http://", "www."):
        site = site.replace(p, "")
    return site.split("/")[0]


def upsert_cold_leads(items: list[dict], tenant: str, campaign_id: str = ""):
    from .lead_filter import is_valid_lead
    from cli.db import get_supabase

    sb = get_supabase()
    count = 0
    for entry in items:
        if not is_valid_lead(entry):
            continue
        email = extract_email(entry)
        if not email:
            continue
        record = {
            "tenant_id": tenant,
            "email": email,
            "company_name": entry.get("name", "") or "",
            "domain": _domain(entry.get("site", "")),
            "phone": entry.get("phone", ""),
            "location": entry.get("full_address", "") or "",
            "source": "outscraper",
            "campaign_id": campaign_id,
            "metadata": entry,
        }
        try:
            existing = sb.table("cold_leads").select("id").eq("tenant_id", tenant).eq("email", email).execute()
            if existing.data:
                sb.table("cold_leads").update(record).eq("id", existing.data[0]["id"]).execute()
            else:
                sb.table("cold_leads").insert(record).execute()
            count += 1
        except Exception as e:
            log.warning("Upsert error %s: %s", email, e)
    log.info("Inserted %d/%d leads into cold_leads", count, len(items))

    if count > 0:
        try:
            total = sb.table("cold_leads").select("id", count="exact").eq("tenant_id", tenant).execute()
            total_count = total.count if hasattr(total, 'count') else count
            for milestone in [100, 500, 1000, 2000, 5000]:
                if total_count >= milestone and total_count - count < milestone * 0.5:
                    from slack_notifier.data.notifier import announce_scrape_milestone
                    announce_scrape_milestone(tenant, campaign_id or "scrape", total_count)
                    break
        except Exception:
            pass


def to_csv(items: list[dict], path: str):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(to_flat(e) for e in items)
    log.info("CSV saved: %s (%d rows)", path, len(items))


def to_json(items: list[dict], path: str):
    with open(path, "w") as f:
        json.dump(items, f, indent=2, default=str)
    log.info("JSON saved: %s (%d rows)", path, len(items))


def main():
    parser = argparse.ArgumentParser(description="Outscraper Google Maps scraper")
    parser.add_argument("query", nargs="+", help="Search query (e.g. 'plombier Paris')")
    parser.add_argument("--limit", type=int, default=100, help="Results per query")
    parser.add_argument("--lang", default="fr", help="Language (default: fr)")
    parser.add_argument("--enrichment", nargs="*", default=["contacts_n_leads"],
                        help="Enrichments (e.g. contacts_n_leads emails_validator_service)")
    parser.add_argument("--output", "-o", help="Output file (CSV or JSON)")
    parser.add_argument("--api-key", help="Override OUTSCRAPER_API_KEY")
    parser.add_argument("--db", action="store_true", help="Upsert leads into cold_leads table")
    parser.add_argument("--tenant-id", default=os.getenv("TENANT_ID", "sylk-conseils"),
                        help="Tenant ID for multi-tenant isolation")
    parser.add_argument("--campaign-id", default="", help="Campaign ID to associate leads with")
    args = parser.parse_args()

    key = args.api_key or API_KEY
    if not key:
        log.error("Set OUTSCRAPER_API_KEY or pass --api-key")
        sys.exit(1)

    query = " ".join(args.query)
    log.info("Searching: %s (limit=%d)", query, args.limit)

    items = search_maps(query, limit=args.limit, language=args.lang,
                        enrichment=args.enrichment, api_key=key)

    emails = [(extract_email(e), e.get("name", ""), e.get("site", "")) for e in items if extract_email(e)]
    total_w_email = len(emails)
    log.info("Results: %d total, %d with email", len(items), total_w_email)

    print(json.dumps(items, indent=2, default=str))

    if args.output:
        if args.output.endswith(".csv"):
            to_csv(items, args.output)
        else:
            to_json(items, args.output)

    if args.db:
        upsert_cold_leads(items, args.tenant_id, args.campaign_id)


if __name__ == "__main__":
    main()
