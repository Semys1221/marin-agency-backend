# Marin — Working Method (Simplified)

This document defines the operating workflow for any LLM agent working on this project.

## Source of Truth

Le diagramme **Eraser.io** (`model-marin-agency`) est la source de vérité unique pour toute l'architecture.
**Référence :** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

## Core Files

| File | Role |
|------|------|
| `llm-documentation/build/` | **Build** — specs actionnables à donner directement à un LLM pour builder |
| `llm-documentation/context/` | **Context** — documentation, assets, référence (commercial, branding, séquences) |
| `prerequisite.md` | **Manual tasks** — tout ce qui doit être configuré/setup manuellement avant de builder |
| `create-llm-tasks.md` | **LLM tasks inventory** — inventaire des specs existants (✅) et à créer (❌) |
| `overview.md` | Vision globale du projet |

## The Workflow (Spec-First, Build-Second)

### Phase 1 — Spec
Si une task est ❌ dans `create-llm-tasks.md` :
→ Créer le dossier `build/<ressource>/` ou `context/<ressource>/` selon la nature de la spec.

### Phase 2 — Build
Si une task est ✅ dans `create-llm-tasks.md` :
1. Vérifier `prerequisite.md` — les prérequis manuels sont-ils cochés ?
2. Donner le dossier `build/<ressource>/` à un LLM worker.
3. Suivre l'`AGENTS.md` ou `OVERVIEW.md` du dossier.

**Règle :** Ne jamais donner `agency-frontend` ou `agency-dashboard` à un LLM avant que `agency-backend` soit déployé.
