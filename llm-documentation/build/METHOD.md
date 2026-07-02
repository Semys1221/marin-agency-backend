# Build Method — BVG (Build → Verify → Gate)

Méthode pour builder proprement avec l'IA, unit par unit, sans accumuler de bugs.

---

## Le Cycle

Pour chaque fichier numéroté `N.md` dans `llm-documentation/build/` :

```
┌──────────────────────────────────────────────────┐
│                 0. PRE-BUILD                      │
│   Vérifier create-llm-tasks.md : spec ✅         │
│   Vérifier manual-tasks.md : prérequis cochés    │
│   Vérifier les GATES du module (AGENTS.md)       │
│   Vérifier le diagramme Eraser.io                │
│   Lire le code legacy (trash-ignore/)            │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│                  1. BUILD                         │
│   LLM lit le spec → génère le code               │
│   → place au bon endroit                         │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│                 2. VERIFY                         │
│   ┌─ Lint ─────────────────────────────────┐     │
│   │  npm run lint (JS/TS)                  │     │
│   │  ruff check . (Python)                 │     │
│   │  → Zéro erreur, zéro warning           │     │
│   └────────────────────────────────────────┘     │
│   ┌─ Typecheck ───────────────────────────┐     │
│   │  npx tsc --noEmit (JS/TS)             │     │
│   │  mypy . (Python)                      │     │
│   │  → Zéro erreur de type                │     │
│   └────────────────────────────────────────┘     │
│   ┌─ Demo & Edge Cases ───────────────────┐     │
│   │  curl ?demo=true → données mockées    │     │
│   │  Tester : empty state, error state,   │     │
│   │  missing tenant_id (401)              │     │
│   └────────────────────────────────────────┘     │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
    ❌ Échec ──────────┴────────── ✅ Réussite
    Retour BUILD                   GATE PASSED
                                   → Commit
                                   → Passer à N+1
```

---

## Règles

### 0. Pre-Build Gates — tout vérifier avant de builder

Avant de lire le moindre fichier `N.md`, le LLM doit :
1. Vérifier que la spec existe ✅ dans `create-llm-tasks.md`
2. Vérifier que les prérequis manuels sont cochés dans `manual-tasks.md`
3. Vérifier les GATES du module (dans son `AGENTS.md`)
4. Ouvrir le diagramme **Eraser.io** — confirmer que le composant existe
5. Lire le code legacy dans `trash-ignore/Github/Outreach_System/` (patterns à réutiliser)
6. S'assurer que l'environnement est prêt (dépendances installées, `.env` présent)

Si une gate est ROUGE → STOP. Ne pas builder. Signaler le blocage.

---

### 1. Un build unit à la fois
Ne jamais builder le fichier `N+1` avant que `N` ait passé le GATE. C'est la règle la plus importante — un bug dans `N` contaminera tous les suivants.

### 2. Le LLM exécute les checks
L'IA qui build doit aussi lancer les 3 commandes de VERIFY et corriger ses erreurs avant de déclarer le build fini. Elle ne passe pas au fichier suivant tant que le GATE n'est pas vert.

### 3. Pas de lint/typecheck ? Pas de build
Si le projet n'a pas de lint ou typecheck configuré, les installer **avant** de builder. C'est un prérequis au même titre qu'une API key.

### 4. Demo mode obligatoire
Chaque endpoint doit supporter `?demo=true`. Chaque composant doit supporter `DEMO_MODE=true`. Si le spec ne le précise pas, c'est un défaut du spec — le corriger avant de builder.

### 5. Dashboard HTML statique
Pour les projets sans lint/typecheck (HTML + Vanilla JS) :
- Vérifier qu'aucune erreur JS dans la console navigateur
- Vérifier que les appels API mockés retournent des données cohérentes
- Vérifier responsive (mobile first)
- Vérifier les états vides : `Service indisponible`, `Aucune donnée`

### 6. Loop Engineer — Autonomous Quality Control

Pour les assets critiques (vidéo marketing, articles SEO, code complexe), utiliser la boucle adversarial **builder/judge** via le skill Hermes `loop-engineer` :

```
Builder → génère l'asset → Judge → analyse via Definition of Done
    ↑                                │
    └────────── boucle QC ───────────┘
         (max 5 itérations, sinon escalade humaine)
```

