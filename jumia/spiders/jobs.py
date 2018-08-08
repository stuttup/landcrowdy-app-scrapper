# -*- coding: utf-8 -*-
import re
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['deals.jumia.sn']
    start_urls = [
        'https://deals.jumia.sn/offres-emploi',
        'https://deals.jumia.sn/offres-emploi?page=2',
        'https://deals.jumia.sn/offres-emploi?page=3',
        'https://deals.jumia.sn/offres-emploi?page=4',
        'https://deals.jumia.sn/offres-emploi?page=5',
        'https://deals.jumia.sn/offres-emploi?page=6',
        'https://deals.jumia.sn/offres-emploi?page=7',
        'https://deals.jumia.sn/offres-emploi?page=8',
        'https://deals.jumia.sn/offres-emploi?page=9',
        'https://deals.jumia.sn/offres-emploi?page=10',
    ]

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

        yield {
            'titre': extract_with_css('h1 span::text').strip(),
            'description': extract_with_css('div.post-text-content p::text').strip(),
            'lieu': extract_with_xpath("//div[@class='seller-details']/dl/dt[contains(text(), 'Lieu')]/following-sibling::dd[1]/span/text()").strip(),
            'date': extract_with_css('div.seller-details dl time::attr(datetime)'),
            'salaire': extract_with_css('span.price span::text').strip(),
            'image': 'https://deals.jumia.sn' + extract_with_css('div.slide img::attr(src)'),
            'lien': response.request.url,
            'domaines': extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Secteur d'activité')]/span/text()"),
            'type': extract_with_xpath("//div[@class='post-attributes']/div/h3[contains(text(), 'Type de contrat')]/span/text()"),
            'pays': 'SN'
        }

