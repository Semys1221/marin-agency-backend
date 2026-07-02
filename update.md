# Marin — Implementations à faire

Snapshot basé sur `create-llm-tasks.md` + `manual-tasks.md`.  
Date de ce document : 2026-07-01.

---





## Backend — implémentations manquantes

### Spécifications à créer avant build

| # | Ressource | Fichier(s) attendus | Statut |
|---|-----------|---------------------|--------|
| 1 | Règles backend & gates | `build/agency-backend/AGENTS.md` | ❌ à créer |
| 2 | Vue d'ensemble backend | `build/agency-backend/OVERVIEW.md` | ❌ à créer |
| 3 | Build order backend | `build/agency-backend/README.md` | ❌ à créer |
| 4 | Backend API — Node/Express/Prisma | `build/agency-backend/backend-api/` | ❌ à créer |
| 5 | Intégrations — 16 signatures API + code | `build/agency-backend/integration/` | ❌ à créer |
| 6 | Script de duplication | `build/agency-backend/scripts/duplicate.sh` | ❌ à créer |

### Prerequisites / infra manuelles

|| # | Item | Statut |
|---|------|--------|
|| 1 | RLS policies exécutées dans Supabase SQL Editor (`rls-policies.sql`) | ❌ |
|| 2 | DB seed data chargée | ❌ |
|| 3 | Script de test `SELECT 1` Supabase fonctionnel | ❌ |
|| 4 | GUI client DB — TablePlus / Postico installé | ❌ |
|| 5 | Google CLI & MCP installés + configurés | ✅ |
|| 6 | Setup du changement de messagerie `hellomontismedia.com` | ✅ |
|| 7 | Delete all Google projects inutiles | ✅ |
|| 8 | Rename everything « agency work » and not « marin » | ✅ |
|| 9 | Manage my accounts passwords & charges | ✅ |
|| 10 | Renommer mon dashboard Stripe | ✅ |
|| 11 | Configurer `.env` à la racine + `env.variables` avec clés réelles | ❌ |
|| 12 | `src/config/client.ts` template frontend : remplir tous les placeholders | ❌ |
|| 13 | `vercel.json` présent et vérifié | ❌ |
|| 14 | `.opencode.jsonc` configuré avec tous les MCP servers | ❌ |

---





## Frontend — implémentations manquantes

| # | Item | Statut |
|---|------|--------|
| 1 | Shadcn UI initialisé (`npx shadcn-ui@latest init`) | ❌ |
| 2 | `npm install` dans template frontend | ❌ |
| 3 | `npm run dev` démarre sans erreur | ❌ |
| 4 | `VITE_DEMO_MODE=true` affiche données mockées | ❌ |
| 5 | Composants shadcn fonctionnels (button, card, input) | ❌ |
| 6 | `cp -r template clients/test-marin` fonctionnel | ❌ |
| 7 | Fonts Inter + Plus Jakarta Sans installées | ❌ |
| 8 | Crash-test sandbox Stripe + Dropbox test mode validé | ❌ |
| 9 | Production go-live — switch API keys en live + test réel | ❌ |

---





## Communication — implémentations manquantes

| # | Item | Statut |
|---|------|--------|
| 1 | Instantly — domaine vérifié + warmup emails + campagnes configurées | ❌ |
| 2 | Resend — domaine vérifié + template contract test/prod uploadés + API key | ❌ |
| 3 | loop.so — 4 workflows + webhooks entrant/sortant + domaine vérifié | ❌ |
| 4 | Slack — workspace + app installée + bot token + channels | ❌ |
| 5 | MCP Resend installé + connecté | ❌ |
| 6 | MCP Slack installé + configuré | ❌ |
| 7 | MCP Gmail installé + configuré (optionnel) | ❌ |
| 8 | Resend ajouté au Dock macOS | ❌ |
| 9 | loop.so ajouté au Dock macOS | ❌ |

---





## Intégrations externes — implémentations manquantes

