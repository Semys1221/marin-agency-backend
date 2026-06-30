# Marin Agency Funnel

**Depends on:** `template/` (copy template before building this variant).
**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ) — every step and component must trace back to a graph node.

Frontend funnel 22 steps pour l'offre agency principale. Déploiement Vercel par client via duplication du `template/`.

## Stack

| Layer | Stack |
|-------|-------|
| Runtime | Vite 5 + React 18 + TypeScript 5 |
| State | Zustand 4 (single store until payment) |
| UI | Shadcn (Tailwind 3) |
| Forms | react-hook-form + zod |
| Animation | Framer Motion (motion blur, transitions) |
| Payments | Stripe (Elements + JS SDK) |
| E-signature | Dropbox Sign SDK |
| Scheduling | react-calendly |
| Monitoring | Sentry React |
| Hosting | Vercel (1 instance per client) |

## Packages

Voir `template/package.json` pour la liste complète. Les packages additionnels spécifiques à ce variant sont listés dans la section Stack ci-dessus.

## File Tree to Generate

Build these components inside the copied template:

```
clients/{tenant_id}/
├── src/
│   ├── config/
│   │   └── client.ts              # Éditer (branding agency, tokens Stripe/Calendly)
│   ├── components/
│   │   └── steps/
│   │       ├── Landing.tsx         # Step 1 — Multi-section landing page
│   │       ├── Qualification.tsx   # Step 2 — SIRET check (API INSEE)
│   │       ├── Calendly.tsx        # Step 3 — Booking embed
│   │       ├── Cadre.tsx           # Step 4 — Framework card
│   │       ├── Profil.tsx          # Step 5 — Company profile form
│   │       ├── Probleme.tsx        # Step 6 — Pain points checklist
│   │       ├── Objectif.tsx        # Step 7 — Sales target form
│   │       ├── Historique.tsx      # Step 8 — History questions
│   │       ├── Capacite.tsx        # Step 9 — Budget & capacity
│   │       ├── Posture.tsx         # Step 10 — Buying posture
│   │       ├── Blocage.tsx         # Step 11 — Objections
│   │       ├── Solution.tsx        # Step 12 — Solution showcase
│   │       ├── Projection.tsx      # Step 13 — Results projection
│   │       ├── Workflow.tsx        # Step 14 — Timeline
│   │       ├── InactionCost.tsx    # Step 15 — Cost of inaction
│   │       ├── Proposal.tsx        # Step 16 — Quote + interest bar
│   │       ├── Paiement.tsx        # Step 17 — Stripe payment
│   │       ├── Gift.tsx            # Step 18 — Jabra headset gift
│   │       ├── Contract.tsx        # Step 19 — Dropbox Sign
│   │       ├── Onboarding.tsx      # Step 20 — Onboarding form
│   │       ├── Call1.tsx           # Step 21 — First commercial call
│   │       └── Call2.tsx           # Step 22 — Director call
```

## Config Interface

```typescript
interface ClientConfig {
  name: string                           // Nom du client
  domain: string                         // Domaine Vercel
  offerType: 'agency'                    // Toujours 'agency'
  branding: { accent, accentDark, bg, text }
  tokens: {
    stripePublishableKey: string         // Stripe publishable key
    calendlyUrl: string                  // Lien Calendly master
    sentryDsn?: string
  }
  links: {
    microsoft?: string
    quo?: string
    looker?: string
    stripeDashboard?: string
  }
  apiBase: string                        // Backend API URL
  tenantId: string                       // Identifiant unique client
}
```

## API Endpoints (via backend-api)

Le frontend appelle UNIQUEMENT le **backend-api**. Auth: `X-Tenant-ID` header.

