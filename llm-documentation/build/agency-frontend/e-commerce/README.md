# E-Commerce Funnel (Grossiste)

**Depends on:** `template/` (copy template before building this variant).
**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ) — variant e-commerce dans le diagramme.

Frontend funnel 11 steps pour l'offre grossiste. Pipeline identique à l'agence mais plus court : pas de gift, pas d'onboarding, pas de contrat. Le voyage s'arrête au paiement Shopify, puis redirection vers le dashboard Shopify.

## Stack

| Layer | Stack |
|-------|-------|
| Runtime | Vite 5 + React 18 + TypeScript 5 |
| State | Zustand 4 (single store until payment) |
| UI | Shadcn (Tailwind 3) |
| Forms | react-hook-form + zod |
| Animation | Framer Motion |
| Products | Shopify Storefront API (shopify-buy) |
| Payments | Shopify Checkout (external redirect) |
| Scheduling | react-calendly |
| Monitoring | Sentry React |
| Hosting | Vercel (1 instance per client) |

Différence avec l'agence : pas de Stripe, pas de Dropbox Sign. Shopify gère le checkout et le tracking.

## File Tree to Generate

Build these components inside the copied template:

```
clients/{tenant_id}/
├── src/
│   ├── config/
│   │   └── client.ts              # Éditer (offerType: 'ecommerce', tokens Shopify)
│   ├── components/
│   │   └── steps/
│   │       ├── Landing.tsx         # Step 1 — Shopify products gallery
│   │       ├── Qualification.tsx   # Step 2 — SIRET check
│   │       ├── Calendly.tsx        # Step 3 — Booking embed
│   │       ├── Cadre.tsx           # Step 4 — Wholesale framework
│   │       ├── Profil.tsx          # Step 5 — Volume, frequency, budget
│   │       ├── Probleme.tsx        # Step 6 — Pain points
│   │       ├── Objectif.tsx        # Step 7 — Volume/price/deadline goals
│   │       ├── Solution.tsx        # Step 8 — Solution showcase
│   │       ├── Proposal.tsx        # Step 9 — Quote + interest bar
│   │       ├── Paiement.tsx        # Step 10 — Shopify Checkout redirect
│   │       └── Tracking.tsx        # Step 11 — Shopify dashboard redirect
```

## Config Interface

```typescript
interface ClientConfig {
  name: string                           // Nom du client
  domain: string                         // Domaine Vercel
  offerType: 'ecommerce'                 // Toujours 'ecommerce'
  branding: { accent, accentDark, bg, text }
  shopify: {
    storeDomain: string                  // https://{client}.myshopify.com
    storefrontToken: string              // Storefront API access token
  }
  tokens: {
    calendlyUrl: string                  // Lien Calendly master
    sentryDsn?: string
  }
  links: {
    microsoft?: string
    quo?: string
    looker?: string
    shopifyAdmin?: string                // /admin path
  }
  apiBase: string                        // Backend API URL
  tenantId: string                       // Identifiant unique client
}
```

## API Endpoints (via backend-api)

Le frontend appelle UNIQUEMENT le **backend-api**. Auth: `X-Tenant-ID` header.

| Method | Path | Purpose | Dummy Data |
|--------|------|---------|------------|
| `GET` | `/api/leads` | Pipeline leads | `[{id:"lead-001", email:"demo@ex.com"}]` |
| `POST` | `/api/leads/status` | Update lead status | `{ok: true}` |
| `GET` | `/api/funnel/health` | Funnel speed + dead links | `{avg_step_duration_ms:23400}` |
| `GET` | `/api/keys/status` | API key health | `{shopify:"ok"}` |

**Shopify :** Les produits sont fetchés DIRECTEMENT depuis le Storefront API (`shopify-buy` SDK), pas via le backend. Utilise `VITE_SHOPIFY_STOREFRONT_TOKEN` et `VITE_SHOPIFY_STORE_DOMAIN`. Le backend-api n'a pas de proxy Shopify.

## Dummy Data (Demo Mode)

```json
// GET /api/shopify/products (quand DEMO_MODE=true)
[
  { "id": "prod-1", "title": "Lot de 100 pièces", "price": "450€", "image": "/demo/prod-1.jpg" },
  { "id": "prod-2", "title": "Pack découverte 50 unités", "price": "250€", "image": "/demo/prod-2.jpg" }
]
```

Steps render with demo data — no real Shopify API calls, no crashes.

## Funnel Steps

| # | Step | Type | Description |
|---|------|------|-------------|
| 1 | Landing | Gallery | Shopify products gallery with pricing |
| 2 | Qualification | Form | SIRET input + validation |
| 3 | Calendly | Embed | Calendly booking |
| 4 | Cadre | Info | Wholesale framework (volume minimum, délais) |
| 5 | Profil | Form | Volume mensuel, fréquence, budget |
| 6 | Problème | Checklist | Pain points spécifiques grossiste |
| 7 | Objectif | Form | Objectif volume, prix cible, délais |
| 8 | Solution | Showcase | Solution présentée |
| 9 | Proposal | Summary | Devis + barre intérêt 1-10 |
| 10 | Paiement | Redirect → Shopify Checkout | Redirection externe |
| 11 | Tracking | Redirect → Shopify Dashboard | Suivi commande |

## Rules

- Single Zustand store until step 10 (Shopify redirect).
- Stripe et Dropbox Sign ne sont PAS utilisés dans ce variant.
- Shopify Checkout est une redirection externe — pas de paiement in-app.
- Les produits sont fetchés via Storefront GraphQL API (shopify-buy SDK).
- Même design system que l'agence (Marin brand).
- Demo mode : les produits sont mockés, pas d'appel Shopify.

## Références

- `textual-content.md` — Contenu marketing pour chaque étape
- `prompt-design.md` — Prompt Google Stitch pour mockups
- `template/README.md` — Instructions duplication + déploiement
