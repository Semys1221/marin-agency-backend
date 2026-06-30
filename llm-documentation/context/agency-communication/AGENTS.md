# Communication Rules — Marin

## Source of Truth

The Eraser.io diagram (`model-marin-agency`) is the single source of truth. Every sequence, trigger, and API call must trace back to a node/edge. If it's not in the graph, don't build it.

**Reference:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

## Architecture

```
Outreach Engine (Phase 1)               Frontend Engine (Phase 2)
┌──────────────────────────┐           ┌──────────────────────────┐
│  Brain/Gemini → Scraper  │           │  Landing → Calendly →    │
│  → Clean → Campaign      │           │  Detective → Call → CRM │
│       │                  │           │       │                  │
│       ▼                  │           │       ▼                  │
│  Sequence Creator        │           │  Sequence Creator        │
│  (Instantly + Resend)    │           │  (Resend only)           │
└──────────────────────────┘           └──────────────────────────┘
```

- **Instantly** — Called by Outreach Engine (`campaign.py`) for cold outreach campaign creation
- **Resend** — Called by Hermes (transactional events) + Frontend Engine (post-call events)
- **loop.so** — External system, triggered via webhook from Hermes

## Prerequisites — GATES

**If any gate is RED, STOP. Do not write code. Report the blocker to the user.**

### Gate 1: outreach-engine deployed

```
REQUIRED: The outreach-engine (FastAPI) must be running on Render.
          Sequence Creator is a sidecar/utility called by campaign.py.
          Without it, there's no source of leads to push to Instantly.
BLOCKER:  outreach-engine not deployed → STOP.
```

### Gate 2: API keys set

```
REQUIRED: INSTANTLY_API_KEY, RESEND_API_KEY, SUPABASE_URL,
          SUPABASE_SERVICE_ROLE_KEY, SEQUENCE_CREATOR_API_KEY.
PATTERN:  Every API wrapper checks `if not key` → return descriptive error.
          Never hardcode keys. If value is `...`, service is disabled.
BLOCKER:  Any key missing from env → STOP.
```

### Gate 3: Database schema exists

```
REQUIRED: Tables `niche_variable` (id, niche, niche_keyword_1/2/3,
          niche_member, objectif, pain_point, methode, timeline, offre)
          and `email_log` (id, tenant_id, type, to, status, created_at).
BLOCKER:  Schema not deployed → STOP.
```

### Gate 4: Eraser diagram verified

```
REQUIRED: Open the Eraser diagram before writing code. Every sequence,
          trigger, and API endpoint must have a corresponding node/edge.
BLOCKER:  Diagram not verified → STOP.
```

### Gate 5: Existing code read

```
REQUIRED: Read trash-ignore/Github/Outreach_System/ for existing
          campaign creation and email sending patterns before writing
          anything new.
BLOCKER:  Legacy code not read → STOP. Will duplicate work.
```

### Gate 6: Demo mode in every endpoint

```
REQUIRED: Every endpoint supports `DEMO_MODE=true`. Return mock data,
          no external API calls, no side effects.
PATTERN:  If `DEMO_MODE` is true, render dummy JSON from the spec.
BLOCKER:  No dummy data → STOP. Spec incomplete.
```

## Rules

### 1. Three Systems, One Interface

| System | Mode | Called By | Protocol |
|--------|------|-----------|----------|
| Instantly | Cold outreach (7-step A/B/C) | `campaign.py` (outreach-engine) | CLI `instantly create --niche` |
| Resend | Transactional (single email) | Hermes webhook + backend-api | `POST /api/email/send` |
| loop.so | Nurturing (multi-step) | Hermes webhook | External API (loop.so dashboard) |

### 2. Sequence Creator is a Sidecar

`sequence_creator.py` is NOT a standalone service. It is a utility called by:
- `outreach-engine/campaign.py` — for Instantly campaign creation
- Hermes Agent — for transactional Resend sends via `POST /api/email/send`
- CLI — for manual operations

It can run as an HTTP server (`serve` mode) for webhook-triggered sends, but it has no scheduler, no DB listener, no autonomous behavior.

### 3. Instantly Campaign Flow

```
campaign.py → Sequence Creator (CLI) → Instantly API
  1. Read niche from user JSON config
  2. Resolve {niche_variables} from Supabase niche_variable table
  3. Generate A/B/C variants from COLD_EMAIL_MODEL
  4. Check if campaign already exists in Instantly (by name)
  5. If no → Create campaign with 7 steps, schedule, variants
  6. Push leads + activate
  7. Log campaign_id to DB
```

### 4. Resend is Event-Driven Only

Resend emails are NEVER sent proactively. They are always triggered by a specific event:
- `no-show` → Missed call appointment
- `call-reminder` → Upcoming call in < 2h
- `invoice` → Stripe payment processed
- `service-delivery` → Deliverable ready
- `call-description` → Post-call summary
- `information-requested` → AI responder handled inquiry

### 5. No Business Logic in Sequence Creator

`sequence_creator.py` generates email content and pushes to APIs. It does NOT:
- Decide WHEN to send (Hermes decides)
- Decide WHICH leads to push (campaign.py decides)
- Track open rates (Instantly/Resend analytics)
- Store lead state (Supabase stores)

### 6. Email Generator is Part of Outreach Engine

The `Email Generator` module (COLD_EMAIL_MODEL + niche variable resolution + A/B/C variant generation) lives in `sequence_creator.py`. It is called by `outreach-engine/campaign.py` during the campaign creation pipeline, NOT by the frontend.

### 7. Variables Conventions

| Prefix | Source | Example |
|--------|--------|---------|
| `{variable}` | Supabase `niche_variable` table | `{niche}`, `{objectif}` |
| `{{variable}}` | Lead data (resolved by tool) | `{{first_name}}`, `{{phone_number}}` |
| `{{variable}}` | Context data (passed at send time) | `{{nom_prospect}}`, `{{entreprise}}` |

## Anti-Patterns

- ❌ DO NOT add a scheduler to Sequence Creator — It's a sidecar, not an engine
- ❌ DO NOT call Sequence Creator from the frontend — Frontend calls ONLY backend-api
- ❌ DO NOT store lead state in Sequence Creator — Lead state lives in Supabase
- ❌ DO NOT add new email types without adding the corresponding node in Eraser
- ❌ DO NOT use Sequence Creator for anything other than Instantly + Resend — loop.so is external
- ❌ DO NOT hardcode niche variables in email templates — Always resolve from `niche_variable` table
