from ..transport import send_message


def announce_decision(tenant_id: str, niche: str, action: str, reason: str = ""):
    send_message(f"*{tenant_id}* — Décision : `{action}` sur `{niche}`{f' ({reason})' if reason else ''}")


def announce_campaign_created(tenant_id: str, campaign_name: str, instantly_id: str = ""):
    send_message(f"🚀 *{tenant_id}* — Campagne créée : `{campaign_name}` (id={instantly_id})")


def announce_push_complete(tenant_id: str, campaign_name: str, total: int):
    send_message(f"📤 *{tenant_id}* — Push terminé : {total} leads dans `{campaign_name}`")


def announce_campaign_killed(tenant_id: str, niche: str, reason: str = ""):
    send_message(f"🪦 *{tenant_id}* — Niche `{niche}` tuée{f' ({reason})' if reason else ''}")


def announce_campaign_scaling(tenant_id: str, niche: str, reply_rate: float = 0):
    send_message(f"📈 *{tenant_id}* — Niche `{niche}` passe en scaling (reply_rate={reply_rate}%)")
