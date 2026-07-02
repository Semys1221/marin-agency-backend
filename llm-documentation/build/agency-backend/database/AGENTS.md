# Database — LLM Rules

## Gates

1. [ ] **Schéma legacy lu** — reverse-engineered from existing Supabase tables (see `schema.prisma`)
2. [ ] **Eraser diagramme vérifié** — tous les modèles existent comme nodes dans le diagramme
3. [ ] **RLS testées** — `service_role` bypass, `anon` key filtrée par `X-Tenant-ID`
4. [ ] **Demo mode** — chaque table supporte `?demo=true` avec seed data

## Tech Stack

| Component | Technologie |
|-----------|------------|
| ORM | Prisma (Node.js) |
| DB | Supabase Postgres 17 |
| Migrations | Prisma Migrate |
| RLS | Supabase SQL (via dashboard) |

## Ordre de build

1. `schema.prisma` — définir le schéma complet
2. `npx prisma db push` — pousser en dev
3. `rls-policies.sql` — exécuter dans Supabase SQL Editor
4. `seed.sql` — charger les données de test
5. Vérifier avec `supabase db dump`

## Règles

- Les tables legacy (`campaign_*`, `leads`, `niche_variable`, `rdv_details`) ne DOIVENT PAS être modifiées
- Les nouvelles tables utilisent `tenant_id` comme clé de partition
- `call-recordings` bucket storage existe déjà
- Ne pas ajouter de login/signup — auth model = shared DB + X-Tenant-ID
