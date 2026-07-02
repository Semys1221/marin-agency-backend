from ..transport import send_message


def announce_error(tenant_id: str, error: str):
    send_message(f"⚠️ *{tenant_id}* Erreur : {error}")


def announce_error_spike(tenant_id: str, count: int, service: str):
    send_message(f"⚠️ *{tenant_id}* — {count} erreurs en 5min sur `{service}` — check logs")


def announce_key_dead(service: str):
    send_message(f"🔴 *Clé API morte* — `{service}` — ops paused")
