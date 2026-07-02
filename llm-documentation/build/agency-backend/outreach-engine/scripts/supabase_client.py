import os
from supabase import create_client, Client

_URL = os.getenv("SUPABASE_URL", "")
_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
_TENANT = os.getenv("TENANT_ID", "sylk-conseils")

_client: Client | None = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        _client = create_client(_URL, _KEY)
    return _client


def tenant_id() -> str:
    return _TENANT


def is_configured() -> bool:
    return bool(_URL and _KEY and _URL != "...")
