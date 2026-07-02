# slack-notifier

Sends notifications to Slack via `#all-montismedia` (C0BEJ9R1ELC).

## Functions

- `send_message(text)` — raw message
- `announce_niches(tenant_id, count)` — niche generation success
- `announce_decision(tenant_id, action, target, reason)` — scaling decision
- `announce_error(tenant_id, error)` — error alert
