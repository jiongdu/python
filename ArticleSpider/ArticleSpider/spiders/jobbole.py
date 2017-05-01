# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/111038']

    def parse(self, response):
        selector = response.xpath('//*[@id="post-111038"]/div[1]/h1/text()')
        pass
