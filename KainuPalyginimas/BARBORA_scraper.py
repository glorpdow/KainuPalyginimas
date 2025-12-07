from playwright.sync_api import sync_playwright
import time

# Kai išjungi browserio langą po palieidmo, kažkiek veikia. Visų produktų neišscrapina, bet keli yra. Needs work
# Yra yra nėra bus
def scrape_barbora(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # I love head, gimme head
        page = browser.new_page()
        
        url = f"https://barbora.lt/paieska?q={query}"
        page.goto(url, timeout=60000)

        PRODUCT_NAME_LINK_SELECTOR = 'a[href^="/produktai/"]' 

        try:
            page.wait_for_selector(PRODUCT_NAME_LINK_SELECTOR, timeout=30000)
        except Exception:
            print(f"Nu pzdc kzn: {query}")
            browser.close()
            return []

        product_links = page.locator(PRODUCT_NAME_LINK_SELECTOR)
        count = product_links.count()

        results = []

        for i in range(count):
            product_link = product_links.nth(i)
            
            product_card = product_link.locator('xpath=./../../..') 

            try:
                title = product_link.text_content().strip()
            except:
                title = None

            try:
                alt_name = product_card.locator("img").get_attribute("alt")
            except:
                alt_name = None

            price = None
            try:
                price_block = product_card.locator('[aria-label^="kaina:"]')
                aria_label = price_block.get_attribute('aria-label')
                
                price_str = (
                    aria_label.split(',')[0]
                    .replace('kaina:', '')
                    .replace('€', '')
                    .replace(',', '.')
                    .strip()
                )
                price = float(price_str)
            except Exception as e:
                pass

            results.append({
                "title": title,
                "alt_slug": alt_name,
                "price": price,
            })

        browser.close()
        return results


if __name__ == "__main__":
    products = scrape_barbora("pienas")
    import json
    #print(json.dumps(products[:5], indent=4, ensure_ascii=False))
    print(products)
