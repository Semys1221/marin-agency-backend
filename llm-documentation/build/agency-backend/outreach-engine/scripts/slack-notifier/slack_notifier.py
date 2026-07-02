import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_script_dir = Path(__file__).resolve().parent
_dotenv_path = _script_dir
for _ in range(10):
    if (_dotenv_path / ".env.local").exists():
        load_dotenv(_dotenv_path / ".env.local")
        break
    _dotenv_path = _dotenv_path.parent

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "...")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_ID", "")


def _is_configured() -> bool:
    return bool(SLACK_BOT_TOKEN and SLACK_CHANNEL and SLACK_BOT_TOKEN != "...")


def send_message(text: str) -> dict:
    if not _is_configured():
        return {"error": "Slack non configuré"}

    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        client = WebClient(token=SLACK_BOT_TOKEN)
        result = client.chat_postMessage(channel=SLACK_CHANNEL, text=text)
        return {"ok": True, "ts": result["ts"]}
    except ImportError:
        return {"error": "slack_sdk not installed"}
    except SlackApiError as e:
        return {"error": str(e)}


def announce_niches(tenant_id: str, count: int) -> dict:
    return send_message(f"🧠 {count} niches generated for {tenant_id}")


def announce_error(tenant_id: str, error: str) -> dict:
    return send_message(f"⚠️ Brain error for {tenant_id}: {error}")


def announce_decision(tenant_id: str, action: str, target: str, reason: str) -> dict:
    return send_message(f"🤖 Hermes decision — {action} on {target} ({reason})")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="marin")
    parser.add_argument("--message", default="Test notification")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        print(json.dumps({"demo": True, "message": args.message}, indent=2))
    else:
        result = send_message(args.message)
        print(json.dumps(result, indent=2))
