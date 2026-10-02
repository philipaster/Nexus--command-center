from flask import Flask, render_template, request, jsonify
import sqlite3
import secrets
import string
import platform
import time
import os
from datetime import datetime

app = Flask(__name__)
DB = "nexus.db"
START_TIME = time.time()

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0,
        created TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        created TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

def system_info():
    return {
        "os": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "processor": platform.processor() or "Unknown",
        "hostname": platform.node(),
        "uptime": round(time.time() - START_TIME, 1)
    }

@app.route("/")
def home():
    conn = db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks, notes=notes, info=system_info())

@app.post("/api/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="Task title required"), 400
    conn = db()
    cur = conn.execute(
        "INSERT INTO tasks(title, created) VALUES(?, ?)",
        (title, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(task))

@app.patch("/api/tasks/<int:task_id>")
def toggle_task(task_id):
    conn = db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify(error="Task not found"), 404
    new_state = 0 if task["done"] else 1
    conn.execute("UPDATE tasks SET done=? WHERE id=?", (new_state, task_id))
    conn.commit()
    conn.close()
    return jsonify(done=new_state)

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    conn = db()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify(ok=True)

@app.post("/api/notes")
def add_note():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    body = str(data.get("body", "")).strip()
    if not title or not body:
        return jsonify(error="Title and body required"), 400
    conn = db()
    cur = conn.execute(
        "INSERT INTO notes(title, body, created) VALUES(?, ?, ?)",
        (title, body, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    note = conn.execute("SELECT * FROM notes WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(note))

@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id):
    conn = db()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify(ok=True)

@app.get("/api/system")
def system():
    return jsonify(system_info())

@app.get("/api/generate-password")
def generate_password():
    try:
        length = max(8, min(int(request.args.get("length", 20)), 64))
    except ValueError:
        length = 20
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*_-+="
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    return jsonify(password=password)

@app.get("/api/stats")
def stats():
    conn = db()
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done = conn.execute("SELECT COUNT(*) FROM tasks WHERE done=1").fetchone()[0]
    notes = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    conn.close()
    return jsonify(tasks=total, completed=done, notes=notes)

@app.errorhandler(404)
def not_found(_):
    return jsonify(error="NEXUS route not found"), 404

if __name__ == "__main__":
    init_db()
    print("\nNEXUS COMMAND CENTER")
    print("Open: http://127.0.0.1:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
