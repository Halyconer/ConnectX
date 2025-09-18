from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")

        # Wait for 5 seconds to give the page time to load
        page.wait_for_timeout(5000)

        # Click on a column to make a move
        page.click('.cell[data-col="3"]')

        # Wait for the animation to complete
        page.wait_for_timeout(2000) # Wait for 2 seconds to be safe

        page.screenshot(path="jules-scratch/verification/verification.png")
        browser.close()

run()
