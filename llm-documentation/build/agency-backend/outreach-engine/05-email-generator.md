# Email Generator — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=rr9ShOtTvKAgONN4y5LF

## Purpose
Renders email content from base templates + niche-specific variables from Supabase. Generates A/B/C variants for each niche.

## Database Tables

### niche_variable
```prisma
model NicheVariable {
  id        String @id @default(uuid()) @db.Uuid
  niche     String @unique
  variables Json   @default("{}")  // {niche, niche_keyword_1/2/3, niche_member, objectif, pain_point, methode, timeline}
  template  String? // Base email template with {variables}
  @@map("niche_variable")
}
```

### campaign_settings
```sql
CREATE TABLE campaign_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  niche TEXT NOT NULL,
  variants JSONB DEFAULT '[]',    -- rendered A/B/C variants
  active_variant TEXT DEFAULT 'A',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, campaign_id)
);
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior
1. Read email template model from `niche_variable`
2. Resolve variables from DB rows -> `{niche}`, `{niche_keyword_1}`, `{niche_member}`, `{objectif}`, `{pain_point}`, `{methode}`, `{timeline}`
3. Generate 3 variants (A/B/C) with different: subject lines, opening hooks, CTAs
4. Store rendered variants in `campaign_settings`

## Template Variables
| Variable | Source | Example |
|----------|--------|---------|
| `{niche}` | niche_variable | grossiste beauté |
| `{niche_keyword_1}` | niche_variable | grossiste cosmétique |
| `{niche_member}` | niche_variable | grossiste |
| `{objectif}` | niche_variable | développer votre clientèle |
| `{pain_point}` | niche_variable | vous cherchez à étendre votre réseau |
| `{methode}` | niche_variable | un système de prospection automatisé |
| `{timeline}` | niche_variable | sous 48h |

## Edge Cases
- Missing template → hardcoded fallback template
- Unresolved variables → leave `{variable}` as-is in output
- Demo mode: return pre-rendered examples for each variant
