# -*- coding: utf-8 -*-
import hashlib
import logging
import logging.config
from datetime import datetime

import scrapy
from requests.utils import urlparse

from eshop.items import Product, ProductLoader
from eshop.data.rules import website_rules


logger = logging.getLogger(__name__)


class LcSpider(scrapy.Spider):
    name = 'lc'

    def __init__(self, urls=None, *args, **kwargs):
        super(LcSpider, self).__init__(*args, **kwargs)
        self.urls = urls

    def start_requests(self):
        # What we want is an item in English and its Chinese translation which
        # could parse in the same way. Two items would go into ItemPineline
        # separately, and we mix two became one by eshop.utils.dealitem.ItemMixer,
        # actually what we need in Chinese website is only the transtion text -
        # title, desc and detail. There is only one rule in both English and Chinese
        # website. `rule` here is the hostname which is the key in `website_rules`.

        for url in self.urls:
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
        print 'Parsing %s' % response.url
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
        pl.add_value('found_date', datetime.strftime(datetime.now(), 'fd%Y%m%d'))

        text_css = website_rules[rule]['text_css']
        for field, css in text_css.items():
            pl.add_css(field, css)

        photo_urls_css = website_rules[rule]['photo_urls_css']
        photo_urls_re = website_rules[rule]['photo_urls_re']
        if photo_urls_re:
            pl.add_css('photo_urls', photo_urls_css, re=photo_urls_re)
        else:
            pl.add_css('photo_urls', photo_urls_css)

        logger.info(pl.load_item())
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
