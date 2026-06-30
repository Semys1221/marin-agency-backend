# Resend Transactional Emails — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=PHEXZcauLV-1kcnFY5DR

## Purpose
Sends event-driven transactional emails via Resend. 10 types triggered by specific funnel events. Also manages nurture sequences for post-call and post-sale.

## Database Tables

### email_tracking
```prisma
model EmailTracking {
  id          String   @id @default(uuid()) @db.Uuid
  tenantId    String   @map("tenant_id")
  leadEmail   String   @map("lead_email")
  campaignId  String?  @map("campaign_id")
  event       String   // 'sent' | 'opened' | 'clicked' | 'replied' | 'bounced'
  timestamp   DateTime @default(now())
  metadata    Json     @default("{}")
  @@index([tenantId])
  @@map("email_tracking")
}
```

## API Integrations
### Resend
```typescript
import { Resend } from 'resend';
const resend = new Resend(RESEND_API_KEY);
await resend.emails.send({
  from: 'Marin <hello@marin.app>',
  to: lead.email,
  subject: 'Votre appel de découverte',
  html: '<p>Bonjour {{name}}...</p>'
});
```

## Env Vars
```
RESEND_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Email Types
| # | Email | Trigger |
|---|-------|---------|
| 1 | Interested (pre-call) | Detective intelligence gathered — pre-call authority email |
| 2 | Info Requested | Lead asked a question (AI auto-responder) |
| 3 | No-Show | Missed call appointment |
| 4 | Call Reminder | Upcoming call (1h before) |
| 5 | Indecision | Post-call — lead is undecided |
| 6 | Onboarding | Deal closed — welcome & next steps |
| 7 | Invoice | Contract signed via Dropbox Sign |
| 8 | Service Delivery | Service delivered to client |
| 9 | Call Description | Post-call summary with next steps |
| 10 | Upsell | Cross-sell opportunity |

## Nurture Sequences (Resend Transactional Sequence)

These are multi-step email chains triggered by specific events, documented in the Eraser diagram as `Resend Transactional Sequence` (Aftermath group).

### Post-Call Nurture (Indecis & Not Interested)
- **Indecis → Resend Transactional Sequence**: J+1 follow-up, J+3 value recap, J+7 final offer, J+30 check-in
- **Not Interested → Resend Transactional Sequence**: J+1 thank you, J+30 re-engagement if lead opens

### Post-Sale Nurture (Aftermath)
- **Call Description → Upsell → Resend Transactional Sequence**: post-call summary email → upsell opportunity → ongoing nurture (J+7, J+30, J+90)
- Service Delivery confirmation automatically triggers CRM update (`clients.status`)

## Edges (from Eraser diagram)
- `Lead Intelligence > Interested: pre-call authority` — detective data triggers the pre-call "Interested" email
- `Interested > Info Requested: AI responder` — if lead replies, AI auto-responds
- `Info Requested > No-Show: missed call` — if call is missed after interest
- `No-Show > Call Reminder: upcoming call` — reminder for rescheduled call
- `Call Reminder > Indecision: post-call` — indecision email after call
- `Closed Won > Onboarding: send welcome` — onboarding email triggers on deal closed
- `Dropbox Sign > Invoice: send invoice` — invoice email triggers after contract signed
- `Service Delivery > CRM Update: deliverable sent` — delivery email triggers CRM update
- `Client Dashboard HTML > Call Description: post-call summary` — dashboard action triggers call description email
- `Call Description > Upsell: cross-sell` — call description leads to upsell email
- `Upsell > Resend Transactional Sequence: nurture` — upsell triggers ongoing nurture sequence
- `Indecis > Resend Transactional Sequence: nurture` — indecision triggers follow-up sequence
- `Not Interested > Resend Transactional Sequence: final` — not interested triggers final sequence

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/emails/renewal` | Email subscriptions due for renewal |
| GET | `/api/sequences/perf` | Sequence performance + open rates |

## Behavior
1. Event fires (booking, payment, contract signed, etc.)
2. Select correct template, render with lead variables
3. Send via Resend API
4. Track open/click in `email_tracking`
5. For nurture sequences: schedule next email based on sequence config

## Edge Cases
- Resend key dead → log, no crash
- Invalid email → log error, skip silently
- Rate limited → queue and retry
- Demo mode: log to console, don't send
