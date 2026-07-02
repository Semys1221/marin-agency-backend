# CLI — Module de démarrage

Ce dossier contient **5 fichiers** et **17 fonctions**.

Il prépare tout ce qu'il faut avant de lancer la pipeline : connexion à la base de données, lecture de la configuration, création des tenants (clients), suggestions par IA, et assistant interactif.

L'ordre ci-dessous est l'ordre d'exécution dans la pipeline.

---

## 1. `config.py` — 2 fonctions

Lecture et validation du fichier de configuration d'un tenant.

1. `read_config(tenant_id, demo=False)` → dict | None  
   Va chercher le fichier `users/{tenant_id}/config.json` sur le disque. Si `demo=True`, retourne une configuration factice.

2. `validate_config(config)` → list[str]  
   Vérifie que la configuration a bien les champs obligatoires (niches, name, keywords). Retourne une liste d'erreurs (vide si tout est bon).

---

## 2. `db.py` — 3 fonctions

Connexion à Supabase (la base de données PostgreSQL).

1. `get_supabase()` → Client  
   Crée et retourne le client Supabase. Ne le crée qu'une seule fois (singleton).

2. `tenant_id()` → str  
   Retourne le `TENANT_ID` depuis les variables d'environnement.

3. `is_configured()` → bool  
   Vérifie que `SUPABASE_URL` et `SUPABASE_SERVICE_ROLE_KEY` sont bien définies dans l'environnement.

---

## 3. `create.py` — 2 fonctions

Création rapide d'un tenant.

1. `create_tenant(tenant_id, niches, target=5000)` → Path  
   Crée un dossier `users/{tenant_id}/` et écrit le fichier `config.json` dedans.

2. `main()`  
   Point d'entrée CLI : prend un tenant_id, des niches (via `--niche` ou `--file`), et appelle `create_tenant`.

---

## 4. `ai.py` — 8 fonctions

Appels à l'IA Hermes (OpenAI-compatible) pour générer des suggestions.

1. `_ia_available()` → bool  
   Vérifie si la clé API Hermes est configurée.

2. `_call_ia(prompt, system, temperature)` → str | None  
   Appelle l'API Hermes et retourne la réponse texte.

3. `_parse_json_list(text)` → list | None  
   Nettoie la réponse markdown et extrait un tableau JSON.

4. `_parse_json(text)` → dict | None  
   Nettoie la réponse markdown et extrait un objet JSON.

5. `suggest_keywords(niche_name)` → list[str] | None  
   Demande 30 mots-clés Google Maps pour une niche.

6. `suggest_pain_points(niche_name, offer)` → list[str] | None  
   Demande 6 problèmes clients pour la niche et l'offre.

7. `suggest_benefits(niche_name, offer, pain_points)` → list[str] | None  
   Demande 6 bénéfices pour la niche, basés sur les pain points.

8. `generate_sequences(niches_data)` → dict | None  
   Demande la génération complète des emails (2 cold + 3 interested) pour chaque niche.

---

## 5. `setup.py` — 7 fonctions ( + main et if __name__ )

Assistant interactif pour créer un tenant pas à pas.

1. `ask(prompt, default)` → str  
   Affiche une question et attend la réponse de l'utilisateur.

2. `ask_int(prompt, default)` → int  
   Comme `ask` mais pour un nombre entier.

3. `pick_from_list(items, label, max_choices, min_choices)` → list[str]  
   Affiche une liste numérotée et laisse choisir plusieurs éléments.

4. `pick_ctas()` → list[str]  
   Propose 3 CTA prédéfinis et laisse l'utilisateur choisir.

5. `save_tenant(tenant_id, niches)` → Path  
   Sauvegarde la configuration du tenant dans `users/{tenant_id}/config.json`.

6. `save_sequences(tenant_id, sequences)` → Path  
   Sauvegarde les séquences d'emails dans `users/{tenant_id}/sequences.json`.

7. `main()`  
   Assistant complet : saisie du tenant, des niches, suggestions IA, génération des emails, sauvegarde.

---

## Tester ce module

```bash
# Tester la config
python -m cli.config --tenant marin --demo

# Tester la base de données (nécessite SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY)
python -c "from cli.db import is_configured; print('OK' if is_configured() else 'Pas configuré')"

# Tester la création rapide
python -m cli.create test-tenant --niche plombier "plombier paris" "plombier lyon"

# Tester l'assistant interactif
python -m cli.setup
```
