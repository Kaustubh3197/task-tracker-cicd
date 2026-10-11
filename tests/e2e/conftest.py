"""Start the real app on a free port so Playwright can test it in a browser.

If E2E_BASE_URL is set (e.g. the Docker container in CI, or the deployed site),
tests run against that address instead.
"""

import os
import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture(scope="session")
def base_url(tmp_path_factory):
    external = os.getenv("E2E_BASE_URL")
    if external:
        yield external.rstrip("/")
        return

    db_file = tmp_path_factory.mktemp("e2e") / "e2e.db"
    app = create_app({"DATABASE": str(db_file), "APP_VERSION": "e2e"})
    server = make_server("127.0.0.1", 0, app)  # port 0 = any free port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


@pytest.fixture(autouse=True)
def clean_tasks(page, base_url):
    """Delete all tasks before each test so tests don't affect each other."""
    tasks = page.request.get(f"{base_url}/api/tasks").json()["tasks"]
    for task in tasks:
        page.request.delete(f"{base_url}/api/tasks/{task['id']}")
