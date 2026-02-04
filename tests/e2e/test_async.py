"""
Async API Example - Chạy đơn giản với 1 function

Chạy file này: python tests/e2e/test_async_simple.py
"""

import asyncio
import time
from playwright.async_api import async_playwright, expect


async def test_async_concurrent_login():
    """
    Async API - Chạy 3 logins ĐỒNG THỜI
    
    Demo ưu điểm của Async khi chạy nhiều operations cùng lúc
    """
    print("="*60)
    print("ASYNC API - CONCURRENT OPERATIONS DEMO")
    print("="*60)
    
    async def login_and_check(email, name):
        """Login và verify cho 1 user"""
        start = time.time()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            # Login
            await page.goto("https://demo.thingsboard.io/login")
            await page.get_by_label("Email").fill(email)
            await page.get_by_label("Password").fill("Tuilasieunhan@")
            await page.get_by_role("button", name="Sign in").click()
            
            # Verify
            await page.wait_for_url("https://demo.thingsboard.io/home", timeout=10000)
            await expect(page).to_have_title("ThingsBoard Demo | Home")
            
            await browser.close()
        
        elapsed = time.time() - start
        return f"✓ {name} - {elapsed:.2f}s"
    
    print("\n🚀 Chạy 3 logins ĐỒNG THỜI với asyncio.gather()...")
    start_total = time.time()
    
    # Chạy 3 logins cùng lúc
    results = await asyncio.gather(
        login_and_check("hi.newagenewera@gmail.com", "User 1"),
        login_and_check("hi.newagenewera@gmail.com", "User 2"),
        login_and_check("hi.newagenewera@gmail.com", "User 3"),
    )
    
    total = time.time() - start_total
    
    print("\n📊 RESULTS:")
    for result in results:
        print(f"  {result}")
    
    print(f"\n⏱️  Total time: {total:.2f}s")
    print(f"💡 Nếu dùng Sync (tuần tự): ~{total * 3:.2f}s")
    print(f"🎉 Async nhanh hơn ~3x!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_async_concurrent_login())
