# Build Rules — Marin

> Le cycle complet de build (Pre-Build → Build → Verify → Gate) est défini dans [METHOD.md](./METHOD.md).

## Source of Truth

Eraser.io diagram (`model-marin-agency`) : https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

Tout ce que tu construis doit exister dans ce diagramme. Si ce n'est pas dans le graphe, ne le construis pas.

## GATES (vérifier avant chaque build)

### Gate 1: Supabase déployé
Tous les appels DB wrap dans try/catch. Si connexion échoue → rendre "Service indisponible", jamais de crash.

### Gate 2: API keys en placeholder
Toutes les clés API dans env.variables avec valeur `...`. Si valeur = `...`, le service retourne une erreur descriptive. Jamais de hardcode.

### Gate 3: Eraser.io vérifié
Ouvrir le diagramme avant d'écrire la moindre ligne de code. Vérifier que le composant existe comme node/edge.

### Gate 4: Auth model
Single shared DB. `X-Tenant-ID` header. Pas de login/signup. Si header manquant → 401.

### Gate 5: Demo mode sur chaque endpoint
`?demo=true` retourne des données mockées. Aucun appel API externe. Aucun effet de bord.

### Gate 6: Code existant lu
Lire `trash-ignore/Github/Outreach_System/` avant d'écrire du nouveau code. Réutiliser les patterns.

## Règles

### 1. 1 fichier = 1 session AI
Chaque fichier numéroté est un build unit. Builder dans l'ordre numérique. Ne jamais builder le fichier `N+1` avant que `N` soit déployé.

### 2. Chaque fichier est self-contained
DB schema, code API, env vars, edge cases, dummy data — tout est dans le fichier. Pas besoin de chercher ailleurs.

### 3. Tech stack locked
| Phase | Stack |
|-------|-------|
| Outreach | Python 3.12+, FastAPI, APScheduler |
| Frontend | NodeJS 20+, Express, Prisma |
| Frontend (UI) | Next.js/React, Zustand, Shadcn |
| Dashboards | HTML statique + Vanilla JS |
| DB | Supabase Postgres |
| AI | Gemini 1.5 Flash |

### 4. Pas d'ad-hoc
Si un composant n'est pas dans le diagramme Eraser, ne pas le builder. Si tu en as besoin, update le diagramme d'abord.
