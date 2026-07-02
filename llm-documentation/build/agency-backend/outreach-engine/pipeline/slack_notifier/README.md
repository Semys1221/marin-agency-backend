# Slack Notifier — Module de notifications

Ce dossier contient **1 fichier** et **5 fonctions**.

Il envoie des notifications Slack à chaque étape importante de la pipeline : démarrage, décision de rotation, création de tenant, et erreurs.

---

## `slack_notifier.py` — 5 fonctions

1. `_is_configured()` → bool  
   Vérifie si le token Slack (`SLACK_BOT_TOKEN`) est défini dans l'environnement.

2. `send_message(text, channel="")` → bool  
   Envoie un message texte dans un channel Slack. Retourne True si envoyé, False si erreur.

3. `announce_niches(tenant_id, niche_count)`  
   Prépare et envoie un message : "X niches prêtes pour le scraping".

4. `announce_error(tenant_id, error)`  
   Prépare et envoie un message d'erreur pour un tenant.

5. `announce_decision(tenant_id, niche, action, reason="")`  
   Prépare et envoie la décision de rotation (scrape, close, wait).

---

## Tester ce module

```bash
# Test sans token Slack (mode démo via la pipeline)
python -c "
from slack_notifier.slack_notifier import _is_configured
print('Slack configuré:', _is_configured())
"

# Test d'envoi (nécessite SLACK_BOT_TOKEN)
python -m slack_notifier.slack_notifier --channel "#general" --text "Test depuis la pipeline"
```
