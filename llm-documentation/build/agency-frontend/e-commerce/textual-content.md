# Textual Content — E-Commerce Funnel (Grossiste)

Modules de contenu prêts à l'emploi pour chaque étape du funnel e-commerce. Structure clé-valeur pour intégration directe dans les composants React.

```
Format :
- headline       → Titre principal (H1)
- subheadline    → Sous-titre (H2)
- description    → Texte de corps
- cta            → Bouton d'action
- fields[]       → Champs de formulaire {label, placeholder, type, required, options?}
- states{}       → Variants : loading, empty, error, success
- meta{}         → SEO : title, description
```

---

## 1. Landing Page

```json
{
  "headline": "Catalogue grossiste — Prix professionnels",
  "subheadline": "Accédez à notre sélection de produits aux meilleurs prix. Inscription gratuite.",
  "heroCta": "Voir le catalogue",
  "heroSecondary": "Demander un devis personnalisé",
  "sections": [
    {
      "title": "Notre catalogue",
      "description": "Des centaines de références adaptées aux revendeurs, e-commerçants et grossistes.",
      "products": []
    },
    {
      "title": "Pourquoi nous choisir ?",
      "items": [
        { "icon": "truck", "title": "Livraison rapide", "text": "Expédition sous 24-72h partout en France" },
        { "icon": "euro", "title": "Prix dégressifs", "text": "Plus vous achetez, moins vous payez à l'unité" },
        { "icon": "headset", "title": "Service client dédié", "text": "Un commercial attitré pour vous accompagner" },
        { "icon": "shield", "title": "Qualité garantie", "text": "Produits contrôlés, conformes aux normes européennes" }
      ]
    },
    {
      "title": "Comment ça marche",
      "steps": [
        "Inscription et vérification SIRET",
        "Appel avec notre équipe commerciale",
        "Devis personnalisé",
        "Commande et suivi Shopify"
      ]
    }
  ],
  "meta": { "title": "Marin Grossiste — Catalogue B2B", "description": "Catalogue grossiste en ligne. Prix professionnels, livraison rapide, service client dédié." }
}
```

---

## 2. Qualification SIRET

```json
{
  "headline": "Vérifions votre éligibilité",
  "description": "Seuls les professionnels peuvent accéder à nos prix grossistes. La vérification prend 2 secondes.",
  "fields": [
    { "name": "siret", "label": "Numéro SIRET", "placeholder": "123 456 789 00012", "type": "text", "required": true, "maxLength": 14, "pattern": "[0-9]{14}" }
  ],
  "cta": "Vérifier mon SIRET",
  "states": {
    "idle": { "message": "Saisissez votre numéro SIRET à 14 chiffres." },
    "loading": { "message": "Vérification en cours…" },
    "valid": { "message": "SIRET valide — Bienvenue ! Vous pouvez accéder à nos prix pro.", "nextStep": "Découvrir le catalogue" },
    "invalid": { "message": "Ce numéro SIRET n'est pas reconnu. Vérifiez et réessayez.", "hint": "Vous devez être un professionnel immatriculé pour accéder à nos prix." },
    "error": { "message": "Service de vérification indisponible. Réessayez ou contactez-nous." }
  }
}
```

---

## 3. Calendly

```json
{
  "headline": "Prenez rendez-vous avec notre équipe",
  "description": "Un commercial spécialisé dans la vente B2B vous rappelle sous 24h pour discuter de vos besoins.",
  "embedType": "calendly",
  "calendlyUrl": "https://calendly.com/marin-agency/grossiste",
  "states": {
    "loading": { "message": "Chargement du calendrier…" },
    "booked": { "message": "Rendez-vous confirmé ! Un email récapitulatif vous a été envoyé.", "nextSteps": ["Notre commercial vous appelle à l'heure convenue", "Préparez vos volumes et besoins", "Devis personnalisé après l'appel"] },
    "error": { "message": "Calendrier indisponible. Rafraîchissez ou contactez-nous directement." }
  }
}
```

---

## 4. Cadre

