# Information Requested — Resend

**Déclencheur :** Demande d'information via l'AI responder
**Type :** Email unitaire, réponse automatique
**Système :** Resend

Email unique envoyé quand un prospect demande plus d'infos. Pas de relance — le prospect a initié le contact.

## Template

**Sujet :** Suite à votre demande d'information — {{entreprise}}

```
Bonjour {{nom_prospect}},

Vous avez demandé plus d'informations sur nos services pour {{entreprise}}. Je vous remercie pour votre intérêt.

Voici ce que nous proposons aux {{niche}} :
• {{benefice_1}}
• {{benefice_2}}
• {{benefice_3}}

Ces solutions sont conçues pour vous permettre d'atteindre vos objectifs sans complexité inutile.

Souhaitez-vous que je vous booke un créneau {{rdv_date}} pour qu'on en parle en détail ? Un échange de 15 minutes suffit pour voir si notre accompagnement correspond à vos besoins.

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du prospect |
| `{{entreprise}}` | Nom de l'entreprise |
| `{{niche}}` | Secteur d'activité (grossiste, kiné, etc.) |
| `{{benefice_1/2/3}}` | 3 bénéfices clés |
| `{{rdv_date}}` | Créneau proposé |
