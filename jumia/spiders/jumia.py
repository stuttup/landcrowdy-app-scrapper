# -*- coding: utf-8 -*-
import re
import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'jumia'
    allowed_domains = ['deals.jumia.sn']
    start_urls = [
        'https://deals.jumia.sn/appartements-a-vendre?',
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
        'https://deals.jumia.sn/maisons-a-vendre?page=5'
    ]

    def parse(self, response):
        for href in response.css('div.announcement-infos a::attr(href)'):
            yield response.follow(href, self.parse_annonce)

        for ref in response.css('li.next a::attr(href)'):
            yield response.follow(ref, self.parse())

    def parse_annonce(self, response):
        def extract_with_css(query):
            return re.sub(r"[\n\t]*", "", response.css(query).extract_first())

        yield {
            'titre': extract_with_css('h1 span::text').strip(),
            'description': extract_with_css('div.post-text-content p::text').strip(),
            'lieu': extract_with_css('div.seller-details dl dd span::text').strip(),
            'date': extract_with_css('div.seller-details dl time::attr(datetime)'),
            'prix': extract_with_css('span.price span::text').strip(),
            'image': extract_with_css('div.slide img::attr(src)'),
            'link': response.request.url,
            'superficie': extract_with_css('div.post-attributes div:nth-of-type(1) h3:nth-of-type(2) span::text'),
            'chambres': extract_with_css('div.post-attributes div:nth-of-type(1) h3:nth-of-type(1) span::text'),
            'type': 'location' if 'louer' in response.request.url else 'vente',
            'pays': 'SN'
        }
