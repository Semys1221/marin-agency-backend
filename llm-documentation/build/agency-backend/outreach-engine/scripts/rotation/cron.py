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

from rotation_engine import decide

_CONFIG_DIR = _script_dir.parent / "config-reader" / "users"
_INTERVAL_MINUTES = 15


def run_for_tenant(config_path: Path) -> list[dict]:
    try:
        with open(config_path) as f:
            config = json.load(f)
    except Exception as e:
        print(f"  [cron] Erreur lecture {config_path.name}: {e}")
        return []

    tenant_id = config.get("tenant_id", config_path.parent.name)
    print(f"  [cron] Décision pour {tenant_id}...")
    result = decide(config)
    for d in result:
        print(f"    → {d.get('action', '?')}: {d.get('niche', d.get('reason', ''))}")
    return result


def run_all(demo: bool = False):
    print(f"\n{'=' * 50}")
    print(f"  ROTATION ENGINE — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}")

    if not _CONFIG_DIR.exists():
        print(f"  [cron] Aucun dossier config trouvé: {_CONFIG_DIR}")
        return

    tenants = sorted(_CONFIG_DIR.iterdir())
    if not tenants:
        print("  [cron] Aucun tenant trouvé")
        return

    for tenant_dir in tenants:
        if not tenant_dir.is_dir():
            continue
        config_file = tenant_dir / "config.json"
        if not config_file.exists():
            continue
        run_for_tenant(config_file)


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
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n  [cron] Arrêt demandé...")
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
