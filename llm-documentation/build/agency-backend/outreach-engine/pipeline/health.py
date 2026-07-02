"""Minimal HTTP health server for Render web services.

If the health server fails to start for any reason, the failure is logged
and execution continues. This keeps batch/worker services usable even
when multiple entrypoints are imported in the same process.
"""
import http.server
import logging
import os
import socketserver
import threading

logger = logging.getLogger("health")

PORT = int(os.environ.get("PORT", "10000"))


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args, **kwargs):
        pass


def start():
    if os.environ.get("DISABLE_HEALTH"):
        return None
    try:
        server = socketserver.ThreadingTCPServer(("", PORT), _Handler)
        server.allow_reuse_address = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        logger.info("Health server started on port=%s", PORT)
        return server
    except OSError as exc:
        logger.warning("Health server not started: %s", exc)
        return None
