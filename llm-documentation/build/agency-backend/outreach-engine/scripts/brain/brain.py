import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

_script_dir = Path(__file__).resolve().parent
_load_dotenv_path = _script_dir
for _ in range(10):
    if (_load_dotenv_path / ".env.local").exists():
        load_dotenv(_load_dotenv_path / ".env.local")
        break
    _load_dotenv_path = _load_dotenv_path.parent

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config-reader'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'niche-store'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'slack-notifier'))
from config_reader import read_config, validate_config
from niche_store import save_niche_hunt, set_active_niche, flag_niche_hunt_exhausted, flag_needs_review
from slack_notifier import announce_niches, announce_error

HERMES_API_KEY = os.getenv("HERMES_API_KEY", "...")
HERMES_BASE_URL = os.getenv("HERMES_BASE_URL", "http://localhost:8642/v1")

_DEMO_NICHES = [
    {"name": "plombier_paris", "keywords": ["plombier Paris"], "location": "Paris"},
    {"name": "plombier_lyon", "keywords": ["plombier Lyon"], "location": "Lyon"},
    {"name": "plombier_marseille", "keywords": ["plombier Marseille"], "location": "Marseille"},
]


def _hermes_client():
    from openai import OpenAI
    return OpenAI(base_url=HERMES_BASE_URL, api_key=HERMES_API_KEY)


def _build_prompt(niche: str, keywords: list[str]) -> str:
    kw = ", ".join(keywords)
    return (
        f"Generate 10 location-based sub-niches within '{niche}' "
        f"for cities all across France. "
        f"Keywords: {kw}. "
        "Return ONLY a JSON array of objects with keys: name (string), keywords (array of strings), location (string). "
        "No markdown, no explanation."
    )


def _parse_response(text: str) -> list[dict] | None:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, list):
        return None

    for item in data:
        if not all(k in item for k in ("name", "keywords", "location")):
            return None

    if len(data) != 10:
        return None

    return data


def generate_niches(tenant_id: str, demo: bool = False) -> dict:
    if demo:
        return {"niches": _DEMO_NICHES, "demo": True}

    if HERMES_API_KEY == "...":
        return {"error": "HERMES_API_KEY non configuré"}

    config = read_config(tenant_id)
    if config is None:
        return {"error": f"Config not found for {tenant_id}"}

    errors = validate_config(config)
    if errors:
        return {"error": "Invalid config", "details": errors}

    all_sub_niches = []
    hunts_created = 0

    for niche_entry in config.get("niches", []):
        niche_name = niche_entry["name"]
        keywords = niche_entry.get("keywords", [])
        prompt = _build_prompt(niche_name, keywords)

        last_error = None
        for attempt in range(3):
            try:
                client = _hermes_client()
                response = client.chat.completions.create(
                    model="hermes-agent",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                text = response.choices[0].message.content or ""
                sub_niches = _parse_response(text)
                if sub_niches is None:
                    last_error = "Invalid response (not 10 niches)"
                    time.sleep(2 ** attempt)
                    continue

                hunt = save_niche_hunt(tenant_id, sub_niches)
                if hunt and hunt.get("id"):
                    set_active_niche(hunt["id"], 0)
                all_sub_niches.extend(sub_niches)
                hunts_created += 1
                break

            except Exception as e:
                last_error = str(e)
                time.sleep(2 ** attempt)

        if last_error:
            announce_error(tenant_id, f"{niche_name}: {last_error}")

    if hunts_created > 0:
        announce_niches(tenant_id, len(all_sub_niches))
    else:
        announce_error(tenant_id, last_error or "No niches generated")

    return {
        "niches": all_sub_niches,
        "hunts_created": hunts_created,
        "total_sub_niches": len(all_sub_niches),
    }


def run():
    import argparse
    parser = argparse.ArgumentParser(description="Brain — Generate niches via Hermes API")
    parser.add_argument("--tenant", default="marin")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    result = generate_niches(args.tenant, demo=args.demo)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
