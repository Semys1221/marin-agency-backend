# Context — Documentation & Référence

Ce dossier définit **ce qui est injecté en contexte** dans les specs de `build/`. Il ne contient pas de code, ni de specs actionnables — seulement la matière première qui nourrit la construction.

## Logique

L'agence dans `build/` est pensée comme un **shell** : une architecture réutilisable (backend, frontend, communication) qui reste stable quelle que soit la niche qu'on y insère. Le `context/` contient tout ce qui **varie** ou s'**ajoute** au fil du temps :

- **`agency-book/`** — Offres, contrats, positionnement, branding. Le "quoi" qu'on vend.
- **`agency-communication/`** — Séquences email, configurations live, comptes. Le "comment" on communique.
- **`duplication-method/`** — Pattern pour dupliquer proprement un dossier de spec LLM.

## Niche actuelle vs niches futures

Actuellement, nous (Marin — agence marketing) nous adressons à **1 niche** : les **grossistes**. Toute la stack (funnel 22 steps, offres, contrats, séquences) est calibrée pour eux.

Mais l'agence reste **la même** quel que soit le client. Le shell ne change pas. Si demain on s'adresse à des **couvreurs**, des **médecins**, ou n'importe quelle autre niche, on :

1. Ne touche pas au shell (`build/`)
2. Ajoute une nouvelle spec dans `build/` qui référence le contexte existant
3. Ajuste le contenu commercial dans `context/agency-book/` si nécessaire

Nous sommes **l'agence marketing** — le client change, pas nous.

## Relation Build ↔ Context

```
build/agency-backend/       ← Le shell technique (API, DB, scraping, infra)
build/agency-frontend/      ← Le shell funnel (agency 22-step, e-commerce 11-step)
build/agency-frontend/dashboard/  ← Dashboards clients statiques
    ↓
    utilisent / référencent
    ↓
context/agency-book/        ← Offres, contrats, branding (le contenu commercial)
context/agency-communication/ ← Séquences, templates email, configurations live
```

Le shell reste identique — le contexte change selon le client ou la niche.
