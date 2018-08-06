#from time import time, sleep
from datetime import datetime, date
import csv
import re

#import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

from scrappers.database import DatabaseSession, ListeMaison, ListeJob, ListeTerrain



class BaseScrapper:
    """Base scrapper object with methods to retrieve and save data

    """

    def __init__(self, browser='firefox', **kwargs):
        """initialise the web driver instance

        :param browser: The web browser used
        :param kwargs:
        """
        options = webdriver.IeOptions() if browser == 'ie' else webdriver.ChromeOptions() if browser == 'chrome' \
            else webdriver.FirefoxOptions()
        # add additional optional arguments
        options_args = []
        if 'headless' in kwargs and kwargs.get('headless'):
            options_args.append('--headless')
        for op in options_args:
            options.add_argument(op)
        self.driver = webdriver.Ie(ie_options=options) if browser == 'ie' else webdriver.Chrome(chrome_options=options)\
            if browser == 'chrome' else webdriver.Firefox(firefox_options=options)

    def connect_to_website(self, website_url):
        """Connects to the website to pull data from

        :param website_url:
        :return: Boolean
        """
        _attempts = 0
        while _attempts < 3:
            try:
                self.driver.get(website_url)
                self.driver.fullscreen_window()
                #self.driver.implicitly_wait(3)
                return True
            except Exception as e:
                _attempts += 1
                print(f'Error while connecting to {website_url}', f'Attempt #{_attempts}', end='\n')
        return False

    def search(self, query='Immobilier', website_url='https://deals.jumia.sn', **kwargs):
        """ Execute custom search on the scrapped website

        :param query: Sting - Terms to search
        :param kwargs:
        :return:
        """
        _connected = self.connect_to_website(website_url)
        try:
            self.driver.find_element_by_class_name('-close_popup').click()
        except Exception as e:
            pass

        self.driver.implicitly_wait(3)

        #_category = self.driver.find_element_by_xpath("//select/option[@value='141']")

        #select_category = Select(self.driver.find_element_by_id('search-category'))
        #self.driver.execute_script("arguments[0].scrollIntoView(true);", _category)

        #select_category.select_by_value("141")
        #self.driver.implicitly_wait(5)
        #search_input = self.driver.find_element_by_id('header-search-input')
        #search_input.send_keys(query)
        #search_btn = self.driver.find_element_by_id('header-search-submit')
        #search_btn.click()

        #self.driver.implicitly_wait(5)

    def get_deals(self, category='appartements-a-vendre', website_url='https://deals.jumia.sn/', **kwargs):
        """ Execute custom search on the scrapped website

        :param category: Sting - Terms to search
        :param kwargs:
        :return:
        """
        _connected = self.connect_to_website(website_url+category)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "nav")))
        try:
            self.driver.find_element_by_class_name('-close_popup').click()
        except Exception as e:
            pass

        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        annonces = soup.find_all('div', class_='post')

        results = []

        for a in annonces:
            results.append(
                {
                    'titre': re.sub(r"[\n\t]*", "", a.find(class_='address').text.split(',')[0]).strip(),
                    'ville': re.sub(r"[\n\t]*", "", a.find(class_='address').text.split(',')[1]).strip(),
                    'description': re.sub(r"[\n\t]*", "", a.find(class_='announcement-infos').a.span.text).strip(),
                    'date': a.find(class_='price-date').time.text,
                    'prix': a.find(class_='price-date').span.text.strip(),
                    #'image': a.find(class_='product-images')['data-src'] or a.find(class_='product-images')['src'],
                    'image': a.img['data-src'] if 'data-src' in a.img.attrs else a.img['src'],
                    'lien': website_url+a.find(class_='announcement-infos').a['href'],
                    'type': 'location' if 'louer' in category else 'vente'
                }
            )

        return results

    def disconnect(self):
        self.driver.quit()

    def process_results(self, html, type='location', **kwargs):
        """Process the downloaded scrapping results.

        :param html:
        :param kwargs:
        :return:
        """
        # Create beautifulsoup object
        soup = BeautifulSoup(html, 'html.parser')

        annonces = soup.find_all('li', class_='highlight-box')

        results = []
        for a in annonces:
            results.append({'title': a.div.h3.text.strip(), 'type': type, 'link': 'https://house.jumia.sn' + a.div.h3.a.get('href'),
                            'address': a.div.p.text, 'price': a.div.find(class_='listing-price').text,
                            'image': a.find(class_='listing-image').img.get('src')})

        return results

    def save_results_to_file(self, input, output='annonces.csv'):
        """

        :param input:
        :return:
        """
        fieldnames = ['type', 'titre', 'description', 'ville', 'prix', 'date', 'lien', 'image']

        with open(output, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'type': 'Type', 'titre': 'Titre', 'description': 'Description', 'ville': 'Ville', 'prix': 'Prix', 'date': 'Date',
                             'lien': 'Lien','image': 'Image'})
            writer.writerows(input)

    def reset_database(self):
        with DatabaseSession() as session:
            print("Removing previous records")
            try:
                session.query(ListeMaison).delete()
                session.commit()
            except:
                session.rollback()

    def save_results_to_database(self, input, **kwargs):
        """

        :param input:
        :param kwargs:
        :return:
        """
        with DatabaseSession() as session:
            print("Inserting new records")
            for i in input:
                m = ListeMaison(titre=i.get('titre', 'Test'), description=i.get('description', 'Test'),
                                image=i.get('image', 'test'), lien= i.get('lien', 'Test'),pays='SN',
                              ville=i.get('ville', ''), quartier=i.get('ville', ''), superficie=50,
                              prix=i.get('prix', 0), chambres=2, type=i.get('type', 'location'), date=datetime.now().date())
                try:
                    session.add(m)
                except Exception as e:
                    print(e)
                    session.rollback()
            session.commit()

            maisons = session.query(ListeMaison).all()

            for m in maisons:
                print(m.titre)

#if __name__ == '__main__':
    #scrapper = BaseScrapper()
    #for cat in ['appartements-a-vendre', 'appartements-a-louer', 'studios-chambres-a-louer', 'maisons-a-vendre',
                #'maisons-a-louer', 'terrains-parcelles', 'locaux-commerciaux-bureaux', 'locaux-industriels',
                #'investissements-immobiliers']:
        #scrapper.save_results_to_file(scrapper.get_deals(category=cat), 'deals.csv')
    #scrapper.disconnect()