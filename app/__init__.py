"""Task Tracker: a tiny Flask app used to demonstrate a full CI/CD pipeline."""

import os

from flask import Flask

from app import db
from app.routes import bp


def _detect_version() -> str:
    """Short commit id set by the pipeline, or by Render when it builds the app."""
    version = os.getenv("APP_VERSION", "dev")
    if version == "dev" and os.getenv("RENDER_GIT_COMMIT"):
        version = os.environ["RENDER_GIT_COMMIT"][:7]
    return version


def create_app(config: dict | None = None) -> Flask:
    """App factory: tests create a fresh app with their own temporary database."""
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.getenv("DATABASE", "tasks.db"),
        APP_VERSION=_detect_version(),
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(bp)
    return app
