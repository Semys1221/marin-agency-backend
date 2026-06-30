# Call Page + Live Form — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=DbCzoKhJrHmMF4joGckm

## Purpose
Real-time call interface for the agent. Shows lead info + Detective intelligence + live form saving to DB. Supports pause/resume.

## Database Tables

### call_sessions (read/write)
```prisma
model CallSession {
  id            String    @id @default(uuid()) @db.Uuid
  tenantId      String    @map("tenant_id")
  clientId      String    @map("client_id") @db.Uuid
  callNumber    Int?      @map("call_number")
  status        String    @default("scheduled")  // scheduled | ongoing | completed | no_show
  scheduledAt   DateTime? @map("scheduled_at")
  liveFormData  Json      @default("{}") @map("live_form_data")
  notes         String?
  recordingUrl  String?   @map("recording_url")
  decision      String?   // closed_won | indecis | not_interested
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")
  client Client @relation(fields: [clientId], references: [id])
  @@map("call_sessions")
}
```

## API Integrations
### Supabase (Prisma)
```typescript
// Real-time update on every field change
await prisma.callSession.update({
  where: { id: sessionId },
  data: { liveFormData: currentFormData }
})
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior
1. Agent opens call page at scheduled time
2. Page displays: lead name, company, phone, Detective intelligence, previous notes
3. Live form during call: pain points, objections, budget, timeline
4. Every field autosaves to `call_sessions.liveFormData` in real time
5. Agent can pause → progress not lost
6. On resume → form state restored from DB
7. Agent marks complete → triggers Decision component

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/calls/content` | Call scripts, upsells |

## Edge Cases
- Connection lost → local Zustand cache, sync on reconnect
- Agent closes browser → next load restores from DB
- Demo mode: pre-populated form data, no DB persistence
