# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()

    brand = scrapy.Field()
    title = scrapy.Field()
    title_ch = scrapy.Field()
    desc = scrapy.Field()
    desc_ch = scrapy.Field()
    details = scrapy.Field()
    details_ch = scrapy.Field()

    photo_urls = scrapy.Field()
    sreenshot_filename = scrapy.Field()

    last_update = scrapy.Field()