| # | Service | Statut clé API / compte |
|---|---------|--------------------------|
| 1 | Outscraper | ❌ compte + crédits |
| 2 | Gemini AI | ❌ clé API |
| 3 | Handshake | ❌ compte |
| 4 | DBBounce | ❌ compte + crédits |
| 5 | Stripe | ❌ clés + mode test + webhook endpoint |
| 6 | Calendly | ❌ event type + OAuth + webhook |
| 7 | Shopify | ❌ store créé manuellement + storefront token + UCP CLI |
| 8 | Sentry | ❌ projet + DSN |
| 9 | Dropbox Sign | ❌ clé + template uploadé test/prod |
| 10 | Google Workspace | ❌ domaine vérifié + GCP project + APIs |
| 11 | INSEE | ❌ compte API |
| 12 | Looker Studio | ❌ rapport créé |
| 13 | Quo.com | ❌ compte + call recording activé |
| 14 | Supabase Storage RLS | ❌ policies exécutées |
| 15 | MCP PostgreSQL | ❌ installé |
| 16 | Shopify Agents UCP | ❌ CLI + plugin + profile |

---





## Déploiement — implémentations manquantes

| # | Item | Statut |
|---|------|--------|
| 1 | Render service « Engine » Python/FastAPI créé + `ENGINE_URL` | ❌ |
| 2 | Vercel project lié (`vercel link`) | ❌ |
| 3 | Stripe webhook endpoint prod → `ENGINE_URL/webhooks/stripe` | ❌ |
| 4 | Calendly webhook pointe vers backend | ❌ |
| 5 | Dropbox Sign webhook pointe vers backend | ❌ |
| 6 | Nombre de téléphone de test configuré | ❌ |
| 7 | Test emails validés pour sandbox séquences | ❌ |
| 8 | GitHub Actions secrets ajoutés | ❌ |
| 9 | Workflow `.github/workflows/deploy.yml` créé | ❌ |
| 10 | Propagation DNS vérifiée (`dig`, `MX`, `SPF`, `DKIM`, `DMARC`, `CNAME`) | ✅ |
| 11 | Vercel + Supabase + Render + GitHub liés | ✅ |
| 12 | Domaine `marincie.homes` acheté + nameservers pointés | ✅ |

---





## Physical / ops — implémentations manquantes

| # | Item | Statut |
|---|------|--------|
| 1 | Stock Jabra vérifié (Evolve 20 + earbuds + Evolve2 75) | ❌ |
| 2 | Process d’envoi défini (adresse client post-paiement → commande → tracking) | ❌ |
| 3 | Fournisseur identifié (Amazon Business, LDLC Pro, Jabra direct) | ❌ |
| 4 | LLC US créée via Stripe Atlas | ❌ |
| 5 | CRM Google Contacts structuré | ❌ |

---





## Files attendus — à encoder

| # | Fichier | Contenu | Statut |
|---|---------|---------|--------|
| 1 | `daily-work-routine.md` | Routine quotidienne explicitée | ❌ à créer |
| 2 | `llm-documentation/build/agency-backend/infrastructure/env.variables` | Toutes clés API | ❌ valeurs en `...` |
| 3 | `llm-documentation/build/agency-backend/infrastructure/METHOD.md` | Comment utiliser chaque outil CLI | ❌ |
| 4 | `build/agency-backend/database/rls-policies.sql` | RLS policies Supabase | à exécuter |
| 5 | Prisma schema + migrations | `build/agency-backend/database/` | à produire |
| 6 | Backend API | `build/agency-backend/backend-api/` | spec puis build |
| 7 | Intégrations | `build/agency-backend/integration/` | spec puis build |

---





## Ordre de travail recommandé

1. **Spec d'abord** : créer les 6 specs backend manquantes dans `llm-documentation/build/agency-backend/`
2. **Infra de base** : `.env`, env.variables, RLS, Supabase local, seed data
3. **Build backend** : agency-backend → agency-communication
4. **Setup services externes** : comptes + clés API par service
5. **Frontend** : template → funnels → dashboards
6. **Déploiement** : Render + Vercel + webhooks + CI
7. **Ops & branding** : Slack, CRM, Jabra, LLC, daily routine
8. **Go-live** : crash-test sandbox → production
