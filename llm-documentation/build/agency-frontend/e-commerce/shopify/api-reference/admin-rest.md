# REST Admin API Reference

**Legacy API as of October 1, 2024.** New apps must use [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql).

**API Version:** 2026-01

## Client Libraries

| Library | Installation |
|---------|-------------|
| Remix | `npm install --save @shopify/shopify-app-remix` |
| Node.js | `npm install --save @shopify/shopify-api` |
| Ruby | `bundle add shopify_api` |
| cURL | Available by default on macOS/Linux |

## Authentication

Include token as `X-Shopify-Access-Token` header on all requests.

```bash
curl -X GET https://{shop}.myshopify.com/admin/api/2026-01/shop.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Access-Token: {password}'
```

## Endpoint Pattern

`https://{store_name}.myshopify.com/admin/api/2026-01/{resource}.json`

### CRUD Examples

**Create a product (POST):** `/admin/api/2026-01/products.json`
**Get a product (GET):** `/admin/api/2026-01/products/{id}.json`
**Update a product (PUT):** `/admin/api/2026-01/products/{id}.json`
**Delete a product (DELETE):** `/admin/api/2026-01/products/{id}.json`

## Rate Limits

- **40 requests per app per store per minute**
- Replenishes at 2 requests per second
- 10x limit for Shopify Plus stores
- Response header: `X-Shopify-Shop-Api-Call-Limit: 40/40`
- 429 response includes `Retry-After` header

## Error Codes

| Code | Description |
|------|-------------|
| 401 Unauthorized | Invalid API key or access token |
| 402 Payment Required | Store frozen |
| 403 Forbidden | Incorrect access scopes |
| 404 Not Found | Resource not available |
| 422 Unprocessable Entity | Semantic error in request body |
| 429 Too Many Requests | Rate limit exceeded |
| 5xx | Shopify internal error |

Source: [REST Admin API docs](https://shopify.dev/docs/api/admin-rest)
