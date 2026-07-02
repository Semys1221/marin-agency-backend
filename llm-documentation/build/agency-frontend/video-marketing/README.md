# Video Marketing — Marin

Produire des vidéos motion design style Vox (explainer, landing page, motion graphics) en utilisant **OpenCode + Remotion**. Aucun logiciel de montage vidéo (After Effects, Premiere) requis — tout est généré par code React.

## Pourquoi ce dossier

Marin a besoin de contenu vidéo pour son propre marketing : vidéo de présentation du service, explication du funnel, témoignages dynamiques, contenu social. Au lieu de payer un motion designer ou d'apprendre After Effects, on utilise OpenCode pour générer des vidéos programmatiquement via Remotion.

## Stack

| Technologie | Rôle |
|-------------|------|
| **OpenCode** | Agent LLM qui écrit le code, exécute les commandes et itère |
| **Remotion** | Framework React de vidéo programmatique (npm) |
| **FFmpeg** | Analyse de vidéos existantes, extraction de frames |
| **Node.js 20+** | Runtime |
| **npm** | Gestion de packages |

## Types de vidéos qu'on peut produire

| Type | Usage | Durée typique |
|------|-------|---------------|
| **Explainer** | Présentation du service Marin sur la landing page | 60-90s |
| **Funnel step** | Animation pour une étape du tunnel de vente | 15-30s |
| **Testimonial** | Témoignage client dynamique (chiffres, barres) | 30-60s |
| **Social clip** | Court format pour LinkedIn / Instagram | 15-30s |
| **Onboarding** | Vidéo d'explication pour client après vente | 60-120s |

## Conventions

- **Design system** : Utiliser les tokens du branding Marin (couleurs, typo) définis dans `agency-frontend/AGENTS.md`
- **Police** : Inter (headings) + Inter (body) — identique au funnel
- **Voice-over** : Optionnel — peut être ajouté dans Remotion ou monté après
- **Durée** : Définie dans le spec de chaque vidéo (fps, frames)
- **Render** : ProRes `.mov` à la meilleure qualité pour édition, ou MP4 pour web

## Build Order

| Step | Fichier | Description |
|------|---------|-------------|
| 1 | `AGENTS.md` | Règles et gates pour la production vidéo |
| 2 | `workflow.md` | Méthode pas-à-pas (art direction → render) |
| 3 | `prompts/` | Prompts prêts-à-l'emploi par type de vidéo |
