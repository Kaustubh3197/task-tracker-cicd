from flask import Blueprint, abort, current_app, jsonify, render_template, request

from app.db import get_db
from app.services import ValidationError, clean_title, summarize

bp = Blueprint("main", __name__)


def _row_to_dict(row) -> dict:
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def _get_task_or_404(task_id: int) -> dict:
    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        abort(404, description="Task not found")
    return _row_to_dict(row)


@bp.errorhandler(404)
def not_found(err):
    return jsonify(error=err.description), 404


@bp.get("/")
def index():
    return render_template("index.html", version=current_app.config["APP_VERSION"])


@bp.get("/health")
def health():
    """Used by Docker, CI smoke tests and the hosting platform to check the app is alive."""
    get_db().execute("SELECT 1")
    return jsonify(status="ok", version=current_app.config["APP_VERSION"])


@bp.get("/api/tasks")
def list_tasks():
    rows = get_db().execute("SELECT * FROM tasks ORDER BY id").fetchall()
    tasks = [_row_to_dict(r) for r in rows]
    return jsonify(tasks=tasks, summary=summarize(tasks))


@bp.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    try:
        title = clean_title(data.get("title"))
    except ValidationError as e:
        return jsonify(error=str(e)), 400

    db = get_db()
    cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    return jsonify(_get_task_or_404(cur.lastrowid)), 201


@bp.patch("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    _get_task_or_404(task_id)
    data = request.get_json(silent=True) or {}
    if not isinstance(data.get("done"), bool):
        return jsonify(error="'done' must be true or false"), 400

    db = get_db()
    db.execute("UPDATE tasks SET done = ? WHERE id = ?", (int(data["done"]), task_id))
    db.commit()
    return jsonify(_get_task_or_404(task_id))


@bp.delete("/api/tasks/<int:task_id>")
def delete_task(task_id: int):
    _get_task_or_404(task_id)
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return "", 204
