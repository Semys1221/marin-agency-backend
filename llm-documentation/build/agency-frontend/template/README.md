# Template Funnel Client

Ce dossier est le **template de base** pour le funnel vente client (Vite + React + Zustand + Shadcn). Chaque client reçoit une copie de ce dossier déployée sur Vercel.

## Organisation

```
template/
├── package.json              # Dépendances (React, Zustand, Shadcn, Stripe, etc.)
├── vite.config.ts            # Vite config + alias @/
├── tsconfig.json             # TypeScript config
├── tailwind.config.ts        # Tailwind + thème Marin (couleurs, animations)
├── postcss.config.js
├── index.html
├── src/
│   ├── main.tsx
│   ├── App.tsx               # Router, init Sentry, charge config
│   ├── config/
│   │   └── client.ts         # Configuration du client (éditer par instance)
│   ├── stores/
│   │   └── funnel.ts         # Zustand store (22 steps agency / 11 steps e-commerce)
│   ├── components/
│   │   ├── ui/               # shadcn components
│   │   ├── steps/            # Composants d'étape du funnel
│   │   └── FunnelFlow.tsx    # Contrôleur de funnel (navigation + transitions)
│   ├── lib/
│   │   ├── utils.ts          # cn() helper
│   │   └── api.ts            # Fetch wrapper + demo mode
│   ├── types/index.ts        # Types partagés
│   ├── hooks/useDemoMode.ts  # Demo mode hook
│   └── styles/globals.css    # Tailwind directives + design tokens
└── vercel.json               # Config déploiement Vercel
```

## Configurer un nouveau client

1. **Copier ce dossier :** `cp -r template clients/{tenant_id}`
2. **Éditer `src/config/client.ts` :**
   - `name` — nom du client
   - `domain` — domaine Vercel (ex: `sportpro.marin.app`)
   - `offerType` — `'agency'` (22 steps) ou `'ecommerce'` (11 steps)
   - `branding` — couleurs personnalisées
   - `tokens` — clés Stripe, Calendly, Sentry
   - `links` — URLs services externes
   - `tenantId` — identifiant unique du client
3. **Installer :** `cd clients/{tenant_id} && npm install`
4. **Développer :** `npm run dev` (démo sans backend : `VITE_DEMO_MODE=true npm run dev`)
5. **Déployer :** `vercel --prod`

## Démarrer en développement

```bash
# Mode normal (attend le backend API)
npm install
npm run dev

# Mode demo (mock data, pas besoin de backend)
VITE_DEMO_MODE=true npm run dev
```

## Ce qui change par client vs ce qui ne change jamais

| Change par client | Ne change jamais |
|------------------|-----------------|
| `config/client.ts` (branding, tokens, tenantId) | `stores/funnel.ts` (logique funnel) |
| Couleurs du thème | Composants shadcn (button, card, input) |
| URLs Calendly, Stripe, Sentry | `lib/api.ts` (fetch pattern) |
| Texte du landing (optionnel) | `types/` (modèles de données) |

## API consommées

Le frontend appelle UNIQUEMENT le **backend-api** (NodeJS/Express + Prisma). Jamais l'outreach-engine (Python) directement.

| Endpoint | Method | Usage | Backend |
|----------|--------|-------|---------|
| `/api/leads` | GET | Pipeline leads | backend-api |
| `/api/leads/status` | POST | Mise à jour statut lead | backend-api |
| `/api/campaigns/health` | GET | Statut campagnes | backend-api |
| `/api/keys/status` | GET | Clés API | backend-api |
| `/api/sequences/perf` | GET | Performance séquences | backend-api |
| `/api/crm/prospects` | GET | Prospects CRM | backend-api |
| `/api/funnel/health` | GET | Funnel speed + dead links | backend-api |
| `/api/clients/quota` | GET | Quota client | backend-api |
| `/api/clients/quota` | POST | Nouveau quota client | backend-api |
| `/api/calls/content` | GET | Scripts d'appels | backend-api |
| `/api/sentry/reports` | GET | Bug reports | backend-api |

Auth: `X-Tenant-ID` header — envoyé par `api.ts` sur chaque requête.

## Références

- `agency-front-model/marin-agency/README.md` — Spec complète funnel agency (22 steps)
- `agency-front-model/e-commerce/README.md` — Spec complète funnel e-commerce (11 steps)
- `agency-front-model/AGENTS.md` — Règles de conception
- `agency-back-model/backend-api/README.md` — Backend API (SINGLE entry point)
- `agency-back-model/infrastructure/env.variables` — Variables d'env, dont `VITE_API_BASE`
