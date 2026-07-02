# Pipeline Outreach Engine — Vue Fonctionnelle

Ce document décrit chaque module du pipeline en langage simple. L'objectif est de comprendre **ce que fait** chaque pièce pour pouvoir la tester individuellement.

**Philosophie :** Zéro IA. La connaissance vient du CLI à la création du tenant. Déterministe, prévisible, testable.

---

## 1. supabase_client.py — Connexion à la base de données

**Rôle :** Point d'entrée unique pour parler à Supabase.

- Vérifie que les identifiants Supabase sont configurés
- Crée et réutilise une connexion (pas besoin de se reconnecter à chaque fois)
- Fournit l'ID du client (tenant) utilisé par défaut

**À tester :**
- SUPABASE_URL ou SUPABASE_KEY vides → retourne "non configuré"
- Connexion échoue → pas de crash, message clair

---

## 2. config-reader — La source de vérité du tenant

**Rôle :** Charger la configuration complète d'un client. Créé via le CLI interactif, jamais à la main.

**Fichiers générés par le CLI (create-tenant-cli.py) :**
- `users/<tenant>/config.json` — niches, target, keywords, offer, instantly settings
- `users/<tenant>/sequences.json` — séquences email (optionnel, généré par IA)

**Format complet config.json :**
```json
{
  "tenant_id": "grossiste-a",
  "niches": [
    {
      "name": "grossiste_beaute",
      "target": 1500,
      "instantly_object": "question grossiste",
      "instantly_campaign_id": "grossiste_beaute-grossiste-a-20260701",
      "keywords": [
        "grossiste beauté", "grossiste cosmétique", "distributeur beauté",
        "fournisseur beauté", "grossiste parfumerie", "grossiste maquillage",
        "grossiste esthétique", "grossiste institut beauté"
      ],
      "offer": {
        "description": "Nous aidons les grossistes beauté à obtenir des rendez-vous qualifiés sans démarchage à froid",
        "pain_points": ["démarchage inefficace", "manque de temps commercial"],
        "benefits": ["rendez-vous garantis", "gain de temps commercial"],
        "intro_style": "default",
        "ctas": ["Souhaitez-vous en savoir plus ?"]
      }
    }
  ]
}
```

### Champs par niche

| Champ | Description |
|-------|-------------|
| `name` | Identifiant unique de la niche |
| `target` | Leads nets à push via Instantly avant closure auto (default 1500) |
| `instantly_object` | Objet email Instantly (`question {keyword}`, 1 mot max) |
| `instantly_campaign_id` | Placeholder, créé au moment du push |
| `keywords` | Mots-clés pour le scraping Google Maps |
| `offer.description` | Phrase d'accroche principale |
| `offer.pain_points` | 3 problèmes clients (fixés, les variantes IA formulent différemment) |
| `offer.benefits` | 3 bénéfices (fixés, idem) |
| `offer.intro_style` | `default` ou `{"custom": "..."}` |
| `offer.ctas` | 1-3 calls to action au choix |

### Règles
- **Localisation** : toutes les villes de France par défaut (pas dans la config)
- **Campaign ID** : stocké dans config.json en placeholder, la vraie liaison est dans `campaign_settings` (DB)
- **Séquences email** : optionnelles dans `sequences.json`. Si absentes → templates par défaut dans `push-instantly/lib/sequences.py`
- **Pas de `allowed_domains`** : supprimé (obsolète)
- **Pas de `target` global** : chaque niche a son propre target (default 1500)

### Format sequences.json (optionnel, généré par l'IA)

```json
{
  "grossiste_beaute": {
    "steps": [
      {
        "type": "email", "delay": 0,
        "variants": [
          { "subject": "Question grossiste", "body": "Bonjour,\n\nJ'allais vous joindre au {{phone}}..." },
          { "subject": "Question grossiste", "body": "Bonjour,\n\nJe suis tombé sur votre fiche..." },
          { "subject": "Question grossiste", "body": "Bonjour,\n\nJe travaille exclusivement..." }
        ]
      },
      {
        "type": "email", "delay": 3,
        "variants": [
          { "subject": "Question grossiste", "body": "Bonjour,\n\nJe n'ai pas réussi..." },
          { "subject": "Question grossiste", "body": "Bonjour,\n\nLe plus dur..." },
          { "subject": "Question grossiste", "body": "Bonjour,\n\nUn grossiste comme vous..." }
        ]
      }
    ],
    "subsequence": {
      "conditions": { "lead_activity": [4] },
      "name": "Interested Follow-up",
      "steps": [
        { "type": "email", "delay": 1, "variants": [{ "subject": "Merci", "body": "..." }] },
        { "type": "email", "delay": 4, "variants": [{ "subject": "Témoignage", "body": "..." }] },
        { "type": "email", "delay": 7, "variants": [{ "subject": "Dernier message", "body": "..." }] }
      ]
    }
  }
}
```

Chaque email : max 60 mots. Placesholders : `{{phone}}`, `{{accountSignature}}`.
Les variantes cold (delay 0 et 3) : 3 formulations différentes du même message (pas de nouveau contenu).

