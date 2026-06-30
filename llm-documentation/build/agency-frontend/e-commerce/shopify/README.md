# Shopify — Service e-commerce

Shopify est un **service externe** dans l'architecture Marin — au même titre que PostHog, Stripe ou Calendly. Il ne modifie pas la logique du funnel.

## Principes

- Le funnel React/Zustand reste l'application principale — inchangé.
- Shopify est une source de données produits + backend transactionnel.
- Chaque client a son propre store Shopify (produits, thème, domaine).
- L'intégration se fait via API (Storefront GraphQL ou Admin REST), pas en embeddant le funnel dans Shopify.

## Architecture

```
React/Zustand Funnel (Marin)
    │
    ├── Step 1 : Landing page produits
    │   └── Fetch produits depuis Shopify Storefront API
    │       └── Affiche les produits du client (custom React components)
    │
    ├── Steps 2-18 : Sales tension (référence les produits)
    │   └── Produits stockés dans Zustand
    │
    ├── Step 19 : Call booking (Calendly)
    │
    ├── Step 20-21 : Post-call / Close
    │
    └── Résultat : Deal closed → client achète sur son store Shopify
                                    (transaction gérée 100% par Shopify)
```

## Flux

```
Onboarding Form (admin)
    │
    ├─ Client name, email, domain
    ├─ Store Shopify existant ou à créer
    ├─ Thème (repo Git → fork → custom → push)
    └─ Produits (définis dans client.ts ou API)
         │
         ▼
Funnel client → affiche les produits → build tension → call → close
                                                              │
                                                              ▼
                                              Client achète sur Shopify
                                              (notre backend ne touche pas
                                               aux transactions Shopify)
```

## Ce qui change dans le funnel

Le funnel est **strictement identique** au funnel agency. La seule différence :

| Aspect | Agency | E-commerce (Shopify) |
|--------|--------|----------------------|
| Produits affichés | Services (marketing, dev) | Produits physiques (via Shopify API) |
| Landing page | Présentation services | Présentation produits Shopify |
| Transaction | Stripe (notre système) | Shopify Checkout (externe) |
| Onboarding | Dashboard in-app | Store Shopify + theme |

## Files

- `integration.md` — Détails techniques : API, endpoints, env vars, code snippets.
- `api-reference/` — Documentation de référence Shopify fetchée depuis shopify.dev/docs/api (Admin, Storefront, Webhooks, Hydrogen, Liquid, Functions, etc.).
