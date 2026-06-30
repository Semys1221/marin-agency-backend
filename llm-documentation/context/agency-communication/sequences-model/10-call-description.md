# Call Description — Resend

**Déclencheur :** Post-call summary with "lieux"
**Système :** Resend (transactionnel)
**Type :** Email unitaire

Email unique envoyé après un appel, contenant le récap des sujets discutés, les prochaines étapes et les lieux mentionnés.

## Template
```
Bonjour {{nom_prospect}},

Suite à notre appel {{rdv_date}}, voici le récapitulatif des points abordés :

Sujets discutés : {{call_topics}}
Prochaines étapes : {{next_steps}}
Lieux mentionnés : {{lieux}}

Comme convenu, je vous envoie les informations mentionnées :
• {{info_1}}
• {{info_2}}

On se tient à disposition pour la suite.

{{gmail_signature}}
```
