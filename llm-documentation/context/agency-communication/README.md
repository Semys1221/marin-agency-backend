# Marin — Communication (Triple Architecture + Engine Integration)

Trois systèmes distincts orchestrés par Hermes Agent, avec le Sequence Creator comme sidecar.

## Architecture

```
Outreach Engine (Phase 1)               Frontend Engine (Phase 2)
┌────────────────────────────┐         ┌────────────────────────────┐
│  Brain/Gemini → Scraper    │         │  Landing → Calendly →     │
│  → Clean → Campaign        │         │  Detective → Call → CRM   │
│       │                    │         │       │                   │
│       ▼                    │         │       ▼                   │
│  Email Generator           │         │  Sequence Creator         │
│  → Sequence Creator        │         │  (Resend only)            │
│  → Instantly campaign      │         │                           │
└────────────────────────────┘         └────────────────────────────┘
                                               │
                                               ▼
                                        loop.so (Nurturing)
                                        webhook-triggered
```

## Structure

```
├── AGENTS.md                    ← Rules, gates, anti-patterns (lire en premier)
├── README.md                    ← Ce fichier
├── hermes-api-contract.md       ← Contrat Hermes → Sequence Creator
├── resend-events.md             ← Événements déclencheurs Resend
├── loop-integration.md          ← Webhooks loop.so
├── email-generator.md           ← Module Email Generator (COLD_EMAIL_MODEL)
├── generator-engin/             ← Moteur de génération + envoi
│   ├── README.md
│   ├── sequence_creator.py      ← CLI + API (Instantly + Resend)
│   └── index.html               ← Dashboard HTML
├── sequence-live/               ← Séquences prêtes à l'emploi
│   ├── README.md
│   ├── instantly/               ← 1 campagne cold (7-step A/B/C, .md + .json)
│   ├── resend/                  ← 6 emails transactionnels (.md + .json)
│   └── loop/                    ← 4 séquences nurturing (.md + .json)
├── sequences-model/             ← Specs templates originaux
└── ticket-system/               ← Système de tickets support
```

## CLI Usage

```bash
# Instantly — Cold Outreach
python generator-engin/sequence_creator.py instantly create --niche "kinésithérapeute" --activate
python generator-engin/sequence_creator.py instantly list

# Resend — Transactionnel (6 types)
python generator-engin/sequence_creator.py resend send --type call-reminder --to client@email.com
python generator-engin/sequence_creator.py resend list
python generator-engin/sequence_creator.py resend render --type no-show

# API server (pour webhooks Hermes → Resend)
python generator-engin/sequence_creator.py serve --port 8002
# POST /api/email/send  {"type": "no-show", "to": "...", "vars": {...}}
```

## Flux global

```
                      Hermes Agent
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
    Instantly (Cold)  Resend (Tx)   loop.so (Nurture)
    1 séquence        6 séquences   4 séquences
    7-step A/B/C      single email  multi-step
    campaign push     event-driven  webhook triggers
    (via campaign.py)  (POST /api/email/send)
```
