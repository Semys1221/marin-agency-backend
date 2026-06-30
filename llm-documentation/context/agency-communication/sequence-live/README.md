# sequence-live — Séquences Email Prêtes à l'Emploi

Contenu rédigé mot pour mot, prêt à copier-coller dans les outils.

## Structure

```
sequence-live/
├── README.md
├── instantly/               ← Campagne cold outreach
│   ├── cold-contact.md      ← Version lisible (markdown)
│   └── cold-contact.json    ← Version importable (API Instantly)
├── resend/                  ← Emails transactionnels
│   ├── 01-information-requested.md / .json
│   ├── 02-no-show.md / .json
│   ├── 03-call-reminder.md / .json
│   ├── 04-invoice.md / .json
│   ├── 05-service-delivery.md / .json
│   └── 06-call-description.md / .json
└── loop/                    ← Séquences de nurturing
    ├── 01-interested.md / .json
    ├── 02-indecision.md / .json
    ├── 03-onboarding.md / .json
    ├── 04-upsell.md / .json
    └── 05-parcours.md / .json       ← 1 email/semaine, même contenu, 90 jours
```

## Utilisation

### Instantly
1. Ouvrir `instantly/cold-contact.md` pour visualiser la campagne
2. Créer la campagne dans Instantly avec les variantes A/B/C
3. Ou utiliser `sequence_creator.py`:
   ```
   python sequence_creator.py instantly create --niche "ma-niche" --activate
   ```

### Resend
1. Ouvrir le fichier `.md` du type d'email souhaité
2. Copier le template dans votre code ou Resend API
3. Remplacer les `{{variables}}` par les valeurs réelles
4. Envoyer via l'API:
   ```
   python sequence_creator.py resend send --type call-reminder --to client@email.com
   ```

### loop.so
1. Ouvrir le fichier `.md` correspondant à la séquence
2. Créer les workflows dans loop.so avec les sujets/corps fournis
3. Les fichiers `.json` peuvent être utilisés pour l'import via API

## Conventions

- `{niche_var}` = variable résolue depuis Supabase (table `niche_variable`)
- `{{lead_var}}` = variable résolue par l'outil (prénom, téléphone, etc.)
- La signature `{{gmail_signature}}` = signature standard Evan Nanguy / Marin Agency
