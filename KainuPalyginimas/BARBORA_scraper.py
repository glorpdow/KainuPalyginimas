from playwright.sync_api import sync_playwright
import time

def scrape_barbora(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        url = f"https://barbora.lt/paieska?q={query}"
        page.goto(url, timeout=60000)
        
        products = page.wait_for_selector(".product-card-next", timeout=2000)
        
        products = page.locator(".product-card-next")
        count = products.count()
        
        results = []
        
        for i in range(count):
            print(f"#fti-product-title-category-page-{i}")
            product_card = products.nth(i)
            #product = page.locator(f"#fti-product-title-category-page-{i}")
            
            # dats da title
            try:
                #title = product.inner_html()
                title = page.locator(f"#fti-product-title-category-page-{i}").inner_html()
            except:
                title = None
            
            # money, money, money
            try:
                #title = product.inner_html()
                #price = page.locator('div[aria-label^="kaina:"]').get_attribute("aria-label")
                #price = page.locator(f"#fti-product-card-category-page-{i} [aria-label^='kaina: ']").get_attribute("aria-label")
                price_element = product_card.locator('meta[itemprop="price"]')
                price = price_element.get_attribute("content")
                ### Veikia bet žiauriai žiauriai lėtai
            except:
                price = None
            # I'm going to fucking kill myself
            
            #Reik?, nereik? Bus matyt ig
            '''
            try:
                #title = product.inner_html()
                #imagelink = page.locator(".w-full").text_content().strip()
                imagelink = None
            except:
                imagelink = None
            '''  
            
            results.append({
                "i: " : i,
                "title": title,
                "price" : price
            })

        browser.close()
        return results
    
if __name__ == "__main__":
    products = scrape_barbora("duona")
    print(*products, sep='\n')
