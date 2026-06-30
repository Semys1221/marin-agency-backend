# Ajax API

Lightweight REST API for Shopify themes — no full page reload required.

## Use Cases

- Add products to cart and update cart counter
- Display related product recommendations
- Suggest products as visitor types in search field

## Making Requests

- `GET` — Read cart and some product data
- `POST` — Update cart for current session

```javascript
var cartContents = fetch(window.Shopify.routes.root + 'cart.js')
  .then(response => response.json())
  .then(data => { return data });
```

## Locale-Aware URLs

Use `window.Shopify.routes.root` as base for URLs (always ends with `/`).

## Requirements & Limitations

- **Unauthenticated** — no tokens required
- **No hard rate limits** — standard abuse-prevention applies
- All responses are JSON
- Product JSON: max 250 variants
- Cannot read customer/order data
- Cannot update store data
- **Themes only** — not available on custom storefronts

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cart.js` | GET | Get cart contents |
| `/cart/add.js` | POST | Add item to cart |
| `/cart/update.js` | POST | Update cart quantities |
| `/cart/change.js` | POST | Change specific cart item |
| `/cart/clear.js` | POST | Clear cart |
| `/products/{handle}.js` | GET | Get product JSON |
| `/recommendations/products.json` | GET | Product recommendations |
| `/search/suggest.json` | GET | Search suggestions |
| `/search.json` | GET | Search results |

## Section Rendering API

Request HTML markup for theme sections:

`GET /?sections=section-id-1,section-id-2`

Returns JSON with section IDs as keys and rendered HTML as values.

Source: [Ajax API docs](https://shopify.dev/docs/api/ajax)