```json
{
  "headline": "Comment nous travaillons ensemble",
  "description": "Le cadre de notre relation commerciale est simple et transparent.",
  "points": [
    "Nous fournissons des produits en gros aux revendeurs et grossistes B2B",
    "Prix dégressifs selon vos volumes — plus vous commandez, moins vous payez",
    "Expédition sous 24 à 72h ouvrées",
    "Un commercial dédié pour vous accompagner dans la durée"
  ],
  "cta": "Je comprends, continuer",
  "states": {
    "empty": { "message": "Découvrez comment nous travaillons avec nos partenaires grossistes." }
  }
}
```

---

## 5. Profil

```json
{
  "headline": "Parlez-nous de votre activité",
  "description": "Ces informations nous aident à vous proposer les meilleurs produits et conditions.",
  "fields": [
    { "name": "businessType", "label": "Quel type de revendeur êtes-vous ?", "type": "select", "required": true, "options": ["Détaillant physique", "E-commerçant", "Grossiste / semi-grossiste", "Artisan", "Autre professionnel"] },
    { "name": "monthlyVolume", "label": "Quel volume mensuel estimez-vous commander ?", "type": "select", "required": true, "options": ["< 100 unités", "100 - 500 unités", "500 - 1 000 unités", "1 000 - 5 000 unités", "> 5 000 unités"] },
    { "name": "salesChannels", "label": "Quels sont vos canaux de vente ?", "type": "checkbox", "options": ["Boutique physique", "Site e-commerce", "Marketplace (Amazon, Cdiscount, etc.)", "Vente directe B2B", "Grossiste / revente"] },
    { "name": "yearsActive", "label": "Depuis combien de temps exercez-vous ?", "type": "select", "options": ["Moins d'un an", "1-3 ans", "3-5 ans", "5-10 ans", "Plus de 10 ans"] }
  ],
  "cta": "Suivant",
  "states": {
    "loading": { "message": "Enregistrement…" },
    "error": { "message": "Une erreur est survenue." }
  }
}
```

---

## 6. Problème

```json
{
  "headline": "Quels sont vos besoins actuels ?",
  "description": "Dites-nous ce qui vous manque ou ce qui pourrait être amélioré.",
  "fields": [
    { "name": "painPoints", "label": "Sélectionnez vos principaux défis", "type": "checkbox", "options": [
      "Difficulté à trouver des fournisseurs fiables",
      "Problèmes de qualité ou de délais",
      "Marges insuffisantes sur mes produits actuels",
      "Gamme de produits trop limitée",
      "Processus de commande trop long",
      "Manque de réactivité de mon fournisseur actuel"
    ]},
    { "name": "otherNeed", "label": "Autre besoin (optionnel)", "type": "text", "placeholder": "Précisez…", "required": false }
  ],
  "cta": "Suivant",
  "states": {
    "empty": { "message": "Sélectionnez au moins un besoin pour continuer." },
    "error": { "message": "Une erreur est survenue." }
  }
}
```

---

## 7. Objectif

```json
{
  "headline": "Quel est votre objectif ?",
  "description": "Aidez-nous à comprendre ce que vous visez pour vous faire la meilleure offre.",
  "fields": [
    { "name": "targetVolume", "label": "Quel volume d'achat mensuel visez-vous ?", "type": "number", "placeholder": "500", "min": 1, "required": true },
    { "name": "monthlyBudget", "label": "Budget mensuel approximatif (€)", "type": "number", "placeholder": "5 000", "min": 0, "required": true },
    { "name": "deliveryExpectation", "label": "Délais de livraison attendus", "type": "select", "options": ["24h", "48h", "72h", "1 semaine", "Pas d'urgence particulière"] },
    { "name": "specificNeeds", "label": "Avez-vous des besoins spécifiques ?", "type": "checkbox", "options": ["Marque blanche", "Personnalisation produit", "Conditionnement spécial", "Logistique externalisée (drop shipping)", "Autre"] }
  ],
  "cta": "Suivant",
  "states": {
    "loading": { "message": "Analyse de vos objectifs…" },
    "error": { "message": "Une erreur est survenue." }
  }
}
```

---

## 8. Solution

