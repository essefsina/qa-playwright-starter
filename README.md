# QA Playwright Starter

A hands-on starter for learning **Playwright** — the test-automation tool most
companies are standardizing on. UI tests, API tests, and CI, all wired to
pytest (which you already know).

## What's inside

| Path | What it is |
|---|---|
| `demo_app/index.html` | A tiny self-contained practice app: login form + todo list. Opens from disk, no server needed. |
| `tests/test_login.py` | 4 UI tests: happy-path login, empty-submit validation, wrong password, logout |
| `tests/test_todo.py` | 5 UI tests: add, empty-add error, complete, delete, counting |
| `demo_api/server.py` | Tiny stdlib-only REST API (`/posts`) the API tests run against — no network needed |
| `tests/test_api.py` | 5 API tests using Playwright's request fixture (GET/POST, 200/201/404, response shape, round-trip create) |
| `conftest.py` | Shared `demo_page` fixture — fresh app load per test |
| `.github/workflows/tests.yml` | CI: installs deps + Chromium, runs the suite on every push/PR |

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium   # one-time browser download
pytest                                   # all 14 tests
pytest tests/test_login.py               # just one file
pytest --headed                          # watch the browser work
```

## The 5 Playwright ideas these tests teach

1. **Locators over selectors** — `get_by_role`, `get_by_placeholder`,
   `get_by_label` describe what the user sees, not DOM plumbing. They survive
   redesigns that break CSS/XPath selectors.
2. **Auto-waiting** — no `sleep()` calls anywhere. Actions and `expect()`
   assertions retry until the condition holds or times out.
3. **`expect()` assertions** — `to_be_visible()`, `to_have_text()`,
   `to_have_count()` read like the requirement they verify.
4. **Fixtures for setup** — `demo_page` gives every test a clean app state.
   Same pattern scales to logged-in sessions, test data, API contexts.
5. **API testing without a browser** — the `playwright.request` fixture does
   REST checks with the same assertion style as UI tests.

## Suggested learning path

1. Run the suite, then re-run with `--headed` and watch it.
2. Break something in `demo_app/index.html` and see which test catches it —
   this is the "catch a real issue" muscle.
3. Add a test: todo item text is trimmed of whitespace (hint: check the JS).
4. Add an API test: `GET /posts/999` returns 404 with an `{"error": ...}` body.
5. Learn **trace viewer**: `pytest --tracing on`, then
   `python -m playwright show-trace` — this is what you attach to bug reports.
6. Next tools in the SQA stack: **Docker** (throwaway test environments),
   **k6 or Locust** (load testing), **GitHub Actions** (already in this repo).

## Why Playwright for SQA roles

- Fastest-growing UI automation framework; the default choice for new projects
- One tool covers UI, API, and visual-regression testing
- Python + pytest support means your existing Python skills transfer directly
- Trace viewer + HTML reports make failures explainable to developers —
  that's the SQA skill interviewers probe for
