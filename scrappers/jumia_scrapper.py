from scrappers.base_scrapper import BaseScrapper

buy_scrapper = BaseScrapper(headless=True)

if buy_scrapper.connect_to_website('https://house.jumia.sn/land/buy/'):
    html = buy_scrapper.driver.page_source

    results = buy_scrapper.process_results(html, type='buy')

    buy_scrapper.save_results(results, output='annonces_ventes.csv')

rent_scrapper = BaseScrapper(headless=True)

if rent_scrapper.connect_to_website('https://house.jumia.sn/land/rent/'):
    html = rent_scrapper.driver.page_source

    results = rent_scrapper.process_results(html, type='rent')

    rent_scrapper.save_results(results, output='annonces_locations.csv')

