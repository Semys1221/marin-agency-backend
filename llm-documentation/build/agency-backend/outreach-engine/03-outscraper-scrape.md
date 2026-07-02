# Outscraper Scrape — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=jlkUFWt6qk4_xLbffz-N

## Purpose
Scrapes Google Maps leads using Outscraper SDK based on active niche. Upserts raw leads into `cold_leads` table.

## Database Tables

### cold_leads
```prisma
model ColdLead {
  id          String   @id @default(uuid()) @db.Uuid
  tenantId    String   @map("tenant_id")
  email       String
  companyName String?  @map("company_name")
  domain      String?
  phone       String?
  location    String?
  source      String   @default("outscraper")
  campaignId  String?  @map("campaign_id")
  metadata    Json     @default("{}")
  createdAt   DateTime @default(now()) @map("created_at")
  @@unique([tenantId, email])
  @@index([tenantId])
  @@map("cold_leads")
}
```

### scrape_campaigns
```prisma
model ScrapeCampaign {
  id           String   @id @default(uuid()) @db.Uuid
  tenantId     String   @map("tenant_id")
  campaignId   String   @map("campaign_id")
  name         String
  keywords     String[]
  locations    String[]
  niches       Json     @default("[]")
  target       Int      @default(10000)
  status       String   @default("running")
  leadsFound   Int      @default(0) @map("leads_found")
  leadsCleaned Int      @default(0) @map("leads_cleaned")
  queue        Json     @default("[]")
  progress     Json     @default("{}")
  errors       String[]
  createdAt    DateTime @default(now()) @map("created_at")
  completedAt  DateTime?
  @@unique([tenantId, campaignId])
  @@map("scrape_campaigns")
}
```

### outscraper_usage
```sql
CREATE TABLE outscraper_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  niche TEXT NOT NULL,
  queries_used INT DEFAULT 0,
  leads_found INT DEFAULT 0,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  UNIQUE(tenant_id, niche, date)
);
```

**Doc API:** https://app.outscraper.cloud/api-docs
**Script:** `scripts/outscraper-scrape/outscraper_scraper.py`

## API Integrations
### Outscraper
```python
from outscraper import OutscraperClient
client = OutscraperClient(api_key=OUTSCRAPER_API_KEY)
results = client.google_maps_search([f"{keyword} {location}"], limit=1000, language="fr", enrichment=["contacts_n_leads"])
```

### Supabase
```python
supabase.table("cold_leads").upsert({
  "tenant_id": tenant_id,
  "email": lead["email"],
  "company_name": lead.get("name"),
  "domain": extract_domain(lead.get("site")),
  "phone": lead.get("phone"),
  "location": lead.get("location"),
  "source": "outscraper",
  "campaign_id": campaign_id,
  "metadata": lead
}, on_conflict=["tenant_id", "email"]).execute()
```

## Env Vars
```
OUTSCRAPER_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
SLACK_BOT_TOKEN=...
SLACK_CHANNEL_ID=...
```

## API Endpoints (internal)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/scrape/status` | Status of active scrape jobs |
| POST | `/api/scrape/start` | `{niche, limit}` → start scraping |
| POST | `/api/scrape/stop` | `{niche}` → stop |

## Behavior
1. Read active niche from scheduler or campaign queue
2. Call Outscraper SDK with keywords + location + limit
3. For each lead: upsert into `cold_leads` (place_id dedup via email)
4. Track progress in `scrape_campaigns` (leads_found, errors)
5. Notify Slack at milestones: 100/500/1000/2000/5000 leads
6. Mark complete when target reached

## Edge Cases
- Outscraper key dead → alert Slack, pause, retry 5min
- Rate limited → exponential backoff (1s → 5s → 30s → 2min)
- No results → mark niche exhausted, trigger new niche gen
- Demo mode: return 5 hardcoded leads from fixture
