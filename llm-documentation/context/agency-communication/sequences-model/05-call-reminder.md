# Call Reminder — Resend

**Déclencheur :** Upcoming scheduled call
**Système :** Resend (transactionnel)
**Type :** Email unitaire

Email de rappel envoyé X heures avant un appel programmé. Pas de relance — l'appel est déjà booké.

## Template
```
Bonjour {{nom_prospect}},

Rappel : votre appel {{entreprise}} est prévu {{rdv_date}}.

Lien de l'appel : {{call_link}}

On se retrouve tout à l'heure pour échanger !

{{gmail_signature}}
```
