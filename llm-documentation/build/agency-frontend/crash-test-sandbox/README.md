# Crash-Test Sandbox

**Depends on:** `template/` + `backend-api` deployed with demo mode.
**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ)

Procédure de simulation réelle d'un parcours client complet en mode test (Stripe test mode + Dropbox Sign test mode). À exécuter avant tout go-live pour valider le pipeline frontend ↔ backend.

## Objectif

Vérifier que le funnel entier fonctionne sans risque financier ni envoi réel :

```
Landing → Qualification → Calendly → Paiement Stripe test → Signature Dropbox test → Onboarding → Dashboard
```

Chaque étape doit produire un résultat cohérent dans la base Supabase et/ou le dashboard client.

## Stack Test

| Système | Mode | Credentials |
|---------|------|-------------|
| Stripe | `test` | `pk_test_...` / `sk_test_...` |
| Dropbox Sign | `test` | `HELLOSIGN_TEST_API_KEY` |
| Calendly | Live (gratuit) | Event type existant |
| Supabase | `dev` (projet réel) | Tables dédiées `*_test` ou filtre `tenant_id` |
| Resend | `test` | Domaine vérifié — emails vers `test@mailinator.com` |

## Cartes de test Stripe

| Scénario | Card | Résultat attendu |
|----------|------|------------------|
| Paiement réussi | `4242 4242 4242 4242` | Confirmation Stripe → DB → Email |
| Paiement refusé | `4000 0000 0000 0002` | Erreur Stripe → Message clair dans le composant |
| 3D Secure | `4000 0025 0000 3155` | Challenge 3DS → Validation → Succès |
| Erreur carte | `4000 0000 0000 0001` | Message d'erreur Stripe → Composant affiche l'erreur |

## Procédure

### Prérequis

- [ ] Backend API tourne (local ou Render) avec `DEMO_MODE=true`
- [ ] Stripe en mode test — vérifier `STRIPE_SECRET_KEY` commence par `sk_test_`
- [ ] Dropbox Sign en mode test — vérifier `HELLOSIGN_API_KEY` est une clé test
- [ ] Template frontend copié dans `clients/{test-tenant}/`
- [ ] `src/config/client.ts` du test rempli avec les clés test

### Étapes

1. **Landing** → `DEMO_MODE=true` — vérifier que la page s'affiche avec les données mockées du client test
2. **Qualification** → Saisir SIRET `12345678900001` (SIRET test INSEE) → Validation ✅
3. **Calendly** → Book un event → Vérifier que le webhook reçoit `event.scheduled`
4. **Cadre** → Affiche le framework → Vérifier que le composant rend correctement
5. **Profil → Objectif → Historique → Capacité → Posture → Blocage** → Remplir le formulaire → Vérifier que chaque étape persiste en mémoire (Zustand)
6. **Paiement** → Saisir `4242 4242 4242 4242` → Vérifier que le paiement apparaît dans le dashboard Stripe (mode test)
7. **Gift** → Vérifier que l'affichage du cadeau correspond à l'offre choisie
8. **Contract** → Signer avec Dropbox Sign test → Vérifier que le contrat apparaît dans Dropbox Sign (mode test)
9. **Onboarding** → Remplir le formulaire d'onboarding → Vérifier que les données sont en DB
10. **Call 1 / Call 2** → Vérifier que les écrans de planification d'appel s'affichent

### Vérifications backend

```bash
# 1. Vérifier que la session Stripe a été créée
curl -s http://localhost:8001/api/payments/session?demo=true | jq .

# 2. Vérifier que le contrat a été signé
curl -s http://localhost:8001/api/contracts/status?demo=true | jq .

# 3. Vérifier que le client existe en DB (Supabase)
curl -s "$SUPABASE_URL/rest/v1/clients?select=*" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" | jq .

# 4. Vérifier que l'email de confirmation a été loggé
curl -s http://localhost:8001/api/email/logs?demo=true | jq .
```

## Résultat attendu

```
┌─────────────────────────────────────────────┐
│          CRASH-TEST SANDBOX — RAPPORT        │
├─────────────────────────────────────────────┤
│ ✅ Landing → OK                             │
│ ✅ Qualification → OK                       │
│ ✅ Calendly → OK                            │
│ ✅ Cadre → OK                               │
│ ✅ Profil → OK                              │
│ ✅ Struve → Paiement réussi                 │
│ ✅ Dropbox → Signature réussi               │
│ ✅ Onboarding → OK                          │
│ ✅ Database → Client créé                   │
│ ✅ Email → Log créé                         │
├─────────────────────────────────────────────┤
│ Statut : ✅ Tout vert → Prêt pour go-live   │
└─────────────────────────────────────────────┘
```

## Edge Cases

| Scénario | Action | Résultat attendu |
|----------|--------|------------------|
| Paiement refusé | Carte `4000 0000 0000 0002` | Message "Paiement refusé" + pas de passage à l'étape suivante |
| 3D Secure échoué | Carte `4000 0025 0000 3155` + échouer le challenge | Retour à l'étape paiement |
| Contrat non signé | Fermer Dropbox Sign sans signer | Reste bloqué à l'étape signature |
| SIRET invalide | `00000000000000` | Message "SIRET invalide" |
| Session expirée | Attendre 30 min sans action | Redirection vers le début du funnel |

## Dependencies

- Stripe test mode = auto (clé `sk_test_`)
- Dropbox Sign test mode = auto (clé test HelloSign)
- Calendly = pas de mode test — utiliser un event type dédié "test"
- Resend = pas de mode test — envoyer vers `test@mailinator.com`
