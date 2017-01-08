# -*- coding: utf-8 -*-
import re
import hashlib

import scrapy
from requests.utils import urlparse

from eshop.items import Product, ProductLoader


# Notice: `en2zh` is a function which change the English website to Chinese.
website_rules = {
    'www.lanecrawford.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com.cn', x),
        'css_rules': {
            'brand': '.lc-product-brand-refresh::text',
            'title': '.lc-product-short-description-refresh::text',
            'desc': '.text-paragraph::text',
            'detail': '.sizeAndFit li::text',
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
        # in Chinese website is only the transtion text - title, desc and detail.
        # There is only one rule in both English and Chinese website. `rule`
        # here is the hostname which is the key in `website_rules`.

        url = raw_input('Enter the URL: ')
        rule = urlparse(url).hostname
        pid = self.get_pid(url)

        # Request English website.
        yield scrapy.Request(url, self.parse, meta={'rule': rule, 'lang': 'en-US', 'pid': pid})

        # Request Chinese website if it could.
        if website_rules[rule]['has_zh_maybe']:
            url = self.get_url_zh(rule, url)
            yield scrapy.Request(url, self.parse, meta={'rule': rule, 'lang': 'zh-CN', 'pid': pid})

    def parse(self, response):
        # Parse single item no matter which language.
        pl = ProductLoader(item=Product(), response=response)

        # The value of `lang` is the only difference in parsing.
        rule = response.meta['rule']
        lang = response.meta['lang']
        pid = response.meta['pid']

        pl.add_value('rule', rule)
        pl.add_value('lang', lang)
        pl.add_value('pid', pid)

        # `url_status` is a way to know if there is a Chinese version website.
        pl.add_value('url', response.url)
        pl.add_value('url_status', response.status)
        pl.add_value('website', urlparse(response.url).hostname)

        css_rules = website_rules[rule]['css_rules']
        for field, css in css_rules.items():
            pl.add_css(field, css)

        return pl.load_item()

    def get_pid(self, url):
        return hashlib.md5(url.encode('utf8')).hexdigest()

    def get_url_zh(self, rule, url):
        # Change the English url to Chinese one by 'en2zh' function.
        for r in website_rules:
            if rule == r:
                return website_rules[rule]['en2zh'](url)

    def parse_other_color(self, response):
        # Some pages has more than one color so that we should make another request.
        # TODO: But in lanecrawford.com, other colors are applied by JSON. Make a
        # way to deal with JSON.
        pass
