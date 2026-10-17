"""Login-form tests — happy path, validation, and error states.

Run:  pytest tests/test_login.py
"""
from playwright.sync_api import expect


def test_successful_login_shows_welcome(demo_page):
    demo_page.get_by_placeholder("Username").fill("demo")
    demo_page.get_by_placeholder("Password").fill("demo")
    demo_page.get_by_role("button", name="Sign in").click()

    expect(demo_page.get_by_text("Welcome back, demo!")).to_be_visible()
    # the form hides after a successful login
    expect(demo_page.get_by_placeholder("Username")).to_be_hidden()


def test_empty_submit_shows_required_error(demo_page):
    demo_page.get_by_role("button", name="Sign in").click()

    expect(demo_page.locator("#login-error")).to_have_text(
        "Username and password are required."
    )


def test_wrong_password_shows_invalid_error(demo_page):
    demo_page.get_by_placeholder("Username").fill("demo")
    demo_page.get_by_placeholder("Password").fill("wrong")
    demo_page.get_by_role("button", name="Sign in").click()

    expect(demo_page.locator("#login-error")).to_have_text(
        "Invalid username or password."
    )
    # still on the login form — no welcome message
    expect(demo_page.get_by_text("Welcome back")).to_be_hidden()


def test_logout_returns_to_login_form(demo_page):
    demo_page.get_by_placeholder("Username").fill("demo")
    demo_page.get_by_placeholder("Password").fill("demo")
    demo_page.get_by_role("button", name="Sign in").click()
    expect(demo_page.get_by_text("Welcome back, demo!")).to_be_visible()

    demo_page.get_by_role("button", name="Sign out").click()

    expect(demo_page.get_by_placeholder("Username")).to_be_visible()
    expect(demo_page.get_by_text("Welcome back")).to_be_hidden()
