# User Config — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=nN0c_LscKTt8USVzd0cm

## GATES (must check before building)

- **Gate 1:** Supabase project deployed with URL + service_role_key in env vars. Every DB call wraps in try/catch — never crash.
- **Gate 2:** All API keys defined in env vars with value `...` if not configured. Every API wrapper checks `if (!key || key === '...') return { error: 'non configuré' }`.
- **Gate 3:** Open Eraser diagram before writing a single line. Verify component exists as a node.
- **Gate 4:** Single shared DB. No user accounts. `X-Tenant-ID` header isolates data. Never implement login.
- **Gate 5:** Read existing code in `trash-ignore/Github/Outreach_System/` before writing new code. Reuse patterns.
- **Gate 6:** Every endpoint must support `?demo=true` returning mock data. No real API calls in demo mode.

## Architecture

```
CLI (create-tenant-cli.py) ──→ config.json + sequences.json
                                      │
                                      ▼
                              Rotation Engine (if/else)
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
                     scraper                    push-instantly
                  (outscraper)                    (Instantly API)
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                              Supabase campaign_analytics
                                      │
                                      ▼
                              Rotation Engine (métriques)
```

## Tech Stack

| Layer | Stack |
|-------|-------|
| Runtime | Python 3.12+, CLI interactif |
| CLI | Python, OpenAI SDK (IA Hermes pour suggestions) |
| Rotation | if/else (zéro IA), APScheduler |
| Scraping | Outscraper SDK |
| Email validation | dnspython (MX), Handshake API, DBBounce API |
| Campaigns | Instantly API V2 |
| Notifications | Slack Web API |
| DB | Supabase (`supabase` pip) |

## Purpose

Chaque tenant possède une config JSON et (optionnellement) un fichier sequences.json.
Le CLI interactif crée les deux. Le fichier sequences.json est optionnel : si absent,
`push-instantly/lib/sequences.py` utilise des templates par défaut.

## Création d'un tenant (CLI)

Le CLI est l'outil officiel pour créer un tenant :

```bash
cd scripts/config-reader
python3 create-tenant-cli.py
```

Étapes par niche :
1. Nom de la niche
2. Mots-clés (ou suggestion IA)
3. Target leads nets (default 1500)
4. Offre
5. Pain points (3, sur 6 suggérés par IA)
6. Bénéfices (3, sur 6 suggérés par IA)
7. Style d'introduction
8. CTA (1-3 au choix)
9. L'IA génère 5 emails (2 cold × 3 variantes + 3 interested × 1)

L'IA est **assistante** : elle propose, l'utilisateur valide. Pas de dépendance runtime à l'IA.

## Config Schema

```json
{
  "tenant_id": "grossiste-a",
  "niches": [
    {
      "name": "grossiste_beaute",
      "target": 1500,
      "instantly_object": "question grossiste",
      "instantly_campaign_id": "grossiste_beaute-grossiste-a-20260701",
      "keywords": [
        "grossiste beauté", "grossiste cosmétique", "distributeur beauté",
        "distributeur cosmétique", "fournisseur beauté", "fournisseur cosmétique",
        "grossiste parfumerie", "grossiste maquillage",
        "grossiste soin visage", "grossiste soin capillaire",
        "grossiste esthétique", "grossiste institut beauté"
      ],
      "offer": {
        "description": "Nous aidons les grossistes beauté à obtenir des rendez-vous qualifiés sans démarchage à froid chronophage",
        "pain_points": [
          "démarchage inefficace",
          "manque de temps commercial",
          "clients difficiles à trouver"
        ],
        "benefits": [
          "rendez-vous garantis",
          "gain de temps commercial",
          "clients prêts à acheter"
        ],
        "intro_style": "default",
        "ctas": [
          "Souhaitez-vous en savoir plus ?",
          "Puis-je vous offrir un court appel de 15 min ?"
        ]
      }
    }
  ]
}
```

### Preview email sequences (généré par IA dans sequences.json)

