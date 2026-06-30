# Agency Frontend Model

Frontend funnel templates and specs for Marin agency projects. Each client gets their own Vercel instance duplicated from `template/`.

**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ). Every component, step, and API call must trace back to a node/edge in the graph.

## Build Order

An agent MUST follow this order — never build a variant before the template exists.

| Step | Module | Depends on | Why |
|------|--------|------------|-----|
| 1 | **`template/`** | Nothing | Base project — created once, copied per client |
| 2 | **`marin-agency/README.md`** | template | Full funnel spec (22 steps) — uses template structure |
| 3 | **`e-commerce/README.md`** | template | Full funnel spec (11 steps) — variant of agency funnel |
| 4 | **`dashboard/`** | Backend API deployed | 3 dashboards HTML statique consomment `GET /api/dashboard` |
| 5 | **Deploy** | All above | 1 Vercel instance per client — edit `config/client.ts`, deploy |
| 6 | **`crash-test-sandbox/README.md`** | template + backend | Procédure de simulation client (Stripe + Dropbox test) |
| 7 | **`production-go-live/README.md`** | crash-test sandbox | Checklist de mise en production client |
| 8 | **`call-recording/README.md`** | template + backend | Système d'enregistrement d'appels + transcription |

## Structure

| Chemin | Description |
|--------|-------------|
| `AGENTS.md` | Règles de conception : gates, design tokens, shadcn only |
| `template/README.md` | Template duplication — copier pour chaque nouveau client |
| `marin-agency/README.md` | Spec funnel 22 steps (agency principale) |
| `marin-agency/textual-content.md` | Contenu marketing (headlines, forms, CTAs) |
| `marin-agency/prompt-design.md` | Prompt Google Stitch pour mockups |
| `e-commerce/README.md` | Spec funnel 11 steps (grossiste) |
| `e-commerce/textual-content.md` | Contenu marketing variant e-commerce |
| `e-commerce/prompt-design.md` | Prompt Google Stitch pour mockups e-commerce |
| `reference/` | Mockups, screenshots, wireframes exportés — références visuelles pour le LLM |
| `crash-test-sandbox/README.md` | Procédure de simulation réelle avant go-live |
| `production-go-live/README.md` | Checklist de mise en production client |
| `call-recording/README.md` | Système d'enregistrement d'appels + transcription IA |
| `dashboard/` | Dashboards clients HTML statique (marin + e-commerce + template) |
| `dashboard/AGENTS.md` | Règles dashboard : static HTML only, no framework |
| `dashboard/marin-dashboard/README.md` | Spec dashboard client Marin Agency |
| `dashboard/ecommerce-dashboard/README.md` | Spec dashboard client e-commerce |
| `dashboard/template/README.md` | Template duplication dashboard client |
