from playwright.sync_api import sync_playwright
import time

def scrape_barbora(query):
    with sync_playwright() as p:
        REAL_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        results = []
        pages = 3

        for i in range(pages):
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            url = f"https://barbora.lt/paieska?q={query}&page={i+1}"
            page.goto(url, timeout=20000)
            page.set_default_timeout(10)

            products = page.wait_for_selector(".product-card-next", timeout=20000)
            
            products = page.locator(".product-card-next")
            count = products.count()

            for j in range(count):
                print(f"#fti-product-title-category-page-{j}")
                product_card = products.nth(j)
                #product = page.locator(f"#fti-product-title-category-page-{i}")
        
                try:    
                    title = product_card.locator(f"#fti-product-title-category-page-{j}").inner_html()
                    
                except:
                    title = None

                try:
                    #title = product.inner_html()
                    imagelink = product_card.locator("img").get_attribute("src")
                except:
                    imagelink = None


                try:
                    price_element = product_card.locator('meta[itemprop="price"]')
                    price = price_element.get_attribute("content")
                except:
                    price = None
                
                
                  
                
                results.append({
                    "title": title,
                    "price" : price,
                    "image" : imagelink,
                    "shop" : "barbora"
                })

            browser.close()
        return results
    
if __name__ == "__main__":
    products = scrape_barbora("duona", 3)
    print(*products, sep='\n')
