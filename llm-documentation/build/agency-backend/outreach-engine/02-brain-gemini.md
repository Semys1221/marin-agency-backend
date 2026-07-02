# Brain AI (Gemini) — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=ad4Hnjehs8ahgoUtt5rR

## Purpose
Generates 10 niches from a user's JSON config using Gemini AI, announces on Slack, and decides which niche to scrape next.

## Database Tables

### niche_hunts
```prisma
model NicheHunt {
  id        String   @id @default(uuid()) @db.Uuid
  tenantId  String   @map("tenant_id")
  niches    Json     @default("[]")
  active    Int      @default(0)
  status    String   @default("active")
  createdAt DateTime @default(now()) @map("created_at")
  @@map("niche_hunts")
}
```

### niche_variable
```prisma
model NicheVariable {
  id        String @id @default(uuid()) @db.Uuid
  niche     String @unique
  variables Json   @default("{}")
  template  String?
  @@map("niche_variable")
}
```

## API Integrations
### Gemini
```python
import google.generativeai as genai
genai.configure(api_key=HERMES_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(f"Generate 10 sub-niches within {niche} for {location}")
```

### Slack
```python
from slack_sdk import WebClient
slack = WebClient(token=SLACK_BOT_TOKEN)
slack.chat_postMessage(channel=SLACK_CHANNEL_ID, text=f"🧠 10 niches generated for {tenant}")
```

## Env Vars
```
HERMES_API_KEY=...
SLACK_BOT_TOKEN=...
SLACK_CHANNEL_ID=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Behavior
1. Read tenant config (niche base, keywords, locations)
2. Call Gemini with prompt: "Generate 10 sub-niches within {niche} for {location}"
3. Parse response into structured niche list
4. Store in `niche_hunts` table
5. Announce on Slack: "10 niches generated for {tenant}"
6. Mark first niche as active for scraping
7. Return niche list to scheduler

## Edge Cases
- Gemini key dead (`HERMES_API_KEY === '...'`) → return error, alert Slack, retry 60s
- Invalid response (not 10 niches) → retry up to 3 times, skip
- All niches exhausted → flag "needs human review" on Slack
- Demo mode: return hardcoded list of 3 mock niches

## Dummy Data (demo)
```json
{
  "tenant_id": "marin",
  "niches": [
    {"name": "grossiste_beaute_paris", "keywords": ["grossiste beauté Paris"], "location": "Paris"},
    {"name": "grossiste_beaute_lyon", "keywords": ["grossiste beauté Lyon"], "location": "Lyon"},
    {"name": "grossiste_beaute_marseille", "keywords": ["grossiste beauté Marseille"], "location": "Marseille"}
  ]
}
```
