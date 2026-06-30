# loop.so — Intégration Webhook

loop.so est un système externe de nurturing multi-step. Hermes Agent déclenche les séquences via webhooks. loop.so gère les relances, le timing, et les conditions d'arrêt de façon autonome.

## Architecture

```
Hermes Agent
  → POST https://app.loop.so/api/webhooks/{webhook_id}
    → loop.so démarre la séquence correspondante
      → loop.so gère les relances (timing, contenu)
        → loop.so notifie Hermes (stop condition met)
```

---

## Séquences loop.so

| # | Séquence | Déclencheur | Étapes | Stop condition |
|---|----------|-------------|--------|----------------|
| 1 | Interested | Lead a montré de l'intérêt (réponse Instantly) | J0 → J2 → J5 → J8 | Lead booke un call |
| 2 | Indecision | Post-appel indécis | J+1 → J+3 → J+7 → J+30 | Lead booke ou refuse explicitement |
| 3 | Onboarding | Deal clos, nouveau client | J0 → J3 → J7 → J15 | Onboarding terminé (dashboard actif) |
| 4 | Upsell | Opportunité cross-sell | J0 → J3 → J7 | Achat ou refus explicite |

---

## Webhook Payload (Hermes → loop.so)

**Endpoint :** `POST https://app.loop.so/api/webhooks/{webhook_id}`

**Headers :**
```
Content-Type: application/json
Authorization: Bearer {LOOP_SO_API_KEY}
```

**Body commun :**
```json
{
  "event": "sequence.triggered",
  "sequence": "interested",
  "tenant_id": "client-abc",
  "lead": {
    "email": "jean@dupontfils.fr",
    "first_name": "Jean",
    "last_name": "Dupont",
    "company": "Dupont Fils",
    "phone": "+33612345678"
  },
  "metadata": {
    "campaign_id": "instantly-camp-123",
    "source": "cold-email-reply",
    "call_session_id": null
  }
}
```

**Body par séquence :**

### interested
```json
{
  "event": "sequence.triggered",
  "sequence": "interested",
  "tenant_id": "client-abc",
  "lead": {
    "email": "jean@dupontfils.fr",
    "first_name": "Jean",
    "company": "Dupont Fils"
  }
}
```

### indecision
```json
{
  "event": "sequence.triggered",
  "sequence": "indecision",
  "tenant_id": "client-abc",
  "lead": {
    "email": "jean@dupontfils.fr",
    "first_name": "Jean",
    "company": "Dupont Fils"
  },
  "metadata": {
    "call_session_id": "cs-456",
    "call_date": "2026-07-14T10:00:00Z",
    "decision": "indecis"
  }
}
```

### onboarding
```json
{
  "event": "sequence.triggered",
  "sequence": "onboarding",
  "tenant_id": "client-abc",
  "lead": {
    "email": "jean@dupontfils.fr",
    "first_name": "Jean",
    "company": "Dupont Fils"
  },
  "metadata": {
    "client_id": "client-abc-123",
    "offer": "offer-main",
    "dashboard_url": "https://client-abc.marin.app"
  }
}
```

### upsell
```json
{
  "event": "sequence.triggered",
  "sequence": "upsell",
  "tenant_id": "client-abc",
  "lead": {
    "email": "jean@dupontfils.fr",
    "first_name": "Jean",
    "company": "Dupont Fils"
  },
  "metadata": {
    "client_id": "client-abc-123",
    "current_offer": "offer-main",
    "upsell_type": "branding-equipment"
  }
}
```

---

## Webhook Return (loop.so → Hermes)

Quand une stop condition est atteinte, loop.so notifie Hermes.

**Endpoint :** `POST {ADMIN_WEBHOOK_URL}/api/loop/event`

**Payload :**
```json
{
  "event": "sequence.completed",
  "sequence": "interested",
  "lead_email": "jean@dupontfils.fr",
  "reason": "call_booked",
  "timestamp": "2026-07-14T10:00:00Z"
}
```

**Raisons possibles :**
| Reason | Signification | Action Hermes |
|--------|--------------|---------------|
| `call_booked` | Lead a booké un call | Stopper toutes les séquences pour ce lead |
| `purchase_made` | Client a acheté l'upsell | Mettre à jour le CRM, arrêter la séquence |
| `explicit_refusal` | Lead a refusé explicitement | Marquer lead `lost` |
| `timeout` | Séquence terminée sans action | Marquer lead `cold` ou archiver |

---

## Configuration loop.so

Les workflows loop.so sont configurés manuellement dans le dashboard loop.so :
- 4 workflows : Interested, Indecision, Onboarding, Upsell
- Chaque workflow a son webhook entrant (Hermes → loop.so)
- Chaque workflow a son webhook sortant (loop.so → Hermes)
- Les templates d'emails sont dans `sequence-live/loop/`
