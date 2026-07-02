# Build — Marin Agency

Dossier de travail pour les agents LLM. Contient les specs prêtes à builder, organisées par module.

## Source of Truth

Le diagramme Eraser.io (`model-marin-agency`) est la source de vérité unique.
**Référence :** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

Si un composant n'est pas dans le graphe, ne pas le builder. Si tu as besoin de quelque chose de nouveau, mets à jour le graphe d'abord.

## Build Order

Toujours builder dans cet ordre — un module à la fois, un fichier à la fois.

```
1. agency-backend/outreach-engine/     ← Phase 1 : Python/FastAPI (fichiers 01 à 12)
2. agency-backend/frontend-engine/     ← Phase 2 : NodeJS/Express + Frontend (fichiers 01 à 16)
3. agency-frontend/                    ← Funnels + dashboards clients
```

## Structure

| Chemin | Contenu |
|--------|---------|
| `agency-backend/outreach-engine/` | 12 fichiers numérotés — Outreach Engine (scraping, cleaning, campaigns, hermes, slack) |
| `agency-backend/frontend-engine/` | 16 fichiers numérotés — Frontend Engine (funnel, calls, paiement, CRM, dashboard, ticket system) |
| `agency-backend/ERASER.MD` | Diagramme complet du backend |
| `agency-frontend/` | Funnels (22 steps + 11 steps) + dashboards clients HTML |

## How to Build

1. Lire [METHOD.md](./METHOD.md) — le cycle Pre-Build → Build → Verify → Gate
2. Lire [AGENTS.md](./AGENTS.md) — les GATES spécifiques au module
3. Choisir un module phase (ex: `agency-backend/outreach-engine/`)
4. Builder chaque fichier numéroté dans l'ordre (`01`, `02`, … `12`)
5. 1 session AI = 1 fichier — ne jamais builder tout d'un coup

## Tool Protocol (résumé)

**L'Agent utilise ces outils sans demander :** `git`, `gh`, `supabase`, `vercel`, `render`, `stripe`, `shopify`, `curl`, `jq`, `psql`, `docker`, `npm`, `pip`, `pnpm`.

**L'Agent DOIT demander au Human pour :**
- **ngrok** — avant chaque test de webhook (Stripe, Calendly, Dropbox Sign)
- **Bruno** — si un test `curl` échoue ou que le résultat est ambigu
- **Docker Desktop** — avant la première commande `docker` de la session

Voir [METHOD.md §7](./METHOD.md) pour le protocole complet (MCPs, phases du cycle BVG, etc.).
