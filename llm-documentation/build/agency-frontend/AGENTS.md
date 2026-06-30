# Frontend Rules — Marin

**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ). Every component, step, and API call must exist as a node/edge. If it's not in the graph, don't build it.

## Rule of Thumb

**No ad-hoc UI.** Every component is a shadcn component. Every color is a CSS variable from the brand palette. No raw HTML, no custom CSS, no inline styles.

## Prerequisites — GATES

**If any gate is RED, STOP. Do not write code. Report the blocker to the user.**

### Gate 1: Shadcn initialisé

```
REQUIRED: `npx shadcn-ui@latest init` has been run.
PATTERN:  Before adding ANY component, run `npx shadcn-ui@latest add <name>`.
          Never write raw <div>, <span>, <p>, <h1>, <button> in JSX.
BLOCKER:  Shadcn not initialized → STOP. Run `npx shadcn-ui@latest init` first.
```

### Gate 2: Config client with placeholders

```
REQUIRED: `src/config/client.ts` exists with ALL values as `...`.
PATTERN:  Never hardcode a client name, domain, or API key. Every component
          reads from ClientConfig. If a value is `...`, render a fallback.
BLOCKER:  Config missing or values hardcoded → STOP. Fix config first.
```

### Gate 3: Demo mode in every component

```
REQUIRED: Every data-fetching component supports `?demo=true` or
          `DEMO_MODE=true`. When demo mode is on, return mock data.
          No real API calls. No crashes.
PATTERN:  `lib/api.ts` checks `DEMO_MODE` before every fetch.
          If true, returns dummy JSON from the variant's spec.
BLOCKER:  No dummy data provided → STOP. The variant spec is incomplete.
```

### Gate 4: Template exists before building variant

```
REQUIRED: `template/` must exist with package.json, config, store, shadcn.
PATTERN:  Never build a variant from scratch. Always start from template:
          `cp -r template clients/{tenant_id}`, then edit config, then build
          the step components.
BLOCKER:  Template missing → STOP. Create template/ first.
```

### Gate 5: Eraser diagram verified

```
REQUIRED: Open the Eraser diagram before writing a single component.
          Every funnel step, API call, and integration must be in the graph.
BLOCKER:  Diagram not verified → STOP. Check it now.
```

### Gate 6: No raw HTML

```
REQUIRED: Every piece of UI uses a shadcn component. Zero <div>, <span>,
          <section>, <p>, <h1>, <button>, <input> directly in JSX.
PATTERN:  Layout → <Card>, Form → <Input> + <Label>, Feedback → <Progress>,
          Overlay → <Dialog>, Navigation → <Tabs>, Display → <Badge>.
          Text always wrapped in a Card or Dialog component.
BLOCKER:  Raw HTML detected → STOP. Refactor to use shadcn.
```

## Allowed Components Only

| Category | Components |
|----------|-----------|
| Layout | `Card`, `CardHeader`, `CardContent`, `CardFooter`, `Separator` |
| Form | `Input`, `Textarea`, `Select`, `SelectTrigger`, `SelectContent`, `SelectItem`, `Label`, `Button` |
| Feedback | `Progress`, `Toast`, `Skeleton` |
| Overlay | `Dialog`, `Sheet`, `Tooltip` |
| Navigation | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`, `DropdownMenu` |
| Display | `Badge`, `Avatar`, `Table` |

## Image Storage

| Type | Destination |
|------|-------------|
| Brand (logo, favicon, global CSS) | `agency-book/Esthetic/` |
| Reference images (screenshots, mockups, wireframes) | `agency-frontend/reference/` |
| App runtime images (product photos, etc.) | `public/` in the Vite client project |
| Dynamic images (Shopify CDN, etc.) | Fetched from API — not stored locally |

## Design Tokens

| Token | CSS Variable | Hex |
|-------|-------------|-----|
| Accent light | `hsl(var(--primary))` | `#49C5B6` |
| Accent dark | `hsl(var(--primary-foreground))` | `#015048` |
| Background | `hsl(var(--background))` | `#FAFAFA` |
| Text | `hsl(var(--foreground))` | `#000000` |

Use Tailwind classes: `bg-background`, `text-foreground`, `bg-primary`, `text-primary-foreground`. Never hardcode hex values.

## Dashboard Clients (HTML Statique)

Le dossier `dashboard/` contient les dashboards clients HTML statique. Stack différent du funnel :

| Aspect | Funnel (funnel) | Dashboard (dashboard/) |
|--------|-----------------|----------------------|
| Stack | React + Shadcn + Zustand | HTML + Vanilla JS |
| Endpoint | Nombreux appels individuels | 1 seul `GET /api/dashboard` |
| Public | Prospect (pré-vente) | Client (post-onboarding) |
| Instance | 1 par client (copie du template) | 1 par client (copie du template) |

Voir `dashboard/AGENTS.md` pour les règles de conception dashboard.

## Process

1. Check all gates are GREEN
2. Check `reference/` for screenshots, mockups, or wireframes of the variant — inspect them before coding
3. Copy template: `cp -r template clients/{tenant_id}`
4. Edit `src/config/client.ts` (branding, tokens, apiBase, tenantId)
5. Build step components following the variant README spec
6. Verify demo mode works: `?demo=true` renders mock data without backend
7. Deploy: `cd clients/{tenant_id} && vercel --prod`
