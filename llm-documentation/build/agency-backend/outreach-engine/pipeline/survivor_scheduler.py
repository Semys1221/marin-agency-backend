#!/usr/bin/env python3
"""
Survivor scheduler — Render-safe loop without native cron jobs.

Runs inside engine-marin-agency and repeats:
- rotation decision
- scrape/filter/validate → clean_leads
- push pending clean_leads to Instantly
until the tenant reaches the configured target or a cycle cap is hit.
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [survivor] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("survivor")

_script_dir = Path(__file__).resolve().parent
_dotenv_path = _script_dir
for _ in range(10):
    if (_dotenv_path / ".env.local").exists():
        load_dotenv(_dotenv_path / ".env.local")
        break
    _dotenv_path = _dotenv_path.parent

sys.path.insert(0, str(_script_dir))


def _tenant_config(tenant_id: str) -> Optional[dict]:
    try:
        from cli.tenants import get_tenant
        return get_tenant(tenant_id)
    except Exception as exc:
        log.warning("get_tenant failed: %s", exc)
        return None


def _clean_leads_count(tenant_id: str) -> int:
    try:
        from cli.db import get_supabase
        sb = get_supabase()
        if not sb:
            return -1
        res = sb.table("clean_leads").select("id").eq("tenant_id", tenant_id).execute()
        return len(res.data or [])
    except Exception as exc:
        log.warning("count clean_leads failed: %s", exc)
        return -1


def _run_worker_once(tenant_id: str, dry_run: bool = False) -> None:
    try:
        from worker import run_for_tenant
        run_for_tenant(tenant_id, dry_run=dry_run)
    except Exception as exc:
        log.warning("worker cycle failed: %s", exc)


def _push_once(tenant_id: str, dry_run: bool = False) -> None:
    try:
        from outreach_engine.push_instantly.push import push_all
        push_all(tenant_id, create_if_missing=not dry_run, dry_run=dry_run)
    except Exception as exc:
        log.warning("push cycle failed: %s", exc)


def _rotation_once(tenant_id: str, demo: bool = False) -> None:
    try:
        from rotation_engine.cron import run_once
        run_once(demo=demo)
    except Exception as exc:
        log.warning("rotation cycle failed: %s", exc)


def _notify(message: str) -> None:
    try:
        from slack_notifier.transport.client import send_message
        send_message(message)
    except Exception:
        pass


def run_until_target(
    tenant_id: str,
    target: int = 2000,
    max_cycles: int = 20,
    interval_seconds: int = 60,
    dry_run: bool = False,
) -> None:
    log.info(
        "Starting survivor for tenant=%s target=%d max_cycles=%d interval=%ds",
        tenant_id,
        target,
        max_cycles,
        interval_seconds,
    )

    config = _tenant_config(tenant_id)
    if not config:
        log.error("Tenant config not found for %s", tenant_id)
        return

    current = _clean_leads_count(tenant_id)
    if current < 0:
        log.error("Cannot reach Supabase to count clean_leads")
        return

    log.info("Current clean_leads=%d target=%d", current, target)

    cycle = 0
    while current < target and cycle < max_cycles:
        cycle += 1
        log.info("Cycle %d/%d — current=%d", cycle, max_cycles, current)
        _notify(f"🔄 *Survivor* — cycle {cycle}/{max_cycles} pour `{tenant_id}`")

        _rotation_once(tenant_id, demo=dry_run)
        _run_worker_once(tenant_id, dry_run=dry_run)
        _push_once(tenant_id, dry_run=dry_run)

        current = _clean_leads_count(tenant_id)
        if current < 0:
            log.warning("DB read failed during loop; will retry next cycle")

        if current >= target:
            log.info("Target reached: clean_leads=%d", current)
            _notify(f"✅ *Survivor* — `{tenant_id}` a atteint {current} clean_leads")
            return

        if cycle < max_cycles:
            time.sleep(interval_seconds)

    if current < target:
        log.info("Stopping at cycle %d with clean_leads=%d", cycle, current)
        _notify(
            f"⏹️ *Survivor* — `{tenant_id}` arrêté après {cycle} cycle(s), "
            f"clean_leads={current}, target={target}"
        )


def main():
    parser = argparse.ArgumentParser(description="Survivor scheduler for Render")
    parser.add_argument("--tenant", default=os.getenv("TENANT_ID", "marin-agency"))
    parser.add_argument("--target", type=int, default=2000)
    parser.add_argument("--max-cycles", type=int, default=20)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_until_target(
        tenant_id=args.tenant,
        target=args.target,
        max_cycles=args.max_cycles,
        interval_seconds=args.interval,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
