SCHEDULE = {
    "schedules": [
        {
            "name": "Semaine",
            "timing": {"from": "09:00", "to": "17:00"},
            "days": {"0": False, "1": True, "2": True, "3": True, "4": True, "5": True, "6": True},
            "timezone": "Europe/Paris",
        }
    ]
}


def build_payload(name: str, email_list: list[str]) -> dict:
    from .sequences import cold
    return {
        "name": name,
        "campaign_schedule": SCHEDULE,
        "sequences": cold(),
        "email_list": email_list,
        "email_gap": 20,
        "random_wait_max": 5,
        "daily_limit": 50,
        "text_only": True,
        "first_email_text_only": True,
        "stop_on_reply": True,
        "open_tracking": True,
        "link_tracking": True,
        "insert_unsubscribe_header": True,
    }
