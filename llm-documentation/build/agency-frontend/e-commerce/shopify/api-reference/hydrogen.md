# Hydrogen

Hydrogen is Shopify's opinionated stack for headless commerce, built on [React Router](https://reactrouter.com/home).

**API Version:** 2026-04

## Setup

```bash
npm create @shopify/hydrogen@latest
```

## Authentication

Hydrogen uses Storefront API and Customer Account API.

```js
// server.js
const {storefront} = createStorefrontClient({
  cache,
  waitUntil,
  i18n: {language: 'EN', country: 'US'},
  publicStorefrontToken: env.PUBLIC_STOREFRONT_API_TOKEN,
  privateStorefrontToken: env.PRIVATE_STOREFRONT_API_TOKEN,
  storeDomain: env.PUBLIC_STORE_DOMAIN,
  storefrontId: env.PUBLIC_STOREFRONT_ID,
  storefrontHeaders: getStorefrontHeaders(request),
});
```

```env
SESSION_SECRET="foobar"
PUBLIC_STOREFRONT_API_TOKEN="3b580e70970c4528da70c98e097c2fa0"
PUBLIC_STORE_DOMAIN="hydrogen-preview.myshopify.com"
```

## Versioning

Hydrogen is tied to Storefront API versions (quarterly). Breaking changes in Storefront API → breaking changes in Hydrogen.

## Importing Components

```jsx
import {ShopPayButton} from '@shopify/hydrogen';

export function renderShopPayButton({variantId, storeDomain}) {
  return <ShopPayButton variantIds={[variantId]} storeDomain={storeDomain} />;
}
```

Hydrogen re-exports from `@shopify/hydrogen-react` for convenience.

Source: [Hydrogen docs](https://shopify.dev/docs/api/hydrogen/latest)
