"""Запуск: python app.py. GUI відкривається у браузері."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os

from ciphers import NAME, KEY, MESSAGE, CIPHER, substitute, vigenere, polybius
from rsa_lab import rsa

ROOT = Path(__file__).resolve().parent


def calculate(data):
    value = data["text"].strip()
    if not 0 < len(value) <= 1000:
        raise ValueError("Довжина повідомлення має бути від 1 до 1000 символів.")
    mode, reverse = data["mode"], data["reverse"]
    if mode == "caesar":
        shift = int(data.get("key", ""))
        if not 0 <= shift <= 32:
            raise ValueError("Зсув має бути від 0 до 32.")
        return substitute(value, [shift], reverse)
    if mode == "vigenere":
        return vigenere(value, data.get("key", ""), reverse)
    if mode == "polybius":
        return polybius(value, reverse)
    if mode == "rsa":
        return rsa(value, reverse)
    raise ValueError("Оберіть алгоритм.")


class Handler(BaseHTTPRequestHandler):
    def respond(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            examples = json.dumps(dict(name=NAME, key=KEY, message=MESSAGE, cipher=CIPHER), ensure_ascii=False)
            html = (ROOT / "index.html").read_text(encoding="utf-8").replace("__EXAMPLES__", examples)
            self.respond(html.encode(), "text/html; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/calculate":
            self.send_error(404)
            return
        try:
            size = int(self.headers["Content-Length"])
            if not 0 < size <= 16000:
                raise ValueError("Завеликий запит.")
            result, steps = calculate(json.loads(self.rfile.read(size)))
            reply, status = dict(result=result, steps=steps), 200
        except (TypeError, ValueError, KeyError) as error:
            reply, status = dict(error=str(error)), 400
        self.respond(json.dumps(reply, ensure_ascii=False).encode(), "application/json; charset=utf-8", status)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Відкрийте http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
