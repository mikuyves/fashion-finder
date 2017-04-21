# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, Join, TakeFirst


def remove_slash(x):
    # Slash will make an 'No such file or directory' error.
    return x.replace('/', ' ')


def handle_nobrand(x):
    # Handle no brand item.
    if not x:
        return 'NO BRAND'
    else:
        return x


def handle_notitle(x):
    # Handle no title item.
    if not x:
        return 'No Title'
    else:
        return x


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
    details = scrapy.Field()

    photo_urls = scrapy.Field()

    found_date = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    brand_in = MapCompose(
        unicode.strip, unicode.upper, remove_slash, handle_nobrand
        )
    title_in = MapCompose(
        unicode.strip, unicode.title, remove_slash, handle_notitle
        )
    desc_in = MapCompose(unicode.strip)
    desc_out = Join('\n')
    details_in = MapCompose(unicode.strip)
    details_out = Identity()
    photo_urls_out = Identity()
