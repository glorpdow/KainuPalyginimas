from playwright.sync_api import sync_playwright
import time

def scrape_iki(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headed mode
        page = browser.new_page()
        
        url = f"https://iki.lt/?s={query}"
        page.goto(url, timeout=60000)

        # Wait until at least one product card appears
        page.wait_for_selector(".akcijoskortele", timeout=60000)

        products = page.locator(".akcijoskortele")
        count = products.count()

        results = []

        for i in range(count):
            product = products.nth(i)

            # Extract product title
            try:
                title = product.locator(".akcija_title").text_content().strip()
            except:
                title = None

            # Extract alt attribute (clean product slug)
            try:
                alt_name = product.locator("img.card-img-top").get_attribute("alt")
            except:
                alt_name = None

            # Extract current price
            try:
                price_int = product.locator(".price_block_wrapper .price_int").nth(0).text_content().strip()
                price_cents = product.locator(".price_block_wrapper .price_cents span.sub").nth(0).text_content().strip()
                price = float(f"{price_int}.{price_cents}")
            except:
                price = None

            # Extract old price (optional)
            try:
                old_int = product.locator(".price_old_block .price_int").text_content().strip()
                old_cents = product.locator(".price_old_block .price_cents").text_content().strip()
                old_price = float(f"{old_int}.{old_cents}")
            except:
                old_price = None

            results.append({
                "title": title,
                "alt_slug": alt_name,
                "price": price,
                "old_price": old_price
            })

        browser.close()
        return results


if __name__ == "__main__":
    print(scrape_iki("pienas"))
