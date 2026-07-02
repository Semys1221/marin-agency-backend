import requests

from .config import INSTANTLY_BASE, LEAD_BATCH_SIZE
from .http import instantly_headers, log


def push(campaign_id: str, rows: list[dict]) -> int:
    total_uploaded = 0
    for i in range(0, len(rows), LEAD_BATCH_SIZE):
        batch = _to_instantly_format(rows[i:i + LEAD_BATCH_SIZE])
        result = _push_batch(campaign_id, batch)
        if result:
            total_uploaded += result.get("leads_uploaded", 0)
    return total_uploaded


def _to_instantly_format(rows: list[dict]) -> list[dict]:
    leads = []
    for row in rows:
        lead = {"email": row.get("email", "")}
        if row.get("first_name"):
            lead["first_name"] = row["first_name"]
        if row.get("last_name"):
            lead["last_name"] = row["last_name"]
        if row.get("company_name"):
            lead["company_name"] = row["company_name"]
        if row.get("phone"):
            lead["phone"] = row["phone"]
        leads.append(lead)
    return leads


def _push_batch(campaign_id: str, batch: list[dict]) -> dict | None:
    payload = {
        "campaign_id": campaign_id,
        "leads": batch,
        "skip_if_in_workspace": True,
        "verify_leads_on_import": False,
    }
    resp = requests.post(f"{INSTANTLY_BASE}/leads/add", json=payload, headers=instantly_headers())
    if resp.status_code not in (200, 201):
        log(f"Failed to push leads: {resp.status_code} {resp.text}", "ERROR")
        return None
    result = resp.json()
    log(f"Pushed {result.get('leads_uploaded', 0)}/{len(batch)} leads (dups={result.get('duplicated_leads', 0)}, blocked={result.get('in_blocklist', 0)})")
    return result
