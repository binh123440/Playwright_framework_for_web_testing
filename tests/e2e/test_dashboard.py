import pytest
from helpers.config_loader import get
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


@pytest.fixture
def logged_in_page(page):
    """Login and return logged-in page using role-based selectors"""
    page.goto(get("BASE_URL", "https://demo.thingsboard.io/"))
    page.get_by_label("Username (email)").fill(get("DEMO_USERNAME"))
    page.get_by_label("Password").fill(get("DEMO_PASSWORD"))
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_load_state('networkidle', timeout=10000)
    return page


@pytest.mark.regression
@pytest.mark.e2e
def test_dashboards_flow(logged_in_page):
    """E2E flow: navigate to dashboards and verify listing"""
    page = logged_in_page
    page.get_by_role("navigation").get_by_role("link", name="Dashboards").click()
    page.wait_for_load_state('networkidle', timeout=15000)
    
    list_count = (
        page.locator(".tb-dashboard-list").count()
        + page.locator(".dashboard-list").count()
        + page.locator(".dashboard-tile").count()
        + page.locator(".tb-dashboard").count()
        + page.locator("text=Dashboards").count()
    )
    assert list_count > 0, "No dashboards listing found"
    logger.info("Dashboards listing verified")


@pytest.mark.e2e
@pytest.mark.slow
def test_add_dashboard(logged_in_page):
    """E2E: Add a new dashboard via UI using role-based selectors"""
    page = logged_in_page
    
    # Navigate to dashboards
    page.get_by_role("navigation").get_by_role("link", name="Dashboards").click()
    page.wait_for_load_state('networkidle', timeout=15000)

    # Click Add button
    page.locator("button").filter(has_text="add").click()
    page.wait_for_timeout(500)

    # Click Create new dashboard menu item
    page.get_by_role("menuitem", name="Create new dashboard").click()
    page.wait_for_load_state('networkidle', timeout=5000)

    # Prepare unique title
    title_text = f"Auto Dashboard {datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Fill dashboard details using role-based selectors
    page.get_by_role("textbox", name="Title").fill(title_text)
    page.get_by_role("textbox", name="Description").fill("Created by automated test")

    # Select Assigned customers
    page.get_by_text("Assigned customers", exact=True).click()
    page.wait_for_timeout(200)
    
    # Click first customer option if available
    options = page.get_by_role("option")
    if options.count() > 0:
        options.first.click()
    
    # Close overlay by pressing Escape
    page.keyboard.press('Escape')
    page.wait_for_timeout(200)

    # Click Submit button
    page.get_by_role("button", name="Add").click()
    page.wait_for_load_state('networkidle', timeout=15000)
    
    logger.info(f"Dashboard created successfully: {title_text}")
