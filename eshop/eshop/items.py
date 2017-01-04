# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, Join, TakeFirst

class Product(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()

    brand = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    details = scrapy.Field()

    photo_urls = scrapy.Field()
    sreenshot_filename = scrapy.Field()

    has_cn = scrapy.Field()
    title_cn = scrapy.Field()
    desc_cn = scrapy.Field()
    details_cn = scrapy.Field()

    last_update = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    brand_in = MapCompose(unicode.strip, unicode.upper)
    title_in = MapCompose(unicode.strip, unicode.title)
    desc_in = MapCompose(unicode.strip)
    details_out = Identity()
    photo_urls_out = Identity()

    title_cn_in = MapCompose(unicode.strip)
    desc_cn_in = MapCompose(unicode.strip)
    details_cn_out = Identity()
