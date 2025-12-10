from playwright.sync_api import sync_playwright
import time

def scrape_iki(query,allpages=True):
    all_results_iki = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page_number = 1

        while True:
            # Select correct URL format
            if page_number == 1:
                url = f"https://iki.lt/?s={query}"
            else:
                url = f"https://iki.lt/page/{page_number}/?s={query}"

            print(f"Scraping: page {page_number} → {url}")
            
            page.goto(url, timeout=60000)

            # Try finding products on the page
            try:
                page.wait_for_selector(".akcijoskortele", timeout=15000)
            except:
                print("No products found — stopping.")
                break  # No more pages

            products = page.locator(".akcijoskortele")
            count = products.count()

            # If no products → finished
            if count == 0:
                print("No more products — finished pagination.")
                break

            # Process this page
            for i in range(count):
                product = products.nth(i)

                try:
                    title = product.locator(".akcija_title").text_content().strip()
                except:
                    title = None

                try:
                    alt_name = product.locator("img.card-img-top").get_attribute("alt")
                except:
                    alt_name = None

                try:
                    price_int = product.locator(".price_block_wrapper .price_int").nth(0).text_content().strip()
                    price_cents = product.locator(".price_block_wrapper .price_cents span.sub").nth(0).text_content().strip()
                    price = float(f"{price_int}.{price_cents}")
                except:
                    price = None

                try:
                    old_int = product.locator(".price_old_block .price_int").text_content().strip()
                    old_cents = product.locator(".price_old_block .price_cents").text_content().strip()
                    old_price = float(f"{old_int}.{old_cents}")
                except:
                    old_price = None

                all_results_iki.append({
                    "title": title,
                    "alt_slug": alt_name,
                    "price": price,
                    "old_price": old_price
                })

            if allpages == True:
                page_number += 1
            else:
                break

        browser.close()

    return all_results_iki


if __name__ == "__main__":
    data = scrape_iki("pienas")
    print(f"Scraped {len(data)} products total.")
    print(data)

