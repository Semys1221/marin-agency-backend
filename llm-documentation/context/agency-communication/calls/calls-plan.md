# Calls Plan — 6 appels sur 90 jours

**Rythme :** 1 appel tous les 15 jours
**Durée :** 40 min par défaut
**Déclencheur :** Check-in programmé sur le calendrier client
**Contexte :** Chaque appel s'appuie sur le [Client Dashboard](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=26Oz8D4Inf_qZb08DmOp). L'agent ouvre le dashboard client avant l'appel, consulte les sections pertinentes, et utilise les données pour guider la conversation.

> **Interne :** Les réunions internes agency utilisent **Google Meet**. Les appels clients restent sur **Microsoft Call** ou **Quo.com**.

Référence spec : `build/agency-backend/frontend-engine/11-client-dashboard.md`

---

## Call 1 — J0 : Setup Technique

**Durée :** 60 min (premier setup plus long)
**Objectif :** Installer tout le matériel, donner les accès, activer les outils

**Préparation (dashboard) :**
- `onboarding_tasks` — checklist des tâches de setup
- `clients` — informations du client, coordonnées

**Contenu :**
1. Présentation du service et du parcours 90 jours
2. Explication du matériel fourni : PC, casque Jabra Evolve 20 (ou earbuds), gift Jabra Evolve2 75 si offert
3. Installation et test des outils :
   - Quo.com (appels) — vérifier compte actif
   - Microsoft Call — vérifier accès
   - Calendly — connecter le calendrier
4. Configuration du dashboard client :
   - Accès au dashboard HTML
   - Présentation des sections : leads, campagnes, analytics
   - Présentation des liens externes (Microsoft, Quo, Stripe, etc.)
5. Présentation des scripts de vente et du process
6. Premier appel test audio/vidéo entre l'agent et le commercial
7. Réponse aux questions techniques

**Post-call (dashboard) :**
- Cocher les tâches onboarding terminées dans `onboarding_tasks`
- Envoyer l'email récapitulatif via le trigger "Call Description" (`11-client-dashboard.md:40`)

---

## Call 2 — J15 : Onboarding Commercial

**Durée :** 40 min
**Objectif :** Valider que le commercial est opérationnel, premier debrief des actions

**Préparation (dashboard) :**
- `funnel_progress` — où en est le commercial dans le funnel
- `campaign_analytics` — premiers chiffres de la campagne email
- `clean_leads` — qualité des leads reçus

**Contenu :**
1. Vérification que tout le matériel fonctionne (PC, casque, outils)
2. Retour sur les premiers emails reçus / appels passés
3. Analyse des premiers retours prospects
4. Ajustement du script de vente si nécessaire
5. Coaching sur la prise de contact téléphonique
6. Plan d'action pour les 15 prochains jours
7. Questions / réponses

**Post-call (dashboard) :**
- Mettre à jour le statut des leads si nécessaire (`POST /api/leads/status`)
- Envoyer l'email récapitulatif

---

## Call 3 — J30 : Premiers Résultats & Ajustements

**Durée :** 40 min
**Objectif :** Analyser les premiers résultats concrets, ajuster la stratégie

**Préparation (dashboard) :**
- `campaign_analytics` — taux d'ouverture, réponses, tendances
- `call_sessions` — historique des appels passés par le commercial
- `clean_leads` — nouveaux leads entrants

**Contenu :**
1. Bilan des 30 premiers jours :
   - Nombre d'emails envoyés / ouverts / réponses
   - Nombre d'appels passés
   - Nombre de rendez-vous bookés
   - Premières ventes signées (ou raisons si aucune)
2. Analyse des objections rencontrées par le commercial
3. Ajustement du script / de l'approche selon les retours terrain
4. Coaching : points forts et axes d'amélioration
5. Décisions : faut-il relancer une campagne ? Changer de niche ?
6. Objectifs pour les 30 prochains jours

**Post-call (dashboard) :**
- Mettre à jour `leads/status` (no-show, indecis, closed)
- Ajuster la campagne si besoin (`POST /api/campaigns/stop`)
- Envoyer l'email récapitulatif

---

## Call 4 — J45 : Coaching & Optimisation

**Durée :** 40 min
**Objectif :** Approfondir le coaching commercial, optimiser le process

