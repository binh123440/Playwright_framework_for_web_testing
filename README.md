# Playwright Python scaffold

This scaffold was generated to mirror the structure of the existing Playwright (Python) framework and provide a starting point for Playwright tests in Python.

Quick start

1. Create and activate a virtual environment (recommended):
   - python -m venv .venv
   - .\.venv\Scripts\activate
2. Install dependencies:
   - pip install -r requirements.txt
3. Install browsers:
   - playwright install
4. Run tests:
   - pytest

Structure overview

- pages/: Page objects
- helpers/: small helper modules (config, json, wait, element helpers)
- fixtures/: pytest fixtures (browser/page and screenshot on fail)
- tests/: test cases
- resources/: test data and config
- screenshots/: saved screenshots from failing tests

