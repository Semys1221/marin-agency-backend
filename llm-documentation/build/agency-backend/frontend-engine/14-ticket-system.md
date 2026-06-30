# Ticket System — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=HZaOZXAU0HuC0wL_PY33

## Purpose
Customer support ticket system. Client sends an email → Resend inbound webhook → Gemini auto-replies with human-sounding acknowledgment → Slack notification → SLA 24h tracking → escalation.

## Dependencies
- `database/` (shared Supabase — tickets table)
- `frontend-engine/05-resend-emails.md` (Resend API for replies)
- `outreach-engine/02-brain-gemini.md` (Gemini for auto-reply generation)
- `outreach-engine/10-slack-notifications.md` (Slack for ticket notifications)
- API keys: `RESEND_API_KEY`, `GEMINI_API_KEY`, `SLACK_BOT_TOKEN`, `TICKET_SYSTEM_API_KEY`

## Architecture
```
Client Email → email.marinlite.agency (Resend inbound webhook)
                    │
                    ▼
           Ticket Handler (FastAPI /api/ticket/incoming)
                    │
             ┌──────┴──────┐
             ▼              ▼
      Gemini AI          Slack
      (auto-reply)       (#tickets channel)
             │
             ▼
      Resend API
      (reply to client)
```

## Database Tables

### tickets
```sql
CREATE TABLE tickets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_name TEXT NOT NULL,
  client_email TEXT NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'replied', 'in_progress', 'resolved', 'escalated')),
  ai_reply TEXT,
  assigned_to TEXT,
  sla_deadline TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  resolved_at TIMESTAMPTZ
);
```

## API Integrations

### Resend Inbound Webhook
```python
# Resend → POST /api/ticket/incoming
# Headers: Authorization: Bearer {TICKET_SYSTEM_API_KEY}
{
  "from": "jean.dupont@example.com",
  "sender_name": "Jean Dupont",
  "subject": "Problème de connexion",
  "text": "Bonjour, je n'arrive pas à accéder...",
  "priority": "high"
}
```

### Gemini Auto-Reply
```python
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = f"Rédige un accusé de réception personnalisé et humain pour {client_name}. Remercie, reconnais le problème, donne un délai de 24h. Ne résous PAS le problème."
reply = model.generate_content(prompt).text
```

### Slack Notification
```python
slack.chat_postMessage(
  channel="#tickets",
  text=f"🎫 [HAUTE] Nouveau ticket — {client_name}\nSujet: {subject}\nSLA: 24h"
)
```

## Env Vars
```
RESEND_API_KEY=...
GEMINI_API_KEY=...
SLACK_BOT_TOKEN=...
SLACK_TICKETS_CHANNEL=#tickets
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
TICKET_SYSTEM_API_KEY=...
TICKET_SYSTEM_PORT=8003
RESEND_FROM_EMAIL=Marin Support <support@marinlite.agency>
TICKET_SLA_HOURS=24
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ticket/incoming` | Resend inbound webhook |
| GET | `/api/tickets` | List tickets (optional `?status=open&priority=high`) |
| POST | `/api/tickets/assign` | `{"id": "...", "assignee": "Evan"}` |
| POST | `/api/tickets/resolve` | `{"id": "..."}` |
| POST | `/api/sla/check` | Cron — check overdue SLA tickets |
| GET | `/health` | Health check |

## Behavior
1. Client sends email to `support@marinlite.agency`
2. Resend inbound webhook → `POST /api/ticket/incoming`
3. Create ticket in Supabase with SLA deadline = now + 24h
4. Gemini generates acknowledgment (human tone, no resolution, 24h timeframe)
5. Send reply via Resend API
6. Update ticket status to `replied`, store `ai_reply`
7. Notify Slack `#tickets` with ticket details
8. SLA checker (cron every 30min): if ticket still `open`/`replied` after 24h → escalate to `@support-lead`

## Dashboard
`index.html` — Static HTML dashboard listing tickets with filters (status, priority) and actions (assign, resolve). Fetches from `GET /api/tickets` and posts to assign/resolve endpoints.

## Eraser Diagram Nodes
- `Client Email` → `Resend Inbound Webhook` → `Ticket Handler (FastAPI)`
- `Ticket Handler` → `Gemini AI` (auto-reply generation)
- `Ticket Handler` → `Resend API` (send reply)
- `Ticket Handler` → `Slack #tickets` (notification)
- `Dashboard` → `Ticket Handler` (list + actions)
- `SLA Checker` → `Ticket Handler` (cron trigger)

## Edge Cases
- Invalid Resend webhook signature → return 401, log warning
- Gemini API dead → reply with graceful fallback text, still create ticket
- Slack token dead → log to console, no crash
- Duplicate webhook → dedup by Resend event ID
- DEMO_MODE: return mock tickets, skip all external API calls
