# Scrape — Module de collecte de leads

Ce dossier contient **3 fichiers** et **12 fonctions**.

Il récupère des leads depuis Google Maps (via Outscraper), filtre ceux qui ont un email ou un téléphone, et déduplique les données en base.

Ordre d'exécution : scraper → filtrer → dédupliquer.

---

## 1. `outscraper_scraper.py` — 7 fonctions

Appels à l'API Outscraper pour chercher des entreprises sur Google Maps.

1. `search_maps(query, limit=100, language="fr", enrichment=None, api_key="")` → list[dict]  
   Lance une recherche Google Maps. `query` peut être un mot-clé ou une liste de mots-clés.

2. `extract_email(entry)` → str  
   Extrait le premier email trouvé dans un résultat (parmi email, email_1, email_2, email_3).

3. `to_flat(entry)` → dict  
   Réduit un résultat aux champs les plus utiles (supprime les données brutes).

4. `_domain(site)` → str  
   Extrait le nom de domaine depuis une URL (enlève https:// et www).

5. `upsert_cold_leads(items, tenant, campaign_id="")`  
   Insère ou met à jour les leads dans la table Supabase `cold_leads`.

6. `to_csv(items, path)`  
   Sauvegarde les résultats dans un fichier CSV.

7. `to_json(items, path)`  
   Sauvegarde les résultats dans un fichier JSON.

---

## 2. `lead_filter.py` — 5 fonctions

Filtre les leads pour ne garder que ceux qui sont utiles.

1. `has_email(entry)` → bool  
   Vérifie si l'entrée contient au moins un email.

2. `has_phone(entry)` → bool  
   Vérifie si l'entrée contient un numéro de téléphone.

3. `is_valid_lead(entry)` → bool  
   Retourne True si l'entrée a un email OU un téléphone.

4. `filter_leads(items)` → list[dict]  
   Garde seulement les entrées valides depuis une liste.

5. `filter_stats(items)` → dict  
   Calcule les stats : total, avec email, avec téléphone, valides, filtrés.

---

## 3. `dedup_leads.py` — 3 fonctions ( + main )

Nettoie les doublons dans les tables Supabase.

1. `dedup(tenant_id, apply=False)` → int  
   Lance le nettoyage des doublons pour un tenant. Si `apply=False`, affiche seulement ce qui sera fait.

2. `_fix_clean_leads(sb, tenant, apply)`  
   Supprime les doublons dans `clean_leads` (campaign_id NULL et "" pour le même email).

3. `_fix_cold_leads(sb, tenant, apply)`  
   Normalise les campaign_id NULL → "" dans `cold_leads`.

---

## Tester ce module

```bash
# Tester le scraping (mode démo sans API)
python -c "
from outreach_engine.scrape.outscraper_scraper import extract_email
from outreach_engine.scrape.lead_filter import filter_leads, filter_stats
data = [{'email': 'test@example.com', 'phone': '01 23 45 67 89'}]
print('Valide:', filter_leads(data))
print('Stats:', filter_stats(data))
"

# Tester la déduplication (prévisualisation seulement)
python -m outreach_engine.scrape.dedup_leads --tenant-id marin
```
