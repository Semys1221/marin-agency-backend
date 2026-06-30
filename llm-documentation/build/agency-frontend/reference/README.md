# Reference — Images & Visuels

Références visuelles pour le développement du frontend.

## Convention de stockage

| Contenu | Destination |
|---------|-------------|
| Brand (logo, favicon, global CSS) | `agency-book/Esthetic/` |
| Mockups, screenshots, wireframes du frontend | `agency-frontend/reference/` |
| Images dynamiques de l'app (produits, etc.) | `public/` dans le projet client (Vite) |

## Structure

```
reference/
├── README.md        ← this file
├── screenshots/     ← Captures d'écran du funnel réel
├── mockups/         ← Exports Google Stitch / Figma / design tool
└── wireframes/      ← Schémas fonctionnels, user flows
```

## Quand ajouter une image ici

- Un mockup de funnel a été créé dans un outil externe → exporter dans `mockups/`
- Une capture d'écran d'un funnel existant doit servir de référence → `screenshots/`
- Un schéma de flux ou d'architecture UI est nécessaire → `wireframes/`

Les images dans `reference/` sont lues par l'agent LLM pour comprendre le rendu attendu avant de coder.
