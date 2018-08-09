# -*- coding: utf-8 -*-
import re
import scrapy
from selenium import webdriver


class JumiaSpider(scrapy.Spider):
    name = 'jumia'
    allowed_domains = ['deals.jumia.sn']
    _stop_following_links = False
    _items_scrapped = 0
    start_urls = [
        'https://deals.jumia.sn/appartements-a-vendre',
        'https://deals.jumia.sn/appartements-a-vendre?page=2',
        'https://deals.jumia.sn/appartements-a-vendre?page=3',
        'https://deals.jumia.sn/appartements-a-vendre?page=4',
        'https://deals.jumia.sn/appartements-a-vendre?page=5',
        'https://deals.jumia.sn/appartements-a-louer',
        'https://deals.jumia.sn/appartements-a-louer?page=2',
        'https://deals.jumia.sn/appartements-a-louer?page=3',
        'https://deals.jumia.sn/appartements-a-louer?page=4',
        'https://deals.jumia.sn/appartements-a-louer?page=5',
        'https://deals.jumia.sn/appartements-meubles',
        'https://deals.jumia.sn/appartements-meubles?page=2',
        'https://deals.jumia.sn/appartements-meubles?page=3',
        'https://deals.jumia.sn/appartements-meubles?page=4',
        'https://deals.jumia.sn/appartements-meubles?page=5',
        'https://deals.jumia.sn/studios-chambres-a-louer',
        'https://deals.jumia.sn/studios-chambres-a-louer?page=2',
        'https://deals.jumia.sn/studios-chambres-a-louer?page=3',
        'https://deals.jumia.sn/studios-chambres-a-louer?page=4',
        'https://deals.jumia.sn/studios-chambres-a-louer?page=5',
        'https://deals.jumia.sn/maisons-a-vendre'
        'https://deals.jumia.sn/maisons-a-vendre?page=2'
        'https://deals.jumia.sn/maisons-a-vendre?page=3'
        'https://deals.jumia.sn/maisons-a-vendre?page=4'
        'https://deals.jumia.sn/maisons-a-vendre?page=5',
        'https://deals.jumia.sn/maisons-a-louer',
        'https://deals.jumia.sn/maisons-a-louer?page=2'
        'https://deals.jumia.sn/maisons-a-louer?page=3'
        'https://deals.jumia.sn/maisons-a-louer?page=4'
        'https://deals.jumia.sn/maisons-a-louer?page=5'
    ]

    def __init__(self, **kwargs):
        scrapy.Spider.__init__(self, **kwargs)
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(firefox_options=options)

    def parse(self, response):
        for href in response.css('div.announcement-infos a::attr(href)'):
            # image_url = response.xpath("//div[@class='alignleft']/img[@class='product-images']/@src").extract_first()
            # request = response.follow(href, self.parse_annonce)
            # request.meta['image_url'] = image_url
            yield response.follow(href, self.parse_annonce)
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, self.parse)

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
        type_annonce = extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Type de Transaction')]/span/text()")
        item = {}
        try:
            item['titre'] = extract_with_css('h1 span::text').strip()
        except:
            pass
        try:
            item['type'] = type_annonce if len(type_annonce) > 0 else 'location' if 'louer' in response.request.url else 'vente'
        except:
            pass
        try:
            item['description'] = extract_with_css('div.post-text-content p::text').strip()
        except:
            pass
        try:
            item['lieu'] = extract_with_xpath("//div[@class='seller-details']/dl/dt[contains(text(), 'Lieu')]/following-sibling::dd[1]/span/text()").strip()
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
            item['chambres'] =  extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Nombre de pièces')]/span/text()")
        except:
            pass
        try:
            item['superficie'] = extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Superficie')]/span/text()")
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
            item['image'] = self.driver.find_element_by_xpath("//div[@class='slider active']/img").get_attribute('src')
        except:
            pass

        yield item
