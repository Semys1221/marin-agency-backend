# No-show — Resend

**Déclencheur :** Appel manqué (prospect absent)
**Type :** Email unitaire
**Système :** Resend

Email unique envoyé immédiatement après un appel manqué. Proposition de reprogrammation rapide.

## Template

**Sujet :** Vous avez manqué notre appel — {{entreprise}}

```
Bonjour {{nom_prospect}},

Vous aviez un appel prévu avec nous {{rdv_date}} mais nous n'avons pas pu vous joindre.

Pas d'inquiétude, ça arrive ! Je vous propose de {{proposition_rebond}}.

Réservez directement ici un créneau qui vous convient :
{{calendly_link}}

Bonne journée,

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du prospect |
| `{{rdv_date}}` | Date/heure de l'appel manqué |
| `{{proposition_rebond}}` | Proposition de rebond (ex: "reprogrammer dès cette semaine") |
| `{{calendly_link}}` | Lien Calendly |
