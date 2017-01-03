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
    title_ch = scrapy.Field()
    desc = scrapy.Field()
    desc_ch = scrapy.Field()
    details = scrapy.Field()
    details_ch = scrapy.Field()

    photo_urls = scrapy.Field()
    sreenshot_filename = scrapy.Field()

    last_update = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    brand_in = MapCompose(unicode.strip, unicode.upper)

    title_in = MapCompose(unicode.strip, unicode.title)
    title_ch_in = MapCompose(unicode.strip, unicode.title)

    desc_in = MapCompose(unicode.strip)
    desc_ch_in = MapCompose(unicode.strip)

    details_out = Identity()
    details_ch_out = Identity()

    photo_urls_out = Identity()
