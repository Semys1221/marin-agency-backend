# Workflow — Production Vidéo avec OpenCode + Remotion

Ce workflow produit une vidéo motion design complète sans éditeur vidéo. Tout se passe dans OpenCode + un navigateur (Remotion Studio).

---

## Phase 1 — Installation

```bash
mkdir video-project && cd video-project
npm init -y
npm i remotion @remotion/cli @remotion/renderer
npx remotion init
npm run remotion studio
```

Remotion Studio s'ouvre dans le navigateur. Chaque composition apparaît dans la sidebar.

---

## Phase 2 — Art Direction

Avant d'écrire du code, définir le style visuel. Prompt à donner à OpenCode :

```
Create an ART_DIRECTION.md file in the project root with these sections:

1. COLOR PALETTE — brand colors (accent: #49C5B6, dark accent: #015048, bg: #FAFAFA, text: #000000)
2. TYPOGRAPHY — Inter for both headings and body
3. VISUAL VIBE — clean, modern, data-driven, Vox-like cut-out style
4. MOTION LANGUAGE — spring physics for pop-ins, smooth easing for transitions
5. BACKGROUND — solid light or dark with subtle gradient, no noise

Use actual Tailwind/CSS color values. Be specific enough that any scene
generated will look consistent with this direction.
```

Cette phase ne génère pas de code vidéo — elle établit le cadre créatif.

---

## Phase 3 — Story (Scènes + Flow)

Définir les scènes, leur ordre et leur timing. Prompt :

```
Create a STORY.md file defining the video structure.

Format:
Scene 1 (0-5s):   Hook / Opening visual
Scene 2 (5-20s):  Problem statement
Scene 3 (20-40s): Solution presentation
Scene 4 (40-55s): How it works / Key features
Scene 5 (55-65s): Social proof / Results
Scene 6 (65-75s): CTA / Closing

For each scene include:
- Duration in seconds (and frames at 30fps)
- On-screen text or key message
- Visual description (cut-outs, charts, animations)
- Voice-over narration text (if any)
- Transitions (cut, fade, slide)
```

Le storyboard guide toutes les phases suivantes.

---

## Phase 4 — Asset Spec (Inventory)

Définir les assets visuels nécessaires. Prompt :

```
Based on STORY.md, create an ASSETS.md file specifying every
visual element needed.

For each asset specify:
- Type: cutout | icon | chart | text | background
- Description (e.g. "illustration of a sales person on phone")
- Dimensions / aspect ratio
- Color constraints
- Animation intent (spring-in, fade, draw, count-up)
- If it's a chart: data points, labels, animation style

Separate into "static library" (reusable across scenes) and
"scene-specific" (only used once).
```

Cette phase évite les assets incohérents d'une scène à l'autre.

---

## Phase 5 — Motion Primitives

Définir des patterns d'animation réutilisables. Prompt :

```
In src/motion/primitives.ts, create reusable animation functions:

1. fadeIn(delay: number) → spring-based opacity 0→1
2. springIn(delay: number, direction: 'up' | 'left' | 'right' | 'down') → position + scale spring
3. countUp(from: number, to: number, frame: number, duration: number) → animated number
4. drawLine(delay: number, length: number) → line that draws itself
5. staggerChildren(parentDelay: number, childGap: number, count: number) → staggered children

Use Remotion's spring() and interpolate() from 'remotion'.
Each primitive should accept (frame: number, ...params) and return
CSS-compatible values (opacity, transform string, etc).

Export all primitives as named exports.
```

Ces primitives sont le "vocabulaire d'animation" de la vidéo.

---

## Phase 5.5 — QC Loop (Autonomous Quality Control)

Avant de builder chaque scène, activer la boucle adversarial builder/judge pour garantir la qualité sans intervention humaine.

### Prerequisites

- `definition-of-done.md` dans la racine du projet (critères qualité vidéo)
- Hermes Agent avec le skill `loop-engineer` chargé
- Modèle AI configuré (Gemini recommandé)

### DoD template pour vidéo

