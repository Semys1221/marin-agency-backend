# Dashboard Rules — Marin

## Rule of Thumb

**Simple as simple. Efficiency over design. Minimal backend, just links and redirections.**

---

## Prerequisites (Important)

The dashboard READMEs document the target state, but the backend API does not exist yet. When building:

1. **No backend = loading/error states** — All fetch calls will fail. Code must handle empty/error gracefully. Every section must show something useful even when the API is unreachable.
2. **Demo mode** — Provide a `DEMO_MODE=true` flag that renders static mock data so the layout is visible without the backend.
3. **Credentials** — All env vars in the READMEs are placeholders (`...`). The builder must use variables, not hardcoded values.
4. **Auth flow** — The backend doesn't exist yet, so auth is speculative. Build with a placeholder `X-Tenant-ID` header.

---

## Rules

### 1. Static HTML Only

Le dashboard est une **page HTML statique**. Pas de Shadcn, pas de React, pas de framework JS lourd.

### 2. One API Endpoint

Le dashboard fetch UNIQUEMENT `GET /api/dashboard?tenant_id=X` (endpoint aggrégé). Plus de 13 appels individuels.

### 3. No Logic, Just Links

Le dashboard ne fait pas de traitement métier. Il affiche des liens et des données.

### 4. Multi-Instance par Template

Chaque client reçoit une copie du dashboard dans son projet Vercel. La seule chose qui change est le `config/client.js`.

### 5. Services Externes = Simples Liens

Les services (Microsoft, Quo, Calendly, Stripe, Shopify, Looker Studio) sont déjà configurés pour le client.

### 6. Une Page, Pas d'App

Pas de routing, pas de navigation interne. Une seule page HTML qui liste tout.

### 7. Le Dashboard n'est PAS le Funnel

Le funnel de vente (Zustand + Shadcn) est une app React séparée. Le dashboard est la page d'accueil post-onboarding.

### 8. Dashboard Opérations

Le dashboard équipe (outreach) est dans `agency-backend/outreach-engine/12-operations-dashboard.md`.
