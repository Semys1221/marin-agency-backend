# Email Cleaning — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=pJP9cb61sDXIxOHswPul

**Doc MyEmailVerifier:** https://github.com/pat-myemailverifier/myemailverifier-api

## Purpose
Two-stage email validation: MX check + syntax → MyEmailVerifier API. Outputs clean leads ready for campaigns.

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

### MyEmailVerifier API
```python
import requests

MYEMAILVERIFIER_API_KEY = os.getenv("MYEMAILVERIFIER_API_KEY")

resp = requests.get(
    "https://api.myemailverifier.com/api/validate_single.php",
    params={"apikey": MYEMAILVERIFIER_API_KEY, "email": email},
    timeout=10,
)
data = resp.json()
# data = {
#   "Address": "test@example.com",
#   "Status": "Valid" | "Invalid" | "Catch-all" | "Unknown",
#   "catch_all": "true" | "false",
#   "Disposable_Domain": "true" | "false",
#   "Role_Based": "true" | "false",
#   "Free_Domain": "true" | "false",
#   "Diagnosis": "Mailbox Exists and Active" | ...
# }
```

## Env Vars
```
MYEMAILVERIFIER_API_KEY=V5IOl8dgKfhHo5Ln
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior

### Stage 1 — Quick Clean (MX + Syntax)
1. Read raw leads from `cold_leads`
2. MX record check via dnspython — reject domains without MX
3. Syntax validation — reject malformed emails
4. Role-based detection (`contact@`, `info@`, `admin@`) → flag high risk

> **Petit volume (< 100 leads) :** utiliser `scripts/email-validator/cleaner.py --local`.
> Pour le pipeline complet : `scripts/email-validator/cleaner.py` (stage 1 local + stage 2 API).

### Stage 2 — MyEmailVerifier API
1. Send survivors to MyEmailVerifier API
2. Reject `Invalid` or `Catch-all` emails
3. Accept `Valid` emails (optionally flag `Role_Based` as high risk)

## Edge Cases
- MyEmailVerifier key dead → cleaner.py fallback sur stage 1 (`--local`)
- API rate limited (30 req/min default) → client.py queue + retry automatique
- All leads rejected → mark campaign "needs new source"
- Demo mode (`--demo`) → zéro appel API, risques aléatoires
