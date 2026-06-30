# Shopify Agents — Universal Commerce Protocol (UCP)

Build AI agents that authenticate with Shopify, search products, build carts, create checkouts, and track orders using the Universal Commerce Protocol (UCP).

**Ce que UCP permet :**
- Découvrir des produits (Global Catalog × millions de produits Shopify)
- Construire des paniers chez des marchands
- Convertir en checkout et compléter l'achat (trusted agents uniquement)
- Suivre les commandes (statut, fulfillment, refunds)

**Ce que UCP ne permet PAS :**
- Créer des stores Shopify — toujours manuel via Partner Dashboard
- Gérer l'admin du store (produits, thèmes, clients) — utiliser l'Admin API pour ça

---

## Installation

### UCP CLI

```bash
npm install -g @shopify/ucp-cli
```

### Shopify AI Toolkit (plugin pour votre agent)

**Claude Code :**
```bash
claude plugin install shopify-ai-toolkit@claude-plugins-official
```

**Codex :**
```bash
codex plugin add shopify@openai-curated
```

---

## Initialisation du profil

```bash
ucp profile init --name agent
```

Vérifier : `ucp doctor`

---

## Tiers d'authentification

| Tier | Auth | Capacités |
|------|------|-----------|
| **Token** | JWT (Bearer) | Catalog, Cart, Checkout, `complete_checkout`, Orders (avec scope) — rate limits les plus hauts |
| **Signed** | HTTP Signatures (RFC 9421) | Catalog, Cart, Checkout — pas de `complete_checkout` ni Orders |
| **Anonymous** | Pas d'auth | Catalog, Cart, Checkout — rate limits les plus bas |

### Buyer-linked tokens

Un token qui porte l'identité d'un client connecté Shop. Permet des résultats personnalisés dans le Global Catalog.

---

## Architecture

```
Agent → UCP CLI / MCP → Shopify
                           ├── Global Catalog (recherche multi-marchands)
                           ├── Storefront Catalog (marchand spécifique)
                           ├── Cart MCP (panier)
                           ├── Checkout MCP (checkout + completion)
                           └── Order MCP (suivi commande)
```

### Profile UCP

L'agent se présente via un **profile JSON** hébergé à une URL. Shopify fetch ce profile et négocie les capacités :

```json
{
  "ucp": {
    "version": "2026-04-08",
    "services": {
      "dev.ucp.shopping": [{
        "version": "2026-04-08",
        "transport": "mcp",
        "schema": "https://ucp.dev/2026-04-08/services/shopping/mcp.openrpc.json"
      }]
    },
    "capabilities": {
      "dev.ucp.shopping.checkout": [{ "version": "2026-04-08" }],
      "dev.ucp.shopping.cart": [{ "version": "2026-04-08" }],
      "dev.ucp.shopping.order": [{ "version": "2026-04-08" }],
      "dev.ucp.shopping.catalog.search": [{ "version": "2026-04-08" }],
      "dev.ucp.shopping.catalog.lookup": [{ "version": "2026-04-08" }]
    }
  }
}
```

Inclure l'URL du profile dans chaque requête MCP :

```json
{
  "meta": {
    "ucp-agent": {
      "profile": "https://votre-domaine.com/ucp-profile.json"
    }
  }
}
```

---

## CLI Commands

### Catalog Search

```bash
ucp catalog search \
  --set /query='wireless headphones under $100' \
  --set /context/address_country=US \
  --view :compact \
  --format md
```

### Cart Create

```bash
ucp cart create --business https://{merchant-domain} \
  --set /line_items/0/item/id='{variant_id}' \
  --set /line_items/0/quantity=1 \
  --set /context/address_country=US
```

### Checkout Create

```bash
ucp checkout create --business https://{merchant-domain} \
  --input '{"cart_id":"{cart_id}","line_items":[]}'
```

### Checkout Complete

```bash
ucp checkout update {checkout_id} --input-schema --business https://{merchant-domain}
ucp checkout update {checkout_id} --business https://{merchant-domain} --input '...'
ucp checkout complete {checkout_id} --business https://{merchant-domain}
```

### Order Get

```bash
ucp order get {order_id} --business https://{merchant-domain}
```

---

## Order Webhooks

Souscrire aux événements de cycle de vie des commandes (fulfillment, refunds, returns, cancellations).

---

## Références

- [Quickstart](https://shopify.dev/docs/agents/get-started/quickstart)
- [Agent profiles](https://shopify.dev/docs/agents/profiles)
- [Auth and rate limiting](https://shopify.dev/docs/agents/profiles/auth-and-rate-limiting)
- [UCP CLI GitHub](https://github.com/Shopify/ucp-cli)
- [Shopify AI Toolkit](https://shopify.dev/docs/apps/build/ai-toolkit)