```json
{
  "headline": "Notre offre pour votre activité",
  "description": "Une solution adaptée à votre profil et à vos objectifs.",
  "solution": {
    "summary": "Des produits de qualité aux meilleurs prix, avec un accompagnement commercial dédié.",
    "features": [
      { "icon": "package", "title": "Large gamme", "text": "Des centaines de références adaptées à votre marché." },
      { "icon": "euro", "title": "Prix négociés", "text": "Conditions tarifaires dégressives selon vos volumes." },
      { "icon": "truck", "title": "Logistique optimisée", "text": "Expédition rapide, suivi en temps réel via Shopify." },
      { "icon": "headset", "title": "Accompagnement", "text": "Un commercial dédié pour vous conseiller et vous suivre." },
      { "icon": "bar-chart", "title": "Dashboard Shopify", "text": "Suivez vos commandes, stocks et historiques en temps réel." }
    ]
  },
  "cta": "Cette offre m'intéresse — voir le devis",
  "secondaryCta": "J'ai besoin de plus d'informations"
}
```

---

## 9. Proposition — Devis

```json
{
  "headline": "Votre devis personnalisé",
  "description": "Récapitulatif des produits et conditions proposés.",
  "sections": [
    { "title": "Produits sélectionnés", "fields": ["Références", "Quantités", "Prix unitaire", "Total"] },
    { "title": "Conditions", "fields": ["Délai de livraison estimé", "Frais de port", "Conditions de paiement"] }
  ],
  "interestBar": {
    "label": "À quel niveau êtes-vous intéressé par cette offre ?",
    "min": 1,
    "max": 10,
    "hint": "Votre réponse nous aide à prioriser votre dossier."
  },
  "cta": "J'accepte — passer au paiement",
  "secondaryCta": "Modifier ma sélection",
  "states": {
    "loading": { "message": "Génération de votre devis…" },
    "error": { "message": "Impossible de générer le devis. Veuillez réessayer." }
  }
}
```

---

## 10. Paiement — Shopify Checkout

```json
{
  "headline": "Finalisez votre commande",
  "description": "Vous allez être redirigé vers la page de paiement sécurisée Shopify pour finaliser votre achat.",
  "orderSummary": {
    "items": [
      { "label": "Produits", "value": "Détail dans le récapitulatif" },
      { "label": "Total", "value": "Montant total TTC" }
    ]
  },
  "redirectInfo": "Vous quittez momentanément notre site pour le paiement sécurisé Shopify. Vous serez redirigé automatiquement vers votre dashboard de suivi après la transaction.",
  "cta": "Procéder au paiement sécurisé",
  "states": {
    "idle": { "message": "Prêt à finaliser votre commande." },
    "redirecting": { "message": "Redirection vers Shopify Checkout…" },
    "success": { "message": "Paiement confirmé ! Votre commande est en cours de traitement.", "nextSteps": ["Email de confirmation envoyé", "Préparation de votre commande", "Notification dès expédition"] },
    "error": { "message": "Le paiement a échoué. Vous pouvez réessayer depuis votre panier.", "possibleReasons": ["Fonds insuffisants", "Coordonnées bancaires incorrectes", "Problème de connexion Shopify"] },
    "cancelled": { "message": "Paiement annulé. Votre panier est conservé." }
  }
}
```

---

## 11. Suivi — Dashboard Shopify

```json
{
  "headline": "Commande confirmée !",
  "description": "Votre commande est en cours de préparation. Suivez-la en temps réel depuis votre dashboard Shopify.",
  "orderStatus": {
    "confirmed": "Commande confirmée",
    "preparation": "En cours de préparation",
    "shipped": "Expédiée",
    "delivered": "Livrée"
  },
  "infoCards": [
    { "title": "Numéro de commande", "value": "#XXXXX" },
    { "title": "Statut", "value": "Confirmée" },
    { "title": "Livraison estimée", "value": "Sous 24-72h" },
    { "title": "Transporteur", "value": "À définir" }
  ],
  "trackingCta": "Suivre ma commande sur Shopify",
  "supportCta": "Besoin d'aide ? Contactez notre service client",
  "states": {
    "loading": { "message": "Chargement des informations de suivi…" },
    "error": { "message": "Impossible de récupérer les informations de suivi. Vérifiez votre email pour le lien direct." }
  }
}
```
