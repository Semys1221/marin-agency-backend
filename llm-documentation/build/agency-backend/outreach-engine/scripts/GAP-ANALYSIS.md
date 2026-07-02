# Gap Analysis — Outreach Engine scripts/

**Source de vérité :** Eraser.io `model-marin-agency` — Phase 1 Workflow  
**Révision :** scripts/ existants au 2026-07-01

---

## Légende

| Symbole | Signification |
|---------|--------------|
| ✅ | Présent et conforme |
| ⚠️ | Présent mais écart documenté |
| ❌ | Manquant |

---

## Workflow — line par line

| # | Étape | Spec | Code | Statut |
|---|-------|------|------|--------|
| 1 | **User Config** — JSON par dossier user | `01-user-config.md` | `config-reader/config_reader.py` + `users/marin/config.json` | ✅ |
| 2 | **Brain** — génère 10 niches, Slack, loop | `02-brain-gemini.md` | `brain/brain.py` | ⚠️ Spec dit Gemini, code utilise Hermes Agent (documenté dans le README brain). `niche_generator.py` référencé dans le README mais n'existe pas — tout est dans `brain.py` |
| 3 | **Outscraper** — scrape, dedup, filter | `03-outscraper-scrape.md` | `outscraper-scrape/outscraper_scraper.py`, `dedup_leads.py`, `lead_filter.py` | ✅ |
| 4 | **Quick Clean** — MX + syntax + role/disposable | `04-email-cleaning.md` | `email-validator/email_validator.py` | ✅ Stage 1 local |
| 5 | **Deep Clean** — API payante | `04-email-cleaning.md` | `email-validator/myemailverifier_client.py` + `cleaner.py` | ⚠️ Spec dit "DB Bounce", code utilise MyEmailVerifier. Même concept, vendor différent |
| 6a | **Campagne check** — existe dans Instantly ? | `07-instantly-campaign.md` | `push-instantly/lib/campaign.py` | ✅ |
| 6b | **Sequence Creator** — A/B/C → 7-step variants | `06-sequence-creator.md` | ❌ Aucun module standalone. `push-instantly/lib/sequences.py` est embarqué, pas un service dédié | ❌ |
| 6c | **Campaign Setup** — créer campagne Instantly | `07-instantly-campaign.md` | ❌ Pas de module Campaign Setup distinct | ❌ |
| 6d | **Push leads** — envoyer vers Instantly | `07-instantly-campaign.md` | `push-instantly/push.py` | ✅ |
| 7 | **Benchmarks** — analyse perf, Kill & Replace / Scale | `08-benchmarks.md` | `scaling-decision/hermes_agent.py` | ✅ |
| 8 | **Loop** — retour au scraping | `08-benchmarks.md` | ❌ Aucun scheduler/loop | ❌ |

---

## Modules transverses

| Module | Spec | Code | Statut |
|--------|------|------|--------|
| **niche-store** — CRUD niche_hunts + niche_variable | `02-brain-gemini.md` | `niche-store/niche_store.py` | ✅ |
| **slack-notifier** — Notifications Slack | `10-slack-notifications.md` | `slack-notifier/slack_notifier.py` | ✅ |
| **supabase_client** — Client DB partagé | — | `supabase_client.py` | ✅ |
| **APScheduler** — Scheduler du pipeline | Techstack Phase 1 | ❌ Aucun scheduler | ❌ |
| **Sequence Creator Sidecar** — CLI + HTTP server standalone | `11-sequence-creator-sidecar.md` | ❌ Aucun sidecar | ❌ |
| **Hermes Agent orchestrateur global** — orchestre toute la Phase 1 | `09-hermes-agent.md` | ⚠️ `scaling-decision/hermes_agent.py` ne fait que le scaling, pas l'orchestration globale | ⚠️ Partiel |
| **Email Generator** — template rendering + A/B/C variants | `05-email-generator.md` | ❌ Aucun module de génération d'emails | ❌ |

---

## Conformité détaillée par fichier existant

### `config-reader/` ✅
- Lit JSON tenant (`users/<tenant>/config.json`)
- Validate config (niche, keywords, locations required)
- Mode demo
- Conforme au plan

### `brain/brain.py` ⚠️
- Génère 10 niches via LLM ✅
- Parse réponse JSON ✅
- Retry 3x ✅
- Store dans Supabase (niche_hunts) ✅
- Slack notification ✅
- **Écart :** utilise Hermes Agent au lieu de Gemini direct (évolution assumée, README le documente)
- **Écart :** le README brain liste `niche_generator.py` comme fichier séparé — n'existe pas

### `outscraper-scrape/` ✅
- Scrape Outscraper API
- Deduplication
- Filtrage
- Upsert cold_leads
- Conforme

### `email-validator/` ✅ / ⚠️
- **Stage 1 (local)** : syntax regex, MX records, role-based, disposable — conforme
- **Stage 2 (API)** : check SMTP, catch-all, spam traps via MyEmailVerifier — **vendor différent de "DB Bounce" dans le plan, mais fonctionnellement équivalent**
- `assign-niche.py` : assigne niche + campaign aux clean_leads — fonctionnalité bonus non listée dans le plan mais utile

### `niche-store/` ✅
- CRUD niche_hunts
- Gestion active_niche
- Conforme

### `push-instantly/` ⚠️
- Push leads vers Instantly ✅
- Campaign check ✅
- Gestion comptes/settings/config ✅
- **Manque :** hook vers Sequence Creator (inexistant) pour les campagnes nouvelles
- **Manque :** Campaign Setup comme étape séparée

### `scaling-decision/hermes_agent.py` ⚠️
- Analyse performance / décision scale ou kill ✅
- **Écart de scope :** le diagram 09 montre un Hermes Agent qui orchestre TOUTE la Phase 1. Ici il ne fait que le scaling. L'orchestrateur global n'existe pas.

### `slack-notifier/` ✅
- Notifications pour tous les événements pipeline
- Conforme

---

## Résumé — ce qu'il manque

1. **Sequence Creator** (spec `06-sequence-creator.md`) — A/B/C variants → 7-step multi-variant → Campaign Setup
2. **Sequence Creator Sidecar** (spec `11-sequence-creator-sidecar.md`) — CLI + HTTP server deployable
3. **Campaign Setup** (spec `07-instantly-campaign.md`) — création de campagne Instantly
4. **Email Generator** (spec `05-email-generator.md`) — template rendering + A/B/C variants
5. **APScheduler / Loop** — retour automatique au scraping après benchmarks
6. **Hermes Agent orchestrateur global** — le `scaling-decision/` actuel est insuffisant

**Total : 6 modules manquants** sur les ~12 que compte le plan Phase 1.
