from jumia.base_scrapper import BaseScrapper

scrapper = BaseScrapper(headless=True)

categories = ['appartements-a-vendre', 'appartements-a-louer', 'studios-chambres-a-louer', 'maisons-a-vendre',
                'maisons-a-louer', 'terrains-parcelles', 'locaux-commerciaux-bureaux', 'locaux-industriels',
                'investissements-immobiliers']

scrapper.reset_database()

for cat in categories:
    scrapper.save_results_to_database(scrapper.get_deals(category=cat))
scrapper.disconnect()