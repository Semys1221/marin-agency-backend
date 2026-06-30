# Invoice — Resend

**Déclencheur :** Payment/invoice sent
**Système :** Resend (transactionnel)
**Type :** Email unitaire

Email unique envoyé automatiquement lors de l'émission d'une facture. Pas de séquence — la facture est gérée par Stripe/compta.

## Template
```
Bonjour {{nom_prospect}},

Veuillez trouver ci-joint la facture pour {{produit}}.

Montant : {{montant}}
Échéance : {{echeance}}

Pour toute question, contactez-nous à {{support_email}}.

{{gmail_signature}}
```
