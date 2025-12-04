from IKI_scraper import scrape_iki
from BARBORA_scraper import scrape_barbora


def scrape_all_stores(product_name: str):
    """
    Runs all scrapers and returns one big result list.
    """
    results = []

    try:
        results.extend(scrape_iki(product_name))
    except Exception as e:
        print("IKI failed:", e)

    try:
        results.extend(scrape_barbora(product_name))
    except Exception as e:
        print("Barbora failed:", e)

    return results
