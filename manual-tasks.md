# Prérequis — Configuration manuelle complète

Tout ce qui doit exister sur la machine ou être configuré manuellement pour que l'IA puisse travailler.
Cocher au fur et à mesure.

---

## Dépendances entre ressources

Ordre à respecter pour donner un dossier à un LLM :

| Ressource | Dépend de | Raison |
|-----------|-----------|--------|
| `agency-backend` | *(aucune)* | Socle — API, DB, scraping |
| `agency-frontend` | `agency-backend` | Consomme les API backend |
| `agency-dashboard` | `agency-backend` | Fetch les données backend |
| `agency-communication` | `agency-backend` | API d'envoi, webhooks, DB |
| `agency-book` | *(aucune)* | Docs statiques |

**Règle :** ne jamais donner `agency-frontend` ou `agency-dashboard` à un LLM avant que `agency-backend` soit opérationnel.

---

## 1. Matériel & OS

- [x] **macOS** — à jour (au moins Sonoma 14+)
- [x] **Espace disque** — au moins 10 Go libres
- [x] **Connexion internet stable**
- [x] **Terminal** — Warp (recommandé) ou iTerm2 + zsh

---

## 2. Gestionnaire de paquets système

- [x] **Homebrew** — `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- [x] Vérifier : `brew doctor`

---

## 3. Langages & Runtimes

- [x] **nvm** (Node Version Manager) — `brew install nvm`
  - Installer Node v20+ : `nvm install 20 && nvm use 20`
  - Vérifier : `node -v` (>=20) et `npm -v`
- [x] **pyenv** (Python Version Manager) — `brew install pyenv`
  - Installer Python 3.12+ : `pyenv install 3.12 && pyenv global 3.12`
  - Vérifier : `python3 --version`
- [x] **pip** — `python3 -m ensurepip --upgrade`
- [x] **pnpm** (optionnel, recommandé) — `npm install -g pnpm`

---

## 4. CLI & Outils système

- [x] **Link Supabase, Vercel, GitHub** — connecter les comptes entre eux (déploiements automatiques)
- [x] **Download les outils sur le PC** — installer les binaires CLI (Supabase, Vercel, GitHub)
- [x] **Vérifier l'usage & l'intérêt de chaque outil** — comprendre le rôle de chaque CLI avant de l'utiliser
- [x] **Git** — déjà présent sur macOS. Vérifier : `git --version` ✅ `2.54.0`
  - Configurer : `git config --global user.name "Evan Nanguy"` + `git config --global user.email "evan@marin.app"` ✅
- [x] **GitHub CLI** — `brew install gh && gh auth login` ✅ `2.95.0` — loggué (`Semys1221`)
- [x] **MCP GitHub** — `@modelcontextprotocol/server-github` installé dans la config de l'agent ✅
- [x] **Supabase CLI** — `brew install supabase/tap/supabase` ✅ `2.108.0`
   - Vérifier : `supabase --version` ✅
   - `supabase login` ✅
- [x] **MCP Supabase** — `supabase/mcp` (https://mcp.supabase.com/mcp) configuré dans la config de l'agent ✅
- [x] **Vercel CLI** — `npm install -g vercel && vercel login` ✅ `51.6.1` — loggué (`pvj6qhfpdv-1260`)
- [x] **MCP Vercel** — `@vercel/mcp` (https://mcp.vercel.com) configuré dans la config de l'agent ✅ — OAuth ✅
- [x] **Render CLI** — `npm install -g @renderinc/cli` ✅ `2.21.0`
- [x] **Stripe CLI** — `brew install stripe/stripe-cli/stripe` ✅ `1.43.2`
   - Vérifier : `stripe --version` ✅
   - `stripe login` ✅
- [x] **Shopify CLI** — `npm install -g @shopify/cli @shopify/theme` ✅ `3.94.3`
  - Vérifier : `shopify version` ✅
- [x] **curl / wget** — normalement présents ✅ (`curl 8.7.1`, `wget 1.25.0`)
- [x] **jq** (JSON parser) — `brew install jq` ✅ `1.8.2`
- [x] **PostgreSQL client** (psql) — `brew install libpq` ✅ `psql 18.4`
- [x] **Docker** (pour Supabase local) — `brew install --cask docker` ✅ `29.6.1`
- [x] **MCP Docker** — `@modelcontextprotocol/server-docker` (communautaire) installé (gestion conteneurs, images, compose) ✅
- [x] **ngrok** (tunnel pour webhooks locaux) — `brew install ngrok` ✅ `3.39.8`
  - Auth token : `ngrok config add-authtoken <token>` ✅ déjà configuré
  - Alternative : **localtunnel** — `npm install -g localtunnel` ✅ `2.0.2`
- [x] **Bruno** (client API graphique, alternative Postman) — `brew install bruno` ✅ app GUI dans `/Applications/`
- [x] **METHOD.md** — `llm-documentation/build/METHOD.md` documenté pour savoir comment utiliser chaque outil

---

## 4.1 Tasks à faire

- [x] **Se faire passer pour une autre société**

- [x] **Installer Googles CLI & MCP**

- [x] **Set up le changement de messagerie hellomontismedia.com**
- [x] **Delete all my Google project** 
- [x] **Rename everything « agency work » and not « marin »**

- [x] **Manage my accounts passwords & charges**

- [x] **Renommer mon dashboard Stripe**
- [x] **Ajouter une feuille « update »** — liste de toutes les implémentations à faire
- [x] **Write my daily work routine document.**

- [x] **L'IA est au courant de l'utilisation de tous les outils'**
- [x] **Installer et set up le Hermes agent**

## 5. VS Code — Éditeur

- [x] **VS Code** installé — `brew install --cask visual-studio-code`
- [x] **Code CLI** dans PATH : `code` (Cmd+Shift+P → "Shell Command: Install 'code' command in PATH")

### Extensions obligatoires

- [x] **Prisma** — `code --install-extension Prisma.prisma`
- [x] **Tailwind CSS IntelliSense** — `code --install-extension bradlc.vscode-tailwindcss`
- [x] **ESLint** — `code --install-extension dbaeumer.vscode-eslint`
- [x] **Prettier** — `code --install-extension esbenp.prettier-vscode`
- [x] **Python** — `code --install-extension ms-python.python`
- [x] **YAML** — `code --install-extension redhat.vscode-yaml`
- [x] **PostCSS** — `code --install-extension csstools.postcss`
- [x] **GitLens** (optionnel) — `code --install-extension eamodio.gitlens`
- [x] **Thunder Client** (optionnel, API tests) — `code --install-extension rangav.vscode-thunder-client`

### Settings VS Code recommandés

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "files.associations": {
    "*.css": "tailwindcss"
  },
  "tailwindCSS.experimental.classRegex": [
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

---

## 6. Authentification & Sécurité

### 6.1 GitHub — déjà en HTTPS + token

- [x] **`gh auth` connecté** — déjà fait (compte `Semys1221`, token avec scopes repo/workflow)
- [x] **Remote en HTTPS** — déjà fait (`https://github.com/...`)
- [x] **SSH** — pas nécessaire (HTTPS + token suffit)
- [x] **MCP GitHub** — `@modelcontextprotocol/server-github` installé dans la config de l'agent (permissions: lecture/écriture repos)

