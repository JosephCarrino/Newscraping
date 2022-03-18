#!/usr/bin/env python

import scrapy


class AbcgetSpider(scrapy.Spider):
    name = 'abcGet'
    allowed_domains = ['www.abc.es']
    start_urls = ['http://www.abc.es/']

    def parse(self, response):
        pass
