# Shopify Integration

## Client Config

Chaque client e-commerce a un store Shopify. Les produits sont définis dans `src/config/client.ts` :

```ts
// src/config/client.ts
export interface ClientConfig {
  // ... existing fields ...
  shopify?: {
    storeDomain: string          // client-store.myshopify.com
    storefrontAccessToken: string // Storefront API (public)
    products: Product[]          // fetched from API or defined statically
  }
}
```

## Approche recommandée : Storefront API

Le funnel fetch les produits live depuis le store Shopify du client via la **Storefront GraphQL API** (publique, sécurisée côté client).

### 1. Setup

Dans le store Shopify du client :
- Settings → Sales channels → Custom storefront → Create Storefront API access token

Dans `.env` du projet funnel :

```
VITE_SHOPIFY_STOREFRONT_TOKEN=xxx
VITE_SHOPIFY_STORE_DOMAIN=client-store.myshopify.com
```

### 2. Zustand store pour Shopify

```ts
// stores/shopify.ts
import { create } from 'zustand'

interface ShopifyProduct {
  id: string
  title: string
  description: string
  priceRange: { minVariantPrice: { amount: string; currencyCode: string } }
  images: { edges: { node: { url: string; altText: string | null } }[] }
  handle: string
}

interface ShopifyStore {
  products: ShopifyProduct[]
  loading: boolean
  error: string | null
  fetchProducts: () => Promise<void>
}

export const useShopifyStore = create<ShopifyStore>((set) => ({
  products: [],
  loading: false,
  error: null,
  fetchProducts: async () => {
    set({ loading: true, error: null })
    try {
      const domain = import.meta.env.VITE_SHOPIFY_STORE_DOMAIN
      const token = import.meta.env.VITE_SHOPIFY_STOREFRONT_TOKEN
      const query = `{
        products(first: 50) {
          edges {
            node {
              id, title, description, handle
              priceRange { minVariantPrice { amount, currencyCode } }
              images(first: 3) { edges { node { url, altText } } }
            }
          }
        }
      }`
      const res = await fetch(`https://${domain}/api/2024-07/graphql.json`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': token },
        body: JSON.stringify({ query })
      })
      const json = await res.json()
      set({ products: json.data.products.edges.map(e => e.node), loading: false })
    } catch (e) {
      set({ error: e.message, loading: false })
    }
  }
}))
```

### 3. Step 1 — Landing page produits

```tsx
// components/steps/Landing.tsx
import { useShopifyStore } from '../../stores/shopify'
import { useFunnelStore } from '../../stores/funnel'

export default function Landing() {
  const { products, loading, fetchProducts } = useShopifyStore()
  const setData = useFunnelStore((s) => s.setData)
  const next = useFunnelStore((s) => s.next)

  useEffect(() => { fetchProducts() }, [])

  return (
    <div>
      <h1>Nos produits</h1>
      {loading && <p>Chargement...</p>}
      <div className="product-grid">
        {products.map((p) => (
          <div key={p.id} className="product-card">
            <img src={p.images.edges[0]?.node.url} alt={p.title} />
            <h3>{p.title}</h3>
            <p>{p.priceRange.minVariantPrice.amount} €</p>
            <button onClick={() => {
              setData('selectedProduct', p)
              next()
            }}>
              Je veux ça
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Approche alternative : Static config (plus simple, zéro API)

Si les produits changent rarement, on les définit directement dans `client.ts` :

```ts
const config: ClientConfig = {
  shopify: {
    storeDomain: 'client-store.myshopify.com',
    products: [
      {
        id: 'lot-1',
        title: 'Lot de 10 palettes',
        price: '1500',
        image: '/images/palettes.jpg',
        description: 'Palettes en bois traité — livraison 48h'
      }
    ]
  }
}
```

## Checkout Link

Quand le client veut acheter, on le redirige vers Shopify :

```tsx
// Dans un step du funnel
const product = useFunnelStore((s) => s.data.selectedProduct)
const storeDomain = config.shopify?.storeDomain

return (
  <a
    href={`https://${storeDomain}/products/${product.handle}`}
    target="_blank"
    rel="noopener noreferrer"
  >
    Voir sur Shopify
  </a>
)
```

Ou checkout direct via Storefront API (plus avancé) : utiliser le `checkoutCreate` mutation pour générer un lien de checkout.

## Provisionnement d'un nouveau client Shopify

Quand un deal est closed (Phase 2 step 12 → Closed Won) :

### Étape 1 — Créer le store Shopify (manuel)

**La Partner API Shopify ne permet pas de créer des stores.** Cette étape est manuelle :

1. Aller sur https://partners.shopify.com → Dashboard → Stores → Create store
2. Choisir "Development store" (transférable au client plus tard)
3. Noter le nom du store (`{client}.myshopify.com`)

### Étape 2 — Configurer via Admin API (automatisé)

Une fois le store créé, tout est automatisable via l'Admin API REST/GraphQL :

1. **Créer un token Storefront API** — `POST /admin/api/2026-04/storefront_access_tokens.json`
2. **Pousser le thème** — `shopify theme push` depuis le repo Git du thème client
3. **Configurer les produits** — via Admin API (GraphQL `productCreate`) ou import CSV
4. **Lier le domaine** — config DNS manuellement dans le dashboard Shopify

### Résultat

Le `client.ts` du frontend contient alors :

```ts
shopify: {
  storeDomain: 'client.myshopify.com',
  storefrontAccessToken: 'pk_xxx' // créé à l'étape 2
}
```

## Env Variables

```
# .env (projet funnel)
VITE_SHOPIFY_STOREFRONT_TOKEN=pk_xxx
VITE_SHOPIFY_STORE_DOMAIN=client-store.myshopify.com
```
