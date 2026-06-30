# Dashboard Client — E-commerce (Grossiste)

> **⚠️ Prérequis :** Ce dashboard nécessite le backend NodeJS/Prisma déployé avec les 12 endpoints API.  
> Sans backend, tout affiche "Erreur". Utiliser `DEMO_MODE=true` pour le développement (voir section Dummy Data).  
> Les services externes (Shopify, Microsoft, Quo, Calendly, Stripe, Looker) doivent être configurés pour le client AVANT que les liens fonctionnent.

Page HTML statique déployée sur Vercel pour chaque client e-commerce (grossiste). Point d'entrée après onboarding.

**Principe :** Même approche que le dashboard Marin Agency, mais le paiement et le tracking sont gérés par Shopify. Le dashboard redirige vers Shopify pour le suivi de commande.

## Architecture

```
                    ┌──────────────────────────┐
                    │   Dashboard HTML          │
                    │  (static endpoint)        │
                    └──────┬──────────┬────────┘
                           │          │
              ┌────────────┘          └────────────┐
              ▼                                      ▼
   ┌────────────────────┐              ┌────────────────────┐
   │ Links externes     │              │ API Backend        │
   │ (redirects)        │              │ (NodeJS + Prisma)  │
   │                    │              │                    │
   │ • Microsoft        │              │ • /api/leads       │
   │ • Quo.com          │              │ • /api/campaigns   │
   │ • Looker Studio    │              │ • /api/keys        │
   │ • Calendly         │              │ • /api/sequences   │
   │ • Shopify admin    │              │ • /api/calls       │
   │ • Shopify tracking │              │ • /api/crm         │
   └────────────────────┘              │ • /api/clients     │
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

Tu es un développeur fullstack. Génère le code complet du **dashboard client E-commerce (Grossiste)** — une page HTML statique déployée sur Vercel comme point d'entrée unique pour un client grossiste post-onboarding. Même approche que le dashboard Marin Agency, mais adapté à Shopify (paiement et tracking).

### Contraintes techniques

- **Stack :** HTML statique + CSS Tailwind (via CDN) + JS vanilla
- **Pas de framework :** Pas de React, pas de Shadcn, pas de routing
- **Déploiement :** 1 instance Vercel par client. Template dupliqué, config client gelée à la build.
- **Backend API :** NodeJS + Prisma sur Render (mêmes endpoints que Marin Agency)
- **Paiement :** Shopify Checkout (redirection, pas de Stripe intégré)
- **Tracking :** Shopify Dashboard (redirection, pas de tracking interne)
- **Services externes :** Simples liens — déjà configurés pour le client
- **Écriture API :** Seulement `POST /api/leads/status`
- **1 seule page :** Tout est sur une page. Pas de navigation interne.

---

## 1. Configuration Client (config.ts)

```typescript
export interface ClientConfig {
  name: string                                        // tenant_id dans la DB
  domain: string                                      // {client}.marin.app
  branding: {
    accent: string                                    // #49C5B6
    accentDark: string                                // #015048
    bg: string                                        // #FAFAFA
    text: string                                      // #000000
    logo?: string
  }
  tokens: {
    calendlyUrl: string                               // https://calendly.com/{client}
  }
  funnel: {
    steps: string[]                                   // 11 étapes du funnel e-commerce
  }
  links: {
    microsoft?: string                                // https://account.microsoft.com
    quo?: string                                      // https://quo.com
    looker?: string                                   // https://lookerstudio.google.com/embed/reporting/{ID}
    stripeDashboard?: string                          // https://dashboard.stripe.com
  }
  shopify: {                                          // Spécifique e-commerce
    storeDomain: string                               // https://{client}.myshopify.com
    adminPath: string                                 // /admin
    trackingPath: string                              // /account ou /orders
  }
}
```

## 2. Configuration Runtime (config/client.js)

Pas de Vite, pas de build step. Les variables sont chargées depuis `config/client.js` au runtime :

```javascript
// config/client.js (exemple pour le client "sportpro")
var ClientConfig = {
  name: 'SportPro',
  domain: 'sportpro.marin.app',
  apiBase: '/api',
  tenantId: 'sportpro',
  sentryDsn: 'https://...@...ingest.sentry.io/...',
  branding: {
    accent: '#49C5B6',
    accentDark: '#015048',
    bg: '#FAFAFA',
    text: '#000000',
  },
  tokens: {
    calendlyUrl: 'https://calendly.com/sportpro',
  },
  links: {
    microsoft: 'https://account.microsoft.com',
    quo: 'https://quo.com',
    looker: 'https://lookerstudio.google.com/embed/reporting/{ID}',
    stripeDashboard: 'https://dashboard.stripe.com',
  },
  shopify: {
    storeDomain: 'https://sportpro.myshopify.com',
    adminPath: '/admin',
    trackingPath: '/account',
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
Réponse : { leads: [{ id, email, company_name, first_name?, last_name?, phone?, status, created_at }] }
```
Rendu : Tableau leads. 2 onglets "Contactés" / "Pas contactés". Actions "Double tap".

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
Rendu : Accordéon cliquable par numéro d'appel. Contenu en lecture seule.

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
| **Shopify Admin** | `shopify.storeDomain + shopify.adminPath` | Administration Boutique |
| **Shopify Store** | `shopify.storeDomain` | Voir la Boutique |
| **Suivi Commande** | `shopify.storeDomain + '/account'` | Suivi Commandes |

## 5. Spécificités E-commerce vs Agence

| Fonctionnalité | E-commerce | Agency |
|---------------|------------|--------|
| **Paiement** | Shopify Checkout (lien externe) | Stripe (intégré) |
| **Tracking commande** | Dashboard Shopify (lien externe) | Dashboard Marin |
| **Contrat** | Pas de contrat | Dropbox Sign |
| **Cadeau** | Pas de cadeau | Casque Jabra |
| **Onboarding** | Pas d'onboarding long | Formulaire intégré |
| **Suivi 90 jours** | Oui (plan fait/reste à faire) | Oui |
| **Planification appels** | Oui | Oui |
| **KPIs globaux** | Instantly + Site + Calendly | Instantly + Site + Calendly |

> **Note Shopify Token :** `VITE_SHOPIFY_STOREFRONT_TOKEN` et `VITE_SHOPIFY_STORE_DOMAIN` sont listés dans les env vars mais **ne sont pas utilisés** par le dashboard actuel (Shopify = liens externes uniquement). Ils sont conservés pour une future feature Storefront API (affichage catalogue / commandes dans le dashboard). En attendant, les ignorer.

### Suivi du Plan 90 Jours
Section spécifique avec :
- Progression : "Jour X / 90"
- Liste des étapes accomplies / restantes
- Prochain appel programmé (date + heure)
- Métriques clés : objectif ventes, panier moyen, progression

### Opportunités Upsell
Section liste des opportunités d'upsell proposées au client avec statut (accepté/en attente/refusé).

### Filtrage Questions RDV
Afficher les questions de filtrage posées lors du rendez-vous découverte pour contextualiser l'accompagnement.

## 6. Fonctionnalités

### Communes avec l'agence
- Stop sending on booking
- Emails needs renewal
- Looker Studio embeds
- Niche campaign exhausted → needs new scraping
- Active leads list (contacted / not contacted)
- CRM prospect sends an email
- Lead status update ("double tap")
- Calls content : upsell, course, etc.
- Redirect Calendly
- Outscraper key dead / Gemini key dead alerts
- New client → quota + 90-day objective update
- Funnel speed + dead links (Sentry bug reports)
- Stop campaign below 2% reply rate
- Lead intelligence sheet for call
- Email sequence performance & open rates
- Gmail sending to CRM prospect email (open rate)

### Spécifiques e-commerce
- 90-day plan tracking (fait / reste à faire)
- Call planning
- Microsoft & Quo.com access
- Headset tracking (Jabra)
- Stripe dashboard link
- Looker Studio embeds
- CRM spreadsheet rendez-vous (contester / pas présent)
- Filter questions asked at RDV
- Call scripts
- Upsell opportunities list
- Global KPIs (Instantly, Website, Calendly)
- Redirection Shopify Checkout
- Tracking Shopify

## 7. Structure de la Page

```
┌──────────────────────────────────────────────┐
│  HEADER : Logo + "{config.name}"             │
│  [Dernier rafraîchissement] [↻ Rafraîchir]   │
├──────────────────────────────────────────────┤
│  SECTION 1 — Plan 90 Jours                   │
│  (barre progression, étapes, prochain appel) │
├──────────────────────────────────────────────┤
│  SECTION 2 — Alertes                         │
│  (clés API, campagnes, reply rate)           │
├──────────────────────────────────────────────┤
│  SECTION 3 — Leads & CRM                     │
│  (tableau leads + double tap)                │
├──────────────────────────────────────────────┤
│  SECTION 4 — Commandes & Shopify             │
│  (liens admin boutique, suivi commandes)     │
├──────────────────────────────────────────────┤
│  SECTION 5 — Appels & Scripts                │
│  (accordéon scripts + upsells)               │
├──────────────────────────────────────────────┤
│  SECTION 6 — Séquences Email                 │
│  (performances + open rates)                 │
├──────────────────────────────────────────────┤
│  SECTION 7 — Services & Liens                │
│  (grille Microsoft, Quo, Calendly, Stripe)   │
├──────────────────────────────────────────────┤
│  SECTION 8 — KPIs & Reporting                │
│  (iframe Looker Studio)                      │
├──────────────────────────────────────────────┤
│  FOOTER : Bugs Sentry + Support              │
└──────────────────────────────────────────────┘
```

## 8. Règles Architecture

1. **Statique :** `index.html` unique. CSS Tailwind CDN. JS vanilla.
2. **Pas de build step :** HTML/CSS/JS simples. Tailwind via CDN.
3. **Pas de React :** Aucun import React. Aucun JSX. Aucun bundler.
4. **Palette :** Utiliser les couleurs du `config.branding`.
5. **Multi-instance :** Répertoire dupliqué. Modifier `config.ts` + déploiement Vercel.
6. **Shopify = lien externe :** Le dashboard ne fait que rediriger vers Shopify Admin / Store / Orders. Pas d'API Shopify côté dashboard.
7. **Responsive :** Tailwind grid. 2 colonnes desktop, 1 colonne mobile.
8. **Polling :** Rafraîchir les données toutes les 30s (ou manuellement).

## 9. Dummy Data (Développement sans Backend)

Ajoute un mode dummy identique au dashboard Marin Agency pour le développement :

```javascript
// config/demo.js
const DEMO = typeof DEMO_MODE !== 'undefined' && DEMO_MODE === 'true'

const DEMO_DATA = {
  leads: [
    { id: '1', email: 'paul@example.com', company_name: 'SportPro', status: 'new', created_at: '2025-06-01' },
  ],
  campaigns: [
    { id: '1', name: 'Sport Niche 1', status: 'exhausted', reply_rate: 0.8, is_exhausted: true },
  ],
  keys: { outscraper: 'ok', gemini: 'dead' },
  renewals: [],
  sequences: [
    { id: '1', name: 'Cold Outreach', sent: 120, opened: 45, open_rate: 37.5, replied: 8, reply_rate: 6.7 },
  ],
  scripts: [
    { call_number: 1, title: 'Appel Découverte', content: '# Appel 1' },
  ],
  prospects: [],
  funnel: { funnel_speed: 1200, dead_links: [] },
  reports: [],
}

function getDemoData(path) {
  const key = path.split('/').pop()
  return DEMO_DATA[key] || []
}
```

Usage : le mode demo s'active via `?demo=true` dans l'URL (vérifié dans `app.js` au démarrage). En mode demo, les fetchs retournent `getDemoData(path)` au lieu d'appeler l'API.

## 10. Fichiers à Générer

```
dashboard/
├── index.html                     # Page principale unique
├── config/
│   └── client.ts                  # Config client + shopify block
├── js/
│   ├── api.js                     # Fonctions fetch pour chaque endpoint
│   ├── render.js                  # Fonctions de rendu DOM
│   └── app.js                     # Initialisation, polling, events
├── css/
│   └── style.css                  # Surcouches CSS mineures
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

## Notes sur les Features Backend-dépendantes

Certaines features listées nécessitent des endpoints qui ne sont pas encore implémentés :
- **"90-day plan tracking"** — nécessite `GET /api/clients/progress` qui n'est pas dans les endpoints actuels.
- **"Headset tracking"** — nécessite un endpoint ou une table pour tracker l'envoi du matériel.
- **"CRM spreadsheet rendez-vous"** — suppose une intégration Google Sheets, pas documentée.

Ces features sont documentées comme cible. En l'absence du backend, le dashboard peut afficher des sections vides avec "Fonctionnalité à venir".

## Multi-instance

Même mécanisme que l'agence. Le dashboard est dupliqué depuis le template avec la config client. Voir `../../template/README.md`.

## Références

- `../template/` — Template de base pour duplication
- `../AGENTS.md` — Règles de conception dashboard
- `../../agency-back-model/eraser/model-dashboard.md` — Modèle Eraser.io
- `../../agency-documentation/duplication.md` — Process de duplication
