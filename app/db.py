import sqlite3
from contextlib import closing

from flask import Flask, current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT    NOT NULL,
    done  INTEGER NOT NULL DEFAULT 0
);
"""


def get_db() -> sqlite3.Connection:
    """One database connection per request."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app: Flask):
    # Note: `with sqlite3.connect()` alone does not close the connection
    with closing(sqlite3.connect(app.config["DATABASE"])) as conn:
        conn.executescript(SCHEMA)
    app.teardown_appcontext(close_db)
