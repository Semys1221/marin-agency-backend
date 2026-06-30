# Call Reminder — Resend

**Déclencheur :** Appel programmé (X heures avant)
**Type :** Email unitaire
**Système :** Resend

Email de rappel envoyé automatiquement avant un appel. Pas de relance — l'appel est déjà booké.

## Template

**Sujet :** Rappel : votre appel {{entreprise}} — {{rdv_date}}

```
Bonjour {{nom_prospect}},

Rappel : votre appel {{entreprise}} est prévu {{rdv_date}}.

Lien de l'appel : {{call_link}}

On se retrouve tout à l'heure pour échanger ! Si vous avez besoin de déplacer le créneau, vous pouvez le faire directement depuis le lien de confirmation.

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du prospect |
| `{{entreprise}}` | Nom de l'entreprise |
| `{{rdv_date}}` | Date/heure de l'appel |
| `{{call_link}}` | Lien de l'appel (Google Meet, Zoom, etc.) |
