# GraphQL Admin API Reference

The Admin API lets you build apps and integrations that extend and enhance the Shopify admin.

**API Version:** 2026-04

## Client Libraries

| Library | Installation |
|---------|-------------|
| React Router | `npm install -g @shopify/cli@latest && shopify app init` |
| Node.js | `npm install --save @shopify/shopify-api` |
| Ruby | `bundle add shopify_api` |
| cURL | Available by default on macOS/Linux |
| Direct API Access | Embedded app — enabled via TOML config |

## Authentication

All requests require a valid Shopify access token as `X-Shopify-Access-Token` header.

### React Router

```js
import { authenticate } from "../shopify.server";

export async function loader({request}) {
  const { admin } = await authenticate.admin(request);
  const response = await admin.graphql(`query { shop { name } }`);
}
```

### Node.js

```ts
const client = new shopify.clients.Graphql({session});
const response = await client.query({data: 'query { shop { name } }'});
```

### cURL

```bash
curl -X POST \
  https://{shop}.myshopify.com/admin/api/2026-04/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}' \
  -d '{ "query": "query { shop { name } }" }'
```

### Direct API Access (embedded apps)

```ts
const response = await fetch('shopify:admin/api/2026-04/graphql.json', {
  method: 'POST',
  body: JSON.stringify({ query: `query { shop { name } }` }),
});
```

## Endpoint

`POST https://{store_name}.myshopify.com/admin/api/2026-04/graphql.json`

## Rate Limits

Calculated query costs in cost points. Each field costs a set number of points.

```json
{
  "extensions": {
    "cost": {
      "requestedQueryCost": 3,
      "actualQueryCost": 3,
      "throttleStatus": {
        "maximumAvailable": 1000.0,
        "currentlyAvailable": 997,
        "restoreRate": 50.0
      }
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| THROTTLED | Rate limit exceeded |
| ACCESS_DENIED | Authentication error |
| SHOP_INACTIVE | Store is not active |
| INTERNAL_SERVER_ERROR | Shopify internal error |
| MAX_COST_EXCEEDED | Query cost exceeds limit |

Source: [GraphQL Admin API docs](https://shopify.dev/docs/api/admin-graphql/latest)
