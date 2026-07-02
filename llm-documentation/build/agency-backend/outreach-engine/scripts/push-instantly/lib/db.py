from supabase import create_client, Client

from .config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY


def _client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def fetch_clean_leads(tenant_id: str, campaign_name: str | None = None, limit: int | None = None) -> list[dict]:
    query = _client().table("clean_leads").select("*").eq("tenant_id", tenant_id)
    if campaign_name:
        query = query.eq("campaign_id", campaign_name)
    if limit:
        query = query.limit(limit)
    return query.execute().data


def get_distinct_campaigns(tenant_id: str) -> list[str]:
    resp = _client().table("clean_leads").select("campaign_id").eq("tenant_id", tenant_id).neq("campaign_id", "").neq("campaign_id", None).execute()
    campaigns = set()
    for row in resp.data:
        c = row.get("campaign_id")
        if c:
            campaigns.add(c)
    return sorted(campaigns)


def mark_leads_contacted(tenant_id: str, campaign_name: str):
    _client().table("clean_leads").update({"status": "contacted"}).eq("tenant_id", tenant_id).eq("campaign_id", campaign_name).execute()


def save_instantly_campaign_id(tenant_id: str, campaign_id: str, instantly_campaign_id: str, niche: str = ""):
    payload = {
        "tenant_id": tenant_id,
        "campaign_id": campaign_id,
        "instantly_campaign_id": instantly_campaign_id,
        "niche": niche,
        "status": "running",
    }
    _client().table("campaign_settings").upsert(payload, on_conflict=["tenant_id", "campaign_id"]).execute()
