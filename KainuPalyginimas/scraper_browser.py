from playwright.sync_api import sync_playwright


def scrape_with_browser(url, wait_selector):
    """
    Opens a real browser, loads the page,
    waits for specific HTML to appear,
    and returns the final HTML.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, timeout=30000)
        page.wait_for_selector(wait_selector, timeout=30000)

        html = page.content()
        browser.close()
        return html
