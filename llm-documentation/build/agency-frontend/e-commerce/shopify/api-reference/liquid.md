# Liquid Reference

Liquid is a template language created by Shopify, used to build [Shopify Themes](https://shopify.dev/themes).

## Basics

Liquid outputs objects and their properties, with logic via tags and filters.

```liquid
<title>{{ page_title }}</title>
{% if page_description -%}
  <meta name="description" content="{{ page_description | truncate: 150 }}">
{%- endif %}
```

## Tags (Logic)

Tags use `{% %}` delimiters.

```liquid
{% if product.available %}
  Price: $99.99
{% else %}
  Sorry, this product is sold out.
{% endif %}
```

### Common Tags
- `{% if %}`, `{% else %}`, `{% endif %}` — Conditionals
- `{% for item in array %}`, `{% endfor %}` — Loops
- `{% assign var = value %}` — Variable assignment
- `{% capture var %}` — Capture block output
- `{% include 'snippet' %}` — Include snippets
- `{% section 'name' %}` — Include sections
- `{% liquid %}` — Multiple tags in one block

## Filters (Output Modification)

Filters use the `|` pipe character.

```liquid
{{ product.title | upcase }}
{{ product.title | remove: 'Health' }}
{{ product.title | upcase | remove: 'HEALTH' }}
```

### Common Filters
- `append`, `prepend` — String concatenation
- `capitalize`, `upcase`, `downcase` — Case transformation
- `truncate: 150` — Truncate strings
- `date: "%Y-%m-%d"` — Date formatting
- `money`, `money_with_currency` — Price formatting
- `link_to`, `img_tag` — HTML generation
- `json` — JSON output
- `where`, `map`, `sort` — Array manipulation

## Objects

Objects use `{{ }}` delimiters and represent store resources.

```liquid
{{ product.title }}
{{ collection.products }}
{{ shop.name }}
{{ customer.email }}
```

### Common Objects
- `product` — Current product resource
- `collection` — Current collection resource
- `cart` — Shopping cart
- `customer` — Logged-in customer
- `shop` — Store settings
- `page` — Current page
- `article`, `blog` — Blog content
- `linklist` — Navigation menus
- `settings` — Theme settings

Object access: globally available, template-specific, or through parent objects.

## Resources

- [Liquid Cheat Sheet](https://www.shopify.com/partners/shopify-cheat-sheet)
- [Theme Check](https://shopify.dev/themes/tools/theme-check) (VS Code linter)
- [Shopify CLI for Themes](https://shopify.dev/themes/tools/cli)
- [Open source Liquid](https://github.com/Shopify/liquid)

Source: [Liquid docs](https://shopify.dev/docs/api/liquid)
