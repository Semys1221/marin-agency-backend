# Video Marketing Rules — Marin

**Source of truth :** Les specs dans `video-marketing/`. Chaque vidéo produite doit suivre le workflow défini dans `workflow.md` et utiliser les prompts du dossier `prompts/`.

## Prerequisites — GATES

### Gate 1: Node.js 20+ installé

```
REQUIRED: node -v → v20.x ou supérieur
BLOCKER:  Node.js absent → STOP. Installer via nvm.
```

### Gate 2: Remotion installé

```
REQUIRED: npm ls remotion (ou remotion présent dans package.json)
PATTERN:  npm init -> npm i remotion @remotion/cli @remotion/renderer
BLOCKER:  Remotion absent → STOP. Lancer le setup décrit dans workflow.md.
```

### Gate 3: FFmpeg disponible

```
REQUIRED: ffmpeg -version → doit retourner une version
PATTERN:  brew install ffmpeg (sur mac)
BLOCKER:  FFmpeg absent → STOP. Installer avant de lancer le workflow.
```

### Gate 4: Projet Remotion initialisé

```
REQUIRED: Remotion Studio se lance (npm run remotion studio)
PATTERN:  Lancer Studio dans un terminal séparé pendant le workflow
BLOCKER:  Studio ne démarre pas → STOP. Vérifier l'install.
```

## Règles de production

### 0. QC Loop — Autonomous Quality Control

Toute production vidéo passe par une boucle adversarial builder/judge avant validation.

```
Builder → génère l'asset → Judge → analyse via Definition of Done
    ↑                                │
    └────────── boucle QC ───────────┘
         (max 5 itérations, sinon escalade humaine)
```

- La `definition-of-done.md` doit exister à la racine du projet vidéo
- Le skill Hermes `loop-engineer` doit être chargé
- Max 5 loops — en cas de hard fail, bloquer et demander intervention humaine

### 1. Spec d'abord, code ensuite

Avant d'écrire une ligne de code vidéo, définir dans un fichier de spec :
- **Art direction** (palette, typo, vibe)
- **Story** (scènes, flow, timing)
- **Asset inventory** (cut-outs, icônes, charts)
- **Motion primitives** (patterns d'animation)

### 2. Itérer dans OpenCode

Ne jamais éditer le code Remotion à la main. Toujours itérer via des prompts en langage naturel :
```
"Animate scene 1 with the logo springing up first, followed by the tagline.
Stagger them so they don't all move at once."
```

### 3. Preview en temps réel

Garder Remotion Studio ouvert (`npm run remotion studio`) visible dans le navigateur pendant tout le workflow. Les modifications de code apparaissent instantanément.

### 4. Voice-over sync

Si la vidéo a une narration, la voice-over doit être prête AVANT le sync. Utiliser FFmpeg pour extraire le timing si besoin.

### 5. Render final

| Usage | Format | Qualité |
|-------|--------|---------|
| Web (landing page, social) | MP4 | Medium-High |
| Client delivery / montage | ProRes `.mov` | Best |
| Preview / itération | MP4 | Low |

### 6. Assets

| Type | Source |
|------|--------|
| Cut-outs personnages / objets | Générés par IA (Midjourney, DALL-E) ou libres de droit |
| Logo Marin | `agency-book/grossiste/esthetic/` |
| Icônes | Lucide React (shadcn native) ou SVG custom |
| Charts | Code Remotion (spring + interpolate) |
| Background music | Royalty-free (Pixabay, Uppbeat) |
| Voice-over | Enregistrement interne ou ElevenLabs |

## Process

1. Vérifier les 4 gates
2. Lire le workflow (`workflow.md`)
3. Choisir le type de vidéo → sélectionner le prompt dans `prompts/`
4. Lancer Remotion Studio dans un terminal
5. Exécuter le workflow depuis OpenCode
6. Itérer par prompts en langage naturel jusqu'au résultat satisfaisant
7. Rendre la version finale
