# Marin — Daily Work Routine

Routine opérationnelle journalière du projet Marin Agency Backend.  
Objectif : progression prévisible, sans oublis, sans surcharge.

---





## Structure de la journée

| Créneau | Durée | Focus |
|---------|-------|-------|
| 08h00 – 08h30 | 30 min | Morning tri : emails + Slack + tickets |
| 08h30 – 09h00 | 30 min | Revue de `update.md` : mettre à jour les cases cochées |
| 09h00 – 12h30 | 3h30 | Deep work — un seul module à la fois |
| 12h30 – 13h30 | 1h | Pause |
| 13h30 – 16h30 | 3h | Deep work — suite ou second module selon avancement |
| 16h30 – 17h00 | 30 min | Wrap-up : commit + update `update.md` + note dans `manual-tasks.md` si blocker |
| 17h00 – 17h30 | 30 min | Tests manuels rapides + vérification déploiements Render/Vercel |

Total deep work : 6h30 par jour  
Total overhead : 1h30 par jour

---





## Morning tri — 08h00

1. **Emails** — traiter seulement les sujets « Marin », « Supabase », « Render », « Stripe », « Vercel », « Shopify », « Instantly », « Resend ».  
   Ignorer le reste.
2. **Slack** — vérifier uniquement le channel `#marin-engine` s’il existe.
3. **Tickets** — regarder `update.md` section « blockers » si j’en ai créé une la veille.
4. **Render / Vercel deploy status** — 2 clics : vérifier que le dernier deploy est healthy.

Si un deploy est en erreur : 15 min de debug avant deep work, sinon on ignore et on avance la veille.

---





## Deep work — règles

1. **Un seul module actif par session** — ne pas ouvrir le prochain dossier avant que le courant soit ✅ dans `update.md`.
2. **Ordre strict** : spec d’abord, build ensuite. Jamais l’inverse.
3. **Avant de donner un dossier à un LLM** : vérifier les prérequis cochés dans `manual-tasks.md`.
4. **Anti-overengineering** :
   - préférer un package existant
   - pas de duplication avant 3 occurrences
   - pas d’abstraction prématurée
5. **Demo mode d’abord** — toute feature doit avoir un mode démo fonctionnel avant connexion aux vrais services.

---





## Fin de journée — 16h30

1. `git add -A && git commit -m "progress: <module> — <ce qui a été fait>" && git push`
2. Ouvrir `update.md` et cocher toutes les cases de la journée.
3. Si blocker non résolu : ajouter une ligne dans `manual-tasks.md` section « Tasks à faire » avec contexte précis.
4. Git commit des docs mises à jour.
5. Noter dans un fichier `WORKLOG.md` à la racine :
   - Module travaillé
   - Ce qui a été accompli
   - CE QUI NE MARCHE PAS / blocker
   - Plan pour demain matin

---





## Exemple de journée type

### Jour 1 — Backend API spec

- **08h00** : tri emails + render deploy status ✅
- **08h30** : update `update.md`
- **09h00–12h30** : créer `build/agency-backend/backend-api/README.md` + routes API listées
- **13h30–16h30** : créer `backend-api/AGENTS.md` + template code
- **16h30** : commit + push + `update.md` case cochée
- **17h00** : vérifier `npm run dev` template frontend (template toujours vert)

### Jour 2 — Integrations spec

- Même rituel, focus `build/agency-backend/integration/`

---





## Checklist quotidienne

- [ ] Morning tri fait
- [ ] Deep work ≥ 6h
- [ ] Un seul module travaillé
- [ ] `update.md` mis à jour avec les cases du jour
- [ ] Commit + push faits
- [ ] Blocker noté si applicable
- [ ] Deploys Render/Vercel vérifiés healthy

---





## Règle d’arrêt

Si un problème prend plus de 45 min sans avancer :
1. Le documenter dans `manual-tasks.md`
2. Passer à un autre module
3. Revenir le lendemain avec du recul

Le projet avance par modules complétés, pas par résolution de bugs infinie.
