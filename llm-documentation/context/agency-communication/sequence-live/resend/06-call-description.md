# Call Description — Resend

**Déclencheur :** Post-appel (résumé + lieux mentionnés)
**Type :** Email unitaire
**Système :** Resend

Email unique envoyé après un appel, contenant le récap des sujets discutés, les prochaines étapes et les lieux mentionnés.

## Template

**Sujet :** Récapitulatif de notre appel — {{entreprise}}

```
Bonjour {{nom_prospect}},

Suite à notre appel {{rdv_date}}, voici le récapitulatif des points abordés :

Sujets discutés : {{call_topics}}
Prochaines étapes : {{next_steps}}
Lieux mentionnés : {{lieux}}

Comme convenu, je vous envoie les informations mentionnées :
• {{info_1}}
• {{info_2}}

On se tient à disposition pour la suite. N'hésitez pas si vous avez des questions.

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du prospect |
| `{{entreprise}}` | Nom de l'entreprise |
| `{{rdv_date}}` | Date de l'appel |
| `{{call_topics}}` | Sujets discutés |
| `{{next_steps}}` | Prochaines étapes |
| `{{lieux}}` | Lieux mentionnés |
| `{{info_1/2}}` | Informations complémentaires |
