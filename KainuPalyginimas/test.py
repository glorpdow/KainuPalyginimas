from Scraper import scrape_all_stores

print("begin")

results = scrape_all_stores("pienas")  # "milk"

for r in results:
    print(r)