- **Definition of Done (DoD)** : fichier `definition-of-done.md` requis à la racine du projet, listant les critères de passage (technique, qualité, contenu, performance)
- **Builder** : LLM qui génère ou modifie l'asset
- **Judge** : LLM adversarial qui évalue chaque critère du DoD avec preuve à l'appui
- **Loop** : max 5 itérations. En cas de hard fail (boucle épuisée), escalade vers le humain
- **Skill associé** : `loop-engineer` installé dans Hermes Agent (`~/.hermes/skills/loop-engineer/SKILL.md`)

Le cycle BUILD (étape 1) intègre la boucle QC pour les composants marqués comme nécessitant une validation automatique.

---

## 7. Agent vs Human — Tool Protocol

L'Agent utilise certains outils CLI sans demander. Pour d'autres, il DOIT demander au Human.

| Tool | Utilisé par | Usage |
|------|-------------|-------|
| `psql` | Agent (Bash) | Requêtes SQL directes, debug DB, vérifier seed data |
| `jq` | Agent (Bash) | Parser les réponses curl dans les tests Verify |
| `curl` / `wget` | Agent (Bash) | Tester les endpoints pendant le cycle Verify |
| Bruno | Human | Tester les endpoints visuellement (optionnel) |
| ngrok | Human | Lancer `ngrok http 8000` quand l'Agent bosse sur des webhooks |

**Règle :** L'Agent utilise `psql`, `jq`, `curl`, `wget` sans demander la permission. Pour Bruno et ngrok, l'Agent DOIT demander au Human de lancer la commande.

---

## 7. Tools Inventory — Usage complet

Tous les outils ci-dessous sont **installés et configurés ✅** (cf. `manual-tasks.md`). Ce tableau définit qui les utilise et comment.

### 7.1 CLI — Agent les utilise sans demander

L'Agent peut lancer ces commandes via Bash à tout moment.

| Tool | Usage | Quand |
|------|-------|-------|
| `git` | Versionning, add/commit/log | Commit après Gate ✅ |
| `gh` | GitHub CLI — issues, PRs, repos | Pre-Build (vérifier legacy), Gate (PR) |
| `supabase` | Init, start, status, db push | Pre-Build (vérifier connexion), Verify (db dump) |
| `vercel` | Déploiements, link, env vars | Gate (deploy — toi-même, sans demander) |
| `render` | Services, logs, deploys | Gate (deploy engine) |
| `stripe` | Webhooks, listen, trigger events | Verify (tester webhooks stripe) |
| `shopify` | Admin CLI, theme, UCP | Build (config store) |
| `curl` / `wget` | Test endpoints, webhooks | **Verify systématique** — chaque endpoint |
| `jq` | Parser JSON dans les pipelines curl | Verify (avec curl) |
| `psql` | Requêtes SQL directes sur Supabase | Verify (check DB state, seed data) |
| `docker` | Conteneurs, images, compose | Build (supabase local) |
| `nvm` / `node` / `npm` | Node.js runtime management | Pre-Build + Build |
| `pyenv` / `python3` / `pip` | Python runtime management | Pre-Build + Build |
| `pnpm` | Package manager (optionnel) | Build si utilisé |

### 7.2 GUI / Persistant — Agent DOIT demander au Human

Ces outils sont graphiques ou nécessitent un processus persistant. L'Agent ne peut pas les lancer seul.

| Tool | Action que le Human doit faire | Quand l'Agent DOIT demander |
|------|-------------------------------|---------------------------|
| **Bruno** | Ouvrir l'app (dans `/Applications/Bruno.app`) et tester un endpoint | **Quand un test curl échoue** ou que le résultat JSON est ambigu / besoin visuel |
| **ngrok** | Lancer `ngrok http <port>` dans un terminal séparé | **Avant chaque test de webhook** (Stripe, Calendly, Dropbox Sign) — le demander AVANT de builder le endpoint |
| **localtunnel** | Alternative : `lt --port <port>` | Si ngrok indisponible |
| **Docker Desktop** | Vérifier que l'app Docker est lancée avant `docker` commands | **Avant la première commande docker** de la session |

### 7.3 MCP Servers — Automatiques (déjà configurés)

Ces serveurs sont branchés dans la config de l'Agent. Il les utilise sans commande CLI.

