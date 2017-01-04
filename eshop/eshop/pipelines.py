# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
import requests
import hashlib
from urllib import quote

from utils.screenshot import get_screenshot
from utils.secret import BASEPATH


class SaveItemPineline(object):
    '''
    Make a folder to save all the item data, as follow:
    foldername: brand - title
    info.txt: title_cn, desc_cn, details_cn, title, desc, details, url
    *.jpg: photos
    *.png: screenshot of the item url(modified as no discount)
    '''
    def process_item(self, item, spider):
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
            if item['has_cn']:
                f.write(item['title_cn'].encode('utf8'))
                f.write('\n\n')
                f.write(item['desc_cn'].encode('utf8'))
                f.write('\n\n')
                f.write('\n'.join(item['details_cn']).encode('utf8'))
                f.write('\n\n')

            # Write standard content in English.
            f.write(item['title'].encode('utf8'))
            f.write('\n\n')
            f.write(item['desc'].encode('utf8'))
            f.write('\n\n')
            f.write('\n'.join(item['details']).encode('utf8'))
            f.write('\n\n')
            f.write(item['url'].encode('utf8'))

        # Download photos.
        # TODO: Is requests better than ImagesPineline or `scrapy.Request`?
        for num, photo_url in enumerate(item['photo_urls'], start=1):
            photo = requests.get(photo_url)
            filename = '%s_%d.jpg' % (filename_base, num)
            filepath = '/'.join([folderpath, filename])
            with open(filepath, 'wb') as f:
                f.write(photo.content)

        # Save the screenshot of the item for showing the price.
        get_screenshot(item['url'], filepath)

        return item

#class ScreenshotPineline(object):
#    '''Pipeline that uses Splash to render screenshot of
#    every Scrapy item.'''
#
#    SPLASH_URL = 'http://localhost:8050/render.png?url={}'
#
#    def process_item(self, item, spider):
#        encoded_item_url = quote(item['url'])
#        screenshot_url = self.SPLASH_URL.format(encoded_item_url)
#        request = scrapy.Request(screenshot_url)
#        dfd = spider.crawler.engine.download(request, spider)
#        dfd.addBoth(self.return_item, item)
#        return dfd
#
#    def return_item(self, response, item):
#        # if response.status != 200:
#            # Error happened, return item.
#        #     return item
#
#        # Save screenshot to file, filename will be hash of url.
#        url = item['url']
#        url_hash = hashlib.md5(url.encode('utf8')).hexdigest()
#        filename = '{}.png'.format(url_hash)
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#
#        # Store filename in item.
#        item['screenshot_filename'] = filename
#        return item