### CLI de création

```bash
# CLI interactif (recommandé)
python3 create-tenant-cli.py

# Le CLI :
# 1. Demande les infos de chaque niche (nom, keywords, target, offer, etc.)
# 2. IA suggère keywords / pain points / benefits (optionnel)
# 3. IA génère 5 emails par niche (2 cold × 3 variants + 3 interested)
# 4. Sauvegarde config.json + sequences.json
```

**Mode sans IA :** si `HERMES_API_KEY` non configuré, le CLI fonctionne en manuel.

**À tester :**
- Client inexistant → erreur "config not found"
- Fichier mal formaté → erreur JSON
- Mode démo → données mockées sans fichier
- `niches[]` vide → erreur validation
- Keywords vides pour une niche → erreur
- Sequences absentes → pas de crash, templates par défaut à l'envoi

---

## 3. rotation — Le cerveau du scheduling

**Rôle :** Décide quelle niche scraper et quand, en lisant les métriques Instantly.

**Zéro IA.** Règles if/else pures dans `rotation/rotation_engine.py`.

### Logique détaillée

```
Pour chaque niche :
  1. pending               → activer, scrape immédiat
  2. < 1000 sent           → scrape (pas assez de données)
  3. >= target ET bons taux → scaling (continue)
  4. >= target ET mauvais  → close, active la suivante
  5. < 2% reply + >24h idle → close (sauf si booking rate important)
```

### Table `rotation_state`

| Champ | Type | Description |
|-------|------|-------------|
| tenant_id | text | Identifiant du client |
| niche_name | text | Nom de la niche |
| status | text | pending / active / at_target / scaling / closed / paused |
| leads_pushed | int | Leads nets envoyés à Instantly |
| emails_sent | int | Emails envoyés |
| reply_rate | numeric | Taux de réponse (%) |
| positive_reply_rate | numeric | Taux de réponse positive (%) |
| booking_rate | numeric | Taux de prise de RDV (%) |
| last_message_at | timestamptz | Dernier envoi |
| opened_at | timestamptz | Activation |
| closed_at | timestamptz | Fermeture |
| closed_reason | text | Raison de fermeture |

### Fichiers

- `rotation/rotation_state.py` : CRUD Supabase pour `rotation_state`
- `rotation/metrics.py` : lecture des métriques depuis `campaign_analytics`
- `rotation/rotation_engine.py` : décisions (if/else)
- `rotation/cron.py` : APScheduler toutes les 15 min (ou `--once`)

**À tester :**
- Aucune rotation_state → initialiser toutes les niches en pending, activer la 1ère
- < 1000 sent → scrape
- reply_rate < 2% + >24h → close, active suivante
- Target atteint + bons taux → scaling
- Target atteint + mauvais taux → close
- Toutes fermées → wait

---

## 4. outscraper-scrape — Acquisition de leads

**Rôle :** Scrape Google Maps pour trouver des prospects.

### 4a. outscraper_scraper.py — Moteur de recherche

- Envoie une requête à Outscraper (ex: "plombier Paris")
- Itère sur toutes les villes de France (liste interne)
- Pour chaque résultat avec un email : insert ou update dans `cold_leads`
- Peut exporter en CSV ou JSON

**À tester :**
- Clé API manquante → erreur
- Requête sans résultats → liste vide, pas d'erreur
- Mode DB → vérifier que `cold_leads` est remplie
- Export CSV/JSON → fichier créé

### 4b. lead_filter.py — Filtrage

- Vérifie si un prospect a un email ou un téléphone
- Filtre une liste pour ne garder que les valides
- Donne des statistiques (total, avec email, avec téléphone, valides)

**À tester :**
- Entrée vide → 0 résultats
- Prospect sans email ni téléphone → filtré
- Mélange valides/invalides → stats correctes

### 4c. dedup_leads.py — Nettoyage des doublons

- Cherche les doublons dans `cold_leads` et `clean_leads`
- Normalise les `campaign_id` NULL en chaîne vide
- Supprime les lignes en double (garde la plus ancienne)
- Mode preview : montre ce qui serait fait sans appliquer
- Mode apply : exécute les suppressions

**À tester :**
- Preview sans doublons → "tout est propre"
- Preview avec doublons → liste des lignes à supprimer
- Apply → les doublons disparaissent
- Tenant scoped → ne touche pas aux autres clients

---

## 5. email-validator — Nettoyage des emails

**Rôle :** Pipeline en 2 étages pour valider les emails avant envoi.

### 5a. email_validator.py — Vérification locale (gratuite)

Vérifications sans coût :
- **Format** : l'email ressemble-t-il à un email ?
- **MX record** : le domaine accepte-t-il des emails ? (DNS)
- **Rôle** : email de type info@, contact@, support@ → risque élevé
- **Jetable** : email issu d'un service jetable → invalide
- **SMTP** (optionnel) : vérifie si le serveur accepte l'email
- **Catch-all** (optionnel) : détecte si le domaine accepte tout

Résultat : chaque email a un score de risque (low / medium / high).

