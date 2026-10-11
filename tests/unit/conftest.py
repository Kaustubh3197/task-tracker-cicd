import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    """A fresh app with an empty temporary database for every test."""
    app = create_app({"DATABASE": str(tmp_path / "test.db"), "TESTING": True})
    return app.test_client()
