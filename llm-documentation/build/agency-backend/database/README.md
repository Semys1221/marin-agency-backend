# Database — Spec

## Description

Base de données Supabase Postgres partagée (multi-tenant via `tenant_id`).

## Modèle d'auth

- **Shared DB** — tous les clients dans la même base
- **Pas de login/signup** — pas d'authentification utilisateur
- **`X-Tenant-ID` header** — chaque requête API doit l'inclure
- **Service role key** — utilisée côté backend pour les opérations privilégiées
- **Anon key** — utilisée côté client (RLS restreint)

## Ordre de build

| # | Fichier | Description |
|---|---------|-------------|
| 1 | `schema.prisma` | Schéma Prisma complet (legacy + nouveaux modèles) |
| 2 | `01-migrations.sql` | Migrations initiales (tables existantes) |
| 3 | `02-new-tables.sql` | Nouvelles tables (tenants, clients, tickets...) |
| 4 | `rls-policies.sql` | Politiques RLS tenant isolation |
| 5 | `seed.sql` | Seed data (tenant "marin", leads test) |

## Gates

- [ ] Gate 1: Supabase project déployé (`SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` dans env)
- [ ] Gate 2: DATABASE_URL configurée dans `.env.local`
- [ ] Gate 3: Extensions activées (pgcrypto, uuid-ossp)
- [ ] Gate 4: Schema existant lu (tables legacy)
- [ ] Gate 5: Eraser diagramme vérifié
- [ ] Gate 6: RLS policies testées avec service_role vs anon key

## Dépendances

- `infrastructure/env.variables` — toutes les vars d'env
- `llm-documentation/build/agency-backend/outreach-engine/` — legacy schema à préserver
