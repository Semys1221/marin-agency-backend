# Detective Agent — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=RDJuOVOzmiHpWpPisVN4

## Purpose
Scrapes lead's website from company domain and returns structured JSON intelligence for the agent's call prep.

## Database Tables

### clients (write — metadata + detective_data)
```prisma
model Client {
  id               String   @id @default(uuid()) @db.Uuid
  tenantId         String   @unique @map("tenant_id")
  companyName      String   @map("company_name")
  email            String?
  domain           String?  // company website domain
  metadata         Json     @default("{}")  // stores detective intelligence here
  @@map("clients")
}
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior
1. Receive company domain (from landing page)
2. Scrape website for: tagline, services, team size, social links, recent news, pricing
3. Parse into structured JSON intelligence
4. Store in `clients.metadata.detective_data`
5. Display on call page for agent

## Output Schema
```json
{
  "company_name": "Example SARL",
  "domain": "example-sarl.fr",
  "tagline": "Votre partenaire beauté depuis 2010",
  "services": ["Distribution cosmétique", "Conseil en image"],
  "team_size_estimate": "10-50",
  "social_links": ["linkedin.com/company/example"],
  "recent_news": ["Nouveau partenariat avec X (juin 2026)"],
  "pricing_tier": "premium",
  "raw_summary": "Entreprise familiale basée à Lyon..."
}
```

## Edge Cases
- No website → return empty intelligence, flag to agent
- Website blocked (403) → skip, log
- Very large site → scrape only top 3 pages
- Demo mode: return hardcoded intelligence fixture
