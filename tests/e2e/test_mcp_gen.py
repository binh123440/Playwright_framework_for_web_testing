import time
from playwright.sync_api import expect
from pages.login_page import LoginPage
from helpers.config_loader import get


def test_export_swimming_pool_dashboard(page):
    """
    Test export functionality for Swimming pool scada system dashboard
    """
    # Navigate to login page
    url = get("BASE_URL", "https://demo.thingsboard.io/login")
    page.goto(url)
    
    # Login
    login = LoginPage(page)
    login.login("hi.newagenewera@gmail.com", "Tuilasieunhan@")
    
    # Wait for navigation to complete after login
    page.wait_for_url("https://demo.thingsboard.io/home", timeout=10000)
    
    # Wait for home page to load
    page.wait_for_timeout(2000)
    
    # Navigate to Dashboards page - use main navigation link
    page.get_by_role("navigation").get_by_role("link", name="Dashboards").click()
    page.wait_for_timeout(2000)
    
    # Verify we're on dashboards page
    expect(page).to_have_url("https://demo.thingsboard.io/dashboards")
    
    # Click on Swimming pool scada system dashboard
    page.get_by_role("row", name="Swimming pool scada system").click()
    page.wait_for_timeout(3000)
    
    # Verify dashboard is loaded
    expect(page).to_have_title("ThingsBoard Demo | Dashboard")
    expect(page.locator("h1")).to_contain_text("Swimming pool scada system")
    
    # Wait a bit for dashboard to fully load
    page.wait_for_timeout(2000)
    
    # Click the download/export button to open the menu
    page.locator("button").filter(has_text="file_download").click()
    page.wait_for_timeout(1000)
    
    # Wait for export dialog heading to appear
    page.wait_for_selector("h2:has-text('Export dashboard')", state="visible")
    
    # Setup download listener before clicking export button in dialog
    with page.expect_download(timeout=30000) as download_info:
        # Click "Export" button in the export dialog
        page.get_by_role("button", name="Export", exact=True).click()
    
    download = download_info.value
    
    # Verify download was successful
    assert download is not None, "Download should have started"
    
    # Get the suggested filename
    suggested_filename = download.suggested_filename
    print(f"\nDownloaded file: {suggested_filename}")
    
    # Save the downloaded file
    download_path = f"./downloads/{suggested_filename}"
    download.save_as(download_path)
    
    print(f"Dashboard exported successfully to: {download_path}")
    
    # Optional: Verify the file exists
    import os
    assert os.path.exists(download_path), f"Downloaded file should exist at {download_path}"
