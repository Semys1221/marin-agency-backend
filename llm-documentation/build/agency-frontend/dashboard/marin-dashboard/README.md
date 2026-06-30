# Dashboard Client — Marin Agency

> **⚠️ Prérequis :** Ce dashboard nécessite le backend NodeJS/Prisma déployé avec les 12 endpoints API.  
> Sans backend, tout affiche "Erreur". Utiliser `DEMO_MODE=true` pour le développement (voir section Dummy Data).  
> Les services externes (Microsoft, Quo, Calendly, Stripe, Looker) doivent être configurés pour le client AVANT que les liens fonctionnent.

Page HTML statique déployée sur Vercel pour chaque client Marin Agency. Point d'entrée unique après onboarding.

**Principe :** Tous les services sont déjà configurés. Le dashboard ne fait que lier + fetch.

## Architecture

```
                    ┌──────────────────────┐
                    │   Dashboard HTML      │
                    │  (static endpoint)    │
                    └──────┬───────┬───────┘
                           │       │
              ┌────────────┘       └────────────┐
              ▼                                   ▼
   ┌────────────────────┐              ┌────────────────────┐
   │ Links externes     │              │ API Backend        │
   │ (redirects)        │              │ (NodeJS + Prisma)  │
   │                    │              │                    │
   │ • Microsoft        │              │ • /api/leads       │
   │ • Quo.com          │              │ • /api/campaigns   │
   │ • Looker Studio    │              │ • /api/keys        │
   │ • Calendly         │              │ • /api/sequences   │
   │ • Stripe           │              │ • /api/calls       │
   └────────────────────┘              │ • /api/crm         │
                                        │ • /api/clients     │
                                        │ • /api/funnel      │
                                        └─────────┬──────────┘
                                                   │
                                                   ▼
                                         ┌────────────────────┐
                                         │   Supabase DB      │
                                         │   + Sentry         │
                                         └────────────────────┘
```

---

## Instructions pour le LLM

Tu es un développeur fullstack. Génère le code complet du **dashboard client Marin Agency** — une page HTML statique (pas React/Shadcn) déployée sur Vercel comme point d'entrée unique pour un client post-onboarding.

### Contraintes techniques

- **Stack :** HTML statique + CSS Tailwind (via CDN) + JS vanilla
- **Pas de framework :** Pas de React, pas de Shadcn, pas de routing
- **Déploiement :** 1 instance Vercel par client. Template dupliqué, config client gelée à la build.
- **Backend API :** NodeJS + Prisma sur Render (endpoints listés ci-dessous)
- **Services externes :** Simples liens (`<a href="..." target="_blank">`) — déjà configurés pour le client
- **Écriture API :** Seulement `POST /api/leads/status`. Le reste est lecture seule.
- **1 seule page :** Tout est sur une page. Pas de navigation interne.

---

## 1. Configuration Client (config.ts)

```typescript
export interface ClientConfig {
  name: string                                        // tenant_id dans la DB
  domain: string                                      // {client}.marin.app
  branding: {
    accent: string                                    // #49C5B6 (défaut)
    accentDark: string                                // #015048 (défaut)
    bg: string                                        // #FAFAFA (défaut)
    text: string                                      // #000000 (défaut)
    logo?: string                                     // URL logo client
  }
  tokens: {
    stripePublishableKey: string                      // pk_live_... (Stripe.js)
    calendlyUrl: string                               // https://calendly.com/{client}
  }
  funnel: {
    steps: string[]                                   // 22 étapes du funnel agency
  }
  links: {
    microsoft?: string                                // https://account.microsoft.com
    quo?: string                                      // https://quo.com
    looker?: string                                   // https://lookerstudio.google.com/embed/reporting/{ID}
    stripeDashboard?: string                          // https://dashboard.stripe.com
  }
}
```

## 2. Configuration Runtime (config/client.js)

Pas de Vite, pas de build step. Les variables sont chargées depuis `config/client.js` au runtime :

```javascript
// config/client.js (exemple pour le client "modemaison")
var ClientConfig = {
  name: 'ModeMaison',
  domain: 'modemaison.marin.app',
  apiBase: '/api',
  tenantId: 'modemaison',
  sentryDsn: 'https://...@...ingest.sentry.io/...',
  branding: {
    accent: '#49C5B6',
    accentDark: '#015048',
    bg: '#FAFAFA',
    text: '#000000',
  },
  tokens: {
    calendlyUrl: 'https://calendly.com/modemaison',
  },
  links: {
    microsoft: 'https://account.microsoft.com',
    quo: 'https://quo.com',
    looker: 'https://lookerstudio.google.com/embed/reporting/{ID}',
    stripeDashboard: 'https://dashboard.stripe.com',
  },
}
```

Chaque appel API envoie le header : `X-Tenant-ID: {ClientConfig.tenantId}`.

> **Auth :** `tenantId` est défini dans `config/client.js` — changé par client.  
> Le tenant est déterminé par le domaine client : `{client}.marin.app` → `tenantId={client}`.  
> Pas de login, pas de cookie. Le header seul isole les données par tenant côté backend (RLS Supabase).

