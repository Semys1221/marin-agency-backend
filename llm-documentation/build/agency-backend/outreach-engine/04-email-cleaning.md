# Email Cleaning — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=pJP9cb61sDXIxOHswPul

## Purpose
Three-stage email validation: MX check + syntax → Handshake API → DB Bounce API. Outputs clean leads ready for campaigns.

## Database Tables

### cold_leads (read)
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

### clean_leads (write)
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
  profession  String?
  niche       String?
  status      String   @default("fresh")
  metadata    Json     @default("{}")
  createdAt   DateTime @default(now()) @map("created_at")
  cleanedAt   DateTime @default(now()) @map("cleaned_at")
  @@unique([tenantId, campaignId, email])
  @@index([tenantId])
  @@map("clean_leads")
}
```

## API Integrations
### MX Check (dnspython)
```python
import dns.resolver
try:
    answers = dns.resolver.resolve(domain, 'MX')
    has_mx = len(answers) > 0
except:
    has_mx = False
```

### Handshake API
```python
requests.post("https://api.handshake.com/v1/verify", json={"email": email}, headers={"X-API-Key": HANDSHAKE_API_KEY})
# Returns: {"status": "valid"|"risky"|"invalid", "risk_level": "low"|"medium"|"high"}
```

### DB Bounce API
```python
requests.post("https://api.dbbounce.com/v1/verify", json={"email": email}, headers={"X-API-Key": DBBOUNCE_API_KEY})
# Returns: {"status": "valid"|"bounce", "score": 0-100}
```

## Env Vars
```
HANDSHAKE_API_KEY=...
DBBOUNCE_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior

### Stage 1 — Quick Clean (MX + Syntax)
1. Read raw leads from `cold_leads`
2. MX record check via dnspython — reject domains without MX
3. Syntax validation — reject malformed emails
4. Role-based detection (`contact@`, `info@`, `admin@`) → flag high risk

### Stage 2 — Handshake API
1. Send survivors to Handshake API
2. Reject `risky` or `invalid` emails
3. Accept `valid` with risk_level `low` or `medium`

### Stage 3 — Deep Clean (DB Bounce)
1. Send Handshake-validated leads to DB Bounce
2. Upsert survivors into `clean_leads` with status `fresh`

## Edge Cases
- Handshake key dead → skip Stage 2, use MX-only
- DB Bounce key dead → skip Stage 3, use Handshake-only
- All leads rejected → mark campaign "needs new source"
- Demo mode: skip all API calls, move leads directly with random risk scores
