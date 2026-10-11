"""Business rules, kept free of Flask so they are easy to unit test."""

MAX_TITLE_LENGTH = 200


class ValidationError(ValueError):
    pass


def clean_title(raw) -> str:
    """Trim whitespace and check a task title is valid."""
    if not isinstance(raw, str):
        raise ValidationError("Title must be text")
    title = " ".join(raw.split())  # collapse repeated spaces
    if not title:
        raise ValidationError("Title is required")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValidationError(f"Title must be at most {MAX_TITLE_LENGTH} characters")
    return title


def summarize(tasks: list[dict]) -> dict:
    """Counts shown at the top of the page, e.g. '1 of 3 done'."""
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    return {
        "total": total,
        "done": done,
        "remaining": total - done,
        "percent_done": round(done * 100 / total) if total else 0,
    }
