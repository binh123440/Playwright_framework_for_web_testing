# Re-export fixtures/hooks from the `fixtures` package so pytest will discover them.
# Keeping this tiny shim avoids moving the user's existing fixtures directory.
# from fixtures.conftest import *  # noqa: F401,F403

import os
from pathlib import Path
import importlib
from typing import TYPE_CHECKING
import pytest
from playwright.sync_api import sync_playwright
from helpers.config_loader import get
import re
import shutil

if TYPE_CHECKING:
    # inform static analyzers about the optional dependency without importing it at runtime
    import allure  # type: ignore

REPORTS_DIR = Path(__file__).parents[1] / "reports"
SCREENSHOT_DIR = REPORTS_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(pw):
    headless_str = get("HEADLESS", "false")
    # Convert string to boolean
    headless = headless_str not in ("false", "False", "0", "")
    b = pw.chromium.launch(headless=headless)   
    yield b
    b.close()


@pytest.fixture()
def page(browser, request):
    """Create a context+page and collect console/page errors for later attachment.

    - collects console messages to `request.node._console_logs`
    - keeps behavior identical unless env/config enables video/trace
    """
    ctx = browser.new_context()
    page = ctx.new_page()

    console_logs: list[str] = []

    def _on_console(msg):
        try:
            console_logs.append(f"[{msg.type}] {msg.text}")
        except Exception:
            console_logs.append("[console] <unserializable>")

    def _on_page_error(exc):
        try:
            console_logs.append(f"[pageerror] {exc}")
        except Exception:
            console_logs.append("[pageerror] <unserializable>")

    page.on("console", _on_console)
    page.on("pageerror", _on_page_error)

    # expose for pytest hooks
    request.node._console_logs = console_logs

    yield page

    # cleanup listeners and context
    try:
        page.off("console", _on_console)
        page.off("pageerror", _on_page_error)
    except Exception:
        pass
    ctx.close()


def _safe_name(nodeid: str) -> str:
    # produce a filesystem-safe filename for a test nodeid
    return re.sub(r"[^A-Za-z0-9_.-]", "_", nodeid)

def _get_allure():
    """Return the `allure` module if available, otherwise None (runtime-safe)."""
    try:
        return importlib.import_module("allure")
    except Exception:
        return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On test call-phase failure:
      - save screenshot to ./screenshots/ and ./reports/screenshots/
      - save page HTML
      - attach to Allure if `allure` is installed
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or not rep.failed:
        return

    page = item.funcargs.get("page")
    if not page:
        return

    project_root = Path(__file__).parents[1]

    # canonical location for CI/Allure (single source of truth)
    reports_screenshots = SCREENSHOT_DIR
    reports_screenshots.mkdir(parents=True, exist_ok=True)

    # legacy location (kept only if explicitly requested via env)
    legacy_screenshots = project_root / "screenshots"
    keep_legacy = os.environ.get("KEEP_LEGACY_SCREENSHOTS", "0").lower() in ("1", "true", "yes")
    if keep_legacy:
        legacy_screenshots.mkdir(parents=True, exist_ok=True)

    name = _safe_name(item.nodeid)
    png_path = reports_screenshots / f"{name}.png"
    html_path = reports_screenshots / f"{name}.html"

    # save artifacts to the canonical reports/ location only
    try:
        img_bytes = page.screenshot(path=str(png_path), full_page=True)
    except Exception as exc:
        print(f"[conftest] screenshot failed: {exc}")

    try:
        html = page.content()
        html_path.write_text(html, encoding="utf-8")
    except Exception as exc:
        print(f"[conftest] page content save failed: {exc}")

    # If a legacy directory is requested, mirror artifacts there (best-effort).
    if keep_legacy:
        try:
            if png_path.exists():
                shutil.copy2(str(png_path), legacy_screenshots / png_path.name)
            if html_path.exists():
                shutil.copy2(str(html_path), legacy_screenshots / html_path.name)
        except Exception as exc:
            print(f"[conftest] failed to mirror artifacts to legacy folder: {exc}")

    # attach to Allure (optional; no-op if allure not installed)
    try:
        import allure
        if png_path.exists():
            allure.attach.file(str(png_path), name="screenshot", attachment_type=allure.attachment_type.PNG)
        if html_path.exists():
            allure.attach.file(str(html_path), name="page-source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