### 6.2 API Keys — sécurisation locale

⚠️ **Urgent :** des clés réelles sont commitées dans `llm-documentation/build/agency-backend/infrastructure/env.variables` (SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ANON_KEY, RENDER_API_KEY).

- [x] **Nettoyer `env.variables`** — remplacer les valeurs réelles par `...` dans le fichier versionné
- [x] **Créer `.env.local`** à la racine du projet, ajouté à `.gitignore`, avec les vraies clés
- [x] **Garder une copie locale** des clés dans un fichier `.secrets` (`.gitignore`) ou un note sécurisée sur macOS (Notes avec verrou)

---

## 7. Projets & Repos

- [x] **Repo cloné** — `/Users/evqn/Documents/Agency workspace` (déjà fait)
- [x] **Repo Outreach_System** — vérifier que `trash-ignore/Github/Outreach_System/` existe avec l'engine + cleaner legacy
  - Sinon : cloner depuis GitHub dans `trash-ignore/Github/Outreach_System/`
- [x] **Repos privés accessibles** — si des sous-modules ou repos privés sont utilisés, vérifier que la clé SSH a accès

---

## 8. Services — Comptes & API Keys

### 8.1 Infra & Hébergement

- [x] **Supabase** — Projet créé, ACTIVE_HEALTHY, région ap-northeast-1
  - [x] `SUPABASE_URL` ✅ — `https://rwaggfdqdnfyomvgnsne.supabase.co`
  - [x] `SUPABASE_SERVICE_ROLE_KEY` ✅ — dans `.env.local`
  - [x] `SUPABASE_ANON_KEY` ✅ — dans `.env.local`
  - [x] `DATABASE_URL` ✅ — remplie dans `.env.local` (pooler format)
  - [x] **Extensions activées** : `pgcrypto v1.3`, `uuid-ossp v1.1`, `pg_stat_statements v1.11`, `supabase_vault v0.3.1`
  - [x] **Storage bucket créé** — `call-recordings` (50MB, privé, via API)
  - [ ] **RLS policies** — exécuter `build/agency-backend/database/rls-policies.sql` dans SQL Editor Supabase