**À tester :**
- Email bien formé → valide
- Email sans MX → invalide
- Email rôle (info@) → risk_score = high
- Email jetable → is_valid = false

### 5b. myemailverifier_client.py — Vérification API (payante)

- Appelle MyEmailVerifier pour confirmation avancée
- Limite le débit : max 30 requêtes / minute
- Vérifie le solde de crédits
- En cas de limite (429) : attend 5s et réessaie

**À tester :**
- Clé API manquante → erreur "missing_api_key"
- Crédits épuisés → retourne 0
- Rate limit → attend puis réussit

### 5c. cleaner.py — Orchestrateur 2 étages

1. Passe tous les emails en local (gratuit)
2. Pour les valides, appelle l'API payante
3. Écrit `valid_emails.txt` et `invalid_emails.txt`
4. Mode `--db` : lit `cold_leads` → nettoie → écrit `clean_leads`

**À tester :**
- Fichier vide → message d'usage
- Mode local → pas d'appel API
- Mode DB → leads passent de cold_leads à clean_leads
- Mode demo → résultats aléatoires, zéro appel
- Upsert : même email → mis à jour, pas dupliqué

---

## 6. push-instantly — Envoi vers Instantly

**Rôle :** Prend les leads nettoyés et les pousse dans Instantly pour lancer les campagnes d'emails.

### 6a. push.py — Point d'entrée

- Choisit une campagne par son nom ou pousse toutes les campagnes
- Cherche la campagne dans Instantly
- Si elle n'existe pas et que `--create-if-missing` est actif : la crée
- Pousse les leads par lots de 1000
- Marque les leads comme "contactés" dans clean_leads
- Sauvegarde l'ID Instantly dans `campaign_settings`
- Mode dry-run : montre sans exécuter

**À tester :**
- Pas de clé API → erreur
- Campagne inexistante sans create → erreur
- Campagne inexistante avec create → création + push
- Dry-run → pas d'appel API
- --all-campaigns → toutes les niches traitées

### 6b. lib/campaign.py — Gestion des campagnes

- **find_by_name** : cherche une campagne par nom exact
- **create** : crée avec configuration (séquences, plages, limite 50/jour)
- **activate** : active la campagne
- **create_with_subsequence** : crée + active + ajoute sous-séquence "Interested Follow-up"

### 6c. lib/accounts.py — Comptes d'envoi

- Liste les comptes email actifs disponibles dans Instantly

### 6d. lib/leads.py — Envoi des leads

- Transforme les leads au format Instantly (email, prénom, nom, société, téléphone)
- Envoie par lots de 1000
- Évite les doublons (skip_if_in_workspace)

**À tester :**
- Lot vide → 0 envoyé
- Lot de 1500 → 2 appels API (1000 + 500)

### 6e. lib/sequences.py — Modèles d'emails

- **cold()** : 2 emails (J0, J+3) avec 3 variantes chacun
- **subsequence()** : 3 emails de follow-up (J+1, J+4, J+7), déclenchée quand le prospect montre de l'intérêt

**Remarque :** Les templates sont aussi disponibles dans `sequences/default.json` pour override par tenant.

### 6f. lib/settings.py — Configuration campagne

- Plages horaires : 9h-17h, semaine
- 20s entre emails, 5s aléatoire, 50/jour, text only, stop on reply

### 6g. lib/db.py — Base de données

- **fetch_clean_leads** : récupère les leads nettoyés par campagne
- **get_distinct_campaigns** : liste toutes les campagnes uniques
- **mark_leads_contacted** : marque les leads comme "contactés"
- **save_instantly_campaign_id** : lie campagne locale ↔ Instantly

---

## 7. slack-notifier — Notifications

**Rôle :** Informe l'équipe à chaque étape clé du pipeline.

- **send_message** : message brut dans le salon configuré
- **announce_niches** : "X niches prêtes pour client Y"
- **announce_error** : "⚠️ Erreur pour client Y : détails"
- **announce_decision** : "Décision — action sur cible (raison)"

**À tester :**
- Slack pas configuré → erreur descriptive, pas de crash
- slack_sdk pas installé → erreur import

---

## Résumé du pipeline complet

```
01. Config           → CLI crée le tenant (niches + keywords + target)
02. Rotation         → décide quelle niche scraper maintenant
03. Outscraper       → scrape Google Maps (toutes les villes)
04. Email Validator  → nettoie les emails (local + API)
05. Push Instantly   → envoie les leads vers Instantly
06. Rotation (loop)  → check métriques, décide si changer de niche
07. Slack            → notifie à chaque étape clé
```

Chaque module peut être testé seul (mode démo ou `--dry-run`), sans impacter les autres ni faire d'appels externes payants.

## Suppressions par rapport à l'ancien système

| Ancien module | Raison |
|---------------|--------|
| `brain/brain.py` | IA inutile, la config CLI suffit |
| `scaling-decision/hermes_agent.py` | Remplacé par `rotation/` (règles pures, sans IA) |
| `assign-niche.py` | Les niches sont connues d'avance dans la config |
| `niche-store/niche_store.py` | Fonctions déplacées dans `rotation/` si besoin |
