# 📒 Simple Notes Assistant

Simple Notes Assistant is a beginner-friendly note-taking web app built with HTML, CSS, and JavaScript on the frontend, and Python Flask with SQLite on the backend. It lets you create, edit, delete, and search notes by title, with extra features like pinning important notes to the top, a dark mode for comfortable reading, and a built-in quiz builder where you can write your own questions for any note and test yourself. All your notes are saved locally in a SQLite database file on your computer, so no internet connection or API key is required to use it.

---

## 📁 Project Structure

```
simple-notes/
├── frontend/
│   ├── index.html              ← Home page
│   ├── css/
│   │   └── style.css           ← All styles + dark mode
│   ├── js/
│   │   └── api.js              ← Shared API helper functions
│   └── pages/
│       ├── add-note.html       ← Add a new note
│       └── view-notes.html     ← View, search, edit, delete, quiz
│
├── backend/
│   ├── app.py                  ← Flask server + all API routes
│   ├── requirements.txt        ← Python packages needed
│   └── notes.db                ← SQLite database (auto-created)
│
└── README.md
```

---

## ✅ Features

| Feature | Description |
|---------|-------------|
| ✏️ Create Notes | Write and save notes with a title and content |
| 📝 Edit Notes | Update any note anytime |
| 🗑 Delete Notes | Remove notes you no longer need |
| 🔍 Search | Search notes by title instantly |
| 📌 Pin Notes | Pin important notes to always show at the top |
| 🌙 Dark Mode | Toggle dark/light mode, preference is saved |
| 🧠 Quiz Builder | Create your own quiz questions for any note |
| ▶ Take Quiz | Answer your quiz and see your score |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | SQLite (built into Python) |

---

## ⚙️ Setup & Run

### 1. Prerequisites
Only **Python 3.9+** is needed. Download from https://www.python.org/downloads/

### 2. Install packages
Open Command Prompt and run:
```bash
cd Downloads\simple-notes\backend
pip install flask flask-cors
```

### 3. Start the backend
```bash
python app.py
```

You should see:
```
✓ Database ready: ...notes.db
🚀 Simple Notes running on http://127.0.0.1:5000
```

### 4. Open the frontend
Go to `simple-notes/frontend/` and double-click **`index.html`**

> ⚠️ Keep the CMD window open while using the app. Closing it stops the backend.

---

## 🗄️ Database

The app uses SQLite which stores all data in a single file called `notes.db` inside the `backend/` folder. This file is created automatically when you run `python app.py` for the first time. No database software or setup is needed.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes` | Get all notes |
| GET | `/api/notes?search=keyword` | Search notes by title |
| GET | `/api/notes/<id>` | Get one note |
| POST | `/api/notes` | Create a note |
| PUT | `/api/notes/<id>` | Update a note |
| DELETE | `/api/notes/<id>` | Delete a note |
| POST | `/api/notes/<id>/pin` | Pin or unpin a note |
| GET | `/api/notes/<id>/quiz` | Get quiz for a note |
| POST | `/api/notes/<id>/quiz` | Save quiz questions |
| DELETE | `/api/notes/<id>/quiz` | Delete quiz |

---

## ❓ Troubleshooting

**"Failed to fetch" or "Load notes failed"**
→ Flask is not running. Open CMD and run `python app.py` inside the `backend/` folder.

**"ModuleNotFoundError: No module named flask"**
→ Run `pip install flask flask-cors` first.

**Notes not saving**
→ Make sure the backend is running on port 5000 before clicking Save.

**Database issues**
→ Delete `notes.db` and restart Flask — it will create a fresh database.
