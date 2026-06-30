# Prompt Design — E-Commerce Funnel (Grossiste)

**Outil :** https://stitch.withgoogle.com  
**Objectif :** Générer un storyboard visuel du funnel e-commerce grossiste — 1 page = 1 étape.  
**Sortie :** Exporter les pages générées dans `../reference/mockups/e-commerce/`.

---

## Prompt à utiliser dans Stitch

```
You are a UX storyboard designer. Generate a visual storyboard of a B2B wholesale e-commerce sales funnel. Each slide in the storyboard represents exactly one step of the funnel. The visual style should be clean, modern, business-professional — use a light background with accent colors (#49C5B6 teal / #015048 dark teal).

The funnel has 11 sequential steps. For each step, illustrate the main UI concept: what the user sees on screen at that stage. Add a short label at the top of each slide with the step number and name.

Step 1 — Landing Page:
Product catalog gallery. Show product cards with images, prices, and a "Voir le catalogue" CTA. Include a hero section with "Catalogue grossiste — Prix professionnels" as headline. Secondary CTA "Demander un devis personnalisé".

Step 2 — Qualification SIRET:
A single input form for SIRET number (14 digits). Show a validation state with a checkmark or error. Headline: "Vérifions votre éligibilité". A "Vérifier mon SIRET" button.

Step 3 — Calendly:
A calendar embed view for booking a discovery call. Show a calendar widget with available time slots. Headline: "Prenez rendez-vous avec notre équipe". Confirmation state after booking.

Step 4 — Cadre (Framework):
A summary card listing 4 bullet points about how the partnership works. Clean information layout. Headline: "Comment nous travaillons ensemble". CTA: "Je comprends, continuer".

Step 5 — Profil (Profile):
A multi-field form with: business type (select), monthly volume (select), sales channels (checkboxes), years active (select). Headline: "Parlez-nous de votre activité".

Step 6 — Problème (Pain Points):
A checkbox selection screen for pain points (6 options like supplier reliability, margins, delays, etc.). Headline: "Quels sont vos besoins actuels ?". A text field for "other".

Step 7 — Objectif (Objective):
A form with number inputs for target volume and monthly budget. A select for delivery expectations, checkboxes for specific needs. Headline: "Quel est votre objectif ?".

Step 8 — Solution:
A feature showcase card with 5 features: large catalog, negotiated prices, optimized logistics, dedicated support, Shopify dashboard. Each with an icon. Headline: "Notre offre pour votre activité". CTA: "Cette offre m'intéresse — voir le devis".

Step 9 — Devis (Proposal/Quote):
A proposal summary card showing selected products, conditions (delivery, shipping, payment). Include an interest bar slider (1-10). CTA: "J'accepte — passer au paiement".

Step 10 — Paiement (Payment):
A payment redirect screen. Show "Redirection vers Shopify Checkout" with a secure payment badge. Order summary sidebar. CTA: "Procéder au paiement sécurisé". Success/error states.

Step 11 — Suivi (Tracking):
An order confirmation dashboard. Show status timeline: confirmed → preparation → shipped → delivered. Info cards with order number, status, estimated delivery, carrier. CTA: "Suivre ma commande sur Shopify".

Flow/transitions: Between each step slide, add a subtle arrow or connector showing forward progression. Step 3 (Calendly) should have a confirmation transition showing the call is booked. Step 10 (Payment) transitions from Shopify redirect back to the tracking dashboard.

Output format: One full-page slide per step, 16:9 aspect ratio, connected in sequence.
```

---

## Notes d'utilisation

1. Copier-coller le prompt dans https://stitch.withgoogle.com
2. Vérifier que chaque étape est bien représentée sur une slide distincte
3. Ajuster les couleurs si le rendu ne correspond pas à la charte (#49C5B6 / #015048)
4. Les textes français doivent être conservés tels quels dans le rendu