| MCP | Usage par l'Agent |
|-----|-------------------|
| GitHub | Issues, PRs, file ops, search |
| Supabase | DB queries, Auth, Storage, Edge Functions |
| Vercel | Projets, déploiements, logs, domaines |
| Docker | Gestion conteneurs, images, compose |
| Render* | Services, logs, deploys |
| Stripe | Webhooks, events, paiements |
| Resend | Envoi emails, contacts, domaines vérifiés |
| Sentry | Investigation erreurs runtime, traces |
| Shopify Storefront | Catalogue produits, panier, checkout |
| Slack | Notifications, messages, channels |
| PostgreSQL | Requêtes SQL directes sur la DB |
| Gmail | Envoi/lecture emails (optionnel) |

*Render est accessible via MCP ET via CLI (`render`). L'Agent choisit selon le besoin.

### 7.4 Tool by Phase — Résumé du cycle BVG

| Phase | Outils que l'Agent utilise sans demander | Outils où l'Agent DOIT demander au Human |
|-------|-----------------------------------------|----------------------------------------|
| **Pre-Build** | `git`, `gh`, `supabase`, Eraser.io, lecture legacy code | Rien |
| **Build** | `node`/`npm`/`pip`, `docker`, `shopify` | **Docker Desktop** (vérifier que l'app tourne avant la 1ère commande) |
| **Verify** | `curl`, `jq`, `psql`, lint (`npm run lint`, `ruff check`), typecheck (`tsc`, `mypy`) | **ngrok** (avant chaque test de webhook), **Bruno** (si curl échoue ou résultat ambigu) |
| **Gate** | `git` (commit), `vercel` (deploy), `render` (deploy) | Rien |

**Règle :** L'Agent exécute les outils CLI sans demander (section 7.1). Pour les outils GUI/persistants (section 7.2), il DOIT demander au moment précis indiqué dans la colonne "Quand".

---

### 7.5 VS Code Extensions — Installées, rien à faire

| Extension | Rôle | Usage |
|-----------|------|-------|
| Prisma | Highlight + autocompletion Prisma schema | Passive — VS Code l'utilise automatiquement |
| Tailwind CSS IntelliSense | Autocompletion classes Tailwind | Passive |
| ESLint | Lint JS/TS en live dans l'éditeur | Passive — l'Agent utilise aussi `npm run lint` |
| Prettier | Format on save | Passive |
| Python | Highlight + LSP Python | Passive |
| YAML | Highlight YAML | Passive |
| PostCSS | Support PostCSS dans VS Code | Passive |
| GitLens (opt.) | Historique git visuel | Passive — optionnel |
| Thunder Client (opt.) | API tests dans VS Code | Passive — optionnel |

**Règle :** Toutes ces extensions sont passives. L'Agent n'a pas besoin d'y penser. Le Human n'a pas besoin de les toucher non plus.

---

### 7.6 Service Protocol — Qui fait quoi pour chaque service

Chaque service externe a un **setup humain** (création de compte, ajout de crédits) et un **usage IA** (API, CLI, MCP). Ce tableau définit ce que l'Agent fait seul et quand il doit demander au Human.

| Service | Setup humain (compte + clé) | Usage IA (CLI/MCP/API) | Si clé = `...` ou manquant → l'Agent doit |
|---------|----------------------------|------------------------|------------------------------------------|
| **Supabase** | ✅ Projet ACTIVE_HEALTHY, extensions activées | MCP Supabase (DB, Auth, Storage) + CLI `supabase` | Retourner "Service indisponible" (Gate 1) |
| **Render** | ✅ API key présente | MCP Render + CLI `render` | Retourner erreur descriptive |
| **Vercel** | ✅ Token + Team ID présents | MCP Vercel + CLI `vercel` | Retourner erreur descriptive |
| **Outscraper** | ❌ Crédits à ajouter | API Python (`outscraper` lib) | Dire au Human : "Ajoute des crédits Outscraper (dashboard → billing)" |
| **Gemini AI** | ❌ Billing à activer (free tier épuisé) | API Python (`google-generativeai`) | Dire au Human : "Active le billing Gemini sur aistudio.google.com" |
| **Handshake** | ❌ Compte + clé | API Python (REST) | Dire au Human : "Crée le compte Handshake sur handshake.com" |
| **DBBounce** | ❌ Crédits à ajouter | API Python (REST) | Dire au Human : "Ajoute des crédits DBBounce (service payant)" |
| **Instantly** | ❌ Domaine vérifié + warmup (2-3 sem.) | API Python (`campaign.py`) | Dire au Human : "Configure le domaine + warmup Instantly" |
| **Slack** | ❌ Workspace + app + channels | MCP Slack + API (`chat.postMessage`) | Dire au Human : "Crée le workspace Slack + installe l'app Marin Engine" |
| **Stripe** | ❌ Mode test activé + webhook secret | MCP Stripe + CLI `stripe listen` | Dire au Human : "Active le mode test Stripe et crée le webhook secret" |
| **Calendly** | ❌ Event type + OAuth credentials | API (webhooks) | Dire au Human : "Crée l'event type Calendly (30min, nom 'Découverte')" |
| **Resend** | ❌ Domaine vérifié (DKIM/SPF) | MCP Resend + API | Dire au Human : "Vérifie le domaine `marincie.homes` dans Resend (DKIM/SPF)" |
| **Shopify** | ❌ Store créé manuellement (Partner Dashboard) | CLI `shopify` + Admin API + MCP Storefront | Dire au Human : "Crée le store Shopify via le Partner Dashboard" |
| **Sentry** | ❌ Projet créé + DSN | MCP Sentry | Dire au Human : "Crée le projet Sentry et récupère le DSN" |
| **Dropbox Sign** | ❌ Template contrat uploadé (test + prod) | API (signature) | Dire au Human : "Upload le template contrat dans Dropbox Sign (test + prod)" |
| **Google Workspace** | ❌ Domaine vérifié + GCP project + APIs activées | API Gmail/Calendar/People (via MCP Gmail) | Dire au Human : "Configure Google Workspace, GCP project, et active les APIs" |
| **INSEE** | ❌ Compte API | API REST | Dire au Human : "Crée le compte API INSEE sur api.insee.fr" |
| **Looker Studio** | ❌ Rapport créé | (embed URL — pas de clé) | Dire au Human : "Crée le rapport Looker Studio et fournis l'ID" |
| **loop.so** | ❌ 4 workflows + webhooks entrants/sortants | API REST + webhooks | Dire au Human : "Configure les 4 workflows loop.so (Interested, Indecision, Onboarding, Upsell)" |
| **Quo.com** | ❌ Compte + call recording activé | (pas d'API — manuel) | Dire au Human : "Crée le compte Quo client + active call recording dans Settings" |
| **Hermes Agent** | ✅ Installé, configuré, Nous Portal connecté | CLI `hermes` + skills | N/A — déjà opérationnel |
| **HermesClaw** | ❌ Docker image à pull (~5GB) | CLI `hermesclaw` + Docker | Dire au Human : "Pull l'image Docker HermesClaw (`docker pull ghcr.io/...`)" |

**Règle :** Si un service a `❌` en Setup humain, l'Agent ne tente PAS d'appeler son API. Il dit au Human ce qui manque et attend le feu vert.

---

### 7.7 Task Protocol — Opérations : Agent vs Human

Certaines opérations du cycle de vie sont faites par l'Agent, d'autres nécessitent le Human. Ce tableau tranche.

| Tâche | Fait par | Déclencheur / Condition |
|-------|----------|-------------------------|
| **Remplir env.variables** avec vraies clés | **Human** (clés sensibles) | L'Agent liste les valeurs encore en `...` et demande au Human |
| **Copier env.variables → .env.local** | Agent (`cp`) | Après que le Human a fourni les clés |
| **Installer dépendances Python** | Agent (`pip install -r requirements.txt`) | Phase Pre-Build, sans demander |
| **Installer dépendances Node** | Agent (`npm install` / `pnpm install`) | Phase Pre-Build, sans demander |
| **Initialiser Shadcn UI** | Agent (`npx shadcn-ui@latest init`) | Phase Pre-Build frontend, sans demander |
| **Prisma generate** | Agent (`npx prisma generate`) | Phase Build, sans demander |
| **Lancer Supabase local** | Agent (`supabase init && supabase start`) | Phase Pre-Build, **après avoir demandé Docker Desktop** |
| **Prisma db push** | Agent (`npx prisma db push`) | Phase Build, sans demander |
| **Exécuter RLS policies** | **Human** (via Supabase SQL Editor) | L'Agent dit : "Exécute `rls-policies.sql` dans le SQL Editor Supabase" |
| **Charger seed data** | Agent (`psql` ou script SQL) | Phase Verify, sans demander |
| **Créer le service Render** | **Human** (via dashboard Render) | L'Agent dit : "Crée le service Render Engine avec ces variables d'env : ..." |
| **Lier le projet Vercel** | Agent (`vercel link`) | Phase Gate, sans demander |
| **Configurer webhook Stripe** | Agent (`stripe listen --forward-to ...`) | Phase Verify, **mais demande ngrok d'abord** |
| **Configurer webhook Calendly** | **Human** (dashboard Calendly → Webhooks) | L'Agent dit : "Ajoute ce webhook URL dans Calendly : ..." |
| **Ajouter les secrets GitHub Actions** | **Human** (Settings → Secrets and variables → Actions) | L'Agent liste les secrets manquants |
| **Lancer le warmup Instantly** | **Human** (dashboard Instantly, 2-3 sem.) | L'Agent suit le statut et rappelle au Human |
| **Créer un store Shopify client** | **Human** (Partner Dashboard → Create store) | L'Agent dit : "Crée un nouveau store pour le client X" |
| **Provisionner compte Microsoft 365** | **Human** (admin.microsoft.com) | L'Agent dit : "Crée le compte Microsoft 365 pour le client X" |
| **Commander + envoyer casques Jabra** | **Human** (logistique) | L'Agent listes les adresses clients + stock |
| **Vérifier propagation DNS** | Agent (`dig mx`, `dig txt`) | Phase Verify, sans demander |
| **Setup Search Console** | **Human** (ajouter site + vérifier propriété) | L'Agent dit : "Ajoute `marincie.homes` à Search Console" |
| **Déployer le frontend** | Agent (`vercel --prod`) | Phase Gate, sans demander |
| **Déployer l'engine** | Agent (`render deploys create ...`) | Phase Gate, sans demander |

**Règle :** L'Agent exécute toutes les tâches marquées "Agent" sans demander. Pour les tâches "Human", il doit décrire précisément ce que le Human doit faire, avec le lien et les paramètres.

---

## Exemple d'application

```
Fichier : build/agency-backend/outreach-engine/03-campaign-creator.md

0. PRE-BUILD
   → create-llm-tasks.md : outreach-engine ✅
   → manual-tasks.md : comptes Outscraper/Gemini/Instantly cochés
   → AGENTS.md Gates : Supabase OK, placeholders OK, Eraser OK
   → Diagramme Eraser : nœud "Campaign Creator" présent
   → Code legacy lu : patterns de l'Outreach_System réutilisés

1. BUILD
   → LLM lit 03-campaign-creator.md
   → Génère le code dans outreach-engine/
   → Ajoute les endpoints avec ?demo=true

2. VERIFY
   → ruff check .                 # Zéro erreur
   → mypy .                       # Zéro erreur de type
   → curl localhost:8000/api/campaigns/create?demo=true
   → Test avec tenant_id manquant → 401
   → Test avec niche inconnue → erreur descriptive

3. GATE
   ✅ Tout vert → commit → passer à 04-campaign-queue.md
```

---

## Résumé

| Phase | Qui fait | Durée estimée |
|-------|----------|---------------|
| PRE-BUILD | LLM (vérification) | 1-2 min |
| BUILD | LLM | Jusqu'à code généré |
| VERIFY | LLM (3 commandes) | 2-5 min |
| GATE | LLM + vérif rapide humaine | 1 min |

Le cycle est rapide, reproductible, et force la qualité sans ralentir le build.

---

## Database Extensions

### pgcrypto — hash, UUID, encrypt

Seule extension Postgres nécessaire explicitement. Installée via Supabase SQL Editor :

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

**Cas d'usage pour l'Agent :** `gen_random_uuid()` est utilisé dans tous les schémas de table pour les clés primaires (`id UUID PRIMARY KEY DEFAULT gen_random_uuid()`). Sans pgcrypto, les inserts DB échouent avec une erreur de fonction manquante. L'Agent doit vérifier que pgcrypto est installé avant de builder un spec qui génère des UUID.

> **Note :** Depuis Postgres 13+, `gen_random_uuid()` est built-in sans extension, mais Supabase 15+ l'exige encore via pgcrypto dans certains contextes. L'installer par précaution.
