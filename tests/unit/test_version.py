"""The version shown on /health tells us which commit is live after a deploy."""

from app import create_app


def test_version_from_pipeline(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_VERSION", "abc1234")
    app = create_app({"DATABASE": str(tmp_path / "t.db")})
    assert app.test_client().get("/health").get_json()["version"] == "abc1234"


def test_version_from_render(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_VERSION", "dev")
    monkeypatch.setenv("RENDER_GIT_COMMIT", "0123456789abcdef")
    app = create_app({"DATABASE": str(tmp_path / "t.db")})
    assert app.config["APP_VERSION"] == "0123456"


def test_version_defaults_to_dev(monkeypatch, tmp_path):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
    app = create_app({"DATABASE": str(tmp_path / "t.db")})
    assert app.config["APP_VERSION"] == "dev"
