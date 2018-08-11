# -*- coding: utf-8 -*-
import re
import scrapy
from selenium import webdriver


class TerrainsSpider(scrapy.Spider):
    name = 'terrains'
    allowed_domains = ['deals.jumia.sn']
    start_urls = [
        'https://deals.jumia.sn/terrains-parcelles',
        'https://deals.jumia.sn/terrains-parcelles?page=2',
        'https://deals.jumia.sn/terrains-parcelles?page=3',
        'https://deals.jumia.sn/terrains-parcelles?page=4',
        'https://deals.jumia.sn/terrains-parcelles?page=5',
        'https://deals.jumia.sn/terrains-parcelles?page=6',
        'https://deals.jumia.sn/terrains-parcelles?page=7',
        'https://deals.jumia.sn/terrains-parcelles?page=8',
        'https://deals.jumia.sn/terrains-parcelles?page=9',
        'https://deals.jumia.sn/terrains-parcelles?page=10',
    ]
    def __init__(self, **kwargs):
        scrapy.Spider.__init__(self, **kwargs)
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')
        self.driver = webdriver.Firefox(firefox_options=options)

    def parse(self, response):
        for href in response.css('div.announcement-infos a::attr(href)'):
            yield response.follow(href, self.parse_annonce)

    def parse_annonce(self, response):
        def extract_with_css(query):
            try:
                r = re.sub(r"[\n\t]*", "", response.css(query).extract_first())
            except:
                r = ''
            return r

        def extract_with_xpath(query):
            try:
                r= re.sub(r"[\n\t]*", "", response.xpath(query).extract_first())
            except:
                r = ''
            return r

        self.driver.get(response.url)

        item = {}
        type_annonce = extract_with_xpath(
            "//div[@class='post-attributes']/div/h3[contains(text(), 'Type de Transaction')]/span/text()")
        try:
            item['titre'] = extract_with_css('h1 span::text').strip()
        except:
            pass
        try:
            item['type'] = type_annonce if len(
                type_annonce) > 0 else 'location' if 'louer' in response.request.url else 'vente'
        except:
            pass
        try:
            item['description'] = extract_with_css('div.post-text-content p::text').strip()
        except:
            pass
        try:
            item['lieu'] = extract_with_xpath(
                "//div[@class='seller-details']/dl/dt[contains(text(), 'Lieu')]/following-sibling::dd[1]/span/text()").strip()
        except:
            pass
        try:
            item['date'] = extract_with_css('div.seller-details dl time::attr(datetime)')
        except:
            pass
        try:
            item['prix'] = extract_with_css('span.price span::text').strip()
        except:
            pass
        try:
            item['superficie'] = extract_with_xpath(
                "//div[@class='post-attributes']/div/h3[contains(text(), 'Superficie')]/span/text()")
        except:
            pass
        try:
            item['statut'] = 'titré'
        except:
            pass
        try:
            item['pays'] = 'SN'
        except:
            pass
        try:
            item['lien'] = response.request.url
        except:
            pass
        try:
            item['image'] = self.driver.find_element_by_css_selector("div.slide.active img").get_attribute('src')
        except:
            pass

        yield item
