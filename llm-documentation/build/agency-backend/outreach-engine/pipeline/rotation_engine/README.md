# Rotation Engine — Module de décision

Ce dossier contient **4 fichiers** et **14 fonctions**.

Il décide quelle niche traiter à chaque cycle de la pipeline. Il lit les métriques des campagnes, vérifie si une niche a assez de leads ou si elle est épuisée, et retourne une action : scrape, wait, ou close.

Ordre d'exécution : metrics (lecture des stats) → rotation_state (état des niches) → rotation_engine (décision) → cron (planification).

---

## 1. `metrics.py` — 4 fonctions

Lecture des métriques de campagne depuis Supabase.

1. `get_niche_metrics(tenant_id, niche_name)` → dict  
   Récupère les dernières métriques d'une niche (total envoyés, ouverts, réponses, etc.).

2. `get_all_metrics(tenant_id)` → dict[str, dict]  
   Récupère les métriques de toutes les niches d'un tenant.

3. `_empty()` → dict  
   Retourne un dictionnaire de métriques vide (tous les compteurs à 0).

4. `_parse(row)` → dict  
   Convertit une ligne brute Supabase en métriques propres et lisibles.

---

## 2. `rotation_state.py` — 8 fonctions

Gestion de l'état de chaque niche (statut, dates, priorité).

1. `_now()`  
   Retourne le timestamp ISO actuel.

2. `get_state(tenant_id, niche_name)` → dict | None  
   Récupère l'état de rotation d'une niche depuis Supabase.

3. `list_states(tenant_id)` → list[dict]  
   Liste tous les états de rotation pour un tenant.

4. `upsert_state(tenant_id, niche_name, updates)` → dict | None  
   Crée ou met à jour l'état de rotation d'une niche.

5. `set_status(tenant_id, niche_name, status, reason="")` → dict | None  
   Change le statut d'une niche (active, paused, closed) et enregistre la date.

6. `init_tenant_niches(tenant_id, niches)`  
   Initialise les niches d'un tenant dans la table `rotation_state` si elles n'existent pas encore.

7. `find_first_pending(tenant_id, niches)` → str | None  
   Trouve la première niche en attente ("pending") pour l'activer.

8. `find_next_active(tenant_id, niches, current_niche)` → str | None  
   Trouve la prochaine niche à activer après la niche courante (rotation circulaire).

---

## 3. `rotation_engine.py` — 5 fonctions

Moteur de décision principal.

1. `decide(tenant_config, demo=False)` → list[dict]  
   Pour chaque niche, regarde les métriques et décide : "scrape", "close", ou "wait". Fonction principale.

2. `_hours_since(ts_str)` → int | None  
   Calcule le nombre d'heures écoulées depuis un timestamp.

3. `_log_decisions(tenant_id, decisions)`  
   Enregistre les décisions dans la table Supabase `rotation_decisions`.

4. `_demo_decisions()` → list[dict]  
   Retourne une décision factice pour le mode démo.

---

## 4. `cron.py` — 4 fonctions

Planification et exécution automatique de la rotation.

1. `run_for_tenant(config_path)` → list[dict]  
   Exécute `decide()` pour un seul tenant à partir de son fichier de config.

2. `run_all(demo=False)`  
   Parcourt tous les dossiers tenants et exécute la rotation pour chacun.

3. `run_once(demo=False)`  
   Exécute une seule passe de rotation pour tous les tenants.

4. `run_loop(demo=False)`  
   Démarre un scheduler qui exécute `run_all()` toutes les 15 minutes.

---

## Tester ce module

```bash
# Tester la décision en mode démo
python -c "
from rotation_engine.rotation_engine import decide
d = decide({'tenant_id': 'marin', 'niches': [{'name': 'grossiste_beaute'}]}, demo=True)
print('Décision:', d)
"

# Tester l'état de rotation
python -c "
from rotation_engine.rotation_state import list_states
states = list_states('marin')
print(f'{len(states)} états trouvés')
"

# Tester le cron en mode once
python -m rotation_engine.cron --once --demo
```
