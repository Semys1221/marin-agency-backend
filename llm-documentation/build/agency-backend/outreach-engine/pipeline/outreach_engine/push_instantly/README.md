# Push Instantly — Module d'envoi de campagnes

Ce dossier contient **1 fichier principal** (`push.py`) et **8 fichiers dans `lib/`** (bibliothèque interne).

Total : **9 fichiers**, **17 fonctions**.

Il pousse les leads nettoyés vers Instantly (plateforme d'emailing froid). Il crée les campagnes, les active, et y injecte les contacts.

Ordre d'exécution : push.py → lib/db (lecture des leads) → lib/accounts (comptes expéditeurs) → lib/campaign (création campagne) → lib/leads (envoi des contacts).

---

## Fichier principal : `push.py` — 3 fonctions

1. `push_campaign(tenant_id, campaign_name, create_if_missing=False, dry_run=False)`  
   Trouve ou crée une campagne Instantly, puis envoie les leads nettoyés.

2. `push_all(tenant_id, create_if_missing=False, dry_run=False)`  
   Parcourt tous les noms de campagne distincts d'un tenant et les pousse vers Instantly.

3. `main()`  
   CLI : choisir une campagne spécifique (`--campaign-name`) ou toutes (`--all-campaigns`), avec option `--dry-run` pour tester sans envoyer.

---

## Bibliothèque interne : `lib/`

### `lib/accounts.py` — 1 fonction

1. `list_active()` → list[str]  
   Récupère la liste des emails des comptes expéditeurs actifs sur Instantly.

### `lib/campaign.py` — 4 fonctions

1. `find_by_name(name)` → dict | None  
   Cherche une campagne Instantly par son nom.

2. `create(name, email_list)` → dict | None  
   Crée une nouvelle campagne Instantly avec les paramètres par défaut.

3. `activate(campaign_id)` → bool  
   Active une campagne (la rend opérationnelle).

4. `create_with_subsequence(name, email_list)` → dict | None  
   Crée une campagne + ajoute la sous-séquence "interested" (relance pour les leads intéressés).

### `lib/db.py` — 4 fonctions

1. `_client()` → Client  
   Crée et retourne le client Supabase.

2. `fetch_clean_leads(tenant_id, campaign_name=None, limit=None)` → list[dict]  
   Récupère les leads nettoyés depuis `clean_leads` pour un tenant et une campagne.

3. `get_distinct_campaigns(tenant_id)` → list[str]  
   Récupère tous les noms de campagne distincts pour un tenant.

4. `mark_leads_contacted(tenant_id, campaign_name)`  
   Marque les leads comme "contacted" dans `clean_leads` après envoi.

5. `save_instantly_campaign_id(tenant_id, campaign_id, instantly_campaign_id, niche="")`  
   Sauvegarde l'ID de campagne Instantly pour un tenant/niche donné.

### `lib/http.py` — 3 fonctions

1. `instantly_headers()` → dict  
   Construit les en-têtes HTTP avec la clé API Instantly.

2. `iso_now()` → str  
   Retourne la date/heure actuelle au format ISO.

3. `log(msg, level="INFO")`  
   Affiche un message dans la console avec timestamp.

### `lib/leads.py` — 3 fonctions

1. `push(campaign_id, rows)` → int  
   Envoie les leads vers une campagne Instantly, par lots de 1000. Fonction principale.

2. `_to_instantly_format(rows)` → list[dict]  
   Convertit les lignes Supabase au format attendu par Instantly.

3. `_push_batch(campaign_id, batch)` → dict | None  
   Envoie un seul lot de leads vers l'API Instantly.

### `lib/sequences.py` — 2 fonctions

1. `cold()` → list  
   Retourne la séquence d'emails cold par défaut (2 steps avec 3 variantes chacun).

2. `subsequence(campaign_id)` → dict  
   Retourne la sous-séquence "interested" pour les leads qui cliquent.

### `lib/settings.py` — 1 fonction

1. `build_payload(name, email_list)` → dict  
   Construit le payload JSON complet pour créer une campagne (paramètres, séquences, comptes).

---

## Tester ce module

```bash
# Test en dry-run (sans envoyer vraiment)
python -m outreach_engine.push_instantly.push \
  --campaign-name "grossiste_beaute" \
  --tenant-id "marin" \
  --dry-run

# Tester toutes les campagnes
python -m outreach_engine.push_instantly.push \
  --all-campaigns \
  --tenant-id "marin" \
  --dry-run

# Tester la connexion à la base
python -c "
from outreach_engine.push_instantly.lib.db import _client
c = _client()
print('Supabase OK:', c is not None)
"
```
