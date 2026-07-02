# Pipeline — Orchestrateur principal

Le fichier `main.py` à la racine contient **5 fonctions**.

Il coordonne tous les modules dans l'ordre : CLI (config) → Rotation (décision) → Outreach (scrape → valide → push) → Slack (notification).

---

## `main.py` — 5 fonctions

1. `phase_create_tenant(demo=False)`  
   Crée un nouveau tenant. En mode démo, retourne une config factice. Sinon, lance l'assistant interactif.

2. `phase_rotation(config, demo=False)` → list[dict]  
   Appelle `rotation_engine.decide()` et retourne les décisions (scrape, close, wait) pour chaque niche.

3. `phase_outreach(decision, config, demo=False)`  
   Exécute toute la pipeline pour une niche : lit la config → scrape les leads → filtre → nettoie les emails → push vers Instantly.

4. `phase_slack(message, demo=False)`  
   Envoie une notification Slack (ou logge simplement en mode démo).

5. `main()`  
   Point d'entrée : parse les arguments (`--demo`, `--once`, `--tenant`, `--create-tenant`), lit la config, appelle les phases dans l'ordre.

---

## Tester la pipeline complète

```bash
# Mode démo (un cycle, sans appels API externes)
python main.py --once --demo

# Créer un nouveau tenant
python main.py --create-tenant

# Lire la config d'un tenant
python main.py --tenant marin

# Avec un fichier de config personnalisé
python main.py --config ./users/marin/config.json --once
```

## Résumé des modules

| Module | Fichiers | Fonctions | Action |
|--------|----------|-----------|--------|
| `cli/` | 5 | 17 | Config, DB, création tenant, IA |
| `scrape/` | 3 | 12 | Scraping Google Maps, filtrage |
| `email_validator/` | 4 | 18 | Validation d'emails, nettoyage |
| `push_instantly/` | 1+8 | 3+14 | Push vers Instantly |
| `rotation_engine/` | 4 | 14 | Décision, métriques, cron |
| `slack_notifier/` | 1 | 5 | Notifications Slack |
| **Total** | **18+8** | **69+14** | |
