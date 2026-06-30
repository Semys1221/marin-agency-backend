# Operations Dashboard — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=OwPrSqrZ8EHvwcDbSvex

**⚠️ Interne — Ne pas dupliquer.** Dashboard pour l'équipe Marin uniquement. Un seul déploiement. `tenant_id` fixe = `marin`.

## Purpose
Dashboard opérationnel de l'Outreach Engine. Vue pipeline leads froids, santé campagnes, alertes clés API, monitoring scraping, contrôle manuel. Page HTML statique — pas de framework.

Ne montre que les données **Phase 1** (outreach). Les données Phase 2 (funnel, CRM, calls) sont dans le dashboard client (`marin-dashboard`).

## Dependencies
- `agency-backend` deployed (endpoints outreach-engine + backend-api)
- `outreach-engine/07-instantly-campaign.md` (campaign health)

## Stack
| Layer | Stack |
|-------|-------|
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Icons | Lucide (via CDN) |
| Styling | Tailwind CDN ou CSS custom |
| Hosting | Vercel (static deploy) |

## Env Vars
```
VITE_API_BASE_URL=https://marin-backend.onrender.com/api
VITE_TENANT_ID=marin
VITE_WORKER_API_KEY=...
```

## API Endpoints Consumed

| Method | Path | Section |
|--------|------|---------|
| GET | `/api/dashboard?tenant_id=marin` | Aggrégé (leads, campaigns, keys, renewals, sequences, reports) |
| POST | `/api/leads/status` | Pipeline — double tap |
| POST | `/api/campaigns/stop` | Contrôle — stop campaign |
| POST | `/api/clients/quota` | Contrôle — nouveau client |

**Données utilisées du endpoint aggrégé :** `leads`, `campaigns`, `keys`, `renewals`, `sequences`, `reports`.
**Données ignorées :** `scripts`, `prospects`, `funnel`, `services` (réservés au dashboard client).

## Page Structure
```
┌──────────────────────────────────────────────┐
│  HEADER : "Operations — Marin"               │
│  [Dernière màj : il y a X min] [↻ Rafraîchir]│
├──────────────────────────────────────────────┤
│  SECTION 1 — Alertes Critiques               │
│  (dead keys Outscraper/Gemini, <2% reply)    │
├──────────────────────────────────────────────┤
│  SECTION 2 — Pipeline Leads                   │
│  (leads froids + cleaned, filtres, doubltap) │
├──────────────────────────────────────────────┤
│  SECTION 3 — Campagnes                        │
│  (santé, reply rate, exhausted, stop button) │
├──────────────────────────────────────────────┤
│  SECTION 4 — Monitoring                       │
│  (perf séquences, renouvellements emails)     │
├──────────────────────────────────────────────┤
│  SECTION 5 — Contrôle                         │
│  (stop campaign, new client quota)            │
├──────────────────────────────────────────────┤
│  SECTION 6 — Bugs Sentry                      │
│  (dernières erreurs scraping/campaign)        │
└──────────────────────────────────────────────┘
```

## Rules
1. **Single instance** — Pas de multi-tenant. `tenant_id` fixe = `'marin'`
2. **Auth** — header `X-Tenant-ID: marin` + `Authorization: Bearer {VITE_WORKER_API_KEY}`
3. **Polling** — `setInterval(fetchAll, 30000)` + bouton rafraîchir manuel
4. **Demo mode** — si `VITE_DEMO_MODE=true`, données mockées sans appels API
5. **Loading/error** — chaque section gère son état. Si API down → `⏳ Données non disponibles`

## Files to Generate
```
/
├── index.html              # Page unique HTML
├── css/style.css           # Styles
├── js/
│   ├── config.js           # Env vars + demo flag
│   ├── fetcher.js          # Fetch wrapper + demo mode
│   └── app.js              # Init polling + load sections
└── config/
    └── demo.js             # Mock data outreach only
```

## Edge Cases
- Backend API down → `⏳ Données non disponibles` par section, jamais de crash
- Demo mode → données mockées, zéro appel API
- Tous les fetch incluent `X-Tenant-ID: marin` + `Authorization: Bearer {WORKER_API_KEY}`
