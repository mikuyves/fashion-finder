# -*- coding: utf-8 -*-
import scrapy

from eshop.items import Product

lc_url = raw_input('Enter the URL: ')

class LcSpider(scrapy.Spider):
    name = 'lc'
    start_urls = [
        lc_url,
    ]

    def parse(self, response):
        item = Product()
        item['url'] = response.url
        item['brand'] = response.css('.lc-product-brand-refresh::text').extract_first().strip().upper()
        item['title'] = response.css('.lc-product-short-description-refresh::text').extract_first().strip()
        item['desc'] = response.css('.text-paragraph::text').extract_first().strip()
        item['details'] = response.css('.sizeAndFit li::text').extract()
        item['photo_urls'] = response.css('.hero-carousel__img::attr(data-xl)').extract()

        yield scrapy.Request(
            url=response.url.replace('.com', '.com.cn'),
            meta={'item': item},
            callback=self.parse_ch,
        )

    def parse_ch(self, response):
        if response.status ==200:
            item = response.meta['item']
            item['title_ch'] = response.css('.lc-product-short-description-refresh::text').extract_first().strip()
            item['desc_ch'] = response.css('.text-paragraph::text').extract_first().strip()
            item['details_ch'] = response.css('.sizeAndFit li::text').extract()
            return item
        else:
            # It could be no Chinese version.
            item['title_ch'] = ''
            item['desc_ch'] = ''
            item['details_ch'] = ''
            self.log('No Chinese version.')
            return item
