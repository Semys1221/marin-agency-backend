# Email Validator — Module de validation d'emails

Ce dossier contient **4 fichiers** et **18 fonctions**.

Il vérifie si les emails sont valides : format correct, domaine avec MX, boîte non jetable, pas un rôle (info@, contact@). Peut aussi appeler une API externe (MyEmailVerifier) et écrire les résultats dans Supabase.

Ordre d'exécution : validation locale → API externe → écriture en base.

---

## 1. `email_validator.py` — 10 fonctions ( + 1 classe ValidationResult avec 3 propriétés + 1 méthode )

Validation locale des emails (sans API externe).

**Classe `ValidationResult` :**
- `__init__(self, email)` → initialise un résultat vide
- `is_valid` (property) → True si format OK + MX OK + pas jetable
- `risk_score` (property) → "high", "medium" ou "low" selon les flags
- `to_dict(self)` → convertit le résultat en dictionnaire

**Fonctions :**

1. `check_format(email)` → bool  
   Vérifie que l'email a un format valide (regex simple).

2. `check_role_based(local_part)` → bool  
   Vérifie si le début est un rôle (info, contact, support...).

3. `check_disposable(domain)` → bool  
   Vérifie si le domaine est dans la liste des domaines jetables.

4. `check_mx(domain)` → bool  
   Vérifie si le domaine a un enregistrement MX (accepte des emails).

5. `check_smtp(email, domain, timeout=5.0)` → str | None  
   Tente une connexion SMTP pour vérifier si la boîte existe vraiment.

6. `check_catch_all(domain)` → bool  
   Teste si le domaine accepte tous les emails (catch-all).

7. `validate_email(email, smtp_check=False, catch_all_check=False)` → ValidationResult  
   Valide un email en plusieurs étapes. C'est la fonction principale.

---

## 2. `myemailverifier_client.py` — 4 fonctions

Appels à l'API MyEmailVerifier pour une vérification plus poussée.

1. `_wait_for_rate_limit()`  
   Attend si on a dépassé 30 appels par minute (rate limiting).

2. `_headers(api_key)` → dict  
   Construit les en-têtes HTTP pour l'API.

3. `verify_email(email, api_key)` → dict  
   Appelle l'API MyEmailVerifier et retourne le résultat brut.

4. `check_credits(api_key)` → str  
   Vérifie le nombre de crédits restants sur le compte.

---

## 3. `cleaner.py` — 7 fonctions

Coordonne la validation et l'écriture en base de données.

1. `_merge_api_result(local, api_data)` → ValidationResult  
   Fusionne les données de l'API externe dans le résultat local (catch-all, disposable, etc.).

2. `_demo_result(email)` → ValidationResult  
   Génère un résultat aléatoire pour le mode démo (pas d'appel API).

3. `clean_emails(emails, use_api=True, api_key="", demo=False)` → list[ValidationResult]  
   Nettoie une liste d'emails : validation locale + optionnellement appel API. Fonction principale à utiliser depuis la pipeline.

4. `_clean_db(use_api, api_key, tenant, campaign_id, demo)`  
   Lit les emails depuis `cold_leads`, les nettoie, et écrit les résultats dans `clean_leads`.

5. `_insert_to_db(tenant, campaign_id, results)`  
   Insère ou met à jour les résultats dans les tables `cold_leads` et `clean_leads`.

6. `main()`  
   CLI complète : lit depuis stdin ou depuis la base, écrit les fichiers valides/invalides.

---

## 4. `assign-niche.py` — 4 fonctions

Assigne une niche et un campaign_id aux leads qui n'en ont pas encore.

1. `slug(text)` → str  
   Transforme un texte en slug URL (minuscules, tirets).

2. `city_to_region(city)` → str  
   Convertit un nom de ville en région française.

3. `find_niche_in_hunts(hunts, name, region)` → str | None  
   Cherche une niche existante dans les chases en cours (niche hunting).

4. `main()`  
   CLI : assigne les niches aux leads dans `clean_leads`.

---

## Tester ce module

```bash
# Tester la validation locale
python -c "
import asyncio
from outreach_engine.email_validator.email_validator import validate_email
r = asyncio.run(validate_email('test@gmail.com'))
print(f'Valide: {r.is_valid}, Risque: {r.risk_score}')
"

# Tester le cleaner en mode démo
python -c "
import asyncio
from outreach_engine.email_validator.cleaner import clean_emails
r = asyncio.run(clean_emails(['test@gmail.com', 'test@example.com'], demo=True))
for rr in r:
    print(f'{rr.email}: valide={rr.is_valid}')
"

# Tester les crédits MyEmailVerifier
python -m outreach_engine.email_validator.myemailverifier_client
```
