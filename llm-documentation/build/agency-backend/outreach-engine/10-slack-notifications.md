# Slack Notifications — Phase 1

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=Kz--lAPp181lxLSJz8io

## Purpose
Sends Slack notifications for every significant pipeline event: scrape milestones, campaign changes, dead keys, errors.

## API Integrations
### Slack
```python
from slack_sdk import WebClient
slack = WebClient(token=SLACK_BOT_TOKEN)
slack.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
```

## Env Vars
```
SLACK_BOT_TOKEN=...
SLACK_CHANNEL_ID=...
```

## Notification Events
| Event | Message | Trigger |
|-------|---------|---------|
| Niches generated | `🧠 *10 niches generated for {tenant}*` | After Gemini |
| Scrape milestone | `📊 *{tenant}*: {count} leads scraped` | 100/500/1000/2000/5000 |
| Campaign created | `🚀 *Campaign {name} created*` | After Instantly create |
| Campaign killed | `🪦 *Campaign {name} killed* — rate {rate}%` | After kill decision |
| Campaign scaled | `📈 *Campaign {name} scaling* — rate {rate}%` | After scale decision |
| Key dead | `🔴 *{key_name} is DEAD* — ops paused` | On key failure |
| Error spike | `⚠️ *{count} errors in 5min* — check logs` | On error threshold |
| New client | `🎉 *New client: {name}* — creating campaign` | On duplication |

## Edge Cases
- Slack token dead → log to console, no crash
- Rate limited → queue messages, send batch
- Channel not found → log warning, skip
- Demo mode: print to console instead of sending
