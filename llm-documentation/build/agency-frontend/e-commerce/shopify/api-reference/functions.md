# Shopify Functions API

Shopify Functions allow developers to customize Shopify's backend logic by running custom code during checkout.

**API Version:** 2026-04

## Overview

Functions run during checkout to implement:
- Custom delivery options
- New discount types
- Cart and checkout validation
- Payment customization
- Order routing
- Cart transformations

## Supported Languages

- **Rust** (recommended — most performant, compiles to Wasm)
- **JavaScript** (via Wasm)

## Scaffolding

```bash
shopify app generate extension
```

## Function Execution Order

1. **Cart lines** → Cart Transform
2. **Cart line discounts** → Discount
3. **Fulfillment groups** → Fulfillment Constraints, Order Routing
4. **Delivery methods** → Pickup Point, Local Pickup, Delivery Customization
5. **Delivery discounts** → Discount
6. **Payment methods** → Payment Customization
7. **Verification** → Cart and Checkout Validation

## Configuration (shopify.extension.toml)

```toml
api_version = "2026-01"

[[extensions]]
name = "t:name"
handle = "my-discount-function"
type = "function"
uid = "..."

  [[extensions.targeting]]
  target = "cart.lines.discounts.generate.run"
  input_query = "src/run.graphql"
  export = "run"

  [extensions.build]
  command = "cargo build --target=wasm32-unknown-unknown --release"
  path = "target/wasm32-unknown-unknown/release/discount.wasm"
  watch = [ "src/**/*.rs" ]
```

## Anatomy

1. **Input** — GraphQL input query defining data shape
2. **Function** — Wasm module processing input → returns operations
3. **Output** — Operations Shopify executes (discounts, delivery options, etc.)

## Resource Limits

| Resource | Limit |
|----------|-------|
| Compiled binary size | 256 kB |
| Runtime linear memory | 10,000 kB |
| Runtime stack memory | 512 kB |
| Execution instruction count | 11 million (up to 200 line items) |
| Function input | 128 kB |
| Function output | 20 kB |

## Availability

- Public apps: all plans
- Custom apps: Shopify Plus only
- Network access: limited to Enterprise stores

Source: [Functions docs](https://shopify.dev/docs/api/functions/latest)
