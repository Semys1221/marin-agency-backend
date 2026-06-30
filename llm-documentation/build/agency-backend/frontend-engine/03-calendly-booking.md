# Calendly Booking — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=lILdJ84u3oZNfkbKFquW

## Purpose
Lead books a discovery call via Calendly. Creates user in DB, sets countdown, offers self-discovery content.

## Database Tables

### clients (write)
```prisma
model Client {
  id               String   @id @default(uuid()) @db.Uuid
  tenantId         String   @unique @map("tenant_id")
  companyName      String   @map("company_name")
  email            String?
  phone            String?
  offer            String   @default("main")
  status           String   @default("active")
  callCount        Int      @default(0) @map("call_count")
  funnelStep       String?  @map("funnel_step")
  metadata         Json     @default("{}")
  createdAt        DateTime @default(now()) @map("created_at")
  updatedAt        DateTime @updatedAt @map("updated_at")
  callSessions     CallSession[]
  @@map("clients")
}
```

### call_sessions (write)
```prisma
model CallSession {
  id            String    @id @default(uuid()) @db.Uuid
  tenantId      String    @map("tenant_id")
  clientId      String    @map("client_id") @db.Uuid
  callNumber    Int?      @map("call_number")
  status        String    @default("scheduled")
  scheduledAt   DateTime? @map("scheduled_at")
  liveFormData  Json      @default("{}") @map("live_form_data")
  notes         String?
  recordingUrl  String?   @map("recording_url")
  decision      String?
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")
  client Client @relation(fields: [clientId], references: [id])
  @@index([tenantId])
  @@map("call_sessions")
}
```

## API Integrations
### Calendly
```typescript
// Webhook payload (incoming)
// POST /webhooks/calendly
// { event: "invitee.created", payload: { email, name, scheduled_event: { start_time } } }
```

## Env Vars
```
CALENDLY_URL=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Webhook
| Method | Path | Events |
|--------|------|--------|
| POST | `/webhooks/calendly` | `invitee.created`, `invitee.canceled` |

## Behavior
1. Embed Calendly scheduling after SIRET validation
2. Lead selects time → Calendly webhook fires `invitee.created`
3. Backend creates user in `clients` + `call_sessions` records
4. Frontend shows countdown timer to call
5. Optional self-discovery content offered
6. Detective Agent triggers after countdown

## Edge Cases
- Lead cancels → update status to `cancelled`, stop sending to lead
- Double booking → dedup via Calendly event URI
- Webhook fails → poll Calendly API for recent events
- Demo mode: simulate booking without real Calendly
