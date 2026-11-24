"""
Simple HTTP Server for Hangman Web Edition
Serves the web/ directory on http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
import sys

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class HangmanHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable cache during development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def start_server(open_browser: bool = True):
    # Ensure port is reusable
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HangmanHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(" 🎮 HANGMAN ARCADE - WEB EDITION")
        print("=" * 60)
        print(f" Web Server is live at: {url}")
        print(" Serving files from:    web/")
        print(" Press Ctrl+C in terminal to stop.")
        print("=" * 60)

        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer successfully shut down.")


if __name__ == "__main__":
    should_open = "--no-browser" not in sys.argv
    start_server(open_browser=should_open)
