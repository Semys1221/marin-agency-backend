# Textual Content — Marin Agency Funnel

Modules de contenu prêts à l'emploi pour chaque étape du funnel. Structure clé-valeur pour intégration directe dans les composants React.

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
  "headline": "Transformez vos prospects en clients avec Marin",
  "subheadline": "L'agence qui construit votre pipeline de vente clé en main — de la prospection à la signature",
  "heroCta": "Réservez votre appel gratuit",
  "heroSecondary": "En savoir plus",
  "sections": [
    {
      "title": "Comment ça marche",
      "steps": [
        "Qualification SIRET instantanée",
        "Appel découverte avec notre équipe",
        "Solution sur mesure en 15 jours",
        "Accompagnement 90 jours avec garantie résultat"
      ]
    },
    {
      "title": "Nos offres",
      "items": [
        { "name": "Offre Principale", "target": "10 ventes", "price": "2 500 €", "guarantee": "10 ventes ou on continue" },
        { "name": "Offre Secondaire", "target": "15 appels qualifiés", "price": "1 900 €", "guarantee": "15 appels ou on continue" }
      ]
    },
    {
      "title": "Garantie",
      "body": "10 ventes ou nous continuons jusqu'à obtention du résultat. Nous sommes payés sur la performance, pas sur la promesse."
    }
  ],
  "meta": { "title": "Marin — Agence de prospection B2B", "description": "Pipeline de vente clé en main pour grossistes B2B. Setup 15 jours, accompagnement 90 jours, résultat garanti." }
}
```

---

## 2. Qualification SIRET

```json
{
  "headline": "Vérifions votre éligibilité",
  "description": "Avant de passer un appel, tous vos prospects sont vérifiés en SIRET instantanément.",
  "fields": [
    { "name": "siret", "label": "Numéro SIRET", "placeholder": "123 456 789 00012", "type": "text", "required": true, "maxLength": 14, "pattern": "[0-9]{14}" }
  ],
  "cta": "Vérifier",
  "states": {
    "idle": { "message": "Saisissez votre numéro SIRET à 14 chiffres" },
    "loading": { "message": "Vérification en cours…" },
    "valid": { "message": "SIRET valide — vous êtes éligible", "nextStep": "Choisir un créneau" },
    "invalid": { "message": "Numéro SIRET non trouvé. Vérifiez et réessayez.", "hint": "Format attendu : 14 chiffres (ex: 12345678900012)" },
    "error": { "message": "Le service de vérification est temporairement indisponible. Réessayez dans quelques minutes." }
  }
}
```

---

## 3. Calendly

```json
{
  "headline": "Choisissez votre créneau",
  "description": "Un de nos commerciaux vous rappelle dans les 24h. Tous nos créneaux sont synchronisés en temps réel.",
  "embedType": "calendly",
  "calendlyUrl": "https://calendly.com/marin-agency/appel-decouverte",
  "states": {
    "loading": { "message": "Chargement du calendrier…" },
    "booked": { "message": "Rendez-vous confirmé ! Un email récapitulatif vous a été envoyé.", "nextSteps": ["Email de confirmation envoyé", "Rappel automatique 24h avant", "Notre commercial vous contactera à l'heure dite"] },
    "error": { "message": "Impossible de charger le calendrier. Rafraîchissez la page ou contactez-nous directement." }
  }
}
```

---

## 4. Cadre

```json
{
  "headline": "Le cadre de notre collaboration",
  "description": "Avant d'aller plus loin, posons le cadre.",
  "points": [
    "Nous travaillons avec des grossistes B2B qui souhaitent externaliser leur prospection",
    "Accompagnement de 90 jours avec un objectif clair et garanti",
    "Vous conservez la main sur toutes les décisions finales",
    "Aucun engagement au-delà de la période définie — pas de reconduction forcée"
  ],
  "cta": "Je comprends le cadre, continuer",
  "states": {
    "empty": { "message": "Préparez-vous à définir le cadre de votre accompagnement." }
  }
}
```

---

## 5. Profil

```json
{
  "headline": "Parlez-nous de votre entreprise",
  "description": "Ces informations nous permettent de personnaliser notre accompagnement.",
  "fields": [
    { "name": "sector", "label": "Secteur d'activité", "type": "select", "required": true, "options": ["Textile", "Alimentaire", "Électronique", "Bricolage", "Santé & Bien-être", "Automobile", "Autre"] },
    { "name": "yearsActive", "label": "Depuis combien de temps êtes-vous en activité ?", "type": "select", "options": ["Moins d'un an", "1-3 ans", "3-5 ans", "5-10 ans", "Plus de 10 ans"] },
    { "name": "salesTeamSize", "label": "Combien de commerciaux avez-vous ?", "type": "number", "placeholder": "0 si vous n'avez pas d'équipe", "min": 0 },
    { "name": "annualRevenue", "label": "Chiffre d'affaires annuel (€)", "type": "select", "options": ["< 100k", "100k - 500k", "500k - 1M", "1M - 5M", "> 5M"] }
  ],
  "cta": "Suivant",
  "states": {
    "loading": { "message": "Enregistrement de votre profil…" },
    "error": { "message": "Une erreur est survenue. Veuillez réessayer." }
  }
}
```

---

## 6. Problème

```json
{
  "headline": "Quels sont vos défis actuels ?",
  "description": "Identifions les points de friction dans votre processus de vente actuel.",
  "fields": [
    { "name": "challenges", "label": "Sélectionnez vos principaux défis", "type": "checkbox", "options": [
      "Difficulté à trouver des prospects qualifiés",
      "Mes commerciaux passent trop de temps à prospecter",
      "Manque de visibilité sur mon pipeline de vente",
      "Taux de transformation insuffisant",
      "Processus de vente non structuré",
      "Rotation trop élevée des commerciaux"
    ]},
    { "name": "otherChallenge", "label": "Autre défi (optionnel)", "type": "text", "placeholder": "Précisez…", "required": false }
  ],
  "cta": "Suivant",
  "states": {
    "empty": { "message": "Sélectionnez au moins un défi pour continuer." },
    "error": { "message": "Une erreur est survenue." }
  }
}
```

---

## 7. Objectif

```json
{
  "headline": "Quel est votre objectif ?",
  "description": "Fixons un cap clair pour les 90 prochains jours.",
  "fields": [
    { "name": "salesTarget", "label": "Combien de ventes souhaitez-vous réaliser sur 90 jours ?", "type": "number", "placeholder": "10", "min": 1, "required": true },
    { "name": "avgBasket", "label": "Panier moyen visé (€)", "type": "number", "placeholder": "1 500", "min": 0, "required": true },
    { "name": "deadline", "label": "Date idéale de début", "type": "date", "required": true },
    { "name": "hasTargetList", "label": "Avez-vous déjà une liste de prospects cibles ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui, j'ai une liste" },
      { "value": "no", "label": "Non, je pars de zéro" },
      { "value": "partial", "label": "J'ai quelques pistes" }
    ]}
  ],
  "cta": "Suivant",
  "states": {
    "loading": { "message": "Analyse de vos objectifs…" },
    "error": { "message": "Une erreur est survenue." }
  }
}
```

---

## 8. Historique

```json
{
  "headline": "Votre historique de prospection",
  "description": "Comprendre votre passé pour mieux construire votre futur.",
  "fields": [
    { "name": "pastAgency", "label": "Avez-vous déjà travaillé avec une agence de prospection ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui, une expérience positive" },
      { "value": "mixed", "label": "Oui, mais mitigé" },
      { "value": "no", "label": "Non, c'est une première" }
    ]},
    { "name": "pastFeedback", "label": "Qu'est-ce qui a fonctionné ou non ?", "type": "textarea", "placeholder": "Partagez votre expérience…", "required": false },
    { "name": "currentCrm", "label": "Comment gérez-vous vos leads actuellement ?", "type": "radio", "options": [
      { "value": "crm", "label": "CRM (HubSpot, Pipedrive, etc.)" },
      { "value": "excel", "label": "Excel / Google Sheets" },
      { "value": "nothing", "label": "Aucun outil — tout est dans ma tête" },
      { "value": "other", "label": "Autre" }
    ]},
    { "name": "currentProcess", "label": "Décrivez votre processus de vente actuel en quelques mots", "type": "textarea", "placeholder": "Par exemple : « Je reçois des leads via mon site, je les appelle un par un, je signe sur devis papier… »", "required": false }
  ],
  "cta": "Suivant"
}
```

---

## 9. Capacité

```json
{
  "headline": "Budget et capacité",
  "description": "Assurons-nous que nous sommes alignés sur les moyens.",
  "fields": [
    { "name": "budget", "label": "Quel budget êtes-vous prêt à investir pour un accompagnement clé en main ?", "type": "select", "options": ["1 500 - 2 000 €", "2 000 - 2 500 €", "2 500 - 3 000 €", "3 000 € et plus"] },
    { "name": "absorptionCapacity", "label": "Avez-vous la capacité d'absorber 10 nouvelles ventes en 90 jours ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui, sans problème" },
      { "value": "maybe", "label": "Oui, mais avec des ajustements" },
      { "value": "no", "label": "Non, c'est trop" }
    ]},
    { "name": "availability", "label": "Vos commerciaux sont-ils disponibles pour les appels de suivi tous les 15 jours ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui" },
      { "value": "limited", "label": "Disponibilités limitées" },
      { "value": "no", "label": "Non" }
    ]}
  ],
  "cta": "Suivant"
}
```

---

## 10. Posture

```json
{
  "headline": "Votre posture d'achat",
  "description": "Quelques questions pour comprendre votre processus de décision.",
  "fields": [
    { "name": "decisionMaker", "label": "Êtes-vous le preneur de décision final ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui, je décide seul" },
      { "value": "team", "label": "Je décide avec mon équipe" },
      { "value": "superior", "label": "Je dois consulter ma direction" }
    ]},
    { "name": "urgency", "label": "Quel est votre niveau d'urgence pour démarrer ?", "type": "radio", "options": [
      { "value": "now", "label": "Le plus tôt possible" },
      { "value": "month", "label": "Dans le mois" },
      { "value": "quarter", "label": "Dans le trimestre" },
      { "value": "exploring", "label": "Je me renseigne" }
    ]},
    { "name": "budgetApproved", "label": "Avez-vous déjà validé un budget pour ce projet ?", "type": "radio", "options": [
      { "value": "yes", "label": "Oui, budget approuvé" },
      { "value": "pending", "label": "En cours de validation" },
      { "value": "no", "label": "Pas encore" }
    ]}
  ],
  "cta": "Suivant"
}
```

---

## 11. Blocage

```json
{
  "headline": "Qu'est-ce qui vous freine ?",
  "description": "Identifions vos objections pour y répondre dès maintenant.",
  "fields": [
    { "name": "objections", "label": "Quelles sont vos principales interrogations ?", "type": "checkbox", "options": [
      "Je ne suis pas sûr que cela fonctionne pour mon secteur",
      "Le prix est un frein pour moi",
      "J'ai déjà été déçu par des prestataires",
      "Mon équipe n'est pas prête",
      "Je manque de temps pour m'impliquer",
      "Je veux voir des résultats avant d'investir"
    ]},
    { "name": "fears", "label": "Avez-vous des craintes spécifiques sur l'externalisation de la prospection ?", "type": "textarea", "placeholder": "Exprimez librement vos craintes…", "required": false },
    { "name": "blocker", "label": "Qu'est-ce qui pourrait vous empêcher de passer à l'action aujourd'hui ?", "type": "textarea", "placeholder": "Soyez honnête, c'est important pour nous.", "required": false }
  ],
  "cta": "Suivant"
}
```

---

## 12. Solution

```json
{
  "headline": "Voici comment nous allons vous aider",
  "description": "Notre solution est construite autour de vos besoins et de vos objectifs.",
  "solution": {
    "summary": "Un pipeline de vente complet, clé en main, de la prospection à la signature.",
    "features": [
      { "icon": "search", "title": "Pipeline complet", "text": "Scraping → qualification → appel → closing → suivi. Tout est automatisé et orchestré." },
      { "icon": "calendar", "title": "Accompagnement 90 jours", "text": "Un commercial dédié, des appels tous les 15 jours, un ajustement continu." },
      { "icon": "bar-chart", "title": "Dashboard temps réel", "text": "Suivez vos performances en direct : appels, ventes, taux de transformation." },
      { "icon": "headphones", "title": "Équipement fourni", "text": "Casque Jabra, logiciels, fond virtuel — votre équipe n'a qu'à se connecter." },
      { "icon": "shield", "title": "Garantie résultat", "text": "Objectif non atteint ? Nous continuons sans frais jusqu'à l'obtention." }
    ]
  },
  "cta": "Cette solution est faite pour moi",
  "secondaryCta": "J'ai encore des questions"
}
```

---

## 13. Projection

```json
{
  "headline": "Imaginez vos résultats dans 90 jours",
  "description": "Visualisons concrètement ce que notre collaboration peut vous apporter.",
  "projections": [
    { "metric": "Chiffre d'affaires", "scenario": "+X %", "detail": "Basé sur votre panier moyen et le nombre de ventes garanti." },
    { "metric": "Pipeline", "scenario": "10 nouvelles ventes", "detail": "Un flux constant de prospects qualifiés et convertis." },
    { "metric": "Productivité", "scenario": "2x plus efficace", "detail": "Vos commerciaux ne prospectent plus — ils vendent." }
  ],
  "questions": [
    "À quoi ressemblerait votre entreprise dans 90 jours avec 10 ventes supplémentaires ?",
    "Quel impact cela aurait-il sur votre équipe et votre moral ?",
    "Êtes-vous prêt à faire le premier pas ?"
  ],
  "cta": "Je suis prêt, passons à l'offre",
  "states": {
    "loading": { "message": "Calcul de votre projection personnalisée…" }
  }
}
```

---

## 14. Workflow

```json
{
  "headline": "Comment ça se passe concrètement",
  "description": "Un process clair, étape par étape, du jour 1 au jour 90.",
  "timeline": [
    { "phase": "Setup", "duration": "Jours 1-15", "tasks": ["Configuration de votre dashboard", "Création de vos campagnes de prospection", "Installation et test des équipements", "Formation de votre équipe commerciale"] },
    { "phase": "Lancement", "duration": "Jours 16-30", "tasks": ["Démarrage des campagnes email", "Premiers appels entrants", "Ajustements des scripts et messages", "Premier bilan bi-mensuel"] },
    { "phase": "Optimisation", "duration": "Jours 31-60", "tasks": ["Analyse des performances", "A/B testing des séquences", "Affinage du ciblage", "Appels de suivi tous les 15 jours"] },
    { "phase": "Résultats", "duration": "Jours 61-90", "tasks": ["Accélération de la cadence", "Closing des opportunités chaudes", "Bilan final et plan de continuation"] }
  ],
  "cta": "Je comprends le process, passons au devis",
  "states": {
    "empty": { "message": "Découvrez le déroulement de votre accompagnement." }
  }
}
```

---

## 15. Coût de l'Inaction

```json
{
  "headline": "Le coût de l'inaction",
  "description": "Chaque jour sans prospection, c'est de l'argent que vous laissez à vos concurrents.",
  "arguments": [
    { "stat": "X ventes perdues par mois", "detail": "En moyenne, nos clients identifient X opportunités manquées chaque mois avant de nous contacter." },
    { "stat": "Retard sur vos concurrents", "detail": "Pendant que vous hésitez, vos concurrents investissent dans leur pipeline de vente." },
    { "stat": "X € de manque à gagner sur 12 mois", "detail": "Multipliez vos ventes potentielles par votre panier moyen. Le calcul est simple." }
  ],
  "cta": "Je ne veux plus attendre — voyons l'offre",
  "secondaryCta": "J'ai besoin d'y réfléchir encore"
}
```

---

## 16. Proposition — Devis

```json
{
  "headline": "Votre devis personnalisé",
  "description": "Récapitulatif de votre projet et de l'offre sélectionnée.",
  "sections": [
    { "title": "Récapitulatif de vos besoins", "fields": ["Secteur", "Objectif de ventes", "Panier moyen", "Équipe commerciale"] },
    { "title": "Offre sélectionnée", "fields": ["Type d'offre", "Prix", "Durée", "Garantie"] },
    { "title": "Services inclus", "fields": ["Dashboard temps réel", "Campagnes de prospection", "Équipement fourni", "Appels de suivi", "Support prioritaire"] }
  ],
  "interestBar": {
    "label": "À quel niveau êtes-vous intéressé ?",
    "min": 1,
    "max": 10,
    "hint": "Votre réponse nous aide à personnaliser notre suivi."
  },
  "cta": "J'accepte — passer au paiement",
  "secondaryCta": "Modifier mes réponses",
  "states": {
    "loading": { "message": "Génération de votre devis…" },
    "error": { "message": "Impossible de générer le devis. Veuillez réessayer." }
  }
}
```

---

## 17. Paiement Stripe

```json
{
  "headline": "Finalisez votre inscription",
  "description": "Paiement sécurisé par Stripe. Vous recevrez une facture par email.",
  "orderSummary": {
    "items": [
      { "label": "Offre sélectionnée", "value": "Offre Principale / Secondaire" },
      { "label": "Prix total", "value": "2 500 € / 1 900 €" },
      { "label": "TVA", "value": "Non applicable (art. 293 B CGI)" }
    ]
  },
  "paymentMethods": ["Carte bancaire", "SEPA"],
  "cta": "Payer et commencer",
  "secureBadge": "Paiement 100% sécurisé par Stripe",
  "states": {
    "idle": { "message": "Prêt à finaliser votre inscription." },
    "loading": { "message": "Traitement du paiement…" },
    "success": { "message": "Paiement confirmé ! Bienvenue chez Marin 🎉", "nextSteps": ["Email de confirmation envoyé", "Votre cadeau de bienvenue vous attend", "Configuration de votre équipe dans les 24h"] },
    "error": { "message": "Le paiement a échoué. Vérifiez vos informations et réessayez.", "possibleReasons": ["Fonds insuffisants", "Coordonnées bancaires incorrectes", "Blocage bancaire"] },
    "cancelled": { "message": "Paiement annulé. Vous pouvez reprendre à tout moment." }
  }
}
```

---

## 18. Cadeau — Jabra Evolve2 75

```json
{
  "headline": "Félicitations ! Vous recevez un cadeau de bienvenue 🎁",
  "description": "En tant que nouveau client, vous recevez un upgrade casque Jabra Evolve2 75 (valeur 300 €).",
  "gift": {
    "name": "Jabra Evolve2 75",
    "value": "300 €",
    "image": "jabra-evolve2-75.png",
    "features": ["Casque sans fil premium", "Réduction de bruit active", "Microphone professionnel", "Confort longue durée"]
  },
  "fields": [
    { "name": "fullName", "label": "Nom et prénom", "type": "text", "placeholder": "Jean Dupont", "required": true },
    { "name": "street", "label": "Adresse postale", "type": "text", "placeholder": "123 Rue de la République", "required": true },
    { "name": "postalCode", "label": "Code postal", "type": "text", "placeholder": "75001", "required": true, "pattern": "[0-9]{5}" },
    { "name": "city", "label": "Ville", "type": "text", "placeholder": "Paris", "required": true },
    { "name": "country", "label": "Pays", "type": "text", "placeholder": "France", "required": true }
  ],
  "shippingInfo": "Expédition sous 48h ouvrées.",
  "cta": "Confirmer mon adresse et recevoir mon cadeau",
  "states": {
    "loading": { "message": "Enregistrement de votre adresse…" },
    "success": { "message": "Votre casque sera expédié sous 48h !" },
    "error": { "message": "Erreur lors de l'enregistrement. Veuillez réessayer." }
  }
}
```

---

## 19. Contrat — Dropbox Sign

```json
{
  "headline": "Signature du contrat de service",
  "description": "Un dernier document pour officialiser notre collaboration.",
  "contract": {
    "title": "Contrat de Prestation de Services — Marin",
    "clauses": ["Durée de l'accompagnement", "Objectifs et garantie", "Prix et modalités de paiement", "Obligations des parties", "Enregistrement des appels", "Anonymat des commerciaux", "Propriété intellectuelle", "Conditions de résiliation"],
    "downloadUrl": "/contracts/marin-service-contract.pdf"
  },
  "signMethod": "dropbox-sign",
  "cta": "Lire et signer",
  "secondaryCta": "Télécharger le contrat",
  "states": {
    "loading": { "message": "Préparation du contrat…" },
    "signed": { "message": "Contrat signé ! Bienvenue officiellement chez Marin 🎉", "nextSteps": ["Contrat envoyé par email", "Onboarding dans les 24h", "Votre équipe sera contactée pour le setup"] },
    "error": { "message": "Erreur lors de la signature. Veuillez réessayer ou contactez-nous." }
  }
}
```

---

## 20. Onboarding

```json
{
  "headline": "Bienvenue chez Marin",
  "description": "Presque fini ! Complétez ces dernières informations pour que nous puissions démarrer.",
  "welcome": {
    "title": "Prochaines étapes",
    "steps": [
      "Vous allez recevoir un email avec l'accès à votre dashboard client",
      "Un commercial dédié vous contactera pour le premier appel",
      "Nous configurons votre équipe et vos équipements"
    ]
  },
  "fields": [
    { "name": "teamSize", "label": "Combien de commerciaux seront formés ?", "type": "number", "placeholder": "3", "min": 1, "required": true },
    { "name": "startDate", "label": "Quand souhaitez-vous démarrer ?", "type": "select", "options": ["Dès que possible", "La semaine prochaine", "Dans 2 semaines", "Le mois prochain"] },
    { "name": "referralSource", "label": "Comment nous avez-vous connu ?", "type": "select", "options": ["Google", "LinkedIn", "Recommandation", "Blog", "Autre"] },
    { "name": "additionalNotes", "label": "Notes complémentaires (optionnel)", "type": "textarea", "placeholder": "Toute information que vous souhaitez partager…", "required": false }
  ],
  "cta": "Terminer et accéder à mon dashboard",
  "states": {
    "loading": { "message": "Création de votre espace client…" },
    "success": { "message": "Votre espace est prêt ! Vous allez être redirigé vers votre dashboard.", "redirectUrl": "/dashboard" },
    "error": { "message": "Une erreur est survenue. Notre équipe vous contactera pour finaliser la configuration." }
  }
}
```

---

## 21. Premier Appel Commercial

```json
{
  "headline": "Votre premier appel est programmé",
  "description": "Préparez-vous pour votre premier échange avec notre équipe.",
  "callDetails": {
    "type": "Appel découverte & confirmation",
    "duration": "30 à 45 minutes",
    "recorded": true,
    "purpose": "Prise de contact, confirmation des besoins définis dans le funnel, lancement de la collaboration"
  },
  "preparation": [
    "Assurez-vous d'avoir votre casque Jabra à portée",
    "Connectez-vous 5 minutes avant l'heure prévue",
    "Ayez sous les yeux les informations sur votre entreprise"
  ],
  "postCall": {
    "emailSummary": "Un email récapitulatif vous sera envoyé après l'appel.",
    "nextCall": "Le prochain appel sera planifié avec votre dirigeant."
  },
  "cta": "Accéder à mon dashboard",
  "states": {
    "scheduled": { "message": "Appel programmé. Un rappel vous sera envoyé 24h avant." },
    "ongoing": { "message": "Appel en cours… Bonne discussion !" },
    "completed": { "message": "Appel terminé. Merci pour votre temps !" },
    "noShow": { "message": "Vous n'avez pas pu participer ? Réservez un nouveau créneau." },
    "cancelled": { "message": "Appel annulé. Vous pouvez reprogrammer depuis votre dashboard." }
  }
}
```

---

## 22. Appel Dirigeant

```json
{
  "headline": "Appel stratégique avec la direction",
  "description": "Un échange pour aligner nos objectifs et valider le plan d'action 90 jours.",
  "callDetails": {
    "type": "Alignement stratégique",
    "duration": "30 à 45 minutes",
    "recorded": true,
    "purpose": "Présentation du plan d'action détaillé, validation des indicateurs de performance, définition des jalons clés"
  },
  "agenda": [
    "Bilan du premier appel et premiers retours",
    "Validation des objectifs 90 jours",
    "Définition des KPIs de suivi",
    "Planification des appels de suivi bi-mensuels",
    "Questions / réponses"
  ],
  "cta": "Voir le planning des prochains appels",
  "states": {
    "scheduled": { "message": "Appel programmé avec le dirigeant." },
    "completed": { "message": "Plan d'action validé. Place à l'exécution !" }
  }
}
```
