# Production Go-Live

**Depends on:** `crash-test-sandbox/` (must pass green before this).
**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ)

Procédure de mise en production d’un client. Bascule les services du mode test vers le mode live, vérifie que tout fonctionne, et active le client.

## Prérequis

- [ ] Crash-test sandbox passé ✅ (tout vert)
- [ ] Contrat signé + paiement reçu (vrai client)
- [ ] Instance Vercel créée (`cp -r template clients/{tenant_id}`)
- [ ] Domaine client configuré (ou sous-domaine `{tenant}.marincie.homes`)

## Étapes

### 1. Switch API Keys

| Service | Avant (test) | Après (live) |
|---------|-------------|--------------|
| Stripe | `sk_test_...` | `sk_live_...` |
| Stripe publishable | `pk_test_...` | `pk_live_...` |
| Dropbox Sign | Clé test HelloSign | Clé production HelloSign |
| Resend | Domaine test | Domaine client vérifié |
| Supabase | Projet dev | Projet prod (ou même projet, RLS filter par tenant_id) |

**Fichiers à modifier :**
- `src/config/client.ts` — API keys du client
- `.env` du projet — variables d'env backend (si propre au client)
- Dashboard Render/Vercel — env vars si service dédié

### 2. Stripe — Activer le mode live

```bash
# 1. Vérifier que le compte Stripe est activé pour le live
stripe login
stripe config --set livemode=true

# 2. Récupérer les clés live
stripe api-keys list --live

# 3. Configurer le webhook live
stripe listen --forward-to https://api.marincie.homes/webhooks/stripe \
  --events checkout.session.completed,customer.subscription.created

# 4. Vérifier que le webhook répond
curl -X POST https://api.marincie.homes/webhooks/stripe \
  -H "Stripe-Signature: $(stripe sig)" -d '{}'
```

### 3. Dropbox Sign — Activer le mode live

```bash
# 1. Générer la clé API production depuis le dashboard HelloSign
# 2. Uploader le template de contrat final (PDF avec champs de signature)
# 3. Tester une signature avec son propre email
```

### 4. Déploiement Vercel

```bash
cd clients/{tenant_id}

# 1. Build en mode production
npm run build

# 2. Déployer sur Vercel
vercel --prod

# 3. Vérifier que le site est accessible
curl -I https://{tenant}.marincie.homes
```

### 5. Vérifications post-go-live

```
┌─────────────────────────────────────────────┐
│          PRODUCTION GO-LIVE — CHECKLIST      │
├─────────────────────────────────────────────┤
│ □ Site accessible (HTTPS)                   │
│ □ Landing page s'affiche                    │
│ □ Calendly bookable                         │
│ □ Stripe paiement live fonctionne           │
│ □ Dropbox Sign signature live fonctionne    │
│ □ Email de confirmation reçu                │
│ □ Dashboard client accessible               │
│ □ Webhooks Stripe actifs + répondent        │
│ □ Webhooks Dropbox Sign actifs              │
│ □ Supabase RLS appliquée par tenant_id      │
│ □ Env vars vérifiées (aucune clé test)      │
│ □ Support email configuré (julie@...)       │
└─────────────────────────────────────────────┘
```

### 6. Test réel (montant symbolique)

```bash
# 1. Faire un paiement réel de 1€ (remboursable)
# 2. Vérifier que le webhook Stripe reçoit l'event
# 3. Vérifier que l'email de confirmation arrive
# 4. Vérifier que le dashboard affiche le paiement
# 5. Rembourser le paiement test
```

## Rollback

Si un problème est détecté après go-live :

```bash
# 1. Re-déployer la version précédente
vercel rollback

# 2. Réactiver les clés test
# Revenir aux clés sk_test_ dans l'env

# 3. Notifier le client
# Envoyer un email "Maintenance en cours"
```

## Security

- Les clés live ne doivent jamais être commitées dans Git
- Les clés live ne doivent jamais apparaître dans les logs
- Chaque tenant_id a ses propres clés (Stripe account separate ou clés dédiées)
- Les webhooks live doivent avoir un endpoint secret unique
- Les emails live doivent avoir un domaine vérifié avec SPF/DKIM/DMARC

## Dependencies

- Compte Stripe activé pour le live (business details, IBAN)
- Domaine `marincie.homes` avec DNS configuré (MX, SPF, DKIM, DMARC)
- Dropbox Sign compte pro activé
- Resend domaine vérifié (enregistrements TXT ajoutés)
- Vercel projet lié (`vercel link` exécuté)
