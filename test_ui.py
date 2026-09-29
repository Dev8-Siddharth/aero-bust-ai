import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 920})
        page.goto("http://127.0.0.1:8000", wait_until="load")
        time.sleep(2)

        # Switch to Day 3
        day3_btn = page.locator("button.day-pill[data-day='3']")
        day3_btn.click()
        time.sleep(1)

        # Click the first alert zone
        page.locator("#alerts-list > div").first.click()
        time.sleep(2)

        # Verify inspector is visible
        inspector = page.locator("#region-inspector-card")
        assert inspector.is_visible(), "Region inspector should be visible"

        page.screenshot(path="dashboard_interactive_test.png")
        browser.close()
        print("INTERACTIVE TEST SUCCESSFUL: Inspector verified!")

if __name__ == "__main__":
    run_test()
