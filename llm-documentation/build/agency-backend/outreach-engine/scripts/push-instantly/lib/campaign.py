import time
import requests

from .config import INSTANTLY_BASE
from .http import instantly_headers, log
from .settings import build_payload
from .sequences import subsequence


def find_by_name(name: str) -> dict | None:
    url = f"{INSTANTLY_BASE}/campaigns"
    params = {"search": name, "limit": 20}
    resp = requests.get(url, headers=instantly_headers(), params=params)
    if resp.status_code != 200:
        log(f"Failed to list campaigns: {resp.status_code} {resp.text}", "ERROR")
        return None
    data = resp.json()
    for c in data.get("items", []):
        if c.get("name", "").strip().lower() == name.strip().lower():
            return c
    return None


def create(name: str, email_list: list[str]) -> dict | None:
    payload = build_payload(name, email_list)
    resp = requests.post(f"{INSTANTLY_BASE}/campaigns", json=payload, headers=instantly_headers())
    if resp.status_code not in (200, 201):
        log(f"Failed to create campaign: {resp.status_code} {resp.text}", "ERROR")
        return None
    campaign = resp.json()
    log(f"Created campaign '{name}' → id={campaign.get('id')} ({len(email_list)} accounts, text_only={payload['text_only']})")
    return campaign


def activate(campaign_id: str) -> bool:
    resp = requests.post(f"{INSTANTLY_BASE}/campaigns/{campaign_id}/activate", headers=instantly_headers())
    if resp.status_code != 200:
        log(f"Failed to activate campaign {campaign_id}: {resp.status_code}", "ERROR")
        return False
    log(f"Activated campaign {campaign_id}")
    return True


def create_with_subsequence(name: str, email_list: list[str]) -> dict | None:
    campaign = create(name, email_list)
    if not campaign:
        return None
    campaign_id = campaign["id"]
    time.sleep(1)
    activate(campaign_id)
    time.sleep(1)
    payload = subsequence(campaign_id)
    resp = requests.post(f"{INSTANTLY_BASE}/subsequences", json=payload, headers=instantly_headers())
    if resp.status_code not in (200, 201):
        log(f"Failed to create subsequence: {resp.status_code} {resp.text}", "ERROR")
    else:
        log(f"Created subsequence 'Interested Follow-up' → id={resp.json().get('id')}")
    return campaign
