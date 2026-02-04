"""
Sync API Example - Chạy TUẦN TỰ 3 users

Chạy file này: pytest tests/e2e/test_sync.py -s
"""

import time
from playwright.sync_api import sync_playwright, expect


def test_sync_sequential_login():
    """
    Sync API - Chạy 3 logins TUẦN TỰ
    
    Demo: Sync chạy từng cái một → Chậm hơn Async
    """
    print("="*60)
    print("SYNC API - SEQUENTIAL OPERATIONS DEMO")
    print("="*60)
    
    def login_and_check(email, name):
        """Login và verify cho 1 user"""
        start = time.time()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Login
            page.goto("https://demo.thingsboard.io/login")
            page.get_by_label("Email").fill(email)
            page.get_by_label("Password").fill("Tuilasieunhan@")
            page.get_by_role("button", name="Sign in").click()
            
            # Verify
            page.wait_for_url("https://demo.thingsboard.io/home", timeout=10000)
            expect(page).to_have_title("ThingsBoard Demo | Home")
            
            browser.close()
        
        elapsed = time.time() - start
        return f"✓ {name} - {elapsed:.2f}s"
    
    print("\n🐌 Chạy 3 logins TUẦN TỰ (từng cái một)...")
    start_total = time.time()
    
    # Chạy 3 logins TUẦN TỰ
    results = []
    results.append(login_and_check("hi.newagenewera@gmail.com", "User 1"))
    results.append(login_and_check("hi.newagenewera@gmail.com", "User 2"))
    results.append(login_and_check("hi.newagenewera@gmail.com", "User 3"))
    
    total = time.time() - start_total
    
    print("\n📊 RESULTS:")
    for result in results:
        print(f"  {result}")
    
    print(f"\n⏱️  Total time: {total:.2f}s")
    print(f"💡 Nếu dùng Async (concurrent): ~{total / 3:.2f}s")
    print(f"😢 Sync chạy tuần tự nên CHẬM HƠN ~3x!")
    print("="*60)