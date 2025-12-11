from playwright.sync_api import sync_playwright

def cleaning(x):
    if not x:
        return None
    return x.replace("\n", "").replace("\t", "").replace(">$","").strip()

def getprice():
    price_int = cleaning(reading(".price_block_wrapper .price_int"))
    price_cents = cleaning(reading(".price_block_wrapper .price_cents span.sub"))

    if not price_int or not price_cents:
        return None

    return f"{price_int}.{price_cents}"

def reading(card):
    try:
        return product.locator(card).first.text_content(timeout=250)
    except:
        return None

def getimage():
    jpg=product.locator("img.card-img-top").first.get_attribute("src")
    
    if not jpg:
        return None

    return jpg

def getdeal():
    try:
        return cleaning(product.locator(".nplusn_tag .main").text_content(timeout=50))
    except:
        return None

def scrape_iki(query, allpages=True):
    all_results_iki = []

    global product
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_number = 1

        while True:
            if page_number == 1:
                url = f"https://iki.lt/?s={query}"
            else:
                url = f"https://iki.lt/page/{page_number}/?s={query}"

            print(f"Scrapinama: puslapis {page_number} --> {url}")
            
            page.goto(url, timeout=15000)

            try:
                page.wait_for_selector(".akcijoskortele", timeout=3000)
            except:
                print("Produktų nerasta.")
                break

            products = page.locator(".akcijoskortele")
            count = products.count()

            for i in range(count):
                print(f"Produktas {i+1}")

                product = products.nth(i)

                title = cleaning(reading(".akcija_title"))
                price = getprice()
                image=getimage()
                deal=getdeal()

                all_results_iki.append({
                    "title": title,
                    "price": price,
                    "image": image,
                    "deal": deal,
                    "shop": "iki"
                })

            if allpages:
                page_number += 1
            else:
                break

        browser.close()

    return all_results_iki

if __name__ == "__main__":
    data = scrape_iki("pienas")
    print(f"Scraped {len(data)} products total.")
    print(data)
