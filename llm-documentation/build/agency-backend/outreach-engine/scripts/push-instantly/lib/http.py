from datetime import datetime, timezone

from .config import INSTANTLY_API_KEY


def instantly_headers() -> dict:
    return {
        "Authorization": f"Bearer {INSTANTLY_API_KEY}",
        "Content-Type": "application/json",
    }


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(msg: str, level: str = "INFO"):
    print(f"[{iso_now()}] [{level}] {msg}")
