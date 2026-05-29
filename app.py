# =============================================================
# app.py - Simple Notes Assistant
# No AI, No API key needed!
# Tech: Flask + SQLite
# =============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*")

# SQLite database file (auto-created on first run)
DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")


# ==============================================================
# DATABASE SETUP — creates tables on first run
# ==============================================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Notes table
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            pinned     INTEGER DEFAULT 0,
            created_at TEXT    NOT NULL,
            updated_at TEXT    NOT NULL
        )
    """)

    # Quiz questions table (linked to a note)
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id    INTEGER NOT NULL,
            question   TEXT    NOT NULL,
            option_a   TEXT    NOT NULL,
            option_b   TEXT    NOT NULL,
            option_c   TEXT    NOT NULL,
            option_d   TEXT    NOT NULL,
            answer     TEXT    NOT NULL,
            FOREIGN KEY (note_id) REFERENCES notes(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"✓ Database ready: {DB_PATH}")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def to_dict(row):
    return dict(row)


# ==============================================================
# NOTES ENDPOINTS
# ==============================================================

# Get all notes (pinned first, then by date)
@app.route("/api/notes", methods=["GET"])
def get_notes():
    search = request.args.get("search", "").strip()
    conn = get_db()
    if search:
        rows = conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? ORDER BY pinned DESC, created_at DESC",
            (f"%{search}%",)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM notes ORDER BY pinned DESC, created_at DESC"
        ).fetchall()
    conn.close()
    return jsonify([to_dict(r) for r in rows])


# Get single note
@app.route("/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(to_dict(row))


# Create note
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.json
    if not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content required"}), 400
    now = datetime.utcnow().isoformat()
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO notes (title, content, pinned, created_at, updated_at) VALUES (?, ?, 0, ?, ?)",
        (data["title"].strip(), data["content"].strip(), now, now)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(to_dict(row)), 201


# Update note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    if not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content required"}), 400
    now = datetime.utcnow().isoformat()
    conn = get_db()
    result = conn.execute(
        "UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?",
        (data["title"].strip(), data["content"].strip(), now, note_id)
    )
    conn.commit()
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Note not found"}), 404
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    return jsonify(to_dict(row))


# Delete note (also deletes its quiz questions)
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db()
    conn.execute("DELETE FROM quiz WHERE note_id = ?", (note_id,))
    result = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"message": "Note deleted"})


# Toggle pin/unpin
@app.route("/api/notes/<int:note_id>/pin", methods=["POST"])
def toggle_pin(note_id):
    conn = get_db()
    row = conn.execute("SELECT pinned FROM notes WHERE id = ?", (note_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Note not found"}), 404
    new_pin = 0 if row["pinned"] else 1  # Toggle
    conn.execute("UPDATE notes SET pinned = ? WHERE id = ?", (new_pin, note_id))
    conn.commit()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    return jsonify(to_dict(row))


# ==============================================================
# QUIZ ENDPOINTS
# ==============================================================

# Get all quiz questions for a note
@app.route("/api/notes/<int:note_id>/quiz", methods=["GET"])
def get_quiz(note_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM quiz WHERE note_id = ?", (note_id,)
    ).fetchall()
    conn.close()
    return jsonify([to_dict(r) for r in rows])


# Save quiz questions for a note (replaces existing)
@app.route("/api/notes/<int:note_id>/quiz", methods=["POST"])
def save_quiz(note_id):
    data = request.json  # Expects {"questions": [...]}
    questions = data.get("questions", [])

    if not questions:
        return jsonify({"error": "No questions provided"}), 400

    conn = get_db()
    # Delete old quiz for this note
    conn.execute("DELETE FROM quiz WHERE note_id = ?", (note_id,))

    # Insert new questions
    for q in questions:
        conn.execute("""
            INSERT INTO quiz (note_id, question, option_a, option_b, option_c, option_d, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            note_id,
            q["question"],
            q["option_a"],
            q["option_b"],
            q["option_c"],
            q["option_d"],
            q["answer"]
        ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Quiz saved!", "count": len(questions)}), 201


# Delete quiz for a note
@app.route("/api/notes/<int:note_id>/quiz", methods=["DELETE"])
def delete_quiz(note_id):
    conn = get_db()
    conn.execute("DELETE FROM quiz WHERE note_id = ?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quiz deleted"})


if __name__ == "__main__":
    init_db()
    print("🚀 Simple Notes running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