- [x] **MCP Supabase** — `supabase/mcp` (https://mcp.supabase.com/mcp) connecté via token (accès DB, Auth, Storage, Edge Functions)
- [x] **Render** — Compte sur https://render.com
  - API key : `RENDER_API_KEY`
- [x] **Vercel** — Compte sur https://vercel.com
  - Token : `VERCEL_TOKEN`
  - Team ID : `VERCEL_TEAM_ID`
- [x] **MCP Vercel** — `@vercel/mcp` (https://mcp.vercel.com) connecté via OAuth (gestion projets, déploiements)
- [x] **Domaine `marincie.homes` acheté** — via Namecheap ou registrar actuel
- [x] **Nameservers pointés vers Vercel** — déléguer la gestion DNS à Vercel (dashboard Vercel → Add Domain → `marincie.homes`)
- [x] **Google Workspace acheté** — sous `marin.app`, utilisateur `evan@marin.app` créé avec licence
- [x] **DNS configuré sur Vercel** :
  - [x] `MX` — Google Workspace (`SMTP.GOOGLE.COM`)
  - [x] `TXT` — SPF, DKIM, DMARC (délivrabilité email)
  - [x] `CNAME` — Vercel (`cname.vercel-dns.com`), Google Workspace (`google.com` + `gv-...`)
  - [x] `A` — éventuels records pour l'engine Render
- [x] **Propagation DNS vérifiée** — `dig mx marincie.homes`, `dig txt marincie.homes`
- [x] **Domaine connecté à Resend** — DKIM/SPF ajoutés dans le dashboard Resend
- [x] **Domaine connecté à loop.so** — DKIM/SPF ajoutés dans le dashboard loop.so

### 8.2 Phase 1 — Outreach Engine

- [x] **Outscraper** — Compte sur https://outscraper.com
  - API key : `OUTSCRAPER_API_KEY`
  - **Crédits ajoutés** — le scraping Google Maps consomme des crédits, le compte doit avoir un solde positif
- [x] **Gemini AI** — API key via https://aistudio.google.com/apikey
  - Clé : `HERMES_API_KEY`
- [x] **Handshake** — Compte sur https://handshake.com
  - API key : `HANDSHAKE_API_KEY`
- [x] **DBBounce** — Compte sur https://dbbounce.com
  - API key : `DBBOUNCE_API_KEY`
  - **Crédits ajoutés** — service payant, solde nécessaire
- [x] **Instantly** — Compte sur https://instantly.ai
  - API key : `INSTANTLY_API_KEY`
  - **Domaine d'envoi vérifié** — ajout des enregistrements DNS SPF/DKIM dans le dashboard Instantly
  - **Warmup des emails** — lancer le warmup des adresses d'envoi (peut prendre 2-3 semaines)
  - **Seuils de warmup minimum** avant de lancer une campagne : 14 jours, taux de réponse > 60%, spam score < 5%, 5-10 emails/jour
  - **Pool d'emails prêt** — au moins 1-2 adresses par campagne
  - **Campagne par défaut** : `INSTANTLY_DEFAULT_CAMPAIGN_ID=...`
- [x] **Slack** — Workspace créé + app installée
  - Workspace : créer sur https://slack.com (ex: `marin-agency.slack.com`)
  - App Slack : créer sur https://api.slack.com/apps (`Marin Engine`)
  - Bot token : `SLACK_BOT_TOKEN` (scopes: `chat:write`, `channels:read`, `reactions:add`)
  - Signing secret : `SLACK_SIGNING_SECRET`
  - Channel ID pour notifications : `SLACK_CHANNEL_ID`
  - Channel ID pour approbation : `SLACK_APPROVAL_CHANNEL_ID`
  - **App installée dans le workspace** — bouton "Install to Workspace" cliqué
  - **Recommandé** : Installer le MCP Slack (`@modelcontextprotocol/server-slack`)
  - **Slack Desktop App** — `brew install --cask slack` (pas indispensable mais utile pour voir les notifs arriver en temps réel)



- [ ] **Test** — Run test en local l'outreach engin
- [ ] **Test** — Tester le nouveau CLI
- [ ] Réaliser 1 par 1 tous les modules d'outreach et les tester.'


### 8.3 Phase 2 — Frontend Engine

- [ ] **Stripe** — Compte sur https://dashboard.stripe.com
  - Secret key : `STRIPE_SECRET_KEY`
  - Publishable key : `STRIPE_PUBLISHABLE_KEY`
  - Webhook secret : `STRIPE_WEBHOOK_SECRET`
  - **Mode test activé** — toutes les clés en mode test pour le développement
  - **Numéro de carte test** : `4242 4242 4242 4242` (valide), `4000 0000 0000 0002` (décliné)
  - **Compte activé pour le live** (quand prêt) — business details, IBAN, etc.
  - **Recommandé** : Installer MCP Stripe (`@stripe/mcp`)
- [ ] **Calendly** — Compte sur https://calendly.com
  - **Event type créé** — nom, durée (30min), lien court configurés dans le dashboard Calendly
  - **Event type test dédié** — créer un 2nd event type nommé "Découverte (Test)" pour le crash-test sandbox (pas de mode test natif Calendly)
  - Event type URL : `CALENDLY_URL` (ex: `https://calendly.com/marin-agency/decouverte`)
  - Client ID + secret (OAuth) : `CALENDLY_CLIENT_ID` + `CALENDLY_CLIENT_SECRET`
  - Webhook key (HMAC) : `CALENDLY_WEBHOOK_KEY=...`
- [ ] **Resend** — Compte sur https://resend.com
  - [ ] API key : `RESEND_API_KEY`
  - [ ] **Domaine d'envoi vérifié** — `marincie.homes` ajouté dans Resend, enregistrements TXT DKIM/SPF/return-path configurés dans le DNS Vercel
  - [ ] **Resend ajouté au Dock macOS** — Site as app (Chrome/Safari → Installer comme app)
  - [ ] **MCP Resend** — `resend-mcp` installé et connecté (envoi emails, gestion contacts, domaines, broadcasts, templates)
  - [ ] **CLI Resend** — `npm install -g resend` (vérifier si CLI officielle existe, sinon utiliser MCP + API REST)
- [x] **Shopify** — Compte Partenaire sur https://partners.shopify.com
  - **Création de store : manuelle uniquement** — la Partner API ne permet PAS de créer des stores. Chaque client e-commerce nécessite un store Shopify créé via le Partner Dashboard (bouton "Create store"). Une fois le store créé, tout le reste est automatisable via Admin API + UCP.
  - Storefront API token (public) : `VITE_SHOPIFY_STOREFRONT_TOKEN`
  - Store domain : `VITE_SHOPIFY_STORE_DOMAIN` → `marin-agency.myshopify.com` ✅
  - **Custom storefront activé** — une fois le store créé, Settings → Sales channels → Custom storefront → créer un token Storefront API
  - **Admin API key** — `SHOPIFY_ADMIN_TOKEN_TEMPLATE` (shpss_...) configuré dans `.env.local` pour le store template
  - **Custom App créée** — Client ID `SHOPIFY_CLIENT_ID` configuré dans `.env.local`
  - **Theme repo** — chaque client a un thème forkable depuis un repo Git Marin
  - **Doc de référence locale** — voir `shopify/api-reference/` pour Admin API, Storefront, Webhooks, Liquid, UCP/Agents, etc.
- [ ] **MCP Shopify Storefront** — endpoint `https://{shop}.myshopify.com/api/mcp` (officiel Shopify, recherche catalogue, gestion panier, checkout)
- [ ] **Sentry** — Projet créé sur https://sentry.io
  - DSN : `SENTRY_DSN`
- [ ] **MCP Sentry** — `@sentry/mcp-server` (https://mcp.sentry.dev) connecté via OAuth (investigation erreurs, traces, performance)
- [ ] **Dropbox Sign (HelloSign)** — Compte sur https://www.hellosign.com
  - API key : `DROPBOX_SIGN_API_KEY` (ancien nom `HELLOSIGN_API_KEY` accepté en alias)
  - **Template contrat uploadé (test)** — uploader le PDF du contrat dans Dropbox Sign, placer les champs de signature, utiliser la clé API test
  - **Template contrat uploadé (prod)** — uploader le même PDF avec la clé API production, vérifier que les champs sont identiques
- [ ] **Google Workspace** — Compte créé sur https://workspace.google.com
  - **Domaine vérifié** — `marin.app` dans Google Admin Console
  - **Utilisateurs créés** — au moins `evan@marin.app` avec licence Google Workspace attribuée
  - **GCP Project** — Créer un projet sur https://console.cloud.google.com
  - Client ID : `GOOGLE_CLIENT_ID`
  - Client secret : `GOOGLE_CLIENT_SECRET`
  - **APIs activées** — Gmail API, Google Calendar API, People API (Contacts)
  - **OAuth Scopes** — `https://www.googleapis.com/auth/gmail.send`, `https://www.googleapis.com/auth/calendar.readonly`, `https://www.googleapis.com/auth/contacts.readonly`
  - **⚠️ Comptes clients Microsoft 365** — l'offre principale inclut un "abonnement Microsoft Pro" pour chaque client. Provisionner les comptes utilisateurs Microsoft 365 pour chaque nouveau client (via admin.microsoft.com).
- [ ] **MCP Gmail** — `@modelcontextprotocol/server-gmail` (communautaire) installé (optionnel — envoi/lecture emails Gmail)
- [ ] **INSEE SIRET** — Compte API sur https://api.insee.fr
  - API key : `INSEE_API_KEY`
  - Client ID : `INSEE_CLIENT_ID`
  - Client secret : `INSEE_CLIENT_SECRET`
- [ ] **Looker Studio** — Rapport créé sur https://lookerstudio.google.com
  - Report ID (pas de clé — embed URL)
- [ ] **loop.so** — Compte sur loop.so
  - [ ] **loop.so ajouté au Dock macOS** — Site as app (Chrome/Safari → Installer comme app)
  - [ ] **Domaine d'envoi vérifié** — `marincie.homes` ajouté dans loop.so (SPF/DKIM configurés dans le DNS Vercel)
  - [ ] **4 workflows configurés** : Interested, Indecision, Onboarding, Upsell
  - [ ] **Webhook entrant** (Hermes → loop.so) — créer pour chaque workflow
  - [ ] **Webhook sortant** (loop.so → Hermes) — configurer dans les stop conditions de chaque workflow
  - [ ] **CLI loop.so** — vérifier si une CLI officielle existe, sinon utiliser l'API REST
  - Voir `context/agency-communication/loop-setup.md` pour le détail pas à pas

- [ ] **Quo.com** (VoIP client) — Compte sur https://quo.com
  - **Compte créé pour chaque client** (offert dans l'offre principale)
  - **Call recording activé** dans les paramètres du compte Quo (Settings → Call Recording)

- [x] **Supabase Storage** — Bucket `call-recordings` créé (via API, 50MB, privé)
  - [x] Bucket créé via API Storage
  - [x] Script RLS créé dans `build/agency-backend/database/rls-policies.sql`
  - [ ] RLS policy à exécuter dans SQL Editor Supabase (nécessite superuser)
  - [x] Limite : 50 MB par fichier

### 8.4 Shopify Agents (UCP — Universal Commerce Protocol)

Shopify Agents permet à l'agent LLM d'interagir directement avec Shopify côté acheteur : rechercher des produits, construire des paniers, créer des checkouts, suivre des commandes.

**⚠️ Limitation :** La création d'un store Shopify reste manuelle (Partner Dashboard). UCP ne gère que les interactions côté acheteur (catalog, cart, checkout, orders). Pour la configuration d'un store existant (produits, thèmes), utiliser l'Admin API.

- [ ] **UCP CLI** — `npm install -g @shopify/ucp-cli`
  - Vérifier : `ucp doctor`
  - Initialiser un profil : `ucp profile init --name agent`
- [ ] **Shopify AI Toolkit installé** — plugin pour Claude Code :
  - `claude plugin install shopify-ai-toolkit@claude-plugins-official`
- [ ] **Agent profile UCP** — Héberger un profile JSON à une URL well-known pour que Shopify puisse négocier les capacités de l'agent (version, cart, checkout, catalog, order)
- [ ] **Token tier** — Générer des credentials API via Dev Dashboard pour le tier le plus élevé (accès à `complete_checkout` et Order MCP)
- [ ] **Doc de référence locale** — Voir `shopify/api-reference/shopify-agents.md` pour les commandes CLI, la configuration du profile, et les exemples de flux

---

## 9. Fichiers de configuration à créer/remplir

- [ ] **`llm-documentation/build/agency-backend/infrastructure/env.variables`** — toutes les clés remplies (aujourd'hui : valeurs en `...`). Source de vérité unique pour toutes les variables d'environnement.
  - **Variables manquantes ajoutées** vs version précédente : `CALENDLY_WEBHOOK_KEY`, `ENGINE_URL`, `RESEND_FROM_EMAIL`, `TICKET_SYSTEM_API_KEY`, `SEQUENCE_CREATOR_API_KEY`, `VITE_WORKER_API_KEY`, `WORKER_API_KEY`, `VITE_API_BASE_URL`, `VITE_TENANT_ID`, `VITE_DEMO_MODE`, `INSTANTLY_DEFAULT_CAMPAIGN_ID`
- [ ] **`.env` local à la racine du projet** — reprendre les clés pertinentes pour le dev local
  ```bash
  cp llm-documentation/build/agency-backend/infrastructure/env.variables .env
  # puis éditer avec les vraies valeurs
  ```
- [ ] **`src/config/client.ts`** dans le template frontend — tous les placeholders en `...` présents
- [ ] **`vercel.json`** — config déploiement Vercel (présent dans template/)

---

## 10. Dépendances projet — Install

- [ ] **Backend Python** — `cd llm-documentation/build/agency-backend && pip install -r requirements.txt` (ou installer manuellement FastAPI, APScheduler, outscraper, google-generativeai, supabase, dnspython)
- [ ] **Frontend template** — `cd llm-documentation/agency-frontend/template && npm install`
- [ ] **Shadcn UI initialisé** — `npx shadcn-ui@latest init` (dans le template)
  - Choisir : Style → Default, Base color → Slate, CSS variables → Yes
- [ ] **Prisma CLI** — `npm install -g prisma` ou dans le projet
- [ ] **Prisma generate** — `npx prisma generate` (une fois le schéma créé)

---

## 11. Fonts du Design System

- [ ] **Inter** installée — https://fonts.google.com/specimen/Inter (Google Fonts) ou `brew install --cask font-inter`
- [ ] **Plus Jakarta Sans** installée — https://fonts.google.com/specimen/Plus+Jakarta+Sans ou `brew install --cask font-plus-jakarta-sans`
- [ ] **Vérifier le rendu** — ouvrir un fichier CSS du projet qui référence `font-family: 'Inter', 'Plus Jakarta Sans'` dans le navigateur

---

## 12. Base de données — Setup

- [ ] **Supabase local** — `supabase init && supabase start` (Postgres locale, pas de risque de casser la prod)
- [ ] **MCP PostgreSQL** — `@modelcontextprotocol/server-postgres` installé (connexion directe à la DB pour requêtes SQL via l'agent)
- [ ] **Migrations Prisma poussées** — `npx prisma db push` (dev) ou `npx prisma migrate deploy` (prod)
- [ ] **RLS policies appliquées** — exécuter `build/agency-backend/database/rls-policies.sql` dans l'éditeur SQL Supabase (ou en local). Le fichier n'existe pas encore — voir `create-llm-tasks.md` section 1 (❌ Database).
- [ ] **Seed data chargée** — exécuter les inserts de test (client "marin", dummy leads)
- [ ] **Vérifier la connexion** — un petit script de test qui fait `SELECT 1` via Supabase
- [ ] **GUI client DB** — TablePlus (`brew install --cask tableplus`) ou Postico pour inspecter Supabase visuellement

---

## 13. Déploiement initial

- [ ] **Render service créé** — "Engine" (Python/FastAPI)
  - Lien : `ENGINE_URL`
  - Variables d'env branchées
- [ ] **Vercel project lié** — `vercel link` dans le template
- [ ] **Stripe webhook endpoint configuré** — `stripe listen --forward-to localhost:8001/webhooks/stripe` + endpoint en prod pointé vers `ENGINE_URL/webhooks/stripe`
- [ ] **Calendly webhook configuré** — pointer vers le backend
- [ ] **Dropbox Sign webhook configuré** — pointer vers le backend
- [ ] **Test data pour les séquences** — emails de test validés (ex: `test@mailinator.com`, `test@example.com`) pour tester l'envoi sans spammer de vrais prospects
- [ ] **Numéros de téléphone de test** — préparer un numéro test pour les appels (Google Voice ou secondaire)

---

## 14. CI / GitHub Actions — Secrets

- [ ] **GitHub Actions activé** sur le repo
- [ ] **Tous les secrets ajoutés** dans Settings → Secrets and variables → Actions :
  - Toutes les clés de `env.variables` (SUPABASE_URL, OUTSCRAPER_API_KEY, STRIPE_SECRET_KEY, etc.)
  - `VERCEL_TOKEN`, `RENDER_API_KEY` pour les déploiements automatiques
- [ ] **Workflow de déploiement** (optionnel) — fichier `.github/workflows/deploy.yml` à créer

---

## 15. AI / MCP — Environnement de travail

### 15.1 MCP Servers — Checklist consolidée

| # | MCP Server | Commande / URL | Status |
|---|-----------|----------------|--------|
| 1 | **Stripe** | `@stripe/mcp` | ❌ À installer |
| 2 | **Supabase** | `supabase/mcp` (https://mcp.supabase.com/mcp) | ❌ À installer |
| 3 | **GitHub** | `@modelcontextprotocol/server-github` | ❌ À installer |
| 4 | **Vercel** | `@vercel/mcp` (https://mcp.vercel.com) | ❌ À installer |
| 5 | **Sentry** | `@sentry/mcp-server` (https://mcp.sentry.dev) | ❌ À installer |
| 6 | **Resend** | `resend-mcp` | ❌ À installer |
| 7 | **Shopify Storefront** | `https://{shop}.myshopify.com/api/mcp` | ❌ À installer |
| 8 | **PostgreSQL** | `@modelcontextprotocol/server-postgres` | ❌ À installer |
| 9 | **Slack** | `@modelcontextprotocol/server-slack` (optionnel) | ❌ À installer |
| 10 | **Gmail** | `@modelcontextprotocol/server-gmail` (optionnel, communautaire) | ❌ À installer |

- [ ] **Fichier `.opencode.jsonc`** configuré avec tous les MCP servers ci-dessus
- [ ] **Eraser.io workspace accessible** — https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ
  - Demander l'accès si pas déjà membre du workspace Eraser.io
- [ ] **Diagramme Eraser.io ouvert et vérifié** contre les specs actuelles
- [ ] **`AGENTS.md` lu** (backend, frontend, dashboard) — les règles sont chargées

---

## 16. Template frontend — Vérification finale

- [ ] `cp -r llm-documentation/agency-frontend/template clients/test-marin` fonctionne
- [ ] `npm run dev` dans le template démarre sans erreur
- [ ] `VITE_DEMO_MODE=true npm run dev` affiche des données mockées
- [ ] Les composants shadcn s'affichent (bouton, card, input)

---

## 17. Checklist Gates (Backend + Frontend)

### Backend Gates (de `llm-documentation/build/agency-backend/AGENTS.md`)

- [ ] **Gate 1** — Supabase project déployé (URL + service_role_key dans env vars)
- [ ] **Gate 2** — API keys avec convention placeholder (`...` si non configuré)
- [ ] **Gate 3** — Diagramme Eraser.io vérifié contre les specs
- [ ] **Gate 4** — Auth model défini (shared DB, tenant_id, pas de login)
- [ ] **Gate 5** — Code existant lu (`trash-ignore/Github/Outreach_System/`)
- [ ] **Gate 6** — Demo mode dans chaque endpoint (`?demo=true`)

### Frontend Gates (de `llm-documentation/agency-frontend/AGENTS.md`)

- [ ] **Gate 1** — Shadcn initialisé (`npx shadcn-ui@latest init`)
- [ ] **Gate 2** — Config client avec placeholders (`src/config/client.ts`)
- [ ] **Gate 3** — Demo mode dans chaque composant (`DEMO_MODE=true`)
- [ ] **Gate 4** — Template existe avant de builder une variante
- [ ] **Gate 5** — Diagramme Eraser.io vérifié
- [ ] **Gate 6** — Aucun HTML brut — que des composants shadcn

---

## Résumé — Comptes à créer

| # | Service | URL | Clé API | Setup manuel supplémentaire |
|---|---------|-----|---------|----------------------------|
| 1 | Supabase | supabase.com | ✅ | Extensions pgcrypto + Storage bucket `call-recordings` + RLS |
| 2 | Render | render.com | ✅ | Service + env vars |
| 3 | Vercel | vercel.com | ✅ | Projet lié |
| 4 | Outscraper | outscraper.com | ✅ | Crédits ajoutés |
| 5 | Gemini AI | aistudio.google.com | ✅ | — |
| 6 | Handshake | handshake.com | ✅ | — |
| 7 | DBBounce | dbbounce.com | ✅ | Crédits ajoutés |
| 8 | Instantly | instantly.ai | ✅ | Domaine vérifié + warmup |
| 9 | Slack | api.slack.com | ✅ | Workspace + app installée + channels |
| 10 | Stripe | dashboard.stripe.com | ✅ | Mode test + activation live |
| 11 | Calendly | calendly.com | ✅ | Event type créé |
| 12 | Resend | resend.com | ✅ | Domaine vérifié (DKIM/SPF) |
| 13 | Shopify | partners.shopify.com | ✅ | Store créé manuellement via Partner Dashboard + Custom storefront activé |
| 14 | Sentry | sentry.io | ✅ | — |
| 15 | Dropbox Sign | hellosign.com | `DROPBOX_SIGN_API_KEY` | Template contrat uploadé (test + prod) |
| 16 | Google Workspace | workspace.google.com | ✅ | Domaine vérifié, GCP project, APIs activées |
| 17 | INSEE | api.insee.fr | ✅ | — |
| 18 | Looker Studio | lookerstudio.google.com | (embed) | Rapport créé |
| 19 | loop.so | loop.so | — | 4 workflows + webhooks entrant/sortant + domaine vérifié |
| 20 | Shopify Agents (UCP) | shopify.dev/docs/agents | — | UCP CLI + plugin agent + profile hébergé |
| 21 | **Quo.com** | quo.com | — | Compte client + call recording activé |
| 22 | **Supabase Storage** | supabase.com (intégré) | (même clé) | Bucket `call-recordings` créé + RLS |

---

## 18. Funnel, Launch & Operations (Bloc 4, 6, 7, 8)

### 18.1 Funnel & Frontend (Bloc 4)

- [ ] **Crash-test sandbox** — Simulation réelle Stripe (test mode) + Dropbox Sign (test mode) pour vérifier frontend ↔ backend communication
- [ ] **Production go-live** — Switch API keys Stripe/Dropbox en live + premier test réel
- [ ] **Call recording activé** — Call recording Quo.com activé pour chaque client

### 18.2 Email & Hermes (Bloc 6)

- [ ] **Instantly campagnes** — Configurer les campagnes cold outreach par niche client (dans le dashboard Instantly)
- [x] **Hermes agent** — Installé, updaté, config de base faite (voir section 19)

### 18.3 Branding & Comptes (Bloc 7)

- [ ] **Slack email import** — Configurer l'intégration email dans Slack
- [ ] **CRM (Google Contacts)** — Créer le CRM contacts
- [ ] **LLC** — Créer US LLC via Stripe Atlas pour stabilité bancaire
- [ ] **Daily work routine** — Rédiger le document de routine quotidienne

### 18.5 Physical Fulfillment (Jabra Headsets)

- [ ] **Stock Jabra** — Vérifier le stock de casques Jabra Evolve 20 + earbuds + Evolve2 75
- [ ] **Process d'envoi** — Définir le processus : collecte adresse client après paiement Stripe → commande → envoi → tracking
- [ ] **Fournisseur** — Identifier le fournisseur (Amazon Business, LDLC Pro, fournisseur direct Jabra)
- [ ] **Tracking** — Notifier le client avec le numéro de suivi après expédition

### 18.6 Email Inbox Management

- [ ] **Inventaire des inboxes** — Voir `context/agency-communication/emails account/` pour la liste complète (60+ inboxes)
- [ ] **Warmup continu** — Maintenir le warmup des inboxes actives dans Instantly (dashboard Instantly → Warmup)
- [ ] **Rotation** — Alterner les inboxes entre campagnes pour éviter la fatigue de domaine
- [ ] **Inboxes dangereuses** — Les inboxes listées dans `dangerous-domain.txt` ne doivent pas être utilisées pour de nouvelles campagnes

### 18.4 Operations Launch (Bloc 8)

- [ ] **Warp organization** — Organiser les code blueprints dans Warp
- [ ] **Start scraping** — Lancer les campagnes de scraping (Outscraper → Supabase)
- [ ] **Start outreach** — Lancer les campagnes d'email outreach

---

## 19. Hermes Agent (Nous Research) — Orchestrateur IA

### 19.1 Installation & Update

- [x] **Hermes Agent installé** — `/Users/evqn/.local/bin/hermes`
- [x] **Version** — `v0.17.0` (updaté depuis v0.15.1, 3339 commits)
- [x] **Python** — 3.11.15 dans venv
- [x] **Config** — `~/.hermes/config.yaml` (v26)
- [x] **Session Nous Portal** connectée (gratuite)
- [x] **SOUL.md** configuré (persona)
- [x] **MEMORY.md** actif (2073 chars)
- [x] **State DB** — 16 sessions historiques

### 19.2 Modèle & Provider

| Status | Provider | Modèle |
|--------|----------|--------|
| ✅ | Nous Portal (free) | `stepfun/step-3.7-flash:free` |
| ✅ Configuré | Gemini API (clé ajoutée) | Quota free tier épuisé — billing requis |

- [x] **Clé Gemini ajoutée** dans `~/.hermes/.env`
- [ ] **Activer billing Gemini** — https://aistudio.google.com/apikey → Enable billing (pay-as-you-go). Passer de 0 req/jour à 1500 req/jour sur `gemini-2.0-flash-lite`.
- [ ] **Configurer Hermes pour utiliser Gemini** — `hermes model` → sélectionner `google/gemini-2.0-flash-lite` ou via Gemini OpenAI-compatible endpoint

### 19.3 Skills installés — 102 skills, dont pertinents pour Marin

| Skill | Catégorie | Utilité pour Marin |
|-------|-----------|-------------------|
| `outscrapper` | Local | Requêtes API Outscraper / Leadsscraper pour scraping Google Maps |
| `outreach-system` | Local (devops) | Contexte du pipeline legacy Outreach_System (Supabase, Render, Smartlead) |
| `google-workspace` | Builtin | Gmail, Calendar, People APIs — emails transactionnels, contacts |
| `himalaya` | Builtin | Email — envoi, lecture, gestion inboxes |
| `maps` | Builtin | Recherche géographique, coordonnées |
| `opencode` | Builtin | Bridge avec OpenCode |
| `claude-code` | Builtin | Bridge avec Claude Code (si utilisé) |
| `webhook-subscriptions` | Builtin | Gestion des webhooks |
| `notion` / `airtable` / `obsidian` | Builtin | Gestion CRM, mémoire, documentation |
| `plan` | Builtin | Writing plans — utile pour le workflow vidéo marketing |
| `github-*` | Builtin | 5 skills GitHub — PR, code review, issues, auth, repos |
| `computer-use` | Builtin | Automatisation navigateur / bureau |

Options à ajouter sur demande :

| Skill | Commande |
|-------|----------|
| Instantly | `hermes skills install instantly` (si dispo dans le hub) |
| Resend | `hermes skills install resend` (ou configurer via API key) |
| Supabase | Déjà accessible via le MCP Supabase dans OpenCode |
| Slack | `hermes skills install slack` (si dispo) |

- [ ] **Installer skills manquants** — explorer `hermes skills search <keyword>` pour les intégrations manquantes (Instantly, Resend, Stripe, etc.)
- [ ] **Créer un skill Marin custom** — bundle de skills pour le pipeline outreach complet (scrape → clean → campaign → benchmark → scale/kill)

### 19.4 Gateway & Messaging

- [ ] **Gateway démarré** — `hermes gateway start` (permet aux messages d'arriver sur tous les canaux : Telegram, Slack, etc.)
- [ ] **Telegram** — Configurer bot Telegram via `hermes telegram setup`
- [ ] **Slack** — Configurer via `hermes slack setup` (ou via le MCP Slack déjà présent dans OpenCode)
- [ ] **Email** — Configurer via skill `himalaya` ou connexion SMTP

### 19.5 Cron Jobs & Automations

- [x] **Cron system check** — `hermes cron list` → 0 jobs actuellement
- [ ] **Cron: Daily briefing** — Résumé journalier de l'activité d'outreach
- [ ] **Cron: Campaign health check** — Vérifier benchmarks et décider kill/scale
- [ ] **Cron: Maintenance** — Nettoyage sessions, rotation inboxes

### 19.6 Pipeline Outreach — Hermes en orchestration

Architecture cible :

```
Hermes Agent (orchestrateur)
├── Skill: outscrapper → Scraping via Outscraper API (payant)
├── Hermes cron → Planification des campagnes
├── Hermes mémoire → Tracking des décisions (kill/scale)
├── Décision AI → Gemini via l'API configurée
├── Notification → Slack / Telegram via gateway
└── Webhook → Callback vers le backend Marin pour les actions
```

- [ ] **Configurer le pipeline complet** : Scrape → Clean → Campaign → Benchmark → Décision → Scale/Kill (via skills + crons Hermes)
- [ ] **Remplacer l'orchestrateur custom Marin** par Hermes Agent comme runtime, tout en gardant Outscraper (scraping), DBBounce (nettoyage), Instantly (envoi) comme APIs payantes

### 19.7 Loop Engineer — Autonomous QC

- [x] **Skill `loop-engineer` créé** — `~/.hermes/skills/loop-engineer/SKILL.md`
- [ ] **Tester la boucle builder/judge** — lancer un premier test :
  ```
  hermes chat -z "Run loop-engineer on project /test with definition-of-done.md"
  ```
- [ ] **Définir les Definition of Done** pour chaque type d'asset :
  - Vidéo marketing (déjà dans `video-marketing/workflow.md`)
  - Contenu SEO (articles de blog)
  - Code (PR, composants)
- [ ] **Configurer max_loops** par type d'asset (recommandé : 5 pour vidéo, 3 pour code)
- [ ] **Escalade humaine** — définir le channel Slack/Telegram pour les hard fails

### 19.9 NVIDIA Agent Toolkit — OpenShell + NemoClaw

Le **NVIDIA Agent Toolkit** (GTC 2026) s'intègre officiellement avec Hermes Agent via **NVIDIA NemoClaw** et le runtime **OpenShell**. Applicable immédiatement pour sécuriser et optimiser les agents autonomes.

#### Stack NVIDIA

```
NVIDIA Agent Toolkit
├── OpenShell          — Runtime sandbox (network/filesystem/process isolation)
├── NemoClaw           — Blueprint Hermes + OpenShell (NVIDIA officiel)
├── HermesClaw         — Idem, version communauté (macOS compatible via Docker)
└── Nemotron 3 Ultra   — Modèle 550B MoE, 5x + rapide, 30% -cher que les frontier
```

#### OpenShell — Ce que ça apporte

| Layer | Mécanisme | Effet |
|-------|-----------|-------|
| **Network** | OPA + HTTP CONNECT proxy | Egress vers hosts approuvés seulement |
| **Filesystem** | Landlock LSM | Accès restreint à `~/.hermes/` + `/sandbox/` |
| **Process** | Seccomp BPF | Syscalls dangereux bloqués (ptrace, mount, etc.) |
| **Credentials** | Privacy router | API keys injectées par OpenShell, jamais vues par Hermes |

**Conséquence** : on peut laisser le loop-engineer tourner en autonomie sans risque de fuite de données ou d'action destructive.

#### MoA (Mixture of Agents) — Amélioration du Judge

Le judge du loop-engineer peut être remplacé par un **panel de modèles** (MoA) :

```
Judge Panel
├── stepfun/step-3.7-flash
├── nvidia/nemotron-3-super (via build.nvidia.com ou OpenRouter)
├── gemini-2.0-flash-lite (si billing activé)
└── Consensus → PASS (unanime) / FAIL (majorité) / ESCALATE (split)
```

MoA est natif dans Hermes v0.17.0 via `hermes model` → presets MoA.

#### HermesClaw — Installation (macOS, Docker, CPU)

```bash
# Prerequisites: Docker Desktop running, git, curl
curl -fsSL https://raw.githubusercontent.com/TheAiSingularity/hermesclaw/main/scripts/install.sh | bash

# Download model (ex: Qwen3 4B)
curl -L -o ~/.hermesclaw/models/Qwen3-4B-Q4_K_M.gguf \
  https://huggingface.co/bartowski/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q4_K_M.gguf

# Start host inference
brew install llama.cpp
llama-server -m ~/.hermesclaw/models/Qwen3-4B-Q4_K_M.gguf --port 8080 --ctx-size 32768 -ngl 99 &

# Start HermesClaw
cd ~/.hermesclaw && docker compose up -d
hermesclaw chat "hello"
```

**Alternative sans GPU local** : utiliser le provider cloud existant (`nous` ou `openrouter`) via `~/.hermes/config.yaml` — HermesClaw route par `inference.local` → provider cloud.

#### Nemotron 3 Ultra via OpenRouter

Dispo sur OpenRouter (déjà configuré comme fallback) :
- Modèle : `nvidia/nemotron-3-super` ou `nvidia/nemotron-3-ultra`
- Provider : `openrouter` avec `OPENROUTER_API_KEY` dans `~/.hermes/.env`
- Avantage : **frontier-level** à prix réduit (5x + rapide, 30% moins cher que GPT/Claude)

#### Checklist

- [ ] **Installer HermesClaw** — `curl -fsSL https://raw.githubusercontent.com/TheAiSingularity/hermesclaw/main/scripts/install.sh | bash`
- [ ] **Tester HermesClaw avec provider cloud** (pas de GPU nécessaire)
- [ ] **Ajouter Nemotron 3 Ultra comme option Judge** dans loop-engineer — via OpenRouter (déjà configuré)
- [ ] **Tester MoA panel** — lancer loop-engineer avec 2+ juges
- [ ] **Définir OpenShell policy** pour Marin : network policy = Outscraper API, DBBounce, Instantly, GitHub
- [ ] **Migrer le pipeline outreach vers HermesClaw sandbox** une fois stable

#### Docker Image HermesClaw (~5GB)

L'image Docker (`ghcr.io/theaisingularity/hermesclaw:latest`) contient Hermes Agent + toutes ses dépendances dans un conteneur prêt à l'emploi. C'est nécessaire pour faire tourner Hermes dans le sandbox OpenShell (isolation réseau/filesystem).

**Pourquoi c'est gros (~5GB)** : l'image embarque Python, Node.js, les binaires Hermes, les dépendances système, et le runtime OpenShell. C'est un one-time download.

**Pourquoi on en a besoin** : sans le conteneur, Hermes tourne à nu sur le host — aucun sandboxing, politique réseau, ou isolation des credentials. Le conteneur + OpenShell = Hermes peut agir en autonomie sans risque de fuite de données.

**Commande à relancer** (connexion stable recommandée, ~5-15 min) :
```bash
docker pull ghcr.io/theaisingularity/hermesclaw:latest
```

Une fois l'image téléchargée, lancer HermesClaw :
```bash
cd ~/.hermesclaw && docker compose up -d
hermesclaw chat "hello"
```

### 19.10 Skills recensés

| Skill | Localisation | Status |
|-------|-------------|--------|
| `outscrapper` | `~/.hermes/skills/outscrapper/skill.md` | ✅ Existe |
| `outreach-system` | `~/.hermes/skills/devops/outreach-system/SKILL.md` | ✅ Existe |
| `loop-engineer` | `~/.hermes/skills/loop-engineer/SKILL.md` | ✅ Créé |

---

## 20. SEO Content Pipeline — Automatisation (via Hermes)

### Concept

Hermes connecte **Google Search Console API** → détecte les keyword gaps (pages classées mais sans article dédié) → rédige un article optimisé → déploie sur **Netlify** ou **WordPress** → monitor les performances.

```
Search Console API → détection keyword gaps → rédaction IA → déploiement → monitoring
```

### Prérequis — Configurations manuelles nécessaires (rien n'est encore possible)

#### 20.1 Google Search Console

- [ ] **Site ajouté à Search Console** — https://search.google.com/search-console
  - Propriété : `marincie.homes` (et éventuels domaines clients)
  - **Propriété vérifiée** — via TXT record DNS ou Google Analytics
- [ ] **GCP Project créé** — https://console.cloud.google.com
  - API : **Google Search Console API** activée
  - OAuth 2.0 credentials : Client ID + Client Secret
  - Scopes : `https://www.googleapis.com/auth/webmasters.readonly`
- [ ] **Hermes configuré** pour utiliser Search Console :
  - `GOOGLE_SEARCH_CONSOLE_CLIENT_ID`
  - `GOOGLE_SEARCH_CONSOLE_CLIENT_SECRET`
  - Pas de skill Hermes natif pour Search Console — à créer ou utiliser `google-workspace` comme base

#### 20.2 Destination de déploiement

Choisir une des deux options (ou les deux) :

- [ ] **Netlify** — Compte sur https://netlify.com
  - `NETLIFY_AUTH_TOKEN` — Personal Access Token
  - **Site créé** — `Netlify CLI` ou dashboard
  - **Build command** — configurée pour le générateur de site (ex: Hugo, 11ty, ou HTML statique)
  - Netlify CLI : `npm install -g netlify-cli && netlify login`

- [ ] **WordPress** — Site WordPress existant ou nouveau
  - **URL du site** + **Credentials API** (Application Password)
  - `WORDPRESS_API_URL` — `https://monsite.com/wp-json/wp/v2/`
  - `WORDPRESS_APP_USERNAME` + `WORDPRESS_APP_PASSWORD`
  - **REST API activée** — désactiver l'authentification cookie si nécessaire

#### 20.3 Pipeline Hermes (à configurer)

- [ ] **Cron : Détection keyword gaps** — hebdomadaire
  ```
  Search Console API → récupérer les queries avec position 5-20
  → filtrer celles sans page dédiée
  → générer liste de keywords à cibler
  ```
- [ ] **Rédaction auto** — Sur chaque keyword détecté :
  ```
  → scraper les top 3 résultats Google pour le keyword
  → analyser la structure (H2, H3, longueur, mots-clés)
  → générer article optimisé (title, meta, headings, body, FAQ)
  ```
- [ ] **Relecture auto (loop-engineer)** — Boucle QC avant déploiement :
  ```
  Judge analyse : fautes, hallucinations, structure SEO, originalité
  → FAIL → rebuild → loop max 3
  → PASS → déploiement
  ```
- [ ] **Déploiement auto** :
  ```
  Netlify : git push → build → deploy
  WordPress : wp-json/wp/v2/posts → POST
  ```
- [ ] **Monitoring** — Mensuel :
  ```
  Re-consulter Search Console API
  → comparer positions avant/après publication
  → rapport de performance
  ```

### Intervention manuelle nécessaire

| Étape | Manuel ? | Pourquoi |
|-------|----------|----------|
| Setup initial Search Console + Netlify/WP | **Oui** | Une fois, configuration API |
| Validation des keywords proposés | **Recommandé** | Éviter de cibler des keywords non pertinents |
| Relecture éditoriale avant déploiement | **Recommandé** | Google pénalise le contenu AI non relu |
| Approbation déploiement | **Optionnel** | Mode auto si confiance établie |
| Correction des hard fails | **Oui** | Si la boucle QC échoue 3 fois |
