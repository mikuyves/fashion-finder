# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, Join, TakeFirst

class Product(scrapy.Item):
    rule = scrapy.Field()
    pid = scrapy.Field()
    lang = scrapy.Field()

    url = scrapy.Field()
    url_status = scrapy.Field()
    website = scrapy.Field()

    brand = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    detail = scrapy.Field()

    photo_urls = scrapy.Field()

    last_update = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    brand_in = MapCompose(unicode.strip, unicode.upper)
    title_in = MapCompose(unicode.strip, unicode.title)
    desc_in = MapCompose(unicode.strip)
    detail_out = Identity()
    photo_urls_out = Identity()
