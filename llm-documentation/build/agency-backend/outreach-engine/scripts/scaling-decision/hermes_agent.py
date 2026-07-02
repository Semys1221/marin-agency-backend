import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv

_script_dir = Path(__file__).resolve().parent
_dotenv_path = _script_dir
for _ in range(10):
    if (_dotenv_path / ".env.local").exists():
        load_dotenv(_dotenv_path / ".env.local")
        break
    _dotenv_path = _dotenv_path.parent

_base = _script_dir.parent
sys.path.insert(0, os.path.join(_base, 'slack-notifier'))
sys.path.insert(0, os.path.join(_base))
from slack_notifier import send_message, announce_decision
from supabase_client import get_supabase, is_configured

HERMES_API_KEY = os.getenv("HERMES_API_KEY", "...")
HERMES_BASE_URL = os.getenv("HERMES_BASE_URL", "http://localhost:8642/v1")


@dataclass
class HermesDecision:
    action: str
    target: str
    reason: str
    triggered_by: str


def _is_key_configured() -> bool:
    return bool(HERMES_API_KEY and HERMES_API_KEY != "...")


def _log_decision(tenant_id: str, decision: HermesDecision) -> dict | None:
    if not is_configured():
        return None

    supabase = get_supabase()
    payload = {
        "tenant_id": tenant_id,
        "action": decision.action,
        "target": decision.target,
        "reason": decision.reason,
        "triggered_by": decision.triggered_by
    }
    result = supabase.table("hermes_decisions").insert(payload).execute()
    return result.data[0] if result.data else None


def _ask_hermes(prompt: str) -> str | None:
    if not _is_key_configured():
        return None

    try:
        from openai import OpenAI
        client = OpenAI(base_url=HERMES_BASE_URL, api_key=HERMES_API_KEY)
        response = client.chat.completions.create(
            model="hermes-agent",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception:
        return None


def _get_campaign_analytics(tenant_id: str) -> dict | None:
    if not is_configured():
        return None

    supabase = get_supabase()
    result = supabase.table("campaign_analytics") \
        .select("*") \
        .eq("tenant_id", tenant_id) \
        .execute()
    return result.data[0] if result.data else None


def _demo_decisions(tenant_id: str) -> list[HermesDecision]:
    return [
        HermesDecision(action="continue", target="niche_0", reason="Demo mode", triggered_by="manual"),
        HermesDecision(action="scrape", target="grossiste_beaute_paris", reason="Demo mode", triggered_by="schedule"),
    ]


_RULES = [
    {"condition": "reply_rate < 2", "action": "kill", "reason": "Reply rate < 2%"},
    {"condition": "reply_rate >= 2 and leads_remaining > 0", "action": "scale", "reason": "Reply rate >= 2% + leads remaining"},
    {"condition": "leads_remaining == 0", "action": "flag_exhausted", "reason": "Niche exhausted"},
    {"condition": "new_client", "action": "create_campaign", "reason": "New client arrives"},
    {"condition": "api_key_dead", "action": "alert", "reason": "API key dead"},
    {"condition": "booking_made", "action": "stop_sending", "reason": "Booking made"},
]


def decide(tenant_id: str, trigger: str = "schedule", demo: bool = False) -> list[HermesDecision]:
    if demo:
        return _demo_decisions(tenant_id)

    decisions = []

    if HERMES_API_KEY == "...":
        decisions.append(HermesDecision(
            action="alert", target="hermes_key", reason="HERMES_API_KEY non configuré", triggered_by=trigger
        ))
        for d in decisions:
            _log_decision(tenant_id, d)
            announce_decision(tenant_id, d.action, d.target, d.reason)
        return decisions

    analytics = _get_campaign_analytics(tenant_id)

    if analytics is None:
        decisions.append(HermesDecision(
            action="wait", target="all", reason="No data to decide", triggered_by=trigger
        ))
        return decisions

    reply_rate = analytics.get("reply_rate", 0)
    leads_remaining = analytics.get("leads_remaining", 0)

    if reply_rate < 2:
        decisions.append(HermesDecision(
            action="kill", target=analytics.get("campaign_id", "unknown"),
            reason="Reply rate < 2%", triggered_by=trigger
        ))
    elif reply_rate >= 2 and leads_remaining > 0:
        decisions.append(HermesDecision(
            action="scale", target=analytics.get("niche_id", "unknown"),
            reason="Reply rate >= 2% + leads remaining", triggered_by=trigger
        ))

    if leads_remaining == 0:
        decisions.append(HermesDecision(
            action="flag_exhausted", target=analytics.get("niche_id", "unknown"),
            reason="Niche exhausted", triggered_by=trigger
        ))

    if not decisions:
        decisions.append(HermesDecision(
            action="continue", target="all", reason="No rule triggered", triggered_by=trigger
        ))

    for d in decisions:
        _log_decision(tenant_id, d)
        announce_decision(tenant_id, d.action, d.target, d.reason)

    return decisions


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="marin")
    parser.add_argument("--trigger", default="schedule", choices=["schedule", "threshold", "manual", "alert"])
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    decisions = decide(args.tenant, trigger=args.trigger, demo=args.demo)
    print(json.dumps([asdict(d) for d in decisions], indent=2))
