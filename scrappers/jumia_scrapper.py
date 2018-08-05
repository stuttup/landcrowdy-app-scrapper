from scrappers.base_scrapper import BaseScrapper

scrapper = BaseScrapper(headless=True)

if scrapper.connect_to_website('https://house.jumia.sn/land/buy/'):
    print('Getting buy posts')
    html = scrapper.driver.page_source

    results = scrapper.process_results(html, type='vente')

    #scrapper.save_results_to_file(results, output='annonces_ventes.csv')
    print("saving to database")
    scrapper.save_results_to_database(results)
else:
    print(f'Failed to connect to website')


if scrapper.connect_to_website('https://house.jumia.sn/land/rent/'):
    print('Getting rent posts')
    html = scrapper.driver.page_source

    results = scrapper.process_results(html, type='location')

    #scrapper.save_results_to_file(results, output='annonces_locations.csv')
    print("saving to database")
    scrapper.save_results_to_database(results)
else:
    print(f'Failed to connect to website')





