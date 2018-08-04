from time import time, sleep
from datetime import datetime
import csv

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


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
                self.driver.implicitly_wait(10)
                return True
            except Exception as e:
                _attempts += 1
                print(f'Error while connecting to {website_url}', f'Attempt #{_attempts}', end='\n')
        return False

    def search(self, query='Terrain', website_url='https://www.jumia.sn/', **kwargs):
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

        search_input = self.driver.find_element_by_id('header-search-input')
        search_input.send_keys(query)
        search_btn = self.driver.find_element_by_id('header-search-submit')
        search_btn.click()

        self.driver.implicitly_wait(5)

    def process_results(self, html, type='rent', **kwargs):
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

    def save_results(self, input, output='annonces.csv'):
        """

        :param input:
        :return:
        """
        fieldnames = ['title', 'type', 'address', 'price', 'link', 'image']

        with open(output, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'title': 'Title', 'type': 'Type', 'address': 'Address', 'price': 'Price', 'link': 'Link',
                             'image': 'Image'})
            writer.writerows(input)
            #for row in input:
                #writer.writerow(row)






if __name__ == '__main__':
    scrapper = BaseScrapper(headless=True)
    if scrapper.connect_to_website('https://house.jumia.sn/land/buy/'):
        html = scrapper.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        results = scrapper.process_results(html, type='buy')

        scrapper.save_results(results, output='annonces_ventes.csv')


