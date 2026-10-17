"""Shared fixtures for the Playwright practice suite."""
import pathlib

import pytest

DEMO_URL = pathlib.Path(__file__).parent.joinpath(
    "demo_app", "index.html"
).as_uri()


@pytest.fixture()
def demo_page(page):
    """A fresh load of the local demo app for every test."""
    page.goto(DEMO_URL)
    return page
