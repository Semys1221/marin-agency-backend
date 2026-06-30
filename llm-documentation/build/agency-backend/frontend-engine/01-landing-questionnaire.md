# Landing Page Questionnaire — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=PyoRd4vxu9VEKCf0V2XB

## GATES (must check before building)

- **Gate 1:** Supabase project deployed. Every DB call wraps in try/catch — never crash.
- **Gate 2:** All API keys defined with value `...` if not configured. Every wrapper checks `if (!key || key === '...') return { error: 'non configuré' }`.
- **Gate 3:** Open Eraser diagram at https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ before writing code. Verify component exists as a node.
- **Gate 4:** Single shared DB. `X-Tenant-ID` header isolates data. Never implement login.
- **Gate 5:** Read existing code in `trash-ignore/Github/Outreach_System/` first.
- **Gate 6:** Every endpoint supports `?demo=true` returning mock data. No real API calls in demo mode.

## Architecture

Two-phase engine:

```
Phase 1: Outreach Engine (24/7 autonome)
  User JSON → Brain/Gemini → Outscraper → Clean → Instantly → Benchmarks → Loop

Phase 2: Frontend Engine
  Interested Lead → Landing → Calendly → Detective → Emails → Call → Decision → CRM
```

Phase 2 = NodeJS/Express + Prisma. Frontend = Next.js/React + Zustand.

## Tech Stack

| Layer | Stack |
|-------|-------|
| Runtime | NodeJS 20+, Express 4.21, TypeScript 5.6 |
| Database | Prisma 5.20 + Supabase Postgres |
| Payments | Stripe SDK 17.0 |
| E-signature | Dropbox Sign SDK 3.0 |
| Email | Resend API |
| Notifications | Slack Bolt 4.1 |
| AI | Gemini SDK 0.21 |
| Monitoring | Sentry Node 8.30 |
| Hosting | Render (API) + Vercel (frontend) |

## Purpose
First touchpoint for interested leads. Multi-step form qualifying the lead, caching answers in Zustand, preparing for booking.

## Database Tables

### funnel_progress
```prisma
model FunnelProgress {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @map("tenant_id")
  clientId  String   @map("client_id") @db.Uuid
  step      String
  data      Json     @default("{}")
  sessionId String?  @map("session_id")
  createdAt DateTime @default(now()) @map("created_at")
  client Client @relation(fields: [clientId], references: [id])
  @@map("funnel_progress")
}
```

### clients
```prisma
model Client {
  id               String   @id @default(uuid()) @db.Uuid
  tenantId         String   @unique @map("tenant_id")
  companyName      String   @map("company_name")
  email            String?
  phone            String?
  offer            String   @default("main")
  instanceDomain   String?  @map("instance_domain")
  status           String   @default("active")
  callCount        Int      @default(0) @map("call_count")
  funnelStep       String?  @map("funnel_step")
  paymentId        String?  @map("payment_id")
  contractId       String?  @map("contract_id")
  metadata         Json     @default("{}")
  createdAt        DateTime @default(now()) @map("created_at")
  updatedAt        DateTime @updatedAt @map("updated_at")
  callSessions     CallSession[]
  funnelProgress   FunnelProgress[]
  @@map("clients")
}
```

## API Integrations
### Supabase (Prisma)
```typescript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()
// prisma.funnelProgress.create({ data: { tenantId, clientId, step, data } })
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/funnel/save-step` | Save current step data |
| GET | `/api/funnel/progress?session_id=X` | Resume session |
| GET | `/api/funnel/health` | Funnel speed + Sentry dead links |

## Behavior
1. Interested lead arrives on landing page (redirect from Instantly reply)
2. Multi-step questionnaire collects: company info, contact, pain points, budget
3. All answers cached in Zustand (survives refresh)
4. Each step persists to `funnel_progress` in Supabase
5. On completion → redirect to Calendly booking

## Edge Cases
- User refreshes mid-form → resume from Zustand + DB
- Invalid SIRET → retry step with error
- Abandon → save partial, follow-up via Resend
- Demo mode: skip API calls, Zustand only
