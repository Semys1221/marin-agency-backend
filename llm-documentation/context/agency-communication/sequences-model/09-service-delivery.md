# Service Delivery — Resend

**Déclencheur :** Service delivered
**Système :** Resend (transactionnel)
**Type :** Email unitaire

Email unique envoyé quand un livrable est prêt. Pas de séquence — notification de disponibilité.

## Template
```
Bonjour {{nom_prospect}},

Votre livrable {{produit}} est prêt pour {{entreprise}}.

Accès : {{livrable_link}}

Si vous avez besoin d'ajustements, notre équipe est à votre disposition sous 24h.

{{gmail_signature}}
```
