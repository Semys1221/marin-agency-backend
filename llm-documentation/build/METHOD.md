# Build Method — BVG (Build → Verify → Gate)

Méthode pour builder proprement avec l'IA, unit par unit, sans accumuler de bugs.

---

## Le Cycle

Pour chaque fichier numéroté `N.md` dans `llm-documentation/build/` :

```
┌──────────────────────────────────────────────────┐
│                 0. PRE-BUILD                      │
│   Vérifier create-llm-tasks.md : spec ✅         │
│   Vérifier manual-tasks.md : prérequis cochés    │
│   Vérifier les GATES du module (AGENTS.md)       │
│   Vérifier le diagramme Eraser.io                │
│   Lire le code legacy (trash-ignore/)            │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│                  1. BUILD                         │
│   LLM lit le spec → génère le code               │
│   → place au bon endroit                         │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│                 2. VERIFY                         │
│   ┌─ Lint ─────────────────────────────────┐     │
│   │  npm run lint (JS/TS)                  │     │
│   │  ruff check . (Python)                 │     │
│   │  → Zéro erreur, zéro warning           │     │
│   └────────────────────────────────────────┘     │
│   ┌─ Typecheck ───────────────────────────┐     │
│   │  npx tsc --noEmit (JS/TS)             │     │
│   │  mypy . (Python)                      │     │
│   │  → Zéro erreur de type                │     │
│   └────────────────────────────────────────┘     │
│   ┌─ Demo & Edge Cases ───────────────────┐     │
│   │  curl ?demo=true → données mockées    │     │
│   │  Tester : empty state, error state,   │     │
│   │  missing tenant_id (401)              │     │
│   └────────────────────────────────────────┘     │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
    ❌ Échec ──────────┴────────── ✅ Réussite
    Retour BUILD                   GATE PASSED
                                   → Commit
                                   → Passer à N+1
```

---

## Règles

### 0. Pre-Build Gates — tout vérifier avant de builder

Avant de lire le moindre fichier `N.md`, le LLM doit :
1. Vérifier que la spec existe ✅ dans `create-llm-tasks.md`
2. Vérifier que les prérequis manuels sont cochés dans `manual-tasks.md`
3. Vérifier les GATES du module (dans son `AGENTS.md`)
4. Ouvrir le diagramme **Eraser.io** — confirmer que le composant existe
5. Lire le code legacy dans `trash-ignore/Github/Outreach_System/` (patterns à réutiliser)
6. S'assurer que l'environnement est prêt (dépendances installées, `.env` présent)

Si une gate est ROUGE → STOP. Ne pas builder. Signaler le blocage.

---

### 1. Un build unit à la fois
Ne jamais builder le fichier `N+1` avant que `N` ait passé le GATE. C'est la règle la plus importante — un bug dans `N` contaminera tous les suivants.

### 2. Le LLM exécute les checks
L'IA qui build doit aussi lancer les 3 commandes de VERIFY et corriger ses erreurs avant de déclarer le build fini. Elle ne passe pas au fichier suivant tant que le GATE n'est pas vert.

### 3. Pas de lint/typecheck ? Pas de build
Si le projet n'a pas de lint ou typecheck configuré, les installer **avant** de builder. C'est un prérequis au même titre qu'une API key.

### 4. Demo mode obligatoire
Chaque endpoint doit supporter `?demo=true`. Chaque composant doit supporter `DEMO_MODE=true`. Si le spec ne le précise pas, c'est un défaut du spec — le corriger avant de builder.

### 5. Dashboard HTML statique
Pour les projets sans lint/typecheck (HTML + Vanilla JS) :
- Vérifier qu'aucune erreur JS dans la console navigateur
- Vérifier que les appels API mockés retournent des données cohérentes
- Vérifier responsive (mobile first)
- Vérifier les états vides : `Service indisponible`, `Aucune donnée`

---

## Exemple d'application

```
Fichier : build/agency-backend/outreach-engine/03-campaign-creator.md

0. PRE-BUILD
   → create-llm-tasks.md : outreach-engine ✅
   → manual-tasks.md : comptes Outscraper/Gemini/Instantly cochés
   → AGENTS.md Gates : Supabase OK, placeholders OK, Eraser OK
   → Diagramme Eraser : nœud "Campaign Creator" présent
   → Code legacy lu : patterns de l'Outreach_System réutilisés

1. BUILD
   → LLM lit 03-campaign-creator.md
   → Génère le code dans outreach-engine/
   → Ajoute les endpoints avec ?demo=true

2. VERIFY
   → ruff check .                 # Zéro erreur
   → mypy .                       # Zéro erreur de type
   → curl localhost:8000/api/campaigns/create?demo=true
   → Test avec tenant_id manquant → 401
   → Test avec niche inconnue → erreur descriptive

3. GATE
   ✅ Tout vert → commit → passer à 04-campaign-queue.md
```

---

## Résumé

| Phase | Qui fait | Durée estimée |
|-------|----------|---------------|
| PRE-BUILD | LLM (vérification) | 1-2 min |
| BUILD | LLM | Jusqu'à code généré |
| VERIFY | LLM (3 commandes) | 2-5 min |
| GATE | LLM + vérif rapide humaine | 1 min |

Le cycle est rapide, reproductible, et force la qualité sans ralentir le build.
