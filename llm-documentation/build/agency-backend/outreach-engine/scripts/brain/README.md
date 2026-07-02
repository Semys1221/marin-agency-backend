# Brain — Niche Generation & Orchestration (Hermes Agent)

Moteur de génération de niches et orchestrateur décisionnel.  
**Toute l'IA passe par Hermes Agent** (API Server sur `http://localhost:8642`) — plus d'appel direct à Gemini.

## Modules

| Fichier | Rôle |
|---------|------|
| `niche_generator.py` | Génère 10 sous-niches via Hermes API, parsing, retry |
| `niche_store.py` | CRUD Supabase pour `niche_hunts` + `niche_variable` |
| `config_reader.py` | Lecture config JSON tenant (niche, keywords, locations) |
| `slack_notifier.py` | Notifications Slack pour les événements brain |
| `hermes_agent.py` | Orchestrateur : règles décision via Hermes API |

## Usage

```bash
# Générer des niches
python niche_generator.py --tenant marin
python niche_generator.py --tenant marin --demo

# Lire config tenant
python config_reader.py --tenant marin

# Lancer l'orchestrateur
python hermes_agent.py --tenant marin
```

## Dépendances

```bash
pip install openai supabase slack-sdk
```

## Architecture

```
config_reader.py ──► niche_generator.py ──► niche_store.py
                          │                      │
                          ▼                      ▼
                   slack_notifier.py       Supabase Postgres
                          │
                          ▼
                   hermes_agent.py (orchestrateur décisionnel)
                          │
                          ▼
              Hermes API (localhost:8642)
```

## Contrat Hermes API

Voir `hermes-api-server.md` pour la doc complète de l'API.
