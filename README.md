# ✦ AI Notes Assistant (SQLite Edition)

A full-stack web app to create, manage, and understand notes using AI (Claude).
**No MongoDB needed — uses SQLite, which is built into Python!**

---

## 📁 Project Folder Structure

```
ai-notes-assistant/
├── frontend/
│   ├── index.html              ← Home page
│   ├── css/
│   │   └── style.css           ← All styles
│   ├── js/
│   │   └── api.js              ← API helper functions (shared)
│   └── pages/
│       ├── add-note.html       ← Add Note page
│       └── view-notes.html     ← View/Search/Edit/Delete notes + AI features
│
├── backend/
│   ├── app.py                  ← Flask API (all routes + AI endpoints)
│   ├── requirements.txt        ← Python dependencies
│   └── notes.db                ← SQLite database file (auto-created on first run)
│
└── README.md
```

---

## ⚙️ Setup Steps

### 1. Prerequisites — Install these first

| Tool | Download |
|------|----------|
| Python 3.9+ | https://www.python.org/downloads/ |

> ✅ No MongoDB, no extra database software needed!
> SQLite is built into Python and the `notes.db` file is created automatically.

---

### 2. Set up the Backend

```bash
# Go into the backend folder
cd ai-notes-assistant/backend

# Create a virtual environment (keeps packages isolated)
python -m venv venv

# Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install required packages (only Flask + Anthropic — no database driver needed!)
pip install -r requirements.txt

# Set your Anthropic API key (get one at https://console.anthropic.com)
# Mac/Linux:
export ANTHROPIC_API_KEY="sk-ant-..."
# Windows:
set ANTHROPIC_API_KEY=sk-ant-...

# Run the Flask server
python app.py
```

You should see:
```
✓ SQLite database ready at: /path/to/backend/notes.db
🚀 AI Notes Assistant backend running on http://localhost:5000
```

The `notes.db` file is created automatically — no setup required.

---

### 3. Open the Frontend

**Option A — Just open the file (simplest):**
```
Double-click: frontend/index.html
```

**Option B — Use VS Code Live Server (recommended):**
1. Install the "Live Server" extension in VS Code
2. Right-click `frontend/index.html` → **Open with Live Server**

**Option C — Use Python's built-in server:**
```bash
cd ai-notes-assistant/frontend
python -m http.server 8080
# Then open: http://localhost:8080
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Claude API key (required for AI features) |

---

## 🚀 Features

| Feature | How it works |
|---------|-------------|
| Create Note | Fill in title + content on Add Note page |
| Edit Note | Open a note → click Edit |
| Delete Note | Click Delete on any note card (with confirmation) |
| Search | Type in the search bar on View Notes page |
| AI Summary | Open a note → click ⚡ Summarize |
| AI Explain | Open a note → click 💬 Explain Simply |
| AI Quiz | Open a note → click 🧠 Quiz Me |

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Backend:** Python + Flask + Flask-CORS
- **Database:** SQLite (built into Python — zero installation!)
- **AI:** Anthropic Claude API (`claude-sonnet-4-20250514`)

---

## 🗄️ SQLite vs MongoDB

| | SQLite | MongoDB |
|--|--------|---------|
| Installation | None (built-in) | Separate install |
| Data file | `notes.db` in your folder | Runs as a service |
| Best for | Simple apps, learning | Large-scale apps |
| Query style | SQL | JSON-like |

---

## ❓ Troubleshooting

**"Failed to load notes" / CORS error**
→ Make sure Flask is running on port 5000 (`python app.py`).

**AI features not working**
→ Check that `ANTHROPIC_API_KEY` is set correctly in your terminal.

**Database issues**
→ Delete `notes.db` and restart Flask — it will recreate a fresh database.
