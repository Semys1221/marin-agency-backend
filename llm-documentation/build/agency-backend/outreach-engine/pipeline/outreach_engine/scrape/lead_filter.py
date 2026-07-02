REQUIRED_FIELDS = ["email", "email_1", "email_2", "email_3"]


def has_email(entry: dict) -> bool:
    return any(entry.get(f) for f in REQUIRED_FIELDS)


def has_phone(entry: dict) -> bool:
    return bool(entry.get("phone"))


def is_valid_lead(entry: dict) -> bool:
    return has_email(entry) or has_phone(entry)


def filter_leads(items: list[dict]) -> list[dict]:
    return [e for e in items if is_valid_lead(e)]


def filter_stats(items: list[dict]) -> dict:
    total = len(items)
    with_email = sum(1 for e in items if has_email(e))
    with_phone = sum(1 for e in items if has_phone(e))
    valid = sum(1 for e in items if is_valid_lead(e))
    return {
        "total": total,
        "with_email": with_email,
        "with_phone": with_phone,
        "valid": valid,
        "filtered_out": total - valid,
    }
