#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
_load_dotenv_path = _script_dir
for _ in range(10):
    if (_load_dotenv_path / ".env.local").exists():
        from dotenv import load_dotenv
        load_dotenv(_load_dotenv_path / ".env.local")
        break
    _load_dotenv_path = _load_dotenv_path.parent

sys.path.insert(0, os.path.join(_script_dir.as_posix(), '..'))
sys.path.insert(0, os.path.join(_script_dir.as_posix(), '..', 'niche-store'))

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("assign_niche")

from supabase_client import get_supabase, is_configured
from niche_store import get_active_niche_hunt, save_niche_hunt

CITY_TO_REGION = {
    "paris": "ile-de-france",
    "marseille": "provence-alpes-cote-dazur",
    "lyon": "auvergne-rhone-alpes",
    "toulouse": "occitanie",
    "nice": "provence-alpes-cote-dazur",
    "nantes": "pays-de-la-loire",
    "strasbourg": "grand-est",
    "montpellier": "occitanie",
    "bordeaux": "nouvelle-aquitaine",
    "lille": "hauts-de-france",
    "rennes": "bretagne",
    "reims": "grand-est",
    "saint-etienne": "auvergne-rhone-alpes",
    "le-havre": "normandie",
    "toulon": "provence-alpes-cote-dazur",
    "grenoble": "auvergne-rhone-alpes",
    "dijon": "bourgogne-franche-comte",
    "angers": "pays-de-la-loire",
    "nimes": "occitanie",
    "clermont-ferrand": "auvergne-rhone-alpes",
    "limoges": "nouvelle-aquitaine",
    "caen": "normandie",
    "perpignan": "occitanie",
    "metz": "grand-est",
    "pau": "nouvelle-aquitaine",
    "la-rochelle": "nouvelle-aquitaine",
    "brest": "bretagne",
    "amiens": "hauts-de-france",
    "tours": "centre-val-de-loire",
    "orleans": "centre-val-de-loire",
    "le-mans": "pays-de-la-loire",
    "mulhouse": "grand-est",
    "avignon": "provence-alpes-cote-dazur",
    "besancon": "bourgogne-franche-comte",
    "poitiers": "nouvelle-aquitaine",
    "valence": "auvergne-rhone-alpes",
    "annecy": "auvergne-rhone-alpes",
    "bayonne": "nouvelle-aquitaine",
    "lorient": "bretagne",
    "niort": "nouvelle-aquitaine",
    "saint-nazaire": "pays-de-la-loire",
    "chambery": "auvergne-rhone-alpes",
    "villeurbanne": "auvergne-rhone-alpes",
    "boulogne-billancourt": "ile-de-france",
    "montreuil": "ile-de-france",
    "saint-denis": "ile-de-france",
    "argenteuil": "ile-de-france",
    "aubervilliers": "ile-de-france",
    "courbevoie": "ile-de-france",
    "versailles": "ile-de-france",
    "aix-en-provence": "provence-alpes-cote-dazur",
    "colombes": "ile-de-france",
    "creteil": "ile-de-france",
    "cergy": "ile-de-france",
}


def slug(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("'", "-").replace(" ", "-").replace("_", "-")
    parts = [p for p in text.split("-") if p]
    return "-".join(parts)


def city_to_region(city: str | None) -> str:
    if not city:
        return "unknown"
    return CITY_TO_REGION.get(slug(city), slug(city))


def find_niche_in_hunts(hunts: list[dict], name: str, region: str) -> str | None:
    for hunt in hunts:
        niches = hunt.get("niches") or []
        for n in niches:
            n_name = n.get("name", "")
            n_loc = n.get("location", "")
            n_keywords = n.get("keywords") or []
            if slug(n_name) == slug(name):
                return n_name
            if slug(n_loc) == slug(region) and any(slug(kw) == slug(name) for kw in n_keywords):
                return n_name
    return None


def main():
    parser = argparse.ArgumentParser(description="Assign niche + campaign to clean leads")
    parser.add_argument("--tenant", default=os.getenv("TENANT_ID", "sylk-conseils"))
    parser.add_argument("--dry-run", action="store_true", help="Show what would be assigned")
    args = parser.parse_args()

    if not is_configured():
        log.error("Supabase non configuré")
        sys.exit(1)

    sb = get_supabase()

    rows = sb.table("clean_leads") \
        .select("*") \
        .eq("tenant_id", args.tenant) \
        .is_("niche", "null") \
        .execute()
    leads = [r for r in (rows.data or []) if (r.get("profession") or "").strip()]
    if not leads:
        log.info("Aucun lead sans niche à assigner")
        return

    active_hunt = get_active_niche_hunt(args.tenant)
    existing_niches = [active_hunt] if active_hunt and active_hunt.get("niches") else []

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    groups: dict[tuple[str, str], list[dict]] = {}

    for lead in leads:
        profession = lead.get("profession", "") or ""
        city = (lead.get("metadata") or {}).get("city", "") or ""
        region = city_to_region(city)
        prof_slug = slug(profession)
        key = (prof_slug, region)
        groups.setdefault(key, []).append(lead)

    if not groups:
        log.info("Aucun groupe à assigner")
        return

    new_niches = []
    total_assigned = 0

    for (prof_slug, region), group in groups.items():
        matched = find_niche_in_hunts(existing_niches, prof_slug, region)
        niche_name = matched or prof_slug
        is_new = not matched
        campaign_name = f"{niche_name}-{region}-{today}"
        lead_count = len(group)

        log.info(
            f"  {niche_name:30s} campaign={campaign_name:45s} leads={lead_count:3d} "
            f"{'(new niche)' if is_new else ''}"
        )

        if is_new:
            new_niches.append({
                "name": niche_name,
                "keywords": [group[0].get("profession", prof_slug)],
                "location": region,
            })

        if not args.dry_run:
            ids = [l["id"] for l in group]
            sb.table("clean_leads") \
                .update({"niche": niche_name, "campaign_id": campaign_name}) \
                .in_("id", ids) \
                .execute()
        total_assigned += lead_count

    if new_niches and not args.dry_run:
        save_niche_hunt(args.tenant, new_niches)
        log.info(f"Nouvelles niches créées : {len(new_niches)}")

    log.info(f"\nTotal : {total_assigned} leads assignés en {len(groups)} groupes")


if __name__ == "__main__":
    main()
