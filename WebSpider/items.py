# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinanceSinaItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()
    url_link = scrapy.Field()
    description = scrapy.Field()
    pass


class EastMoneyItem(FinanceSinaItem):
    pass

