# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from urlparse import urlparse

from scrapy.exceptions import DropItem

from eshop.utils import dealtext
from eshop.utils.dealitem import ItemMixer
#from eshop.settings import FLICKR_PATH
#from flickr.upload import MyFlickr


class CheckItemPipeline(object):
    def process_item(self, item, spider):
        # Check whether an item found in Chinese website has been translated.
        if item['lang'] == 'zh-CN' and not dealtext.match_zh(item['title']):
            raise DropItem('No Chinese translation yet: %s', item)
        # Check whether image urls of item are fit for downloading.
        elif item['lang'] == 'en-US':
            self.check_url(item)
            return item
        else:
            return item

    def check_url(self, item):
        # Check and complete the urls missing scheme and netloc.
        photo_urls = item['photo_urls']
        scheme = urlparse(item['url']).scheme
        netloc = item['website']

        checked_urls = []
        for url in photo_urls:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                pass
            elif not parsed_url.scheme and not parsed_url.netloc:
                url = parsed_url._replace(**{'scheme': scheme, 'netloc': netloc}).geturl()
            elif not parsed_url.scheme:
                url = parsed_url._replace(**{'scheme': scheme}).geturl()
            checked_urls.append(url)

        item['photo_urls'] = checked_urls


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

        # Download item data for uploading.
        mixer = ItemMixer('items.jl')
        mixer.save_items()

#        # Upload to flickr.
#        import os
#        os.chdir(FLICKR_PATH)
#        f = MyFlickr()
#        f.start_upload()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
