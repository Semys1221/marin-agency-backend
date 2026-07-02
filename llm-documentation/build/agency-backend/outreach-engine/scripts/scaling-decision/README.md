# scaling-decision

Decision engine for kill/scale/pause/alert actions on campaigns.

## Usage

```bash
python hermes_agent.py --tenant marin --trigger schedule        # live
python hermes_agent.py --tenant marin --trigger schedule --demo # demo
```

Logs decisions to `hermes_decisions` table and notifies Slack.
