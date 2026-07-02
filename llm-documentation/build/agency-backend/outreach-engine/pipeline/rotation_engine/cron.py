"""
Cron de rotation — exécute rotation_engine.decide() périodiquement.

Utilise APScheduler (BackgroundScheduler) pour un intervalle de 15 min.
Lance une décision pour chaque tenant actif dans config-reader/users/.

Installation :
  pip install apscheduler

Usage :
  python rotation/cron.py              # démarre le scheduler
  python rotation/cron.py --once       # exécute une seule fois
  python rotation/cron.py --demo       # mode démo (décisions mockées)
"""

import json
import os
import sys
import time
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
_base = _script_dir.parent
sys.path.insert(0, os.path.join(_base))
sys.path.insert(0, os.path.join(_script_dir))

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    HAS_SCHEDULER = True
except ImportError:
    HAS_SCHEDULER = False

from cli.tenants import list_tenants, get_tenant

_INTERVAL_MINUTES = 15


def run_for_tenant(tenant_id: str, demo: bool = False) -> list[dict]:
    from rotation_engine import decide

    config = get_tenant(tenant_id)
    if not config:
        print(f"  [cron] Tenant {tenant_id} introuvable")
        return []

    print(f"  [cron] Décision pour {tenant_id}...")
    result = decide(config, demo=demo)
    for d in result:
        print(f"    → {d.get('action', '?')}: {d.get('niche', d.get('reason', ''))}")
    if result:
        try:
            from slack_notifier.transport.client import send_message
            actions = ", ".join(f"{d.get('action')}({d.get('niche','?')})" for d in result)
            send_message(f"🔄 *{tenant_id}* — Rotation : {actions}")
        except Exception:
            pass
    return result


def run_all(demo: bool = False):
    print(f"\n{'=' * 50}")
    print(f"  ROTATION ENGINE — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}")

    tenants = list_tenants()
    if not tenants:
        print("  [cron] Aucun tenant trouvé")
        return

    for config in tenants:
        tid = config.get("tenant_id", "")
        if not tid:
            continue
        run_for_tenant(tid, demo=demo)


def run_once(demo: bool = False):
    run_all(demo=demo)


def run_loop(demo: bool = False):
    if not HAS_SCHEDULER:
        print("  [cron] APScheduler non installé.")
        print("  [cron] Installe-le : pip install apscheduler")
        print("  [cron] Fallback sur mode --once...")
        run_once(demo=demo)
        return

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_all,
        "interval",
        minutes=_INTERVAL_MINUTES,
        id="rotation_engine",
        name="Rotation Engine",
        replace_existing=True,
    )
    scheduler.start()
    print(f"  [cron] Scheduler démarré (toutes les {_INTERVAL_MINUTES} min)")
    print(f"  [cron] Ctrl+C pour arrêter")
    try:
        try:
            from slack_notifier.transport.client import send_message
        except Exception:
            send_message = None
        if send_message:
            send_message(f"⏰ *Scheduler démarré* — rotation toutes les {_INTERVAL_MINUTES} min")
    except Exception:
        pass

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n  [cron] Arrêt demandé...")
        try:
            send_message("⏹️ *Scheduler arrêté*")
        except Exception:
            pass
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Exécute une seule fois et quitte")
    parser.add_argument("--demo", action="store_true", help="Mode démo")
    args = parser.parse_args()

    if args.once:
        run_once(demo=args.demo)
    elif args.demo:
        run_once(demo=True)
    else:
        run_loop(demo=args.demo)
