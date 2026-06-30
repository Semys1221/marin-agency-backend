# Service Delivery — Resend

**Déclencheur :** Livrable prêt
**Type :** Email unitaire
**Système :** Resend

Email unique envoyé quand un livrable est disponible. Pas de séquence — notification de disponibilité.

## Template

**Sujet :** Votre livrable {{produit}} est prêt — {{entreprise}}

```
Bonjour {{nom_prospect}},

Votre livrable {{produit}} est prêt pour {{entreprise}}.

Accès : {{livrable_link}}

Si vous avez besoin d'ajustements ou de précisions, notre équipe est à votre disposition sous 24h ouvrées. Vous pouvez également répondre directement à cet email.

{{gmail_signature}}
```

## Variables

| Variable | Description |
|----------|-------------|
| `{{nom_prospect}}` | Prénom du client |
| `{{produit}}` | Nom du livrable |
| `{{entreprise}}` | Nom de l'entreprise |
| `{{livrable_link}}` | Lien d'accès au livrable |
