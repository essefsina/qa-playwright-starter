"""API tests with Playwright's request fixture — no browser needed.

Same assertion style SQA roles expect for REST API testing:
status codes, response shape, and round-trip creates.
Runs against the local demo API (demo_api/server.py) — no network needed.

Run:  pytest tests/test_api.py
"""
import threading

import pytest
from demo_api.server import run as run_demo_api


@pytest.fixture(scope="module")
def api_base_url():
    server = run_demo_api(0)  # 0 = pick a free port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


@pytest.fixture(scope="module")
def api(playwright, api_base_url):
    ctx = playwright.request.new_context(
        base_url=api_base_url,
        extra_http_headers={"Accept": "application/json"},
    )
    yield ctx
    ctx.dispose()


def test_get_post_returns_200_with_expected_fields(api):
    r = api.get("/posts/1")
    assert r.status == 200
    body = r.json()
    assert body["id"] == 1
    assert body["userId"] == 1
    assert isinstance(body["title"], str) and body["title"]


def test_get_missing_post_returns_404(api):
    r = api.get("/posts/999999")
    assert r.status == 404


def test_create_post_returns_201_and_echoes_payload(api):
    payload = {"title": "qa test", "body": "playwright api", "userId": 7}
    r = api.post("/posts", data=payload)
    assert r.status == 201
    body = r.json()
    assert body["title"] == payload["title"]
    assert body["userId"] == 7
    assert "id" in body  # server assigns the id


def test_created_post_is_retrievable(api):
    r = api.post("/posts", data={"title": "round trip", "userId": 3})
    new_id = r.json()["id"]

    fetched = api.get(f"/posts/{new_id}")
    assert fetched.status == 200
    assert fetched.json()["title"] == "round trip"


def test_post_list_is_a_nonempty_array(api):
    r = api.get("/posts")
    assert r.status == 200
    posts = r.json()
    assert isinstance(posts, list) and len(posts) > 0
    assert all("id" in p and "title" in p for p in posts)
