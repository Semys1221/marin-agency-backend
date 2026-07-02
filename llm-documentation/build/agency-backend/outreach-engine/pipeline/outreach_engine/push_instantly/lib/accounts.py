import requests

from .config import INSTANTLY_BASE
from .http import instantly_headers, log


def list_active() -> list[str]:
    url = f"{INSTANTLY_BASE}/accounts"
    params = {"limit": 100, "status": 1}
    resp = requests.get(url, headers=instantly_headers(), params=params)
    if resp.status_code != 200:
        log(f"Failed to list accounts: {resp.status_code} {resp.text}", "ERROR")
        return []
    data = resp.json()
    emails = [item["email"] for item in data.get("items", []) if item.get("email")]
    log(f"Found {len(emails)} active sending accounts: {emails}")
    return emails
