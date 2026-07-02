import os

INSTANTLY_API_KEY = os.getenv("INSTANTLY_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
TENANT_ID = os.getenv("TENANT_ID", "sylk-conseils")

INSTANTLY_BASE = "https://api.instantly.ai/api/v2"
LEAD_BATCH_SIZE = 1000
