# Checkout UI Extensions

Build extensions that integrate into Shopify's checkout interface.

**API Version:** 2026-04

**Shopify Plus:** Checkout UI extensions for info/shipping/payment steps require Shopify Plus.

## Scaffolding

```bash
shopify app generate extension --template checkout_ui
```

## Architecture

Extensions consist of:
1. **Targets** — Where custom UI appears in checkout
2. **Target APIs** — Access to checkout data and functionality
3. **Web Components** — UI elements from Polaris design system

### Target Types

| Type | Description |
|------|-------------|
| Block | Flexible placement, merchant can reposition (checkout editor) |
| Runnable | Data/functionality without UI (e.g., autocomplete) |
| Static | Fixed locations (before actions, after cart items) |

### Target APIs

Access via `shopify` global object:

```tsx
const subtotal = shopify.cost.subtotalAmount.value;
```

### Web Components

```tsx
import '@shopify/ui-extensions/preact';
import {render} from 'preact';

function Extension() {
  return (
    <s-stack direction="inline">
      <s-image src="https://cdn.shopify.com/YOUR_IMAGE_HERE" />
      <s-stack>
        <s-heading>Heading</s-heading>
        <s-text type="small">Description</s-text>
      </s-stack>
      <s-button onClick={() => console.log('button was pressed')}>Button</s-button>
    </s-stack>
  );
}

export default function extension() {
  render(<Extension />, document.body);
}
```

### Applying Changes

```tsx
// Single change
await shopify.applyAttributeChange({
  type: 'updateAttribute',
  key: 'includeGift',
  value: 'yes',
});

// Multiple changes
await Promise.all([
  shopify.applyAttributeChange({...}),
  shopify.applyMetafieldChange({...}),
]);
```

## Configuration (shopify.extension.toml)

```toml
api_version = "2026-04"

[[extensions]]
type = "ui_extension"
name = "My checkout UI extension"
handle = "my-checkout-extension"
uid = "..."

  [[extensions.targeting]]
  target = "purchase.checkout.block.render"
  module = "./src/Checkout.tsx"

  [[extensions.targeting]]
  target = "purchase.thank-you.block.render"
  module = "./src/ThankYou.tsx"
```

## Capabilities

| Capability | Description |
|------------|-------------|
| `api_access` | Query Storefront API |
| `network_access` | Make external network calls |
| `collect_buyer_consent` | Collect buyer consent (SMS marketing) |
| `block_progress` | Block buyer's progress |

## Deployment

```bash
shopify app dev    # Local testing
shopify app deploy # Production
```

**Bundle size limit:** 64 KB

## Security

- Extensions run in isolated sandbox (Web Worker)
- No access to sensitive payment info or checkout page HTML
- Limited to specific UI components and APIs

Source: [Checkout UI extensions docs](https://shopify.dev/docs/api/checkout-ui-extensions/latest)
