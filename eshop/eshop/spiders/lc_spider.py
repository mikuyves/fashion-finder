# -*- coding: utf-8 -*-
import scrapy

from eshop.items import Product, ProductLoader


lc_url = raw_input('Enter the URL: ')


class LcSpider(scrapy.Spider):
    name = 'lc'
    start_urls = [
        lc_url,
    ]

    product_rules = {
        'brand': '.lc-product-brand-refresh::text',
        'title': '.lc-product-short-description-refresh::text',
        'desc': '.text-paragraph::text',
        'details': '.sizeAndFit li::text',
        'photo_urls': '.hero-carousel__img::attr(data-xl)',
    }

    def parse(self, response):
        pldr = ProductLoader(item=Product(), response=response)
        pldr.add_value('url', response.url)
        for field, css in self.product_rules.items():
            pldr.add_css(field, css)

        yield scrapy.Request(
            url=self.get_cn_url(response.url),
            meta={'item': pldr.load_item()},
            callback=self.parse_cn,
        )

    def parse_cn(self, response):
        # Notice: `response=response` is very important! Because this response
        # is different from that response in self.parse(). If we just pass the
        # meta data with `'pldr'=pldr`, the response would remain the same as
        # before, and we don't know how to change the response inside the pldr.
        # So, we can only pass `item` here, and instantiate a pldr to change
        # the response correctly.
        pldr = ProductLoader(item=response.meta['item'], response=response)

        if response.status ==200:
            pldr.add_value('has_cn', True)
        else:
            pldr.add_value('has_cn', False)

        field_cn = ('title', 'desc', 'details')
        for field, css in self.product_rules.items():
            if field in field_cn:

                if pldr.get_value('has_cn'):
                    pldr.add_css(field + '_cn', css)
                else:
                    pldr.add_css(field + '_cn', '')

        return pldr.load_item()

    def get_cn_url(self, url):
        return url.replace('.com', '.com.cn')

    def parse_other_color(self, response):
        # Some pages has more than one color so that we should make another request.
        # TODO: But in lanecrawford.com, other colors are applied by JSON. Make a
        # way to deal with JSON.
        pass
