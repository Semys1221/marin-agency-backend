# CRM & Onboarding — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=GU_uf1DbbhrXFG4xY5O7

## Purpose
Manages Client + CallSession models. Onboarding logic coded in app (not Google Docs) for automated duplication.

## Database Tables

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
  onboardingTasks  OnboardingTask[]
  @@map("clients")
}
```

### call_sessions
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
}
```

### onboarding_tasks
```prisma
model OnboardingTask {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @map("tenant_id")
  clientId  String   @map("client_id") @db.Uuid
  task      String
  completed Boolean  @default(false)
  dueDate   DateTime? @map("due_date")
  createdAt DateTime @default(now()) @map("created_at")
  @@map("onboarding_tasks")
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
| GET | `/api/crm/prospects?tenant_id=X` | CRM prospects list |
| POST | `/api/clients/quota` | New client quota + 90-day objective |

## Behavior
### CRM
1. Create `clients` record when lead books call
2. Create `call_sessions` for each scheduled/completed call
3. Update client status through funnel steps
4. All scoped by `tenant_id`

### Onboarding (in-app)
1. After Closed Won → create onboarding task list:
   - Setup Microsoft account, Calendly, dashboard deploy
   - Instantly campaign setup, Jabra headset send
   - Onboarding call #1 schedule
2. Track completion in `onboarding_tasks`
3. Agent marks done via dashboard

## Edge Cases
- Duplicate client → upsert on tenant_id
- Task list changes → DB-driven, not hardcoded
- Demo mode: return mock CRM data
