from bs4 import BeautifulSoup
from scraper_browser import scrape_with_browser


def scrape_barbora(product_name: str):
    query = product_name.replace(" ", "+")
    url = f"https://barbora.lt/paieska?q={query}"

    html = scrape_with_browser(url, ".b-product--wrap")

    soup = BeautifulSoup(html, "html.parser")

    items = soup.select(".b-product--wrap")
    results = []

    for item in items:
        title = item.select_one(".b-product-title")
        price_tag = item.select_one(".b-product-price-current")

        if not title or not price_tag:
            continue

        name = title.get_text(strip=True)
        price_text = price_tag.get_text(strip=True)

        # Price format example: "1,49 €"
        price = float(price_text.replace("€", "").replace(",", ".").strip())

        link = item.select_one("a")
        product_url = "https://barbora.lt" + link["href"] if link else None

        results.append({
            "store": "Barbora",
            "name": name,
            "price": price,
            "url": product_url
        })

    return results
