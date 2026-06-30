# LLM Tasks

> Statut basé sur ce qui est **documenté** dans `llm-documentation/` — pas sur l'implémentation.
> ✅ = spec existe dans `build/` ou `context/`  |  ❌ = spec à créer

---

## 1. `build/agency-backend/` — API, DB, scraping, infra

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| Règles backend & gates | `build/agency-backend/AGENTS.md` | ❌ |
| Vue d'ensemble backend | `build/agency-backend/OVERVIEW.md` | ❌ |
| Build order backend | `build/agency-backend/README.md` | ❌ |
| **Database** — Schéma Prisma, tables, RLS | `build/agency-backend/database/` | ❌ |
| **Outreach Engine** — Worker Python/FastAPI | `build/agency-backend/outreach-engine/` | ✅ |
| **Backend API** — Node/Express/Prisma | `build/agency-backend/backend-api/` | ❌ |
| **Infrastructure** — Déploiement, env vars, MCP | `build/agency-backend/infrastructure/` | ✅ |
| **Integrations** — 16 API signatures + code | `build/agency-backend/integration/` | ❌ |
| **Eraser models** — 7 diagrammes (overview, outreach, frontend, dashboard, hermes, duplication, sequence) | `build/agency-backend/eraser/` | ✅ |
| **Frontend Engine** — 16 étapes (questionnaire → dashboard API) | `build/agency-backend/frontend-engine/` | ✅ |
| **Duplication script** | `build/agency-backend/scripts/duplicate.sh` | ❌ |

---

## 2. `build/agency-frontend/` — Funnels (agency + e-commerce)

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| Règles frontend & gates | `build/agency-frontend/AGENTS.md` | ✅ |
| Build order frontend | `build/agency-frontend/README.md` | ✅ |
| **Template frontend** — Base Vite/React/Shadcn/Zustand | `build/agency-frontend/template/` | ✅ |
| **Marin Agency Funnel** — 22 steps (spec + contenu + mockups) | `build/agency-frontend/marin-agency/` | ✅ |
| **E-commerce Funnel** — 11 steps (spec + contenu + mockups + Shopify) | `build/agency-frontend/e-commerce/` | ✅ |
| ✅ Crash-test sandbox — Procédure de simulation réelle (Stripe + Dropbox test mode) | `build/agency-frontend/crash-test-sandbox/README.md` | ✅ |
| ✅ Production go-live — Procédure de mise en production | `build/agency-frontend/production-go-live/README.md` | ✅ |
| ✅ Call recording — Spécification du système d'enregistrement d'appels | `build/agency-frontend/call-recording/README.md` | ✅ |
| ✅ Call frequency / coaching — Déjà documenté dans `context/agency-communication/calls/calls-plan.md` | — | ✅ |

---

## 3. `build/agency-frontend/dashboard/` — Dashboards clients

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| Règles dashboard & gates | `build/agency-frontend/dashboard/AGENTS.md` | ✅ |
| Build order dashboard | `build/agency-frontend/dashboard/README.md` | ✅ |
| **Template dashboard** — Base statique HTML | `build/agency-frontend/dashboard/template/` | ✅ |
| **Marin Dashboard** — Agency client static HTML | `build/agency-frontend/dashboard/marin-dashboard/` | ✅ |
| **E-commerce Dashboard** — Client e-commerce static HTML | `build/agency-frontend/dashboard/ecommerce-dashboard/` | ✅ |

> Le dashboard opérations (équipe) est dans `build/agency-backend/outreach-engine/12-operations-dashboard.md`.

---

