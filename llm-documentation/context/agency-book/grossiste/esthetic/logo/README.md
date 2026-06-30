# Logo Assets — Usage Guide

## SVGs (vector source)

| File | When to use |
|---|---|
| `logo.svg` | Primary logo — dark green gradient. Use in navbars, headers, splash screens. |
| `logo-white.svg` | White version for dark backgrounds (e.g., dark mode navbar, dark hero sections). |
| `logo-black.svg` | Black version for light backgrounds (e.g., light mode, print on white paper). |

## favicon.ico

Multi-size icon (16×16 + 32×32 + 48×48) for browser tabs. Place in site root:

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
```

## Favicon PNGs

Modern alternative to `.ico`. Serve with:

```html
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
```

## Apple Touch Icon

iOS home screen (180×180):

```html
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

Also available as `-white` and `-black` variants for dark/light mode iOS bookmarks.

## PWA Icons

For Progressive Web App manifest:

```html
<link rel="manifest" href="/site.webmanifest">
```

| File | Purpose |
|---|---|
| `icon-192.png` | Splash screen icon |
| `icon-512.png` | Install prompt icon |
| `icon-192-white.png` | Monochrome (adaptive icon on Android) |
| `icon-512-white.png` | Monochrome (adaptive icon on Android) |

## White & Black Variants

Every format has `-white` and `-black` suffixed versions:

- **`-white`** — for dark backgrounds (e.g., dark mode, overlays on images)
- **`-black`** — for light backgrounds (e.g., light mode, print)

## site.webmanifest

PWA manifest referencing the green and monochrome icons. Edit the `name`/`short_name` fields to match your app name before deploying.

---

**Color values used:**
- Dark green: `#153826` (average) / `#204129` (gradient center)
- Gradient: radial from `#204129` (center) → `#071A12` (edge)
