# Invoice — Resend

**Déclencheur :** Facture émise (Stripe/compta)
**Type :** Email unitaire
**Système :** Resend

Email unique envoyé automatiquement lors de l'émission d'une facture. Pas de séquence.

## Template

**Sujet :** Votre facture {{produit}} — {{montant}}

```
Bonjour {{nom_prospect}},

Veuillez trouver ci-joint la facture pour {{produit}}.

Montant : {{montant}}
Échéance : {{echeance}}

Pour toute question concernant cette facture, contactez-nous à {{support_email}}.

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du client |
| `{{produit}}` | Produit/service facturé |
| `{{montant}}` | Montant TTC |
| `{{echeance}}` | Date d'échéance |
| `{{support_email}}` | Email support |
