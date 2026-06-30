# About Shopify APIs

Shopify offers a suite of APIs that allow developers to extend the platform's built-in features.

## Requirements

- All APIs are subject to the [Shopify API License and Terms of Use](https://www.shopify.com/legal/api-terms)
- All APIs are subject to [rate limits](https://shopify.dev/docs/api/usage/limits#rate-limits)
- All APIs require developers to [authenticate](https://shopify.dev/docs/apps/build/authentication-authorization)
- Some APIs are [versioned](https://shopify.dev/docs/api/usage/versioning)

## Scopes and permissions

- Some API features require specific [Shopify plans](https://www.shopify.com/pricing)
- Apps need to request specific [access scopes](https://shopify.dev/api/usage/access-scopes) during install
- Some APIs require approval from Shopify before use

## Available APIs

| API | Type | Use Case |
|-----|------|----------|
| GraphQL Admin API | GraphQL | Build apps that extend Shopify admin (products, customers, orders) |
| REST Admin API (legacy) | REST | Legacy — migrate to GraphQL |
| Storefront API | GraphQL | Custom shopping experiences (headless commerce) |
| Partner API | GraphQL | Automate Partner Dashboard operations |
| Webhooks | — | Receive notifications about store events |
| Shopify Functions | Wasm | Custom backend logic (discounts, delivery, validation) |
| Hydrogen | React | Full-stack React storefront framework |
| Liquid | Template | Shopify theme templates |
| Checkout UI Extensions | Web Components | Customize checkout interface |
| Ajax API | REST | Lightweight theme endpoints (cart, search, recommendations) |
| Customer Account API | GraphQL | Customer accounts, single sign-on |
| Payments Apps API | — | Custom payment providers |

## Deprecated APIs

Deprecated APIs remain available but are unsupported. Migrate to supported alternatives.

Source: [Shopify API docs](https://shopify.dev/docs/api/usage)
