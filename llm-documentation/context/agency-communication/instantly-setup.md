# Instantly — Configuration des Campagnes Cold Outreach

Guide pas à pas pour configurer les campagnes de cold outreach dans Instantly.

**Référence :** Modèle d'email dans `context/agency-communication/sequence-live/instantly/cold-contact.md`

---

## Prérequis

- [ ] Compte Instantly créé (https://instantly.ai)
- [ ] API key générée : `INSTANTLY_API_KEY`
- [ ] Domaine d'envoi vérifié (SPF/DKIM ajoutés dans le DNS)
- [ ] **Warmup terminé** — les adresses d'envoi doivent avoir au moins 2-3 semaines de warmup
- [ ] Pool d'emails prêt (au moins 1-2 adresses par campagne)

---

## 1. Vérifier le warmup

Dans le dashboard Instantly → **Warmup** :

| Métrique | Seuil minimum | Idéal |
|----------|---------------|-------|
| Jours de warmup | 14 jours | 21+ jours |
| Emails envoyés/jour | 5-10 | 15-20 |
| Taux de réponse warmup | > 60% | > 80% |
| Spam score | < 5% | < 2% |

**Ne pas lancer de campagne tant que le warmup n'est pas mature.** Une campagne prématurée brûle le domaine.

---

## 2. Créer une campagne (manuellement)

Dashboard Instantly → **Campaigns** → **New Campaign**

### Configuration de base

| Champ | Valeur |
|-------|--------|
| Campaign name | `{niche} — {date}` (ex: `kiné-bordeaux-20260701`) |
| Sending domain | Sélectionner le domaine vérifié |
| Daily limit | 30-50 emails/jour (démarrer bas, monter progressivement) |
| Reply detection | Activé |
| Bounce handling | Automatic (suspend after 3 bounces) |

### Étapes de l'email

Dans l'onglet **Steps**, créer les 7 étapes de la séquence A/B/C :

```
Step 1  — J0    — Email A (cold contact)    — Sujet A
Step 2  — J+2   — Email B (cold contact)    — Sujet B
Step 3  — J+4   — Email C (cold contact)    — Sujet C
Step 4  — J+7   — Follow-up 1               — Sujet follow-up 1
Step 5  — J+10  — Follow-up 2               — Sujet follow-up 2
Step 6  — J+14  — Follow-up 3               — Sujet follow-up 3
Step 7  — J+21  — Break-up                  — Sujet break-up
```

Pour chaque étape :
1. Copier le contenu depuis `sequence-live/instantly/cold-contact.md`
2. Remplacer les `{niche_var}` et `{{lead_var}}` par les bonnes variables
3. Configurer les variantes A/B/C dans les paramètres de l'étape

### Variantes A/B/C

| Variante | Sujet | Corps | Active |
|----------|-------|-------|--------|
| A | Sujet par défaut | Corps complet | ✅ (100% envoi) |
| B | Sujet alternatif | Corps court | ❌ (test A/B à activer si A sous-performe) |
| C | Sujet question | Corps orienté problème | ❌ (test A/B à activer si B sous-performe) |

### Reply behavior (obligatoire)

Dans l'onglet **Reply Detection** de la campagne :

| Champ | Valeur |
|-------|--------|
| Reply detection | Activé |
| Action on reply | **Move to another sequence** |
| Target sequence | **Positive Reply Follow-up** (3-step) |
| Negative keywords | `unsubscribe`, `désabonné`, `stop`, `spam`, `not interested`, `pas intéressé` |
| Negative action | **Remove from campaign** |

**Stop condition :** Dès qu'une réponse positive est détectée, la séquence froide s'arrête immédiatement. Les steps restantes sont annulées. Le lead reçoit 3 follow-ups max (J+1, J+4, J+7) puis passe en suivi manuel.

Voir `sequence-live/instantly/cold-contact.md` → section **Positive Reply Follow-up** pour le contenu des 3 steps.

---

## 3. Créer une campagne (automatisé)

Quand le pipeline est mature, utiliser le `Sequence Creator` :

```bash
# 1. Vérifier que l'API key est dans l'environnement
export INSTANTLY_API_KEY="sk_live_..."

# 2. Créer la campagne pour une niche
python generator-engin/sequence_creator.py instantly create \
  --niche "kinésithérapeute" \
  --activate

# 3. Vérifier que la campagne a été créée
python generator-engin/sequence_creator.py instantly list

# 4. Pousser les leads
python generator-engin/sequence_creator.py instantly push-leads \
  --campaign-id "camp-123" \
  --tenant-id "client-abc"
```

---

## 4. Configuration des leads

### Upload manuel

Dashboard Instantly → **Leads** → **Import** :
- Format CSV : `email, first_name, last_name, company, phone`
- Max 500 leads par upload (recommandé)
- Vérifier les doublons avant import

### Upload automatisé

Le pipeline d'outreach pousse automatiquement les leads propres vers Instantly via `campaign.py`. Configuration dans `env.variables` :

```
INSTANTLY_API_KEY=...
INSTANTLY_DEFAULT_CAMPAIGN_ID=...
INSTANTLY_DAILY_LIMIT=50
```

---

## 5. Monitoring

### Dashboard Instantly

| Métrique | Où | Seuil d'alerte |
|----------|----|----------------|
| Taux d'ouverture | Campaign → Analytics | < 30% → changer sujet |
| Taux de réponse | Campaign → Analytics | < 5% → changer corps |
| Bounce rate | Campaign → Analytics | > 5% → vérifier liste |
| Spam complaints | Account → Reputation | > 0.1% → STOP campaign |
| Daily active emails | Warmup → Overview | < 3 → pause campaign |

### Slack notifications

Quand une métrique passe sous le seuil, Hermes envoie une notification Slack :

```
⚠️ [Instantly] Campagne "kiné-bordeaux" — taux d'ouverture à 22%
→ Recommandation : Changer le sujet de l'email A
```

## 6. Maintenance

| Fréquence | Action |
|-----------|--------|
| Hebdomadaire | Vérifier les taux d'ouverture/réponse de chaque campagne |
| Bi-mensuel | Ajouter de nouvelles adresses d'envoi au pool |
| Mensuel | Faire un audit des campagnes : arrêter les underperformers |
| Avant chaque nouvelle campagne | Vérifier que le warmup est mature |

## 7. Anti-spam rules

- Ne pas envoyer plus de **50 emails/jour** par adresse
- Espacer les envois sur la journée (pas de burst)
- Ne pas utiliser de liens raccourcis (bit.ly, etc.)
- Toujours inclure un **unsubscribe link** (obligatoire RGPD)
- Personnaliser chaque email avec les `{{lead_var}}`
- Ne pas réutiliser le même contenu pour plus de 2 campagnes consécutives