```json
{
  "grossiste_beaute": {
    "steps": [
      {
        "type": "email", "delay": 0,
        "variants": [
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nJ'allais vous joindre au {{phone}} trouvé dans l'annuaire, mais un email me permettait d'être plus clair.\n\nNous aidons les grossistes beauté à obtenir des rendez-vous qualifiés sans démarchage à froid chronophage.\n\nSouhaitez-vous en savoir plus ?\n— {{accountSignature}}"
          },
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nJe suis tombé sur votre fiche dans l'annuaire des grossistes et j'ai immédiatement pensé à vous.\n\nNotre solution permet aux grossistes beauté de remplir leur agenda de RDV sans perte de temps en prospection.\n\nPuis-je vous offrir un court appel de 15 min ?\n— {{accountSignature}}"
          },
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nJe travaille exclusivement avec des grossistes beauté en France. Votre profil m'intéresse.\n\nNous aidons les professionnels comme vous à gagner du temps commercial en amenant des clients prêts à acheter.\n\nSouhaitez-vous voir une courte vidéo ?\n— {{accountSignature}}"
          }
        ]
      },
      {
        "type": "email", "delay": 3,
        "variants": [
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nJe n'ai pas réussi à vous joindre par téléphone. Je voulais vous parler de notre approche qui supprime le démarchage à froid.\n\n100% des grossistes qui testent notre solution constatent un gain de temps immédiat.\n\nSouhaitez-vous en savoir plus ?\n— {{accountSignature}}"
          },
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nLe plus dur dans votre métier, ce n'est pas de vendre — c'est de trouver des clients disponibles. Nous résolvons ce problème.\n\nNos rendez-vous sont garantis, sans engagement.\n\nPuis-je vous offrir un court appel de 15 min ?\n— {{accountSignature}}"
          },
          {
            "subject": "Question grossiste",
            "body": "Bonjour,\n\nUn grossiste comme vous passe en moyenne 12h/semaine à chercher des clients. Nous ramenons ce temps à zéro.\n\nUn de nos clients a rempli son carnet de RDV en 3 semaines.\n\nSouhaitez-vous voir une courte vidéo ?\n— {{accountSignature}}"
          }
        ]
      }
    ],
    "subsequence": {
      "conditions": { "lead_activity": [4] },
      "name": "Interested Follow-up",
      "steps": [
        { "type": "email", "delay": 1, "variants": [{ "subject": "Merci pour votre retour", "body": "Bonjour,\n\nMerci pour votre intérêt. Je vous invite à réserver un créneau de 15 min pour qu'on échange : [lien calendrier].\n\nBonne journée,\n— {{accountSignature}}" }] },
        { "type": "email", "delay": 4, "variants": [{ "subject": "Témoignage", "body": "Bonjour,\n\nUn grossiste similaire à vous a rempli son carnet de RDV en 3 semaines grâce à notre solution. Sans démarchage.\n\nJe peux vous montrer comment concrètement.\n\n— {{accountSignature}}" }] },
        { "type": "email", "delay": 7, "variants": [{ "subject": "Dernier message", "body": "Bonjour,\n\nJe me permets un dernier message. Si vous êtes trop occupé, dites-le moi et je ne vous relancerai pas.\n\nSinon, je suis disponible pour un appel de 15 min quand vous voulez.\n\n— {{accountSignature}}" }] }
      ]
    }
  }
}
```

### Champs par niche

| Champ | Description |
|-------|-------------|
| `name` | Identifiant unique de la niche |
| `target` | Nombre de leads nets à push via Instantly avant closure auto (default 1500) |
| `instantly_object` | Objet de l'email (format `question {keyword}`, 1 mot max) |
| `keywords` | Mots-clés pour le scraping Google Maps |
| `offer` | Offre, pain points, bénéfices, intro style, CTA |
| `instantly_campaign_id` | Identifiant de campagne (créé au push) |

## Sequences Schema (optionnel)

```json
{
  "grossiste_beaute": {
    "steps": [
      {
        "type": "email",
        "delay": 0,
        "variants": [
          { "subject": "...", "body": "..." },
          { "subject": "...", "body": "..." },
          { "subject": "...", "body": "..." }
        ]
      },
      {
        "type": "email",
        "delay": 3,
        "variants": [
          { "subject": "...", "body": "..." },
          { "subject": "...", "body": "..." },
          { "subject": "...", "body": "..." }
        ]
      }
    ],
    "subsequence": {
      "conditions": { "lead_activity": [4] },
      "name": "Interested Follow-up",
      "steps": [
        { "type": "email", "delay": 1, "variants": [{ "subject": "...", "body": "..." }] },
        { "type": "email", "delay": 4, "variants": [{ "subject": "...", "body": "..." }] },
        { "type": "email", "delay": 7, "variants": [{ "subject": "...", "body": "..." }] }
      ]
    }
  }
}
```

## Rotation Engine

Module `rotation/` décide quelle niche scraper, sans IA. Règles :

1. Niche `pending` → scrape immédiat
2. `< 1000 emails sent` → scrape (pas assez de données)
3. `>= target` ET bons taux (reply ≥ 2% ou booking ≥ 2%) → continue en mode scaling
4. `>= target` ET mauvais taux → close, active la niche suivante
5. `< 2% reply` + `> 24h` depuis dernier message → close (sauf si booking rate important)

Voir `rotation/rotation_engine.py` pour les seuils exacts.

## Rotation State (table Supabase)

```sql
create table rotation_state (
  id uuid primary key default gen_random_uuid(),
  tenant_id text not null,
  niche_name text not null,
  status text not null default 'pending',
  leads_pushed int default 0,
  emails_sent int default 0,
  reply_rate numeric default 0,
  positive_reply_rate numeric default 0,
  booking_rate numeric default 0,
  last_message_at timestamptz,
  opened_at timestamptz,
  closed_at timestamptz,
  closed_reason text,
  created_at timestamptz default now()
);
```

## Edge Cases

- Missing config file → skip tenant, log warning
- Invalid JSON → stop, alert Slack
- Empty niches array → error, no scraping
- Empty keywords → skip that niche
- Sequences absentes → templates par défaut dans `push-instantly/lib/sequences.py`
- IA Hermes non configurée → CLI fonctionne en mode manuel (pas de suggestions, pas de génération d'emails)
- Rotation metrics absentes → fautes à zéro, la niche continue
- Demo mode: décisions mockées, aucun effet de bord