```markdown
# Definition of Done — Vidéo

## Technique
- [ ] Aucune erreur runtime Remotion
- [ ] Toutes les scènes rendent sans crash
- [ ] Durée totale = spec (tolérance ±5 frames)
- [ ] Résolution correcte (1920x1080)

## Animation
- [ ] Toutes les animations se déclenchent
- [ ] Pas d'overlap d'animations (stagger correct)
- [ ] Transitions fluides entre scènes

## Contenu
- [ ] Texte sans faute
- [ ] Assets visuels présents (pas de placeholder)
- [ ] Voice-over synchro audio → texte
```

### Boucle

```
Scène buildée → Judge Hermes analyse via DoD → PASS → scène suivante
                                          → FAIL → feedback builder → rebuild
```

### Prompt d'activation

```
/skill loop-engineer
Target: src/scenes/Scene1.tsx
DoD: definition-of-done.md
Max loops: 5
```

Max loops bas (5) pour la vidéo — une boucle infinie bloquerait tout le projet. En cas de hard fail, escalader vers le humain.

---

Générer chaque scène comme un composant React. Prompt pour chaque scène :

```
Based on STORY.md Scene 1, ASSETS.md, and the motion primitives in
src/motion/primitives.ts, create src/scenes/Scene1.tsx.

Requirements:
- Import { useCurrentFrame } from 'remotion'
- Import { AbsoluteFill } from 'remotion'
- Use primitives from src/motion/primitives.ts for ALL animations
- Animate elements in the order specified in STORY.md
- Use <Sequence from={startFrame}> to structure timing
- Background color from the art direction palette
- All text uses the brand typography

Scene 1 spec:
- Duration: 120 frames (4s at 30fps)
- Elements: [list from ASSETS.md]
- Animation order: [from STORY.md]
```

Répéter pour chaque scène. Tester dans Remotion Studio après chaque scène.

---

## Phase 7 — Composition (Assemblage)

Assembler toutes les scènes dans le fichier `src/Root.tsx`. Prompt :

```
Create src/Root.tsx that imports all 6 scene components.

Register a single <Composition> with:
- id: "MainVideo"
- fps: 30
- width: 1920
- height: 1080
- durationInFrames: total from STORY.md

Render all scenes sequentially using <Sequence from={...}>.
Export Root as default.
```

---

## Phase 8 — Voice-over Sync (Optionnel)

Si une narration est enregistrée, la synchroniser :

1. Placer le fichier audio dans `public/voiceover.mp3`
2. Prompt dans OpenCode :

```
Import the voiceover file into the composition.
Add <Audio src={staticFile('voiceover.mp3')} /> to Root.tsx.
Adjust each scene's frame range to align with narration timing.

The narration text per scene is in STORY.md. Sync scene
transitions to match spoken words — each scene should start
and end on its own sentence in the narration.
```

---

## Phase 9 — Render

Prompt final :

```
Render the composition "MainVideo" to an MP4 file in out/
with medium quality for preview.

Command: npx remotion render src/index.ts MainVideo out/output.mp4
```

Pour le rendu final (haute qualité) :

```
Render in ProRes for highest quality.
npx remotion render src/index.ts MainVideo out/output.mov \
  --codec prores --prores-profile 4444
```

---

## Phase 10 — Post-Production (Optionnel)

Si nécessaire :
- Ajouter la musique de fond dans un éditeur audio ou via Remotion (`<Audio />`)
- Ajuster le timing après avoir vu le rendu — itérer par prompts
- Exporter en MP4 pour le web (H.264)

---

## Récapitulatif des fichiers produits

```
video-project/
├── ART_DIRECTION.md      (phase 2)
├── STORY.md              (phase 3)
├── ASSETS.md             (phase 4)
├── src/
│   ├── Root.tsx           (phase 7 — composition + assembly)
│   ├── index.ts           (entry point, created by remotion init)
│   ├── motion/
│   │   └── primitives.ts  (phase 5 — animation library)
│   └── scenes/
│       ├── Scene1.tsx     (phase 6)
│       ├── Scene2.tsx
│       ├── Scene3.tsx
│       ├── Scene4.tsx
│       ├── Scene5.tsx
│       └── Scene6.tsx
└── public/
    └── voiceover.mp3      (phase 8 — optionnel)
```
