"""Todo-list tests — add, complete, delete, and edge cases.

Run:  pytest tests/test_todo.py
"""
from playwright.sync_api import expect


def _add_todo(page, text):
    page.get_by_label("New todo").fill(text)
    page.get_by_role("button", name="Add").click()


def test_add_todo_appears_in_list(demo_page):
    _add_todo(demo_page, "Write more tests")

    expect(demo_page.get_by_text("Write more tests")).to_be_visible()
    expect(demo_page.get_by_text("1 item")).to_be_visible()


def test_add_empty_todo_shows_error(demo_page):
    demo_page.get_by_role("button", name="Add").click()

    expect(demo_page.locator("#todo-error")).to_have_text(
        "Todo text cannot be empty."
    )
    expect(demo_page.get_by_text("0 items")).to_be_visible()


def test_complete_todo_strikes_it_through(demo_page):
    _add_todo(demo_page, "Review PRs")

    demo_page.get_by_role("button", name="Mark done: Review PRs").click()

    item = demo_page.locator("li", has_text="Review PRs")
    expect(item).to_have_class("done")


def test_delete_todo_removes_it(demo_page):
    _add_todo(demo_page, "Temporary task")

    demo_page.get_by_role("button", name="Delete: Temporary task").click()

    expect(demo_page.get_by_text("Temporary task")).to_be_hidden()
    expect(demo_page.get_by_text("0 items")).to_be_visible()


def test_multiple_todos_count_correctly(demo_page):
    for i in range(3):
        _add_todo(demo_page, f"Task {i}")

    expect(demo_page.get_by_text("3 items")).to_be_visible()
    expect(demo_page.locator("#todo-list li")).to_have_count(3)
