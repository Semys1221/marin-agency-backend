# Instance Duplication — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=zbm5twzQ2PegJ6Q0ix5j

**Note:** Diagram updated — le nœud "Duplication" est présent dans le Full Funnel Eraser.io (groupe violet `Duplication` avec les sous-nœuds `Duplication Form`, `Vercel Deploy`, `Hermes Activation`).

## Purpose
Creates a new client instance via React form. Copies template, configures env, deploys to Vercel, activates Hermes.

## Database Tables

### clients (write)
```prisma
model Client {
  id             String   @id @default(uuid()) @db.Uuid
  tenantId       String   @unique @map("tenant_id")
  companyName    String   @map("company_name")
  email          String?
  offer          String   @default("main")
  instanceDomain String?  @map("instance_domain")
  status         String   @default("active")
  @@map("clients")
}
```

## API Integrations
### Vercel API
```typescript
// Deploy new frontend instance
await fetch(`https://api.vercel.com/v13/deployments`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${VERCEL_TOKEN}` },
  body: JSON.stringify({
    name: `client-${tenantId}`,
    project: 'marin-frontend-template',
    target: 'production'
  })
});
```

## Env Vars
```
VERCEL_TOKEN=...
VERCEL_TEAM_ID=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/clients/quota` | New client → update quota + 90-day objective |

## Behavior
1. Admin opens React duplication form
2. Captures: client name, domain, colors, logo, offer, niche
3. Backend automation:
   - Copy frontend template → new project
   - Modify `config.ts` with client values
   - Create Supabase records (Client, campaign config)
   - Deploy to Vercel via API
   - Create user JSON for outreach engine
   - Activate Hermes campaign for new tenant
4. Client receives access

## Edge Cases
- Template not found → return error, no partial instance
- Vercel deploy fails → rollback created resources
- Duplicate tenant_id → reject with conflict
- Demo mode: simulate deploy without real Vercel API