> **⚠️ L'API backend n'existe pas encore.** Tous les fetch doivent gérer l'état indisponible (afficher "⏳ Données non disponibles" au lieu d'une erreur rouge). Voir section **Dummy Data**.

## 3. API Endpoints (JS Vanilla Fetch)

### GET /api/leads
```
Réponse : {
  leads: [{
    id: string, email: string, company_name: string,
    first_name?: string, last_name?: string,
    phone?: string, status: "new"|"contacted"|"qualified",
    created_at: string
  }]
}
```
Rendu : Tableau leads actifs. 2 onglets "Contactés" / "Pas contactés". Ligne = nom, entreprise, email, téléphone, statut.

### POST /api/leads/status
```
Body : { lead_id: string, status: "no_show"|"indecis"|"closed" }
Réponse : { success: true }
```
Rendu : 3 boutons par ligne lead. Confirmation JS avant envoi.

### GET /api/campaigns/health
```
Réponse : { campaigns: [{ id, name, status, reply_rate, is_exhausted }] }
```
Rendu : Cartes campagnes. Badge orange si reply_rate < 2%. Badge rouge si is_exhausted.

### GET /api/keys/status
```
Réponse : { keys: { outscraper: "ok"|"dead", gemini: "ok"|"dead" } }
```
Rendu : 2 indicateurs couleur. Vert = OK, Rouge = Dead.

### GET /api/emails/renewal
```
Réponse : { renewals: [{ email, service, expires_at, days_remaining }] }
```
Rendu : Tableau avec compteur jours restants. Alerte si < 7 jours.

### GET /api/sequences/perf
```
Réponse : { sequences: [{ id, name, sent, opened, open_rate, replied, reply_rate }] }
```
Rendu : Tableau + barres de progression visuelles.

### GET /api/calls/content
```
Réponse : { scripts: [{ call_number, title, content }] }
```
Rendu : Accordéon cliquable par numéro d'appel.

### GET /api/crm/prospects
```
Réponse : { prospects: [{ id, email, company_name, last_contacted, status }] }
```
Rendu : Tableau prospects. Indicateur email envoyé.

### GET /api/funnel/health
```
Réponse : { funnel_speed: number, dead_links: string[] }
```
Rendu : Section monitoring : vitesse en ms. Si dead links → liste rouge.

### GET /api/sentry/reports
```
Query : ?limit=10&since=7d
Réponse : { reports: [{ message, level, url, timestamp }] }
```
Rendu : Section bugs : 10 dernières entrées. Niveau coloré.

## 4. Services Externes (Liens)

| Service | Lien (depuis config.ts) | Label |
|---------|------------------------|-------|
| Microsoft | `links.microsoft` | Compte Microsoft |
| Quo.com | `links.quo` | Suivi Coaching |
| Looker Studio | `links.looker` | KPIs & Reporting |
| Calendly | `tokens.calendlyUrl` | Prendre RDV |
| Stripe | `links.stripeDashboard` | Dashboard Paiements |

Rendu : Grille de cartes avec icônes. Chaque carte = lien target="_blank".

## 5. Fonctionnalités

- Stop sending on booking
- Emails needs renewal
- Looker Studio embeds
- Niche campaign exhausted → needs new scraping
- Active leads list (contacted / not contacted)
- CRM prospect sends an email
- Lead status update ("double tap") : no-show / indecis / closed
- Calls content : upsell, course, etc.
- Redirect Calendly
- Outscraper key dead / Gemini key dead alerts
- New client → quota + 90-day objective update
- Funnel speed + dead links (Sentry bug reports)
- Stop campaign below 2% reply rate
- Lead intelligence sheet for call
- Email sequence performance & open rates
- Gmail sending to CRM prospect email (open rate)

## 6. Structure de la Page

```
┌──────────────────────────────────────────────┐
│  HEADER : Logo + "{config.name}"             │
│  [Dernier rafraîchissement : date]           │
│  [Bouton ↻ Rafraîchir]                       │
├──────────────────────────────────────────────┤
│  SECTION 1 — Alertes                         │
│  (clés API, campagnes épuisées, reply rate)  │
├──────────────────────────────────────────────┤
│  SECTION 2 — Leads Actifs                    │
│  (tableau filtrable par statut + double tap) │
├──────────────────────────────────────────────┤
│  SECTION 3 — Campagnes & Séquences           │
│  (santé + performances)                      │
├──────────────────────────────────────────────┤
│  SECTION 4 — Appels & Scripts                │
│  (accordéon scripts)                         │
├──────────────────────────────────────────────┤
│  SECTION 5 — Services & Liens                │
│  (grille Microsoft, Quo, Calendly, Stripe)   │
├──────────────────────────────────────────────┤
│  SECTION 6 — Funnel & Monitoring             │
│  (funnel speed, dead links)                  │
├──────────────────────────────────────────────┤
│  SECTION 7 — Looker Studio                   │
│  (iframe embed)                              │
├──────────────────────────────────────────────┤
│  FOOTER : Bugs Sentry + Support              │
└──────────────────────────────────────────────┘
```

