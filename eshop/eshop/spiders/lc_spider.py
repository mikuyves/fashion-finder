# -*- coding: utf-8 -*-
import scrapy

from eshop.items import Product, ProductLoader


lc_url = raw_input('Enter the URL: ')

class LcSpider(scrapy.Spider):
    name = 'lc'
    start_urls = [
        lc_url,
    ]

    def parse(self, response):
        pldr = ProductLoader(item=Product(), response=response)
        pldr.add_value('url', response.url)
        pldr.add_css('brand', '.lc-product-brand-refresh::text')
        pldr.add_css('title', '.lc-product-short-description-refresh::text')
        pldr.add_css('desc', '.text-paragraph::text')
        pldr.add_css('details', '.sizeAndFit li::text')
        pldr.add_css('photo_urls', '.hero-carousel__img::attr(data-xl)')

        yield scrapy.Request(
            url=response.url.replace('.com', '.com.cn'),
            meta={'item': pldr.load_item()},
            callback=self.parse_ch,
        )

    def parse_ch(self, response):
        # Notice: `response=response` is very important! Because this response
        # is different from that response in self.parse(). If we just pass the
        # meta data with `'pldr'=pldr`, the response would remain the same as
        # before, and we don't know how to change the response inside the pldr.
        # So, we can only pass `item` here, and instantiate a pldr to change
        # the response correctly.
        pldr = ProductLoader(item=response.meta['item'], response=response)
        if response.status ==200:
            pldr.add_css('title_ch', '.lc-product-short-description-refresh::text')
            pldr.add_css('desc_ch', '.text-paragraph::text')
            pldr.add_css('details_ch', '.sizeAndFit li::text')
            return pldr.load_item()
        else:
            # It could be no Chinese version.
            pldr.add_value('title_ch', '')
            pldr.add_value('desc_ch', '')
            pldr.add_value('details_ch', '')
            self.log('No Chinese version.')
            return pldr.load_item()
