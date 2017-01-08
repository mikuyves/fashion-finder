# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exceptions import DropItem

from eshop.utils import dealtext
from eshop.utils.dealitem import ItemMixer


class CheckItemPipeline(object):
    '''Check whether an item found in Chinese website has been translated.'''
    def process_item(self, item, spider):
        if item['lang'] == 'zh-CN' and not dealtext.match_zh(item['title']):
            raise DropItem('No Chinese translation yet: %s', item)
        else:
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()
        mixer = ItemMixer('items.jl')
        mixer.save_items()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