**Préparation (dashboard) :**
- `call_sessions` — enregistrements et notes des appels
- `lead intelligence sheet` — fiche de préparation pour chaque prospect
- `campaign_analytics` — performance à mi-parcours

**Contenu :**
1. Analyse détaillée des appels enregistrés :
   - Qualité de la prise de contact
   - Gestion des objections
   - Taux de conversion appel → vente
2. Coaching personnalisé :
   - Points spécifiques à améliorer
   - Jeux de rôle si nécessaire
   - Techniques de closing
3. Revue des prospects chauds et plan d'attaque
4. Optimisation de la campagne email si nécessaire
5. Vérification de l'atteinte des objectifs à mi-parcours

**Post-call (dashboard) :**
- Mettre à jour `call_sessions` avec les notes de coaching
- Envoyer l'email récapitulatif

---

## Call 5 — J60 : Performance & Dernière Ligne Droite

**Durée :** 40 min
**Objectif :** Maximiser les résultats sur le dernier mois, préparer la fin de contrat

**Préparation (dashboard) :**
- `campaign_analytics` — tendance globale
- `prospects` — pipeline des prospects en cours
- `funnel_progress` — progression dans le funnel
- `services` — services activés

**Contenu :**
1. Bilan des 60 premiers jours :
   - Résultats cumulés (ventes, appels, rendez-vous)
   - Comparaison avec l'objectif fixé (10 ventes / 15 appels)
   - ROI estimé pour le client
2. Stratégie pour le dernier mois :
   - Quels prospects relancer en priorité ?
   - Faut-il intensifier les appels ?
   - Actions correctives si l'objectif est en retard
3. Discussion sur la suite :
   - Renouvellement ? Upsell (Branding, Conseil Financier) ?
   - État d'esprit du client sur les résultats
4. Plan d'action J60→J90

**Post-call (dashboard) :**
- Envoyer l'email récapitulatif
- Préparer les devis upsell si intéressé

---

## Call 6 — J75 : Bilan Final & Suite

**Durée :** 40 min
**Objectif :** Clôturer le parcours, présenter les résultats finaux, proposer la suite

**Préparation (dashboard) :**
- `campaign_analytics` — rapport final complet
- `renewals` — options de renouvellement
- `services` — services utilisés et disponibles
- `clients` — informations de facturation

**Contenu :**
1. Bilan final des 90 jours :
   - Résultats globaux : ventes signées, appels passés, taux de conversion
   - Objectif atteint ? (10 ventes offre principale / 15 appels offre secondaire)
   - Si oui : célébration et cas client
   - Si non : explication et offre de poursuite (garantie)
2. Analyse qualitative :
   - Ce qui a fonctionné / ce qui n'a pas fonctionné
   - Apprentissage pour le commercial
   - Recommandations pour l'avenir
3. Proposition de suite :
   - Renouvellement de contrat (mêmes termes ou ajustés)
   - Upsell Branding & Équipement
   - Upsell Conseil Financier
   - Rachat d'actifs (site + funnel)
4. Clôture administrative :
   - Facture finale si applicable
   - Récupération du matériel si non renouvellement
   - Fin des accès dashboard et outils

**Post-call (dashboard) :**
- Envoyer le rapport final complet par email
- Mettre à jour le statut client (renouvellement / clôture)
- Envoyer l'email récapitulatif via Call Description
- Si renouvellement : lancer la séquence Onboarding (boucle)

---

## Notes générales

- **Dashboard first :** Avant chaque appel, l'agent ouvre le dashboard client et prépare les sections pertinentes. Ne jamais arriver sans données.
- **Call Description :** Après chaque appel, cliquer sur le trigger "Call Description" dans le dashboard pour envoyer le résumé post-call au client (spécifié dans `11-client-dashboard.md:40`).
- **40 min par défaut :** Sauf call 1 (60 min pour le setup). Si le client est en retard ou annule, tout report.
- **Garantie :** Si l'objectif n'est pas atteint à J90, le contrat se poursuit gratuitement jusqu'à obtention (offre principale : 10 ventes, offre secondaire : 15 appels). Les calls continuent au même rythme.
- **Support entre les calls :** Le client a accès à l'assistant email 7j/7 (julie@marin.homes) entre les appels pour les questions urgentes.
