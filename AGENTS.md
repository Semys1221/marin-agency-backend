# Marin — LLM Rules

Marin is a digital agency. You are a senior developer — your goal is to help build the project by writing simple, maintainable code. Anti-overengineering. Always propose easy practices, prebuilt packages, or no-code/low-code solutions when available.

## Source of Truth

Le diagramme **Eraser.io** (`model-marin-agency`) est la source de vérité unique pour toute l'architecture.
**Référence :** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

## Workflow

### Phase 1 — Spec (❌ → ✅ dans `create-llm-tasks.md`)
Si une task est ❌ dans `create-llm-tasks.md`, le spec n'existe pas encore.
→ Créer le dossier `llm-documentation/<ressource>/` avec les fichiers de spec.
Une LLM task complète = dossier contenant README.md, AGENTS.md, template/, specs variants.

### Phase 2 — Build (✅ → code implémenté)
Si une task est ✅ dans `create-llm-tasks.md`, le spec existe dans `llm-documentation/<ressource>/`.
→ Donner ce dossier à un LLM worker pour builder le code.
→ Suivre l'`AGENTS.md` ou `OVERVIEW.md` du dossier.

### Vérification préalable
1. Vérifier les dépendances dans `prerequisite.md` (section en haut)
2. Cocher les prérequis manuels avant de donner le dossier au LLM

## Règles

- **Spec d'abord, build ensuite** — ne jamais builder un dossier qui n'a pas de spec complet
- Ne jamais builder sans que les prérequis soient cochés
- Ne jamais donner `agency-frontend` ou `agency-dashboard` à un LLM avant `agency-backend`
- Commencer chaque session par lire les 4 fichiers racine : `README.md`, `overview.md`, `create-llm-tasks.md`, `prerequisite.md`
