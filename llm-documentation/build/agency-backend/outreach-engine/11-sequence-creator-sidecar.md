# Sequence Creator Sidecar — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=YdBJjXEQW9a9CIV7Jsj1

## Purpose
Deployable sidecar (CLI + HTTP server) that wraps email generation, sequence building, and campaign push into a single service. Called by outreach-engine (`campaign.py`) for Instantly cold outreach and by Hermes/backend-api for Resend transactional emails.

## Dependencies
- `05-email-generator.md` (template rendering + A/B/C variants)
- `06-sequence-creator.md` (7-step multi-variant builds)
- `07-instantly-campaign.md` (campaign check/create/push)
- `frontend-engine/05-resend-emails.md` (transactional email types)
- `09-scaling-decision.md` (orchestrator that triggers sends)
- API keys: `INSTANTLY_API_KEY`, `RESEND_API_KEY`, `SEQUENCE_CREATOR_API_KEY`

## Env Vars
```
INSTANTLY_API_KEY=...
RESEND_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
SEQUENCE_CREATOR_API_KEY=...
```

## Behavior

### Mode 1 — CLI (Instantly Campaign Creation)
Called by `outreach-engine/campaign.py` when Hermes detects a new niche or Kill & Replace.

```bash
python sequence_creator.py instantly create \
  --niche "grossiste_beaute" \
  --campaign "Grossistes Beauté Paris - Juin 2026" \
  --activate \
  --leads-file "/data/leads/grossiste_beaute_cleaned.json"
```

Payload provided by Hermes/campaign.py:
```json
{
  "niche": "grossiste_beaute",
  "campaign_name": "Grossistes Beauté Paris - Juin 2026",
  "activate": true,
  "leads": [
    {"email": "contact@example.com", "first_name": "Jean", "phone_number": "+33612345678"}
  ]
}
```

Response (campaign.py parses CLI output):
```json
{
  "status": "created",
  "campaign_id": "instantly-camp-123",
  "steps": 7,
  "variants": {"A": 7, "B": 6, "C": 3},
  "leads_pushed": 1450
}
```

### Mode 2 — HTTP Server (Resend Transactional)
Runs on port 8002. Called by Hermes or backend-api for Resend transactional sends.

**Endpoint:** `POST /api/email/send`
**Auth:** `Authorization: Bearer {SEQUENCE_CREATOR_API_KEY}`

```json
{
  "type": "call-reminder",
  "to": "client@example.com",
  "from_email": "marin@marincie.homes",
  "vars": {
    "nom_prospect": "Jean",
    "entreprise": "Dupont Fils",
    "rdv_date": "lundi 14 juillet à 10h00",
    "call_link": "https://meet.google.com/abc-defg-hij"
  }
}
```

Response:
```json
{"status": "sent", "type": "call-reminder", "to": "client@example.com"}
```

Supported Resend types: `information-requested`, `no-show`, `call-reminder`, `invoice`, `service-delivery`, `call-description`.

### Mode 3 — Dashboard
`index.html` — Static HTML dashboard for manually creating/pushing Instantly campaigns and sending Resend transactional emails. Hosted alongside the HTTP server.

## Hermes API Contract

```
Hermes Agent
  ├── Campaign Management (Instantly)
  │   → Appelle campaign.py (outreach-engine)
  │   → campaign.py appelle Sequence Creator en CLI
  │
  ├── Transactional Emails (Resend)
  │   → POST /api/email/send (Sequence Creator API server)
  │
  └── Nurturing Sequences (loop.so)
      → Webhook vers loop.so (externe)
```

## Eraser Diagram Edges
- `Hermes Agent > Sequence Creator (Dual): orchestrate both modes`
- `Sequence Creator (Dual) > Instantly Cold Mode: switch`
- `Sequence Creator (Dual) > Resend Transactional Mode: switch`
- Full contract defined in `hermes-api-contract.md`

## Edge Cases
- API key missing → return descriptive error, never crash
- Unknown Resend type → return `{"error": "unknown type"}`
- Instantly campaign creation fails → retry up to 3x, then return error
- Demo mode: return mock responses for all CLI + HTTP calls
