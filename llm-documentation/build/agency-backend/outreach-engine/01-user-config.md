# User Config — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=nN0c_LscKTt8USVzd0cm

## GATES (must check before building)

- **Gate 1:** Supabase project deployed with URL + service_role_key in env vars. Every DB call wraps in try/catch — never crash.
- **Gate 2:** All API keys defined in env vars with value `...` if not configured. Every API wrapper checks `if (!key || key === '...') return { error: 'non configuré' }`.
- **Gate 3:** Open Eraser diagram at https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ before writing a single line. Verify component exists as a node.
- **Gate 4:** Single shared DB. No user accounts. `X-Tenant-ID` header isolates data. Never implement login.
- **Gate 5:** Read existing code in `trash-ignore/Github/Outreach_System/` before writing new code. Reuse patterns.
- **Gate 6:** Every endpoint must support `?demo=true` returning mock data. No real API calls in demo mode.

## Architecture

Two-phase engine:

```
Phase 1: Outreach Engine (24/7 autonome)
  User JSON → Brain/Gemini → Outscraper → Clean → Instantly → Benchmarks → Loop

Phase 2: Frontend Engine
  Interested Lead → Landing → Calendly → Detective → Emails → Call → Decision → CRM
```

One engine. One DB. Multiple frontends. Phase 1 is Python/FastAPI, Phase 2 is NodeJS/Express.

## Tech Stack

| Layer | Stack |
|-------|-------|
| Runtime | Python 3.12+, FastAPI, Uvicorn |
| Scheduler | APScheduler |
| AI | Gemini (`gemini-1.5-flash`) |
| Scraping | Outscraper SDK (`outscraper` pip) |
| Email validation | dnspython (MX), Handshake API, DBBounce API |
| Campaigns | Instantly API V2 |
| Notifications | Slack Web API |
| DB | Supabase (REST + `supabase` pip) |
| Hosting | Render (web service) |

## Purpose

JSON config file per tenant defining niche, targets, and allowed domains. The engine reads this to know what to scrape and where to send leads.

## Database Tables

### clients
```prisma
model Client {
  id               String   @id @default(uuid()) @db.Uuid
  tenantId         String   @unique @map("tenant_id")
  companyName      String   @map("company_name")
  email            String?
  offer            String   @default("main")
  instanceDomain   String?  @map("instance_domain")
  shopifyStoreDomain String? @map("shopify_store_domain")
  status           String   @default("active")
  callCount        Int      @default(0) @map("call_count")
  paymentId        String?  @map("payment_id")
  contractId       String?  @map("contract_id")
  metadata         Json     @default("{}")
  createdAt        DateTime @default(now()) @map("created_at")
  updatedAt        DateTime @updatedAt @map("updated_at")
  @@map("clients")
}
```

### niche_variable
```prisma
model NicheVariable {
  id          String @id @default(uuid()) @db.Uuid
  niche       String @unique
  variables   Json   @default("{}")
  template    String?
  @@map("niche_variable")
}
```

## API Integrations

### Supabase
```python
from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
# .table("clients").select("*").eq("tenant_id", tenant_id).execute()
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior

1. Each tenant has a JSON config file at `/users/{tenant}/config.json`
2. Config defines: niche, keywords, locations, target count, allowed domains
3. Engine reads config on startup and each scrape cycle
4. Adding a new client = adding a new JSON file (no code change)

## Config Schema
```json
{
  "tenant_id": "client-a",
  "niche": "grossiste_beaute",
  "keywords": ["grossiste beauté Paris"],
  "locations": ["Paris", "Lyon"],
  "target": 10000,
  "allowed_domains": ["gmail.com", "outlook.fr"],
  "instantly_campaign_id": "camp-789"
}
```

## Edge Cases
- Missing config file → skip tenant, log warning
- Invalid JSON → stop, alert Slack
- Empty keywords → skip niche generation
- Demo mode: return hardcoded `_demo.json` fixture
