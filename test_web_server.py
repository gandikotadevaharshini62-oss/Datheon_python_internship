"""
Verification script for Hangman Web Application.
Tests HTTP server delivery and integrity of web assets.
"""

import threading
import time
import urllib.request
import os
import sys

from server import start_server, PORT, WEB_DIR

def run_tests():
    # 1. Verify files exist on disk
    for filename in ["index.html", "style.css", "app.js"]:
        path = os.path.join(WEB_DIR, filename)
        assert os.path.exists(path), f"File missing: {path}"
        size = os.path.getsize(path)
        assert size > 0, f"File empty: {path}"
        print(f"[OK] Asset exists: {filename} ({size} bytes)")

    # 2. Test server in thread
    server_thread = threading.Thread(target=start_server, args=(False,), daemon=True)
    server_thread.start()
    time.sleep(1)  # Wait for socket to bind

    base_url = f"http://localhost:{PORT}"
    
    endpoints = ["/", "/index.html", "/style.css", "/app.js"]
    for endpoint in endpoints:
        req = urllib.request.Request(base_url + endpoint)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Failed with status: {response.status}"
            content = response.read()
            assert len(content) > 0, f"Empty response for {endpoint}"
            print(f"[OK] HTTP 200: {endpoint} ({len(content)} bytes)")

    print("\nAll web server tests and assets verified successfully!")

if __name__ == "__main__":
    run_tests()
