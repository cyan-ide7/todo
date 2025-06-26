from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'todo.db'

def init_db():
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                CREATE TABLE tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    category TEXT,
                    due_date TEXT,
                    is_done INTEGER DEFAULT 0
                )
            ''')

init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, category, due_date, is_done FROM tasks")
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    category = request.form.get('category')
    due_date = request.form.get('due_date')
    if task:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO tasks (task, category, due_date) VALUES (?, ?, ?)",
                         (task, category, due_date))
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        task = request.form.get('task')
        category = request.form.get('category')
        due_date = request.form.get('due_date')
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("UPDATE tasks SET task=?, category=?, due_date=? WHERE id=?",
                         (task, category, due_date, task_id))
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DB_NAME) as conn:
            task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        return render_template('edit.html', task=task)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