## 4. `build/agency-communication/` + `context/agency-communication/` — Emails, sequences

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| Vue d'ensemble communication | `context/agency-communication/README.md` | ✅ |
| **Sequence models** — Descriptions des 11 séquences | `context/agency-communication/sequences-model/` | ✅ |
| **Live configs** — JSON configurations (Instantly, Resend, loop.so) | `context/agency-communication/sequence-live/` | ✅ |
| **Calls plan** — 6 appels sur 90 jours, 40 min, lié au dashboard client | `context/agency-communication/calls/calls-plan.md` | ✅ |
| ✅ loop.so setup — Configuration des 4 workflows (Interested, Indecision, Onboarding, Upsell) | `context/agency-communication/loop-setup.md` | ✅ |
| ✅ Instantly setup — Configuration des campagnes cold outreach | `context/agency-communication/instantly-setup.md` | ✅ |
| ✅ **Email inbox management** — Inventaire des inboxes, warmed, dangerous domains | `context/agency-communication/emails account/` | ✅ |

---

## 5. `context/agency-book/` — Offres, contrats, marketing

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| **Contrat de service** — Legal contract (2 offres, clauses, SLA) | `context/agency-book/grossiste/contract.md` | ✅ |
| **Offre Principale** — 2500€, 10 ventes, garantie | `context/agency-book/grossiste/offer-contract/offer-main.md` | ✅ |
| **Offre Secondaire** — 1900€, 15 appels, garantie | `context/agency-book/grossiste/offer-contract/offer-secondary.md` | ✅ |
| **Positionnement** — Pain, garantie, solution | `context/agency-book/grossiste/offer-contract/positionnement.md` | ✅ |
| **Framework contractuel** — SLA, clauses, reconduction | `context/agency-book/grossiste/offer-contract/contract-framework.md` | ✅ |
| **Onboarding calls** — 2 calls setup | `context/agency-book/grossiste/offer-contract/onboarding-calls.md` | ✅ |
| **Marketing offer 1** — Livraison & Accès | `context/agency-book/grossiste/marketing/marketing-offer-1-livraison-acces.md` | ✅ |
| **Marketing offer 2** — Onboarding & Opérations | `context/agency-book/grossiste/marketing/marketing-offer-2-onboarding.md` | ✅ |
| **Marketing offer 3** — Suivi, Branding & Équipement | `context/agency-book/grossiste/marketing/marketing-offer-3-suivi-branding.md` | ✅ |
| **Calls content** — Plan d'appels legacy | `context/agency-communication/calls/calls-content.md` | ✅ |
| **Duplication process** — Procédure de duplication d'instance | `context/agency-book/duplication.md` | ✅ |
| **Branding Esthetic** — Logos, CSS, favicons, site.webmanifest | `context/agency-book/grossiste/esthetic/` | ✅ |
| ✅ Upsell Agence 1 — Rachat d'actifs (site + funnel à 10k€) | `context/agency-book/grossiste/offer-contract/upsell/upsell-agence-1.md` | ✅ |
| ✅ Upsell Agence 2 — Nom de domaine perso (500€) | `context/agency-book/grossiste/offer-contract/upsell/upsell-agence-2.md` | ✅ |
| ✅ Upsell Conseil financier | `context/agency-book/grossiste/offer-contract/upsell/upsell-conseil-financier.md` | ✅ |

---

## 6. `context/duplication-method/` — Pattern de duplication

| Task | Fichier(s) | Statut |
|------|-----------|--------|
| **Duplication method** — Pattern pour dupliquer des dossiers LLM-ready | `context/duplication-method/` | ✅ |

---

## Synthèse

| Module | ✅ Documenté | ❌ À créer | Total |
|--------|:-----------:|:---------:|:-----:|
| `build/agency-backend/` | 4 | 7 | 11 |
| `build/agency-frontend/` | 9 | 0 | 9 |
| `build/agency-frontend/dashboard/` | 5 | 0 | 5 |
| `context/agency-communication/` | 7 | 0 | 7 |
| `context/agency-book/` | 15 | 0 | 15 |
| `context/duplication-method/` | 1 | 0 | 1 |
| **Total** | **41** | **7** | **48** |

### ⚠️ 7 specs backend sont à créer

Voir section 1 pour la liste complète des ❌.