## 7. Règles Architecture

1. **Statique :** `index.html` unique. CSS Tailwind CDN `<script src="https://cdn.tailwindcss.com">`. JS vanilla.
2. **Pas de build step :** HTML/CSS/JS simples. Tailwind via CDN pour le style.
3. **Pas de React :** Aucun import React. Aucun JSX. Aucun bundler.
4. **Palette :** Utiliser les couleurs du `config.branding` : accent="#49C5B6", accentDark="#015048", bg="#FAFAFA", text="#000000".
5. **Multi-instance :** Le répertoire est dupliqué. Modifier `config.ts` + déployer sur Vercel.
6. **Looker Studio :** Iframe embed direct dans la section dédiée. Pas de clé API.
7. **Responsive :** Tailwind responsive classes. Grille 2 colonnes desktop, 1 colonne mobile.
8. **Polling :** Rafraîchir les données toutes les 30s (ou manuellement via bouton).

## 8. Dummy Data (Développement sans Backend)

Pour rendre le dashboard testable sans backend, ajoute un mode dummy :

```javascript
// config/demo.js
const DEMO = typeof DEMO_MODE !== 'undefined' && DEMO_MODE === 'true'

const DEMO_DATA = {
  leads: [
    { id: '1', email: 'paul@example.com', company_name: 'SportPro', status: 'new', created_at: '2025-06-01' },
    { id: '2', email: 'marie@example.com', company_name: 'ModeMaison', status: 'contacted', created_at: '2025-05-28' },
  ],
  campaigns: [
    { id: '1', name: 'Sport Niche 1', status: 'active', reply_rate: 3.2, is_exhausted: false },
    { id: '2', name: 'Mode Niche 2', status: 'exhausted', reply_rate: 0.8, is_exhausted: true },
  ],
  keys: { outscraper: 'ok', gemini: 'dead' },
  renewals: [
    { email: 'contact@sportpro.fr', service: 'Microsoft', expires_at: '2025-07-01', days_remaining: 2 },
  ],
  sequences: [
    { id: '1', name: 'Cold Outreach', sent: 120, opened: 45, open_rate: 37.5, replied: 8, reply_rate: 6.7 },
  ],
  scripts: [
    { call_number: 1, title: 'Appel Découverte', content: '# Appel 1\nPrésentation...' },
  ],
  prospects: [
    { id: '1', email: 'jean@example.com', company_name: 'ClientX', last_contacted: '2025-06-10', status: 'contacted' },
  ],
  funnel: { funnel_speed: 1200, dead_links: ['/broken-page'] },
  reports: [
    { id: '1', message: 'TypeError: cannot read prop', level: 'error', url: '/checkout', timestamp: '2025-06-29' },
  ],
}

function getDemoData(path) {
  const key = path.split('/').pop()
  return DEMO_DATA[key] || []
}
```

Usage : le mode demo s'active via `?demo=true` dans l'URL (vérifié dans `app.js` au démarrage). En mode demo, les fetchs retournent `getDemoData(path)` au lieu d'appeler l'API.

## 9. Fichiers à Générer

```
dashboard/
├── index.html                     # Page principale unique
├── config/
│   └── client.ts                  # Config client (changé par instance)
├── js/
│   ├── api.js                     # Fonctions fetch pour chaque endpoint
│   ├── render.js                  # Fonctions de rendu DOM pour chaque section
│   └── app.js                     # Initialisation, polling, event handlers
├── css/
│   └── style.css                  # Surcouches CSS mineures (si besoin)
└── vercel.json                    # Config déploiement Vercel (static SPA fallback)

Exemple `vercel.json` :
```json
{
  "overrides": [
    { "source": "/config/(.*)", "headers": [{"key": "Cache-Control", "value": "no-cache"}]}
  ]
}
```
```

## Notes sur les Features "Backend-dépendantes"

Certaines features listées nécessitent des endpoints ou des données qui ne sont pas encore spécifiés précisément :
- **"Stop sending on booking"** — suppose un webhook Calendly qui met à jour le lead. Pas dans les endpoints actuels.
- **"Emails needs renewal"** — utilise `GET /api/emails/renewal` mais la source des abonnements email n'est pas définie.
- **"Gmail sending to CRM prospect email"** — nécessite une intégration Gmail API côté backend.

Ces features sont documentées comme cible. En l'absence du backend, le dashboard peut afficher des sections vides avec le message "Fonctionnalité à venir".

## Multi-instance

Le dashboard fait partie du template dupliqué par client. Voir `../../template/README.md`.

```
Template/
├── index.html              # Dashboard statique (self-contained)
├── config/client.js        # Config client (branding, tokens, liens)
└── vercel.json
```

Chaque client = copie du template + `config/client.js` modifié + déploiement Vercel.

## Références

- `../template/` — Template de base pour duplication
- `../AGENTS.md` — Règles de conception dashboard
- `../../agency-back-model/eraser/model-dashboard.md` — Modèle Eraser.io
- `../../agency-documentation/duplication.md` — Process de duplication
