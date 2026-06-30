# Sequence Creator — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=SMNBspX1OngIi0aY6-vu

## Purpose
Builds a 7-step multi-variant cold email sequence for Instantly from rendered email variants. Steps scheduled J1→J19.

## Database Tables

### campaign_settings
```sql
CREATE TABLE campaign_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  niche TEXT NOT NULL,
  variants JSONB DEFAULT '[]',
  sequence JSONB DEFAULT '[]',    -- [{step: 1, day: "J1", variant: "A", content: "..."}, ...]
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
1. Receive rendered A/B/C variants for a niche
2. Build 7-step sequence:
   | Step | Day | Action |
   |------|-----|--------|
   | 1 | J1 | Initial email (variant A/B/C) |
   | 2 | J4 | Follow-up #1 |
   | 3 | J7 | Follow-up #2 |
   | 4 | J10 | Follow-up #3 |
   | 5 | J13 | Follow-up #4 |
   | 6 | J16 | Follow-up #5 |
   | 7 | J19 | Final follow-up |
3. Assign different variant to each step (A/B/C rotation)
4. Store sequence in `campaign_settings.sequence`
5. Return sequence_id for campaign push

## Edge Cases
- Less than 3 variants → use same variant for all steps
- Invalid step config → default to 3-step (J1, J7, J14)
- Duplicate sequence for same niche → return existing
- Demo mode: return hardcoded structure with placeholder content
