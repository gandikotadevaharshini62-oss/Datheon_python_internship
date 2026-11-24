# 🎮 Hangman: Terminal & Web Editions

A complete suite of Hangman games built in Python and modern Web technologies (HTML5 / CSS3 / ES6 JS / Web Audio API / SVG / Canvas).

---

## 🌐 Web Edition (Hangman Arcade)

An interactive, responsive web app featuring:
- **Dual Visual Modes**: Dynamic vector SVG illustration with drawing animations, plus a retro ASCII Terminal mode toggle.
- **Categorized Word Banks**: Tech & Coding, Animals & Nature, Space & Science, World & Geography, and All/Mixed.
- **Educational Hints**: In-depth clue for each word accessible via the 💡 Hint button.
- **Web Audio API Synthesizer**: Pure programmatic sound effects (click, correct bell, error buzz, victory fanfare, game over tones) — zero audio downloads needed!
- **Celebration Confetti**: HTML5 canvas particle celebration on victory.
- **Persistent Statistics & Streaks**: Win streaks, games won/played, accuracy, and best streak saved to `localStorage`.
- **Hybrid Input**: Virtual tactile on-screen keyboard + physical keyboard input listener (`A-Z`, `Enter`, `Escape`).

### How to Run the Website:

#### Option 1: Using the Python Web Server
```powershell
cd C:\Users\LAB\.gemini\antigravity\scratch\hangman
python server.py
```
This automatically launches your default web browser and opens:
`http://localhost:8000`

#### Option 2: Direct File Open
You can directly open `web/index.html` in Chrome, Edge, Firefox, or any modern web browser without needing any server:
`file:///C:/Users/LAB/.gemini/antigravity/scratch/hangman/web/index.html`

---

## 💻 Terminal Edition (`hangman.py`)

Run the original terminal game in your command line:

```powershell
cd C:\Users\LAB\.gemini\antigravity\scratch\hangman
python hangman.py
```

### Running Tests:

- Terminal unit & gameplay tests:
  ```powershell
  python -m unittest test_hangman.py -v
  ```
- Web server asset delivery verification:
  ```powershell
  python test_web_server.py
  ```

---

## 📂 Project Structure

```
hangman/
├── hangman.py             # Terminal-based Hangman game in Python 3
├── test_hangman.py        # Automated test suite for terminal game
├── server.py              # Lightweight HTTP server for web version
├── test_web_server.py     # Verification script for web server & assets
├── README.md              # Project documentation
└── web/                   # Web application directory
    ├── index.html         # HTML5 semantic UI & SVG gallows
    ├── style.css          # Dark cyberpunk theme & responsive styles
    └── app.js             # Game engine, audio synth, confetti & stats
```
