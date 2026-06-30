# Instantly Campaign — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=oY278MfOy8Z2ouhW14lY

## Purpose
Full Instantly campaign lifecycle: check if campaign exists, create new campaign, push leads, analyze results.

## Database Tables

### clean_leads
```prisma
model CleanLead {
  id          String   @id @default(uuid()) @db.Uuid
  tenantId    String   @map("tenant_id")
  campaignId  String   @map("campaign_id")
  email       String
  firstName   String?  @map("first_name")
  lastName    String?  @map("last_name")
  companyName String?  @map("company_name")
  domain      String?
  phone       String?
  location    String?
  isRoleBased Boolean  @default(false) @map("is_role_based")
  riskScore   String   @default("medium") @map("risk_score")
  status      String   @default("fresh")
  niche       String?
  metadata    Json     @default("{}")
  createdAt   DateTime @default(now()) @map("created_at")
  cleanedAt   DateTime @default(now()) @map("cleaned_at")
  @@unique([tenantId, campaignId, email])
  @@index([tenantId])
  @@map("clean_leads")
}
```

### campaign_settings (read)
```sql
CREATE TABLE campaign_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  niche TEXT NOT NULL,
  variants JSONB DEFAULT '[]',
  sequence JSONB DEFAULT '[]',
  instantly_campaign_id TEXT,
  status TEXT DEFAULT 'draft',    -- draft | running | paused | completed | killed
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, campaign_id)
);
```

### campaign_analytics
```sql
CREATE TABLE campaign_analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  leads_sent INT DEFAULT 0,
  opens INT DEFAULT 0,
  replies INT DEFAULT 0,
  bounces INT DEFAULT 0,
  reply_rate DECIMAL DEFAULT 0.0,
  checked_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, campaign_id, checked_at)
);
```

### campaign_queue
```sql
CREATE TABLE campaign_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  niche TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## API Integrations

### Instantly API V2
```python
headers = {"X-API-Key": INSTANTLY_API_KEY, "Content-Type": "application/json"}

# Check campaign exists
requests.get("https://api.instantly.ai/api/v2/campaigns", headers=headers)

# Create campaign
requests.post("https://api.instantly.ai/api/v2/campaigns", json={
    "name": name, "steps": sequence
}, headers=headers)

# Push leads
requests.post("https://api.instantly.ai/api/v2/leads", json={
    "campaign_id": campaign_id, "leads": lead_batch
}, headers=headers)

# Get analytics
requests.get(f"https://api.instantly.ai/api/v2/campaigns/{campaign_id}/analytics", headers=headers)
```

## Env Vars
```
INSTANTLY_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
SLACK_BOT_TOKEN=...
SLACK_CHANNEL_ID=...
```

## API Endpoints (internal)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/campaigns/health?tenant_id=X` | Campaign status + reply rates |
| POST | `/api/campaigns/stop` | Stop campaign by ID |

## Behavior
1. Check if campaign exists in Instantly → YES: push directly, NO: create new
2. Create campaign with sequence steps via Instantly API
3. Batch push clean leads (100/batch), update status to `contacted`
4. Track bounces → mark leads as `dead`
5. Fetch analytics periodically → store in `campaign_analytics`

## Edge Cases
- Instantly key dead → alert Slack, pause all ops
- Push fails → retry batch up to 3 times
- No leads to push → log warning
- Demo mode: return hardcoded campaign health, no API calls
