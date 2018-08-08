# -*- coding: utf-8 -*-
import re
import scrapy


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

    def parse(self, response):
        for href in response.css('div.announcement-infos a::attr(href)'):
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

        type_annonce = extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Type de Transaction')]/span/text()")
        yield {
            'titre': extract_with_css('h1 span::text').strip(),
            'description': extract_with_css('div.post-text-content p::text').strip(),
            'lieu': extract_with_xpath("//div[@class='seller-details']/dl/dt[contains(text(), 'Lieu')]/following-sibling::dd[1]/span/text()").strip(),
            'date': extract_with_css('div.seller-details dl time::attr(datetime)'),
            'prix': extract_with_css('span.price span::text').strip(),
            'image': 'https://deals.jumia.sn' + extract_with_xpath("//img[@itemprop='image']/@src"),
            'lien': response.request.url,
            'superficie': extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Superficie')]/span/text()"),
            'chambres': extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Nombre de pièces')]/span/text()"),
            'type': type_annonce if len(type_annonce) > 0 else 'location' if 'louer' in response.request.url else 'vente',
            'pays': 'SN'
        }
