# GraphQL Partner API

Provides access to Partners Dashboard data — transactions, apps, themes, Experts Marketplace.

**API Version:** 2026-04

## Authentication

Two pieces required:
1. **Organization ID** — found in Partners Dashboard URL
2. **Partner API client access token** — created in Settings → Partner API clients

```bash
curl -X POST \
  https://partners.shopify.com/{organization_id}/api/2026-04/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Access-Token: {partner_access_token}' \
  -d '{"query": "{your_query}"}'
```

## Permissions

| Permission | Access |
|------------|--------|
| View financials | Transaction resources, cancel subscriptions |
| Manage apps | App resources, installs, uninstalls, charges |
| Manage themes | Theme resources |
| Manage jobs | Conversation and Job resources (Experts Marketplace) |

## Endpoint

`POST https://partners.shopify.com/{org_id}/api/2026-04/graphql.json`

## Rate Limits

- 4 requests per second per Partner API client
- 429 response when exceeded

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad request |
| 401 | Invalid API client or organization |
| 404 | Resource not found |
| 429 | Too many requests |
| 500 | Shopify internal error |

## Localized Errors

Set `Accept-Language` header for translated error messages:

```json
Accept-Language: es
```

Source: [Partner API docs](https://shopify.dev/docs/api/partner/latest)
