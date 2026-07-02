from ..transport import send_message


def announce_pipeline_start(tenant_id: str):
    send_message(f"🚀 *Pipeline démarré* — `{tenant_id}`")


def announce_pipeline_end(tenant_id: str):
    send_message(f"✅ *Pipeline terminé* — `{tenant_id}`")
