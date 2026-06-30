# Agency Dashboard Model

Modèles et specs pour les dashboards clients du projet Marin. Pages HTML statiques déployées sur Vercel.

Les dashboards sont dans `agency-frontend/dashboard/` — ils font partie du module frontend.
Le dashboard opérations (équipe) est dans `agency-backend/outreach-engine/12-operations-dashboard.md`.

## Contenu

| Chemin | Description |
|--------|-------------|
| `AGENTS.md` | Règles de conception : simple, efficace, minimal backend |
| `marin-dashboard/README.md` | Dashboard client Marin Agency — page HTML statique, liens + API |
| `ecommerce-dashboard/README.md` | Dashboard client E-commerce — page HTML statique, liens + Shopify |
| `template/` | Template de base pour duplication client (index.html + config) |

## Principe

Pas de framework lourd. Le dashboard est une page HTML statique qui :
- Redirige vers les services externes (Microsoft, Quo, Calendly, Stripe, Shopify)
- Fetch les données depuis `GET /api/dashboard?tenant_id=X` (1 seul endpoint aggrégé)
- Sert de point d'entrée unique pour le client après onboarding

## Références

- `agency-backend/frontend-engine/16-dashboard-api.md` — Endpoint API aggrégé
- `agency-backend/outreach-engine/12-operations-dashboard.md` — Dashboard opérations (équipe)
- `agency-backend/frontend-engine/11-client-dashboard.md` — Spec conceptuelle dashboard client
