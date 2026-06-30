# GraphQL Storefront API

Create unique customer experiences on any platform — web, apps, games.

**API Version:** 2026-04

## Client Libraries

| Library | Installation |
|---------|-------------|
| Hydrogen | `npm init @shopify/hydrogen@latest` |
| Storefront API Client | `npm install --save @shopify/storefront-api-client` |
| React Router | `npm install --save @shopify/shopify-app-react-router` |
| Shopify API (Node.js) | `npm install --save @shopify/shopify-api` |
| Ruby | `bundle add shopify_api` |

## Authentication

### Tokenless Access
- Products, Collections, Pages, Cart (read/write), Search
- Query complexity limit: 1,000

### Token-Based (Public or Private)
Required for: Product Tags, Metaobjects/Metafields, Menu, Customers

```bash
curl -X POST \
  https://{shop}.myshopify.com/api/2026-04/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Storefront-Access-Token: {token}' \
  -d '{"query": "{ products(first: 3) { edges { node { id title } } } }"}'
```

### Storefront API Client

```ts
import {createStorefrontApiClient} from '@shopify/storefront-api-client';

const client = createStorefrontApiClient({
  storeDomain: 'http://your-shop-name.myshopify.com',
  apiVersion: '2026-04',
  publicAccessToken: '<your-token>',
});
```

## Endpoint

`POST https://{store_name}.myshopify.com/api/2026-04/graphql.json`

## Directives

- `@inContext(country: FR)` — Localized pricing
- `@inContext(language: ES)` — Translated content
- `@inContext(buyer: {...})` — B2B contextualized pricing
- `@inContext(visitorConsent: {...})` — Privacy compliance
- `@defer` — Stream partial query results (developer preview)

## Rate Limits

- Real buyer traffic: no fixed limit
- Automated traffic (bots/crawlers): rate-limited
- Tokenless access: 1,000 query complexity limit
- Malicious requests: 430 Shopify Security Rejection

## Error Codes

Same as Admin API: ACCESS_DENIED, SHOP_INACTIVE, INTERNAL_SERVER_ERROR, THROTTLED, MAX_COMPLEXITY_EXCEEDED

Source: [Storefront API docs](https://shopify.dev/docs/api/storefront/latest)
