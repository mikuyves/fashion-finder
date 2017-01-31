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
        # title, desc and details. There is only one rule in both English and Chinese
        # website. `rule` here is the hostname which is the key in `website_rules`.

        for url in self.urls:
            rule = website_rules[urlparse(url).hostname]
            pid = self.get_pid(url)

            # Request English website.
            yield scrapy.Request(url, self.parse, meta={'rule': rule, 'lang': 'en-US', 'pid': pid})

            # Request Chinese website if it could.
            if rule['has_zh_maybe']:
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

        pl.add_value('lang', lang)
        pl.add_value('pid', pid)

        # `url_status` is a way to know if there is a Chinese version website.
        pl.add_value('url', response.url)
        pl.add_value('url_status', response.status)
        pl.add_value('website', urlparse(response.url).hostname)
        pl.add_value('found_date', datetime.strftime(datetime.now(), 'fd%Y%m%d'))

        # If it is a brand official webiste, brand has been identified.
        if rule['type'] == 'Official':
            pl.add_value('brand', rule['brand'])
        else:
            pl.add_css('brand', rule['brand'])

        # Get title, description, details for two languages. CSS in some Chinese
        # website is different from English one sometimes, such as: cn.burberry.com.
        if lang == 'zh-CN' and 'text_css_zh' in rule:
            text_css_zh = rule['text_css_zh']
            self.add_text_css(pl, text_css_zh)
        else:
            text_css = rule['text_css']
            self.add_text_css(pl, text_css)

        # Get photo urls.
        photo_urls_css = rule['photo_urls_css']
        # Some urls are in the javascript or JSON data, we need `re`.
        try:
            photo_urls = response.css(photo_urls_css).re(rule['photo_urls_re'])
        except KeyError as e:
            photo_urls = response.css(photo_urls_css).extract()
        # In some cases, we should get a way to calculate the HD photo URLs by
        # small photo URLs which only can be found in the source codes.
        try:
            photo_urls = rule['handle_photo_urls'](photo_urls)
        except KeyError as e:
            pass
        finally:
            # Handle repetition and keep the original order.
            final_photo_urls = list(set(photo_urls))
            final_photo_urls.sort(key=photo_urls.index)
            pl.add_value('photo_urls', final_photo_urls)

        logger.info(pl.load_item())
        return pl.load_item()

    def get_pid(self, url):
        return hashlib.md5(url.encode('utf8')).hexdigest()

    def get_url_zh(self, rule, url):
        # Change the English url to Chinese one by 'en2zh' function.
        return rule['en2zh'](url)

    def add_text_css(self, pl, css_dict):
        for field, css in css_dict.items():
            if css:
                pl.add_css(field, css)
            else:
                # It could be no title, no description or no details.
                pl.add_value(field, u'<NO %s>' % field.upper())

    def parse_other_color(self, response):
        # Some pages has more than one color so that we should make another request.
        # TODO: But in lanecrawford.com, other colors are applied by JSON. Make a
        # way to deal with JSON.
        pass
