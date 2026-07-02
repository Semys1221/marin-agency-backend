# E2E Test — Full Pipeline (Réel)

## Objectif

Tester l'intégralité du pipeline Outreach Engine en mode **réel** (API réelles, Supabase, Slack) :
création tenant → rotation → scraping → validation email → push Instantly → slack notifications.

## Périmètre

| Étape | Module | Réel/Demo | API |
|-------|--------|-----------|-----|
| Création tenant | `cli/create.py` | Réel | — |
| Génération séquences | `cli/ai.py` | Réel | Hermes |
| Rotation | `rotation_engine/` | Réel | Supabase |
| Scraping | `outscraper_scraper.py` | Réel | Outscraper |
| Filtrage | `lead_filter.py` | Réel | — |
| Validation email | `cleaner.py` (MyEmailVerifier) | Réel | MyEmailVerifier |
| Push Instantly | `push_instantly/` | Réel | Instantly |
| Slack notifications | `slack_notifier/` | Réel | Slack |

## Tenant

```
Tenant ID:  grossiste-test
Slack channel: #grossiste-test
Niches (3):
  1. grossiste_materiel_medical  (target: 10 leads)
  2. grossiste_pharmaceutique    (target: 10 leads)
  3. grossiste_optique           (target: 10 leads)
```

## Tables Supabase nécessaires

| Table | Statut | Action |
|-------|--------|--------|
| `clean_leads` | ✅ Existe (12 rows) | Rien |
| `campaign_settings` | ✅ Existe (0 rows) | Rien |
| `rotation_state` | ❌ Manquante | À créer |
| `leads` | ✅ Existe (46k rows) | Rien |

## Déroulement

### 1. Pre-flight
- [x] Vérifier `.env.local` présent (API keys)
- [x] Vérifier connexion Supabase
- [x] Vérifier tables existantes
- [ ] Créer table `rotation_state` si manquante
- [ ] Vérifier comptes Instantly actifs

### 2. Création Tenant
- [ ] Créer dossier `users/grossiste-test/config.json`
- [ ] Créer dossier `users/grossiste-test/sequences.json`
- [ ] Définir 3 niches avec keywords + offres
- [ ] Générer séquences email via Hermes (ou templates par défaut)

### 3. Rotation — Cycle 1
- [ ] Init `rotation_state` dans Supabase
- [ ] Lancer `rotation_engine.decide()` → doit retourner `scrape` pour niche 1
- [ ] Vérifier que `grossiste_materiel_medical` est "active"

### 4. Scraping (Outscraper)
- [ ] Scraper 10 résultats pour "grossiste matériel médical France"
- [ ] Filtrer : garder ceux avec email ou téléphone
- [ ] Logger les stats (total, avec email, avec phone, valides)

### 5. Validation Email (MyEmailVerifier)
- [ ] Nettoyer les emails (format, MX, disposable, role-based)
- [ ] Appeler MyEmailVerifier API pour chaque email
- [ ] Classer : valid / catch-all / role-based / invalid
- [ ] Afficher le score de risque

### 6. Push Clean Leads → Supabase
- [ ] Insérer les leads nettoyés dans `clean_leads` avec `campaign_id = grossiste_materiel_medical-grossiste-test-YYYYMMDD`

### 7. Push Instantly
- [ ] Chercher campagne Instantly existante → créer si absente
- [ ] Récupérer les comptes actifs Instantly
- [ ] Créer campaign + subsequence
- [ ] Pousser les leads dans Instantly
- [ ] Marquer les leads "contacted"

### 8. Slack Notifications
- [ ] Vérifier que Slack reçoit les notifications de chaque phase

### 9. Rotation — Cycle 2 (mimic DB change)
- [ ] Mettre à jour `rotation_state` : marquer niche 1 comme "at_target"
- [ ] Ré-exécuter `decide()` → doit retourner `scrape` pour niche 2

### 10. Nettoyage
- [ ] Optionnel : supprimer le tenant et les campagnes de test

## Gestion d'erreurs

Si une étape échoue (API key manquante, quota dépassé, erreur réseau) :
1. Logger l'erreur avec le message exact
2. Passer à l'étape suivante si non-bloquant
3. Marquer le test comme "⚠️ Partiel" dans le rapport final

## Résultat attendu

```
✅ Tenant grossiste-test créé (3 niches)
✅ Séquences générées
✅ Rotation → scrape grossiste_materiel_medical
✅ X leads scrapés (Outscraper)
✅ Y emails valides (MyEmailVerifier)
✅ Campaign créée sur Instantly
✅ Z leads poussés vers Instantly
✅ Slack notifié à chaque étape
✅ Rotation cycle 2 → scrape grossiste_pharmaceutique
```