| Method | Path | Purpose | Dummy Data |
|--------|------|---------|------------|
| `GET` | `/api/leads` | Pipeline leads | `[{id:"lead-001", email:"demo@ex.com", status:"interested"}]` |
| `POST` | `/api/leads/status` | Update lead status | `{ok: true}` |
| `GET` | `/api/funnel/health` | Funnel speed + dead links | `{avg_step_duration_ms:23400, dropout_rate:0.32}` |
| `GET` | `/api/clients/quota` | Client quota status | `{call_count:3, objective:10}` |
| `POST` | `/api/clients/quota` | Set new client quota | `{ok: true}` |
| `GET` | `/api/keys/status` | API key health | `{stripe:"ok", gemini:"ok"}` |
| `GET` | `/api/calls/content` | Call scripts | `[{call_number:1, title:"Appel Commercial"}]` |
| `GET` | `/api/sequences/perf` | Sequence performance | `[{id:"seq-001", sent:1200, replyRate:0.02}]` |
| `GET` | `/api/crm/prospects` | CRM prospects | `[{name:"Marie", company:"Demo", status:"appointment_set"}]` |

## Dummy Data (Demo Mode)

When `VITE_DEMO_MODE=true` or `?demo=true`, every component returns mock data:

```json
// POST /api/leads/status
{ "lead_id": "lead-001", "status": "no_show", "notes": "Not called" }

// GET /api/funnel/health
{
  "avg_step_duration_ms": 23400,
  "dropout_rate": 0.32,
  "dead_links": ["/gift"],
  "total_active_sessions": 14
}
```

Steps render with hardcoded demo content from `textual-content.md` — no real API calls, no crashes.

## Funnel Steps

| # | Step | Type | Description |
|---|------|------|-------------|
| 1 | Landing | Page | Multi-section landing with hero, offers, CTA |
| 2 | Qualification | Form | SIRET input + validation (API INSEE) |
| 3 | Calendly | Embed | Calendly booking widget |
| 4 | Cadre | Info | 4 bullet points: B2B, 90j, client décide, pas de renouvellement forcé |
| 5 | Profil | Form | Secteur, ancienneté, équipe, CA |
| 6 | Problème | Checklist | 6 challenges checkbox + text optionnel |
| 7 | Objectif | Form | Objectif vente, panier moyen, date début, statut ciblage |
| 8 | Historique | Radio | Expérience agence, CRM actuel, process |
| 9 | Capacité | Select | Budget, capacité absorption, disponibilité |
| 10 | Posture | Radio | Décideur, urgence, budget approuvé |
| 11 | Blocage | Checklist | 6 objections + textarea peurs |
| 12 | Solution | Showcase | 5 features avec icônes |
| 13 | Projection | Cards | 3 metric cards + 3 reflective questions |
| 14 | Workflow | Timeline | 4 phases: Setup → Launch → Optimization → Results |
| 15 | Inaction Cost | Cards | 3 arguments: ventes perdues, retard, manque à gagner |
| 16 | Proposal | Summary | Récap besoins + offre + barre intérêt (1-10) |
| 17 | Paiement | Payment | Stripe Elements (card + SEPA) |
| 18 | Gift | Form | Jabra headset + adresse livraison |
| 19 | Contract | Embed | Dropbox Sign signature |
| 20 | Onboarding | Form | Équipe, date début, source, notes |
| 21 | Call 1 | Info | Prep screen: 30-45min, recorded, discovery |
| 22 | Call 2 | Info | Strategic alignment: 6-item agenda |

## Rules

- Single Zustand store until payment (step 17). After payment, store resets.
- Every step has loading screen + motion blur transition (Framer Motion).
- Mobile & desktop optimized.
- All text content in `textual-content.md` — never hardcode copy in components.
- Design: glassy motion blur, brand colors, Inter/Jakarta fonts.
- Demo mode must work without backend.

## Services intégrés

- **Stripe** — Paiement + facture automatique
- **Dropbox Sign** — Signature électronique des contrats
- **Calendly** — Master Calendly, tous commerciaux synchronisés
- **Sentry** — Monitoring funnel speed, dead links
- **Supabase** — Persistence des données
- **INSEE SIRET API** — Vérification SIRET avant qualification appel

## Références

- `textual-content.md` — Contenu marketing complet (headlines, forms, CTAs) pour chaque étape
- `prompt-design.md` — Prompt Google Stitch pour mockups interactifs
- `template/README.md` — Instructions duplication + déploiement
