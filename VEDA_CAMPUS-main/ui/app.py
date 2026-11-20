import json
import logging
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.faculty_search import get_faculty_directory
from modules.logger import log_interaction
from modules.nlu_engine import KNOWN_SUBJECTS
from modules.veda_core import ask_veda


PROJECT_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = PROJECT_DIR / "ui" / "static"
MAX_REQUEST_SIZE = 8 * 1024


class VedaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/faculty":
            try:
                self._send_json(200, get_faculty_directory())
            except (OSError, json.JSONDecodeError):
                logging.exception("Could not load faculty directory")
                self._send_json(500, {"error": "Faculty data could not be loaded."})
            return

        if self.path == "/api/subjects":
            self._send_json(200, KNOWN_SUBJECTS)
            return

        super().do_GET()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "Invalid request length."})
            return

        if content_length <= 0 or content_length > MAX_REQUEST_SIZE:
            self._send_json(413, {"error": "Request must contain a message under 8 KB."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON."})
            return

        query = payload.get("message") if isinstance(payload, dict) else None
        if not isinstance(query, str) or not query.strip():
            self._send_json(400, {"error": "Enter a message before sending."})
            return

        query = query.strip()
        try:
            response = ask_veda(query)
            log_interaction("WEB", query, response)
        except (OSError, KeyError, TypeError, ValueError):
            logging.exception("Chat request failed")
            self._send_json(500, {"error": "VEDA could not answer right now. Check the server output."})
            return

        self._send_json(200, {"reply": response})


def main():
    port = 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), VedaHandler)
    print(f"VEDA is ready at http://127.0.0.1:{port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping VEDA web server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()