# Post-Call Decision — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=0XtaoappxmYqQ5naJfVJ

## Purpose
Handles decision after call: Closed Won, Indecis, or Not Interested. Each triggers a different path.

## Database Tables

### call_sessions (write — decision)
```prisma
model CallSession {
  id            String    @id @default(uuid()) @db.Uuid
  tenantId      String    @map("tenant_id")
  clientId      String    @map("client_id") @db.Uuid
  decision      String?   // closed_won | indecis | not_interested
  status        String    @default("scheduled")
  notes         String?
  @@map("call_sessions")
}
```

### clients (write — status, callCount)
```prisma
model Client {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @unique @map("tenant_id")
  status    String   @default("active")  // active | paused | archived
  callCount Int      @default(0) @map("call_count")
  @@map("clients")
}
```

### clean_leads (write — lead status)
```prisma
model CleanLead {
  id     String @id @default(uuid()) @db.Uuid
  status String @default("fresh")  // fresh | contacted | replied | interested | client | dead
  @@map("clean_leads")
}
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/leads/status` | Update lead status (no-show, indecis, closed) |
| GET | `/api/crm/prospects` | CRM prospects list |

## Behavior
### Closed Won
1. Update `clean_leads.status = 'client'`
2. Update `clients.status = 'active'`, increment `callCount`
3. Trigger chain (per Eraser diagram): Onboarding email (welcome) → Stripe Payment → Gift (Jabra) → Dropbox Sign → Invoice → CRM Update → Onboarding in App
4. Actual chronological order: Closed Won → send Onboarding email → collect Stripe Payment → ship Gift → sign Dropbox Contract → send Invoice email → CRM Update → Onboarding in App

### Indecis
1. Update `clean_leads.status = 'indecis'`
2. Set `call_sessions.decision = 'indecis'`
3. Trigger: Resend nurture sequence
4. Schedule follow-up call in 7 days

### Not Interested
1. Update `clean_leads.status = 'dead'`
2. Set `call_sessions.decision = 'not_interested'`
3. Trigger: Resend final email
4. Archive lead (soft delete)

## Edge Cases
- Agent closes without selecting → auto-set "indecis" after 24h
- Double submission → idempotent (check decision already set)
- Demo mode: simulate without real side effects
