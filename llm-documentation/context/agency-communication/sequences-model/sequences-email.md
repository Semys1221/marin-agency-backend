# Séquences Email — Architecture Triple

Trois systèmes distincts :

## 1. Instantly — Cold Outreach (1 séquence)

| # | Séquence | Déclencheur | Système |
|---|----------|-------------|---------|
| 1 | Cold Contact | Nouveau lead | Instantly (7-step A/B/C) |

Format multi-variante : 7 steps (J1→J19), variantes A/B/C par step.
Variables résolues depuis table `niche_variable` (Supabase).

## 2. Resend — Transactionnel (6 séquences)

Emails unitaires, event-driven, envoyés une seule fois.

| # | Séquence | Déclencheur |
|---|----------|-------------|
| 1 | Information Requested | Demande d'info via AI |
| 2 | No-show | Appel manqué |
| 3 | Call Reminder | Appel à venir |
| 4 | Invoice | Facture émise |
| 5 | Service Delivery | Livraison service |
| 6 | Call Description | Post-appel avec lieux |

## 3. loop.so — Nurturing (4 séquences)

Séquences multi-step avec suivi, relances, conditions d'arrêt.

| # | Séquence | Déclencheur | Comportement |
|---|----------|-------------|-------------|
| 1 | Interested | Lead a montré de l'intérêt | Relance progressive J0→J2→J5→J8 |
| 2 | Indecision | Post-appel indécis | Nurturing J+1→J+3→J+7→J+30 |
| 3 | Onboarding | Deal clos, nouveau client | Activation J0→J3→J7→J15 |
| 4 | Upsell | Opportunité cross-sell | Campagne J0→J3→J7, arrêt sur achat |

Objectif global : tester 2 offres sur le site e-commerce du grossiste n°1 + acquisition de 10 appels (BNC/BIC) + 10 ventes en 90 jours.
