#!/usr/bin/env python3
"""
Scraper Service — scrape Google Maps via Outscraper pour les niches actives.

Variables d'env : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY,
                   OUTSCRAPER_API_KEY, OUTSCRAPER_ENRICHMENT,
                   TENANT_ID (optionnel, filtre)
"""

import asyncio
import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("scraper_service")

MAX_SCRAPE_PER_CYCLE = 3

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


def _state_list(tenant_id: str) -> list[dict]:
    if not _is_configured():
        return []
    r = _get_supabase().table("rotation_state").select("*").eq("tenant_id", tenant_id).order("created_at").execute()
    return r.data


# ── Phone normalization ─────────────────────────────────────


def _normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    cleaned = phone.strip().replace(" ", "").replace(".", "").replace("-", "")
    if cleaned.startswith("+33"):
        return cleaned
    if cleaned.startswith("0033"):
        return "+33" + cleaned[4:]
    if cleaned.startswith("0") and len(cleaned) >= 10 and cleaned[1:].isdigit():
        return "+33" + cleaned[1:]
    return cleaned


# ── Lead filter ─────────────────────────────────────────────


def _filter_leads(items: list[dict]) -> list[dict]:
    def has_email(e): return any(e.get(f) for f in ("email", "email_1", "email_2", "email_3"))
    def has_phone(e): return bool(e.get("phone"))
    return [e for e in items if has_email(e) or has_phone(e)]


# ── Outscraper scraper ──────────────────────────────────────


def _search_maps(query: str | list[str], limit: int = 100, language: str = "fr",
                 enrichment: list[str] | None = None, api_key: str = "") -> list[dict]:
    from outscraper import OutscraperClient
    key = api_key or os.getenv("OUTSCRAPER_API_KEY", "")
    if not key:
        log.error("OUTSCRAPER_API_KEY not set")
        return []
    client = OutscraperClient(api_key=key)
    kwargs = {"query": query if isinstance(query, list) else [query], "limit": limit, "language": language}
    if enrichment:
        kwargs["enrichment"] = enrichment
    kwargs["country"] = os.getenv("OUTSCRAPER_COUNTRY", "FR")
    results = client.google_maps_search(**kwargs)
    items = []
    for page in results:
        if isinstance(page, list):
            items.extend(page)
    return items


# ── Scrape niche ─────────────────────────────────────────────


def _scrape_niche(tenant_id: str, niche_name: str, keywords: list[str], target: int, campaign_id: str):
    log.info("  [scraper] Niche=%s keywords=%s target=%d", niche_name, keywords, target)
    enrichment = os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(",")
    results = _search_maps(keywords, limit=20, language="fr", enrichment=enrichment,
                           api_key=os.getenv("OUTSCRAPER_API_KEY", ""))
    log.info("  [scraper] %d résultats bruts", len(results))
    valid = _filter_leads(results)
    log.info("  [scraper] %d leads valides", len(valid))

    sb = _get_supabase()
    if not _is_configured() or not sb:
        return
    count = 0
    for entry in valid:
        email = entry.get("email", "")
        raw_phone = entry.get("phone", "")
        address = entry.get("full_address", "") or ""
        if not address:
            parts = [entry.get("city", ""), entry.get("postal_code", ""), entry.get("country_code", "")]
            address = ", ".join(p for p in parts if p)
        record = {
            "tenant_id": tenant_id, "email": email or f"no-email-{raw_phone}",
            "company_name": entry.get("name", "") or "", "phone": _normalize_phone(raw_phone),
            "location": address, "country_code": entry.get("country_code", ""),
            "source": "outscraper", "campaign_id": campaign_id, "metadata": entry,
        }
        try:
            existing = sb.table("cold_leads").select("id").eq("tenant_id", tenant_id).eq("email", email).execute()
            data = getattr(existing, "data", None) or []
            if data:
                sb.table("cold_leads").update(record).eq("id", data[0]["id"]).execute()
            else:
                sb.table("cold_leads").insert(record).execute()
            count += 1
        except Exception:
            pass
    log.info("  [scraper] %d leads → cold_leads", count)


# ── Entry points ─────────────────────────────────────────────


def run_for_tenant(tenant_id: str):
    config = None
    for t in _list_tenants():
        if t.get("tenant_id") == tenant_id:
            config = t
            break
    if not config:
        log.warning("  Tenant %s introuvable", tenant_id)
        return
    states = _state_list(tenant_id)
    state_map = {s["niche_name"]: s for s in states}
    scraped = 0
    for n in config.get("niches", []):
        if scraped >= MAX_SCRAPE_PER_CYCLE:
            break
        name = n.get("name", "")
        s = state_map.get(name, {})
        if s.get("status") not in ("active", "pending"):
            continue
        campaign_id = n.get("instantly_campaign_id") or f"{name}-{tenant_id}"
        _scrape_niche(tenant_id, name, n.get("keywords", [name]), n.get("target", 1000), campaign_id)
        scraped += 1


def run_all():
    log.info("═" * 50)
    log.info("  SCRAPER SERVICE — %s", time.strftime("%Y-%m-%d %H:%M:%S UTC"))
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
    interval = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "15"))
    log.info("  Mode survivor (toutes les %d min)", interval)
    while True:
        run_all()
        for _ in range(interval * 60):
            time.sleep(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scraper Service")
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
