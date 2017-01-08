# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict

import requests

from secret import BASEPATH
from screenshot import get_screenshot


class ItemMixer(object):
    '''Take items out of the json file and combine the same item in different
    languages by pid in every item.
    '''
    def __init__(self, jl_file):
        loaded_items = self.load_items(jl_file)
        self.groups = self.group_items(loaded_items)
        self.items = self.mix_items()

    def group_items(self, loaded_items):
        # Match items by their pid.
        groups = defaultdict(list)
        for item in loaded_items:
            groups[item['pid']].append(item)
        return groups

    def load_items(self, jl_file):
        # Load items from a json file.
        loaded_items = []
        with open(jl_file, 'r') as f:
            for line in f:
                loaded_items.append(json.loads(line))
        return loaded_items

    def mix_items(self):
        # Combine 2 language items into 1.
        items = []
        for group in self.groups.itervalues():
            if len(group) > 1:
                for item in group:
                    if item['lang'] == 'zh-CN':
                        item_zh = item
                    if item['lang'] == 'en-US':
                        item_en = item
                item_en['has_zh'] = True
                item_en['title_zh'] = item_zh['title']
                item_en['desc_zh'] = item_zh['desc']
                item_en['detail_zh'] = item_zh['detail']
                items.append(item_en)
        return items

    def save_items(self):
        for item in self.items:
            self.save_item(item)

    def save_item(self, item):
        brand = item['brand']
        title = '.'.join(item['title'].split(' '))
        foldername = '%s_%s' % (brand, title)
        filename_base = '%s_%s' % (brand, title)
        folderpath = os.path.join(BASEPATH, foldername)

        try:
            os.mkdir(folderpath)
        except OSError as e:
            print e

        # Save the information to a txt file.
        with open(folderpath + '/%s.txt' % filename_base, 'w') as f:
            # Write Chinese content.
            if item['has_zh']:
                f.write(item['title_zh'].encode('utf8'))
                f.write('\n\n')
                f.write(item['desc_zh'].encode('utf8'))
                f.write('\n\n')
                f.write('\n'.join(item['detail_zh']).encode('utf8'))
                f.write('\n\n')

            # Write standard content in English.
            f.write(item['title'].encode('utf8'))
            f.write('\n\n')
            f.write(item['desc'].encode('utf8'))
            f.write('\n\n')
            f.write('\n'.join(item['detail']).encode('utf8'))
            f.write('\n\n')
            f.write(item['url'].encode('utf8'))

        # Download photos.
        for num, photo_url in enumerate(item['photo_urls'], start=1):
            photo = requests.get(photo_url)
            filename = '%s_%d.jpg' % (filename_base, num)
            filepath = '/'.join([folderpath, filename])
            with open(filepath, 'wb') as f:
                f.write(photo.content)

        # Save the screenshot of the item for showing the price.
        get_screenshot(item['url'], filepath)
