# loop.so — Configuration des Workflows

Guide pas à pas pour configurer les 4 workflows de nurturing dans loop.so.

**Référence :** Modèles d'emails dans `context/agency-communication/sequence-live/loop/`

---

## Prérequis

- [ ] Compte loop.so créé (https://loop.so)
- [ ] Domaine d'envoi vérifié dans loop.so (SPF/DKIM ajoutés)
- [ ] Webhook entrant configuré (Hermes → loop.so)
- [ ] Webhook sortant configuré (loop.so → Hermes)

---

## Workflow 1 — Interested

**Déclencheur :** Lead a répondu à un email Instantly (montre de l'intérêt)

### Configuration

1. Dashboard loop.so → **Workflows** → **Create Workflow**
2. Nom : `Interested`
3. Type : `Nurturing`
4. Déclencheur : **Webhook entrant** → `POST /webhook/interested`
5. Webhook URL : `https://app.loop.so/api/webhooks/{webhook_id_interested}`

### Étapes

| Étape | Délai | Sujet | Corps (depuis `01-interested.md`) |
|-------|-------|-------|-----------------------------------|
| 1 | J0 | Réponse personnalisée | Contenu de `01-interested.md` → Email 1 |
| 2 | J+2 | Cas client / Social proof | Contenu Email 2 |
| 3 | J+5 | Objection handling | Contenu Email 3 |
| 4 | J+8 | Dernière relance | Contenu Email 4 |

### Stop conditions

| Condition | Action |
|-----------|--------|
| Lead booke un call Calendly | Arrêter la séquence → Webhook sortant → Hermes |
| Lead répond "désintéressé" | Arrêter → Marquer lead `cold` |
| 4 étapes envoyées sans réponse | Arrêter → Marquer lead `cold` |

### Webhook sortant

- URL : `{ADMIN_WEBHOOK_URL}/api/loop/event`
- Payload : voir `sequence-live/loop/loop-integration.md`

---

## Workflow 2 — Indecision

**Déclencheur :** Post-appel — le commercial a marqué le lead comme "indécis"

### Configuration

1. Dashboard loop.so → **Workflows** → **Create Workflow**
2. Nom : `Indecision`
3. Type : `Nurturing`
4. Déclencheur : **Webhook entrant** → `POST /webhook/indecision`
5. Webhook URL : `https://app.loop.so/api/webhooks/{webhook_id_indecision}`

### Étapes

| Étape | Délai | Sujet | Corps |
|-------|-------|-------|-------|
| 1 | J+1 | Résumé de l'appel + proposition | Contenu de `02-indecision.md` → Email 1 |
| 2 | J+3 | Information complémentaire | Contenu Email 2 |
| 3 | J+7 | Cas client similaire | Contenu Email 3 |
| 4 | J+30 | Dernière relance | Contenu Email 4 |

### Stop conditions

| Condition | Action |
|-----------|--------|
| Lead booke un call | Arrêter → Webhook sortant → Hermes |
| Lead refuse explicitement | Arrêter → Marquer lead `lost` |
| 4 étapes sans réponse | Arrêter → Marquer lead `cold` |

---

## Workflow 3 — Onboarding

**Déclencheur :** Deal clôturé — nouveau client signé

### Configuration

1. Nom : `Onboarding`
2. Type : `Onboarding`
3. Déclencheur : **Webhook entrant** → `POST /webhook/onboarding`
4. Webhook URL : `https://app.loop.so/api/webhooks/{webhook_id_onboarding}`

### Étapes

| Étape | Délai | Sujet | Corps |
|-------|-------|-------|-------|
| 1 | J0 | Bienvenue + accès dashboard | Contenu de `03-onboarding.md` → Email 1 |
| 2 | J+3 | Setup technique (PC, casque, logiciels) | Contenu Email 2 |
| 3 | J+7 | Prochaine étape : call onboarding | Contenu Email 3 |
| 4 | J+15 | Suivi : tout fonctionne ? | Contenu Email 4 |

### Stop conditions

| Condition | Action |
|-----------|--------|
| Dashboard activé (client connecté) | Arrêter → Webhook sortant → Hermes |
| Call onboarding effectué | Arrêter → Webhook sortant |
| Client demande de l'aide | Ne pas arrêter — continue + notifie Hermes |

---

## Workflow 4 — Upsell

**Déclencheur :** Opportunité cross-sell détectée (J60+ du contrat)

### Configuration

1. Nom : `Upsell`
2. Type : `Nurturing`
3. Déclencheur : **Webhook entrant** → `POST /webhook/upsell`
4. Webhook URL : `https://app.loop.so/api/webhooks/{webhook_id_upsell}`

### Étapes

| Étape | Délai | Sujet | Corps |
|-------|-------|-------|-------|
| 1 | J0 | Proposition d'upsell | Contenu de `04-upsell.md` → Email 1 |
| 2 | J+3 | Témoignage / bénéfice upsell | Contenu Email 2 |
| 3 | J+7 | Offre limitée dans le temps | Contenu Email 3 |

### Stop conditions

| Condition | Action |
|-----------|--------|
| Client achète l'upsell | Arrêter → Webhook → Mettre à jour le CRM |
| Client refuse explicitement | Arrêter → Marquer upsell `rejected` |
| 3 étapes sans réponse | Arrêter → Marquer upsell `timeout` |

---

## Vérification finale

```bash
# Tester chaque webhook avec curl
curl -X POST https://app.loop.so/api/webhooks/{webhook_id_interested} \
  -H "Content-Type: application/json" \
  -d '{"event":"sequence.triggered","sequence":"interested","tenant_id":"test","lead":{"email":"test@mailinator.com","first_name":"Test"}}'

curl -X POST https://app.loop.so/api/webhooks/{webhook_id_indecision} \
  -H "Content-Type: application/json" \
  -d '{"event":"sequence.triggered","sequence":"indecision","tenant_id":"test","lead":{"email":"test@mailinator.com","first_name":"Test"}}'

curl -X POST https://app.loop.so/api/webhooks/{webhook_id_onboarding} \
  -H "Content-Type: application/json" \
  -d '{"event":"sequence.triggered","sequence":"onboarding","tenant_id":"test","lead":{"email":"test@mailinator.com","first_name":"Test"}}'

curl -X POST https://app.loop.so/api/webhooks/{webhook_id_upsell} \
  -H "Content-Type: application/json" \
  -d '{"event":"sequence.triggered","sequence":"upsell","tenant_id":"test","lead":{"email":"test@mailinator.com","first_name":"Test"}}'
```

Chaque webhook doit retourner `200 OK`. Vérifier dans le dashboard loop.so que la séquence a bien été déclenchée.
