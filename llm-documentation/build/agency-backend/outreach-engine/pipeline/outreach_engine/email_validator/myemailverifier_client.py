import os
import time
import requests
from collections import deque

API_BASE = "https://api.myemailverifier.com"
CLIENT_BASE = "https://client.myemailverifier.com"
RATE_LIMIT = 30
WINDOW = 60

_timestamps: deque = deque()


def _wait_for_rate_limit():
    now = time.time()
    while _timestamps and now - _timestamps[0] > WINDOW:
        _timestamps.popleft()
    if len(_timestamps) >= RATE_LIMIT:
        sleep_time = _timestamps[0] + WINDOW - now
        if sleep_time > 0:
            time.sleep(sleep_time)
    _timestamps.append(time.time())


def _headers(api_key: str) -> dict:
    return {"User-Agent": "marin-cleaner/1.0"}


def verify_email(email: str, api_key: str | None = None) -> dict:
    key = api_key if api_key is not None else os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if not key or key == "...":
        return {"Status": "Unknown", "error": "No API key configured"}

    _wait_for_rate_limit()

    try:
        resp = requests.get(
            f"{API_BASE}/api/validate_single.php",
            params={"apikey": key, "email": email},
            headers=_headers(key),
            timeout=10,
        )
        if resp.status_code == 429:
            time.sleep(5)
            return verify_email(email, key)
        if resp.status_code != 200:
            return {"Status": "Unknown", "error": f"http_{resp.status_code}"}
        return resp.json()
    except requests.RequestException as e:
        return {"Status": "Unknown", "error": str(e)}


def check_credits(api_key: str | None = None) -> str:
    key = api_key if api_key is not None else os.getenv("MYEMAILVERIFIER_API_KEY", "")
    if not key or key == "...":
        return "No API key configured"

    try:
        resp = requests.get(
            f"{CLIENT_BASE}/verifier/getcredits/{key}",
            headers=_headers(key),
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("credits", "0")
        return "0"
    except requests.RequestException:
        return "0"
