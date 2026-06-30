# Webhooks

Webhook subscriptions receive notifications about particular events in a shop.

**API Version:** 2026-04

**Caution:** Apps distributed through the App Store must subscribe to [mandatory compliance topics](https://shopify.dev/docs/apps/build/privacy-law-compliance).

## Creating Subscriptions

### App Configuration File (TOML)

```toml
[webhooks]
api_version = "2023-04"

[[webhooks.subscriptions]]
topics = ["products/create", "products/update", "products/delete"]
uri = "pubsub://example:pub-sub-topic1"
```

### GraphQL Admin API

```graphql
mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
    webhookSubscription { id, topic, format, includeFields, uri }
  }
}
```

## Key Topics

| Topic | Description |
|-------|-------------|
| `app/uninstalled` | App removed from store |
| `app/scopes_update` | App access scopes changed |
| `products/create` / `update` / `delete` | Product lifecycle |
| `orders/create` / `update` / `delete` | Order lifecycle |
| `carts/create` / `update` | Cart events |
| `checkouts/create` / `update` / `delete` | Checkout events |
| `customers/create` / `update` / `delete` | Customer lifecycle |
| `collections/create` / `update` / `delete` | Collection lifecycle |
| `fulfillments/create` / `update` | Fulfillment events |
| `inventory_levels/update` | Inventory changes |
| `bulk_operations/finish` | Bulk operation complete |
| `app_subscriptions/update` / `approaching_capped_amount` | Billing events |

## Sample Payload (app/uninstalled)

```json
{
  "id": 548380009,
  "name": "Super Toys",
  "email": "super@supertoys.com",
  "domain": null,
  "country": "US",
  "address1": "190 MacLaren Street",
  "zip": "37178",
  "city": "Houston",
  "phone": "3213213210",
  "primary_locale": "en",
  "country_code": "US",
  "currency": "USD",
  "customer_email": "super@supertoys.com",
  "timezone": "(GMT-05:00) Eastern Time (US & Canada)",
  "shop_owner": "John Smith",
  "money_format": "${{amount}}",
  "plan_display_name": "Shopify Plus",
  "plan_name": "enterprise"
}
```

Source: [Webhooks docs](https://shopify.dev/docs/api/webhooks/latest)
