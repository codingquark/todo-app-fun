#!/usr/bin/env python3
import sqlite3
import argparse
import os
from datetime import datetime

DB_FILE = os.path.expanduser("./.todo.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  completed INTEGER DEFAULT 0,
                  created_at TEXT NOT NULL,
                  tags TEXT)''')
    conn.commit()
    conn.close()

def add_task(title, tags=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    created_at = datetime.now().isoformat()
    c.execute("INSERT INTO tasks (title, created_at, tags) VALUES (?, ?, ?)",
              (title, created_at, ','.join(tags) if tags else None))
    conn.commit()
    print(f"Task added: {title}")
    conn.close()

def list_tasks(completed=None, tags=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM tasks"
    conditions = []
    if completed is not None:
        conditions.append(f"completed = {1 if completed else 0}")
    if tags:
        tag_conditions = [f"tags LIKE '%{tag}%'" for tag in tags]
        conditions.append("(" + " OR ".join(tag_conditions) + ")")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    c.execute(query)
    tasks = c.fetchall()
    for task in tasks:
        status = "[x]" if task[2] else "[ ]"
        tags = f" (tags: {task[4]})" if task[4] else ""
        print(f"{task[0]}. {status} {task[1]}{tags}")
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if c.rowcount > 0:
        print(f"Task {task_id} deleted.")
    else:
        print(f"Task {task_id} not found.")
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    if c.rowcount > 0:
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Task {task_id} not found.")
    conn.commit()
    conn.close()

def edit_task(task_id, new_title, new_tags=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if new_tags is not None:
        c.execute("UPDATE tasks SET title = ?, tags = ? WHERE id = ?",
                  (new_title, ','.join(new_tags), task_id))
    else:
        c.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    if c.rowcount > 0:
        print(f"Task {task_id} updated.")
    else:
        print(f"Task {task_id} not found.")
    conn.commit()
    conn.close()

def search_tasks(query):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE title LIKE ? OR tags LIKE ?",
              (f"%{query}%", f"%{query}%"))
    tasks = c.fetchall()
    for task in tasks:
        status = "[x]" if task[2] else "[ ]"
        tags = f" (tags: {task[4]})" if task[4] else ""
        print(f"{task[0]}. {status} {task[1]}{tags}")
    conn.close()

def list_tags():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT tags FROM tasks WHERE tags IS NOT NULL")
    all_tags = c.fetchall()
    unique_tags = set()
    for tags in all_tags:
        unique_tags.update(tags[0].split(','))
    print("Tags:")
    for tag in sorted(unique_tags):
        print(f"- {tag}")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Todo App")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--tags", nargs="*", help="Tags for the task")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--completed", action="store_true", help="Show only completed tasks")
    list_parser.add_argument("--incomplete", action="store_true", help="Show only incomplete tasks")
    list_parser.add_argument("--tags", nargs="*", help="Filter tasks by tags")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark as completed")

    edit_parser = subparsers.add_parser("edit", help="Edit a task")
    edit_parser.add_argument("task_id", type=int, help="ID of the task to edit")
    edit_parser.add_argument("new_title", help="New title for the task")
    edit_parser.add_argument("--tags", nargs="*", help="New tags for the task")

    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("query", help="Search query")

    subparsers.add_parser("tags", help="List all tags")

    args = parser.parse_args()

    init_db()

    if args.command == "add":
        add_task(args.title, args.tags)
    elif args.command == "list":
        completed = True if args.completed else (False if args.incomplete else None)
        list_tasks(completed, args.tags)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "complete":
        complete_task(args.task_id)
    elif args.command == "edit":
        edit_task(args.task_id, args.new_title, args.tags)
    elif args.command == "search":
        search_tasks(args.query)
    elif args.command == "tags":
        list_tags()

if __name__ == "__main__":
    main()

