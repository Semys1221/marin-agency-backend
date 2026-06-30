# Template Dashboard Client

Ce dossier est le **template de base** pour le dashboard client statique. Chaque client reçoit une copie de ce dossier déployée sur Vercel.

## Organisation

```
template/
├── index.html           # Dashboard statique (self-contained)
├── config/client.js     # Configuration du client
└── vercel.json          # Config déploiement Vercel
```

## Comment ça marche

`index.html` est une page HTML unique qui :

1. **Charge `config/client.js`** — branding, liens, tokens
2. **Affiche les liens externes** — Microsoft, Quo, Looker, Calendly, Stripe
3. **Fetch `GET /api/dashboard?tenant_id=X`** — 1 endpoint aggrégé (leads, campagnes, clés, séquences, CRM)
4. **Permet le "double tap"** — mise à jour statut lead (no-show / indécis / vendu)

Les données sont rafraîchies toutes les 30 secondes automatiquement.

## Configurer un nouveau client

1. Copier ce dossier : `cp -r template clients/nouveau-client`
2. Modifier `config/client.js` :
   - `name` — nom du client
   - `domain` — domaine du client
   - `links` — URLs des services (Microsoft, Quo, Looker, Stripe)
   - `tokens.calendlyUrl` — lien Calendly du client
   - `branding` — couleurs personnalisées
3. Déployer : `cd clients/nouveau-client && vercel --prod`

## Références

- `agency-frontend/dashboard/marin-dashboard/README.md` — Spec complète dashboard Marin
- `agency-frontend/dashboard/ecommerce-dashboard/README.md` — Spec complète dashboard e-commerce
- `agency-frontend/dashboard/AGENTS.md` — Règles de conception dashboard
- `agency-backend/frontend-engine/16-dashboard-api.md` — Endpoint API aggrégé
- `agency-backend/outreach-engine/12-operations-dashboard.md` — Dashboard opérations (équipe)
