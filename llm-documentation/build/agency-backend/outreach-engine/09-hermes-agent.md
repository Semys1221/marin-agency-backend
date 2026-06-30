# Hermes Agent — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=Ul74DEaDluJUrRerLLv8

## Purpose
Core AI decision engine orchestrating the outreach pipeline. 4 trigger types: Schedule, Threshold, Manual, Alert.

## Database Tables

### campaign_analytics (read — benchmarks)
### campaign_settings (read/write — update campaign status)
### clean_leads (read/write — update lead status)
### clients (read — check tenant config)
### campaign_queue (read/write — manage queue)

```sql
-- Decision logging
CREATE TABLE hermes_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  action TEXT NOT NULL,            -- scrape | clean | send | pause | kill | scale
  target TEXT NOT NULL,            -- niche_id | campaign_id | lead_id
  reason TEXT NOT NULL,
  triggered_by TEXT NOT NULL,      -- schedule | threshold | manual | alert
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Env Vars
```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
SLACK_BOT_TOKEN=...
SLACK_CHANNEL_ID=...
```

## Decision Model
```python
@dataclass
class HermesDecision:
    action: str       # 'scrape' | 'clean' | 'validate' | 'send' | 'pause' | 'continue' | 'kill' | 'scale'
    target: str       # niche ID, campaign ID, or lead ID
    reason: str
    triggered_by: str # 'schedule' | 'threshold' | 'manual' | 'alert'
```

## Orchestration Targets (from Eraser diagram)
Hermes directly orchestrates these components via dedicated edges:
- `Hermes Agent > Check Campaign Exists` — check before pushing
- `Hermes Agent > Sequence Creator` — create cold sequences for new niches
- `Hermes Agent > Sequence Creator (Dual)` — orchestrate both cold (Instantly) and transactional (Resend) modes
- `Hermes Agent > Analyze Performance` — monitor campaign health
- `Hermes Agent > Kill & Replace` — decide to kill underperforming campaigns
- `Hermes Agent > Scale Campaign` — decide to scale well-performing campaigns

## Decision Rules
| Rule | Action | Trigger |
|------|--------|---------|
| Reply rate < 2% | Kill campaign (→ Generate Niches) | Threshold |
| Reply rate ≥ 2% + leads remaining | Scale campaign (→ Outscraper) | Threshold |
| Niche exhausted (no new leads) | Flag "needs scraping" | Threshold |
| New client arrives | Create campaign, update quota | Alert |
| API key dead | Alert dashboard + Slack | Alert |
| Lead validated | Move to Instantly queue | Schedule |
| Booking made | Stop sending to that lead | Alert |

## Triggers
- **Schedule** — Cron-based scraping, cleaning, campaign checks
- **Threshold** — Reply rate, bounce rate, lead count limits
- **Manual** — Human override via Slack or dashboard
- **Alert** — Dead keys, service outages, error spikes

## Edge Cases
- No data to decide → wait for next cycle
- Conflicting decisions (kill + scale same campaign) → kill wins
- Demo mode: return predetermined decisions based on campaign state
