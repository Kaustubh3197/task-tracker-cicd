"""End-to-end tests: a real browser uses the app the way a person would."""

from playwright.sync_api import Page, expect


def add_task(page: Page, title: str):
    page.get_by_test_id("title-input").fill(title)
    page.get_by_test_id("add-button").click()


def test_page_shows_empty_state(page: Page):
    page.goto("/")
    expect(page).to_have_title("Task Tracker")
    expect(page.get_by_test_id("summary")).to_have_text("No tasks yet")


def test_add_task(page: Page):
    page.goto("/")
    add_task(page, "Learn GitHub Actions")
    expect(page.get_by_test_id("task")).to_have_count(1)
    expect(page.get_by_test_id("task")).to_contain_text("Learn GitHub Actions")
    expect(page.get_by_test_id("title-input")).to_have_value("")
    expect(page.get_by_test_id("summary")).to_have_text("0 of 1 done")


def test_empty_title_shows_error(page: Page):
    page.goto("/")
    add_task(page, "   ")
    expect(page.get_by_test_id("error")).to_have_text("Title is required")
    expect(page.get_by_test_id("task")).to_have_count(0)


def test_complete_task(page: Page):
    page.goto("/")
    add_task(page, "Write Dockerfile")
    add_task(page, "Push to GitHub")
    page.get_by_label('Mark "Write Dockerfile" done').check()
    expect(page.get_by_test_id("summary")).to_have_text("1 of 2 done")
    expect(page.get_by_test_id("task").first).to_have_class("done")


def test_delete_task(page: Page):
    page.goto("/")
    add_task(page, "Delete me")
    page.get_by_label('Delete "Delete me"').click()
    expect(page.get_by_test_id("task")).to_have_count(0)
    expect(page.get_by_test_id("summary")).to_have_text("No tasks yet")


def test_tasks_survive_page_reload(page: Page):
    page.goto("/")
    add_task(page, "Saved in database")
    expect(page.get_by_test_id("task")).to_have_count(1)
    page.reload()
    expect(page.get_by_test_id("task")).to_contain_text("Saved in database")
