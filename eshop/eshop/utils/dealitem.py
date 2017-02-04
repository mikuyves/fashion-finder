# -*- coding: utf-8 -*-
import os
import time
import json
import logging
from collections import defaultdict

import requests
from IPython import embed
import progressbar

from secret import BASEPATH
from screenshot import get_screenshot


logger = logging.getLogger(__name__)


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
                # Add Chinese content into English item, add keys.
                try:
                    item_en['has_zh'] = True
                    item_en['title_zh'] = item_zh['title']
                    item_en['desc_zh'] = item_zh['desc']
                    item_en['details_zh'] = item_zh['details']
                except KeyError as e:
                    print 'There is something wrong with the key %s' % e
                finally:
                    items.append(item_en)

            elif len(group) == 1:
                item_en = group[0]
                item_en['has_zh'] = False
                items.append(item_en)
        return items

    def save_items(self):
        for item in self.items:
            self.save_item(item)

    def save_item(self, item):
        # Define variables we need later.
        brand = item['brand']
        title = item['title']
        f_brand = '-'.join(brand.split(' '))
        f_title = '-'.join(title.split(' ')).replace('/', '')
        foldername = '%s_%s' % (f_brand, f_title)
        filename_base = '%s_%s' % (f_brand, f_title)
        flickr_headline = '%s - %s' % (brand, title)
        folderpath = os.path.join(BASEPATH, foldername)

        # Check whether it has been downloaded before.
        try:
            os.mkdir(folderpath)
        except OSError as e:
            logger.warning(
                '%s has been downloaded before. %s' % (flickr_headline, e)
            )
        else:
            # Save the information to a txt file.
            with open(folderpath + '/%s.txt' % filename_base, 'w') as f:
                # Write Chinese content.
                if item['has_zh']:
                    f.write(
                        '%s %s' % (brand.encode('utf8'), item['title_zh'].encode('utf8'))
                    )
                    f.write('\n\n')
                    f.write(item['desc_zh'].encode('utf8'))
                    f.write('\n\n')
                    f.write('\n'.join(item['details_zh']).encode('utf8'))
                    f.write('\n\n')

                # Write content in English which is standard.
                f.write(flickr_headline.encode('utf8'))
                f.write('\n\n')
                f.write(item['desc'].encode('utf8'))
                f.write('\n\n')
                f.write('\n'.join(item['details']).encode('utf8'))
                f.write('\n\n')
                f.write(item['url'].encode('utf8'))

            # Download photos.
            print '\nDownloading photos of %s from %s' % (flickr_headline, item['website'])
            # Some website such as matchesfashion.com should be requested with
            # User-Agent to download photos.
            headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1'}
            with progressbar.ProgressBar(
                max_value=len(item['photo_urls']), redirect_stdout=True
            ) as bar:
                for num, photo_url in enumerate(item['photo_urls'], start=1):
                    try:
                        photo = requests.get(photo_url, headers=headers)
                    except Exception as e:
                        print e
                    finally:
                        time.sleep(5)
                        if photo.ok:
                            filename = '%s_%d.jpg' % (filename_base, num)
                            filepath = '/'.join([folderpath, filename])
                            with open(filepath, 'wb') as f:
                                f.write(photo.content)
                            bar.update(num)
                        else:
                            logger.warning('%s --> MISSED!' % photo_url)

            # Save the screenshot of the item for showing the regular price.
            print 'Getting a screenshot...'
            get_screenshot(item['url'], filepath, item['website'])
            print 'Done.'

            # Make a file for flickr uploading.
            with open(folderpath + '/ready_to_upload.flk', 'w') as f:
                f.write(flickr_headline.encode('utf8'))

            # Backup mixed item data to a JSON file.
            with open(folderpath + '/item_data.json', 'wb') as f:
                data = json.dumps(item)
                f.write(data)
