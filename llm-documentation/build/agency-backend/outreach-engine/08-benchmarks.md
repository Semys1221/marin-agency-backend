# Benchmarks — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=phlJMCbmAfsVzVIkgknK

## Purpose
Analyzes campaign performance (reply rate, open rate, bounce rate). Recommends: Kill & Replace (bad) or Scale (good).

## Database Tables

### campaign_analytics
```sql
CREATE TABLE campaign_analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  leads_sent INT DEFAULT 0,
  opens INT DEFAULT 0,
  replies INT DEFAULT 0,
  bounces INT DEFAULT 0,
  reply_rate DECIMAL DEFAULT 0.0,
  open_rate DECIMAL DEFAULT 0.0,
  bounce_rate DECIMAL DEFAULT 0.0,
  verdict TEXT,                    -- 'kill' | 'scale' | 'monitor'
  recommendation TEXT,
  checked_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, campaign_id, checked_at)
);
```

### campaign_settings (read)
```sql
-- status: draft | running | paused | completed | killed
SELECT status, niche FROM campaign_settings WHERE tenant_id = ? AND campaign_id = ?
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior
1. Every cycle, fetch analytics for all active campaigns
2. Calculate:
   - Reply rate = replies / sent × 100
   - Open rate = opens / sent × 100
   - Bounce rate = bounces / sent × 100
3. Apply rules:
   | Condition | Action |
   |-----------|--------|
   | Reply rate < 2% | Flag Kill & Replace |
   | Reply rate ≥ 2% and leads remaining | Flag Scale |
   | Open rate < 15% | Flag subject line issue |
   | Bounce rate > 10% | Flag cleaning quality |
4. Send recommendation to Hermes Agent
5. Log all results to `campaign_analytics`

## Post-Benchmark Flow Edges (from Eraser diagram)
- **Kill & Replace → Generate Niches (Gemini)**: bad perf → restart niche generation with new keywords
- **Scale Campaign → Outscraper Scrape**: good perf → scrape more leads for the same campaign
- Both paths are mediated by Hermes Agent (Hermes receives the recommendation, makes the final decision, then triggers the next component)

## Edge Cases
- No data yet → skip, retry next cycle
- All campaigns flagged kill → alert Slack, generate new niches
- Inconsistent data → log warning, use raw values
- Demo mode: return hardcoded benchmark results

## Dummy Data (demo)
```json
{
  "campaign_id": "camp-001",
  "tenant_id": "marin",
  "leads_sent": 1450,
  "opens": 620,
  "replies": 28,
  "reply_rate": 1.93,
  "bounces": 45,
  "verdict": "monitor",
  "recommendation": "reply rate approaching 2% threshold"
}
```
