# -*- coding: utf-8 -*-
import re

import scrapy
from requests.utils import urlparse

from eshop.items import Product, ProductLoader


# Notice: `en2zh` is a function which change the English website to Chinese.
website_rules = {
    'www.lanecrawford.com': {
        'en2zh': lambda x: re.sub(r'.com', '.com.cn', x),
        'css_rules': {
            'brand': '.lc-product-brand-refresh::text',
            'title': '.lc-product-short-description-refresh::text',
            'desc': '.text-paragraph::text',
            'details': '.sizeAndFit li::text',
            'photo_urls': '.hero-carousel__img::attr(data-xl)',
        }
    },
}


class LcSpider(scrapy.Spider):
    name = 'lc'

    def start_requests(self):
        # What we want is an item in English and the Chinese translation which
        # could parse in the same way. Two items would go into ItemPineline
        # separately if we start request with two website, because only sigle
        # item can be accepted, it difficult to combine two items together,
        # especially parsing a ton of urls later. So we try to we start request
        # the English website and then get the Chinese one and combine two
        # languges websites' data together into one item, actually what we need
        # in Chinese website is only the transtion text - title, desc and details.
        # There is only one rule in both English and Chinese website. `rule`
        # here is the hostname which is the key in `website_rules`.

        url = raw_input('Enter the URL: ')
        hostname = urlparse(url).hostname

        yield scrapy.Request(
            url, self.parse, meta={'rule':hostname, 'lang': 'en-US'}
        )

    def parse(self, response):
        # Parse two items, here is the English one.
        item_en = self.parse_item(response)

        # Change the languge to Chinese and parse the Chinese item.
        meta = response.meta
        meta['lang'] = 'zh-CN'
        item_zh = self.parse_item_zh(response.url, meta)

        return item_zh, item_en

    def get_url_zh(self, rule, url):
        # Change the English url to Chinese one by 'en2zh' function.
        for r in website_rules:
            if rule == r:
                return website_rules[rule]['en2zh'](url)

    def parse_item(self, response):
        # Parse single item no matter which language.
        pldr = ProductLoader(item=Product(), response=response)

        # The value of `lang` is the only difference in parsing.
        lang = response.meta['lang']
        pldr.add_value('lang', lang)

        # `url_status` is a way to know if there is a Chinese version website.
        pldr.add_value('url', response.url)
        pldr.add_value('url_status', response.status)
        pldr.add_value('website', urlparse(response.url).hostname)

        rule = response.meta['rule']
        pldr.add_value('rule', rule)
        css_rules = website_rules[rule]['css_rules']
        for field, css in css_rules.items():
            pldr.add_css(field, css)

        return pldr.load_item()

    def parse_item_zh(self, url, meta):
        # Notice: only `callback` in Request can generate a Response object the
        # next function. if we assign it to a varible, that is only a Rquest object.
        return scrapy.Request(
            self.get_url_zh(meta['rule'], url),
            self.parse_item,
            meta=meta,
        )

    def parse_other_color(self, response):
        # Some pages has more than one color so that we should make another request.
        # TODO: But in lanecrawford.com, other colors are applied by JSON. Make a
        # way to deal with JSON.
        pass
