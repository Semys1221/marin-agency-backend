import logging
import os

log = logging.getLogger("slack.transport")

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#marin-pipeline")


def _is_configured() -> bool:
    token = os.getenv("SLACK_BOT_TOKEN", "")
    return bool(token and token != "...")


def send_message(text: str, channel: str = "") -> bool:
    if not _is_configured():
        log.info("[Slack disabled] %s", text)
        return False
    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        client = WebClient(token=SLACK_TOKEN)
        response = client.chat_postMessage(
            channel=channel or SLACK_CHANNEL,
            text=text,
            mrkdwn=True,
        )
        log.info("Message sent to %s", response.get("channel", SLACK_CHANNEL))
        return True
    except ImportError:
        log.warning("slack_sdk not installed. Install: pip install slack-sdk")
        return False
    except Exception as e:
        log.warning("Slack error: %s", e)
        return False
