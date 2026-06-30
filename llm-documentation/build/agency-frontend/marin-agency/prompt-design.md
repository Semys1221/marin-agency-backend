# Prompt Design — Marin Agency Funnel

**Outil :** https://stitch.withgoogle.com  
**Objectif :** Générer un storyboard visuel du funnel agency (22 étapes) — 1 page = 1 étape.  
**Sortie :** Exporter les pages générées dans `../reference/mockups/marin-agency/`.

---

## Prompt à utiliser dans Stitch

```
You are a UX storyboard designer. Generate a visual storyboard of a B2B agency sales funnel for a prospection outsourcing service called "Marin". Each slide in the storyboard represents exactly one step of the funnel. The visual style should be clean, modern, business-professional — use a light background with accent colors (#49C5B6 teal / #015048 dark teal).

The funnel has 22 sequential steps. For each step, illustrate the main UI concept: what the user sees on screen at that stage. Add a short label at the top of each slide with the step number and name.

Step 1 — Landing Page:
A multi-section landing page. Hero with "Transformez vos prospects en clients avec Marin". Show a 4-step "How it works" section, an offers section with 2 pricing cards (Offre Principale 2500€ with 10-sale guarantee, Offre Secondaire 1900€ with 15-call guarantee). Include a "Réservez votre appel gratuit" CTA.

Step 2 — Qualification SIRET:
A single input form for SIRET number validation. Show valid/invalid states. Headline: "Vérifions votre éligibilité". Button: "Vérifier".

Step 3 — Calendly:
Calendar embed with available time slots for a discovery call. Headline: "Choisissez votre créneau". Show confirmation state with next steps after booking.

Step 4 — Cadre (Framework):
4 bullet points displayed as a clean information card: B2B focus, 90-day commitment, client retains decisions, no forced renewal. Headline: "Le cadre de notre collaboration". CTA: "Je comprends le cadre, continuer".

Step 5 — Profil (Profile):
Form with: sector (select), years active (select), sales team size (number), annual revenue (select). Headline: "Parlez-nous de votre entreprise".

Step 6 — Problème (Pain Points):
Checkbox selection for 6 challenges (finding qualified prospects, too much prospecting time, no pipeline visibility, low conversion rate, unstructured process, high turnover). Optional text field. Headline: "Quels sont vos défis actuels ?".

Step 7 — Objectif (Objective):
Form with: sales target (number), average basket (number), ideal start date (date picker), target list status (radio: yes/no/partial). Headline: "Quel est votre objectif ?".

Step 8 — Historique (History):
Radio questions about past agency experience (yes/mixed/no), current CRM method (CRM/Excel/nothing/other), and a textarea for current process description. Headline: "Votre historique de prospection".

Step 9 — Capacité (Capacity):
Budget range selector (select from 1500€ to 3000€+). Radio questions for absorption capacity and team availability every 15 days. Headline: "Budget et capacité".

Step 10 — Posture (Buying Posture):
Radio questions: decision maker type, urgency level (ASAP to exploring), budget approved status. Headline: "Votre posture d'achat".

Step 11 — Blocage (Objections):
Checkbox for 6 common objections (unsure about sector fit, price, past disappointment, team readiness, time, want results first). Textareas for specific fears and blockers. Headline: "Qu'est-ce qui vous freine ?".

Step 12 — Solution:
5-feature showcase with icons: complete pipeline, 90-day coaching, real-time dashboard, Jabra headset provided, result guarantee. Headline: "Voici comment nous allons vous aider". Main CTA + secondary CTA.

Step 13 — Projection (Results Projection):
3 metric cards showing projected outcomes (revenue +X%, 10 new sales, 2x productivity). 3 reflective questions below. Headline: "Imaginez vos résultats dans 90 jours".

Step 14 — Workflow:
A timeline with 4 phases: Setup (Days 1-15), Launch (Days 16-30), Optimization (Days 31-60), Results (Days 61-90). Each with 4 tasks listed. Headline: "Comment ça se passe concrètement".

Step 15 — Coût de l'Inaction (Cost of Inaction):
3 argument cards: "X ventes perdues par mois", "Retard sur vos concurrents", "X € de manque à gagner sur 12 mois". Headline: "Le coût de l'inaction". CTA: "Je ne veux plus attendre".

Step 16 — Devis (Proposal/Quote):
Proposal summary with 3 sections: needs recap, selected offer (with price/duration/guarantee), included services. Interest bar slider (1-10). CTA: "J'accepte — passer au paiement".

Step 17 — Paiement Stripe:
Payment screen with order summary (offer name, price, VAT info). Payment method options: card and SEPA. Secure badge. CTA: "Payer et commencer". Show success state with welcome message and next steps.

Step 18 — Cadeau (Gift — Jabra Evolve2 75):
Gift presentation card showing the Jabra Evolve2 75 headset (value 300€) with 4 features. Address collection form (name, street, postal code, city, country). Headline: "Félicitations ! Vous recevez un cadeau de bienvenue".

Step 19 — Contrat (Contract — Dropbox Sign):
Contract review screen showing 8 clause titles. Dropbox Sign embed area. Download option. Headline: "Signature du contrat de service". CTA: "Lire et signer".

Step 20 — Onboarding:
Welcome screen with 3 next steps. Form: team size (number), start date (select), referral source (select), additional notes (textarea). Headline: "Bienvenue chez Marin". CTA: "Terminer et accéder à mon dashboard".

Step 21 — Premier Appel Commercial (First Commercial Call):
Call preparation screen. Show call details (30-45 min, recorded, discovery purpose). 3 preparation tips. Post-call info. Headline: "Votre premier appel est programmé".

Step 22 — Appel Dirigeant (Director's Call):
Strategic alignment call screen. 6-item agenda displayed. Call details (30-45 min, recorded). Headline: "Appel stratégique avec la direction". Shows planning calendar for follow-up calls.

Flow/transitions: Connect all 22 slides with forward arrows. Steps 1-3 (Landing → SIRET → Calendly) form the qualification entry sequence. Steps 4-11 (Cadre through Blocage) form the discovery/consultation phase. Steps 12-15 (Solution through Inaction Cost) form the solution/persuasion phase. Steps 16-17 form the closing phase. Steps 18-22 form the post-sale/onboarding phase. Use section dividers or color-coded headers to visually group these 4 phases.

Output format: One full-page slide per step, 16:9 aspect ratio, connected in sequence.
```

---

## Notes d'utilisation

1. Copier-coller le prompt dans https://stitch.withgoogle.com
2. Vérifier que les 22 slides sont bien toutes générées
3. Si le nombre de slides est limité par l'outil, diviser le prompt en 2 parties :
   - Partie 1 : Steps 1–11
   - Partie 2 : Steps 12–22
4. Les textes français doivent être conservés tels quels dans le rendu
5. Palette : #49C5B6 (teal clair), #015048 (teal foncé), fond clair
