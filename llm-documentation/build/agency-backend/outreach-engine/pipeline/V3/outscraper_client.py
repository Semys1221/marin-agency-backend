#!/usr/bin/env python3
"""Outscraper API client — 1 fichier, 1 responsabilité : appeler l'API Outscraper."""

import os
import logging

log = logging.getLogger("v3.outscraper")


def search(keywords: list[str], limit: int = 20) -> list[dict]:
    """Interroge l'API Outscraper Google Maps Search.

    Args:
        keywords: Liste de mots-clés (ex: ["grossiste beauté Paris"])
        limit: Nombre max de résultats par requête

    Returns:
        Liste de résultats bruts (dictionnaires). [] si erreur.
    """
    from outscraper import ApiClient

    api_key = os.getenv("OUTSCRAPER_API_KEY", "")
    if not api_key:
        log.warning("[outscraper] OUTSCRAPER_API_KEY non configurée")
        return []

    enrichment = os.getenv("OUTSCRAPER_ENRICHMENT", "contacts_n_leads").split(",")
    client = ApiClient(api_key=api_key)

    try:
        log.info("[outscraper] requête: %s (limit=%s)", keywords, limit)
        results = client.google_maps_search(
            keywords[0] if len(keywords) == 1 else keywords,
            limit=limit,
            language="fr",
            enrichment=enrichment,
        )
    except Exception as e:
        log.warning("[outscraper] échec API: %s", e)
        return []

    # Normalisation du retour
    if results is None:
        log.warning("[outscraper] retour None (crédits épuisés ?)")
        return []
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], list):
        results = results[0]
    if not isinstance(results, list):
        log.warning("[outscraper] type inattendu: %s", type(results))
        return []

    # Filtrer les entrées None
    results = [r for r in results if r is not None]
    log.info("[outscraper] %s résultats", len(results))
    return results


def normalize_phone(raw: str) -> str:
    """Normalise un numéro de téléphone en format international +33."""
    if not raw:
        return ""
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 10 and digits.startswith("0"):
        return "+33" + digits[1:]
    if digits.startswith("33"):
        return "+" + digits
    return raw


def to_lead(entry: dict, queue_id: str, niche: str, city: str) -> dict:
    """Transforme une entrée brute Outscraper en format lead Supabase."""
    email = entry.get("email", "")
    return {
        "campaign_queue_id": queue_id,
        "place_id": entry.get("place_id", ""),
        "email": email or f"no-email-{entry.get('phone', '')}",
        "first_name": entry.get("first_name", "") or "",
        "company_name": entry.get("name", "") or "",
        "domain": email.split("@")[-1] if "@" in email else "",
        "phone": normalize_phone(entry.get("phone", "")),
        "location": entry.get("full_address", "") or "",
        "niche": niche,
        "status": "scraped",
        "valid": False,
        "city": city,
    }
