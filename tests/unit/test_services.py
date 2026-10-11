"""Unit tests: check single functions in isolation. Fast, no browser, no server."""

import pytest

from app.services import MAX_TITLE_LENGTH, ValidationError, clean_title, summarize


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Buy milk", "Buy milk"),
        ("  Buy milk  ", "Buy milk"),
        ("Buy    milk", "Buy milk"),
        ("a" * MAX_TITLE_LENGTH, "a" * MAX_TITLE_LENGTH),
    ],
)
def test_clean_title_accepts_valid_titles(raw, expected):
    assert clean_title(raw) == expected


@pytest.mark.parametrize(
    "raw, message",
    [
        ("", "required"),
        ("    ", "required"),
        (None, "must be text"),
        (123, "must be text"),
        ("a" * (MAX_TITLE_LENGTH + 1), "at most"),
    ],
)
def test_clean_title_rejects_invalid_titles(raw, message):
    with pytest.raises(ValidationError, match=message):
        clean_title(raw)


def test_summarize_empty_list():
    assert summarize([]) == {"total": 0, "done": 0, "remaining": 0, "percent_done": 0}


def test_summarize_counts_done_tasks():
    tasks = [{"done": True}, {"done": False}, {"done": True}]
    assert summarize(tasks) == {"total": 3, "done": 2, "remaining": 1, "percent_done": 67}

def test_title_limit_is_200_characters():
    """Requirement: titles up to 200 characters are allowed, 201 are not."""
    assert clean_title("a" * 200) == "a" * 200

    with pytest.raises(ValidationError):
        clean_title("a" * 201)