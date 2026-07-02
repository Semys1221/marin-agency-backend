from ..transport import send_message


def announce_niches(tenant_id: str, niche_count: int):
    send_message(f"*{tenant_id}*: {niche_count} niches prêtes pour scraping")


def announce_scrape_milestone(tenant_id: str, niche: str, count: int):
    send_message(f"📊 *{tenant_id}* — `{niche}` : {count} leads scrapés")
    if count >= 5000:
        send_message(f"🏁 *{tenant_id}* — `{niche}` a atteint 5000 leads !")


def announce_cleaning_complete(tenant_id: str, campaign_id: str, total: int, valid: int, invalid: int):
    pct = round(valid / total * 100, 1) if total > 0 else 0
    send_message(f"🧹 *{tenant_id}* — Nettoyage terminé : {total} leads, {valid} valides ({pct}%), {invalid} invalides")
