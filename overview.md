# Marin — Overview

## Structure du projet

```
/
├── manual-tasks.md              ← check-list des tâches manuelles
├── overview.md                  ← this file
├── create-llm-tasks.md          ← inventaire des LLM tasks
├── llm-documentation/
│   ├── build/                   ← Specs actionnables — à donner à un LLM pour builder
│   │   ├── agency-backend/      ← API, DB, scraping, infra
│   │   ├── agency-frontend/     ← Funnels (marin-agency, e-commerce, template, dashboard/, reference/)
│   │   └── agency-communication/ ← Generator engine, ticket system
│   └── context/                 ← Documentation, assets, référence
│       ├── agency-book/         ← Offres, contrats, marketing, branding
│       ├── duplication-method/  ← Pattern pour structurer des dossiers LLM-ready
│       └── agency-communication/ ← Séquence models, live configs JSON
├── trash-ignore/                ← Archives, déchets
└── AGENTS.md
```

---

## Ressources actionnables

Les dossiers dans `build/` sont les specs à donner à un LLM pour builder.
Les dossiers dans `context/` sont de la documentation / référence à fournir en contexte.

### `build/agency-backend/`
API backend, base de données Supabase, scraping pipeline, Hermes orchestration, CRM, infrastructure.
Voir `build/agency-backend/OVERVIEW.md` et `build/agency-backend/AGENTS.md`.

### `build/agency-frontend/`
Funnels (agency 22 steps + e-commerce 11 steps) + dashboards clients HTML statique.
Stack funnel : Vite + React + Zustand + Shadcn. Stack dashboard : HTML + Vanilla JS.
Voir `build/agency-frontend/AGENTS.md`.

### `build/agency-frontend/dashboard/`
Dashboards clients statiques HTML : marin agency, e-commerce, template de duplication.
Le dashboard opérations (équipe) est dans `build/agency-backend/outreach-engine/12-operations-dashboard.md`.

### `build/agency-communication/`
Engine de génération de séquences et ticket system.

### `context/agency-communication/`
Séquences email (Instantly, Resend, loop.so) — modèles et configurations live.

### `context/agency-book/`
Offres commerciales, contrats, marketing, branding (Esthetic/), calls content, duplication process.

---

## Agency Book — Offres & Contrat

Tous les documents commerciaux et contractuels sont dans `context/agency-book/grossiste/`.

### agency-book/grossiste/contract.md
Contrat de prestation : offres, livrables, garantie, clauses légales. Prestataire : Evan Nanguy (EI — RCS Bordeaux 885 248 039). Clauses : appels enregistrés, tacite reconduction, mandat SEPA, obligation logiciels/matériels, anonymat.

### agency-book/grossiste/offer-contract/positionnement.md
Positionnement commercial complet : pain (douleur grossiste), garantie (performance ou on continue), pourquoi nous, solution clé en main. Clauses légales externalisées vers contract.md.

### agency-book/grossiste/offer-contract/offer-main.md
- Setup : 15 jours (démarrage J+1 après paiement)
- Accompagnement : 90 jours
- Objectif : 10 ventes entre 800 € et 2 500 €
- Garantie : 10 ventes ou poursuite jusqu'à obtention
- Prix : 2 500 €
- Inclus : Offre 3 complète (Suivi performance, Branding & Équipement)
- Bonus : casque Jabra Evolve 20 + earbuds, abonnement Quo, abonnement Microsoft
- Gift : upgrade casque → Jabra Evolve2 75

### agency-book/grossiste/offer-contract/offer-secondary.md
- Setup : 15 jours (démarrage J+1 après paiement)
- Accompagnement : 90 jours
- Objectif : 15 appels
- Garantie : 15 appels ou poursuite jusqu'à obtention
- Prix : 1 900 €

### agency-book/grossiste/offer-contract/contract-framework.md
- Contrat de service
- Rédaction des contrats
- Textes de tous les livrables
- SLA / délais d'exécution : mises à jour 7–14 jours selon volume
- Reconduction tacite

### agency-book/grossiste/offer-contract/onboarding-calls.md
- Onboarding 1 (dirigeant/payeur) : après vente, présentation service + dashboard
- Onboarding 2 (équipe commerciale) : sous 15 jours, setup technique + logiciels
- Suivi : appels tous les 15 jours

### agency-book/grossiste/marketing/marketing-offer-1-livraison-acces.md — (1) Livraison & Accès
Ce que le client reçoit :
- Page HTML servant de dashboard (redirections vers services tiers)
- Accès au process NodeJS selon l'offre
- Site e-commerce Shopify Pro (valeur 12 000 €)
- Tunnel de vente live (valeur 8 000 €)
- Compte Microsoft Pro
- Calendly Pro
- Dropbox – signature légale des devis
- Envoi automatique des emails de confirmation

### agency-book/grossiste/marketing/marketing-offer-2-onboarding.md — (2) Onboarding & Opérations
- Onboarding dashboard (patron) + onboarding vente (commerciaux)
- 1 appel de suivi tous les 15 jours
- Assistant personnel client automatisé 7j/7 (accusé de réception contextualisé, ex. julie@marin.homes)
- Traitement des réponses < 24h
- Traitement des modifications sous 7–14 jours (hors urgence)
- Emails d'onboarding hebdomadaires
- Facturation mensuelle

### agency-book/grossiste/marketing/marketing-offer-3-suivi-branding.md — (3) Suivi, Branding & Équipement
- Suivi des performances des commerciaux via appels enregistrés
- Refonte logo + global CSS (valeur 500 €)
- Envoi d'un casque upgraded (gift)
