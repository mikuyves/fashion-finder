# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
import json
import logging
import logging.config
from datetime import datetime

import flickrapi
from flickrapi.core import FlickrError
import webbrowser
import progressbar
from IPython import embed

from settings import PROJECT_PATH
from secret import BASEPATH, api_key, api_secret
import data


logging.config.fileConfig(os.path.join(PROJECT_PATH, 'log.conf'))
logger = logging.getLogger('flickr')

date_tag = datetime.strftime(datetime.now(), 'ud%Y%m%d')
date_photoset = datetime.strftime(datetime.now(), 'FOUND-%Y.%m')


def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


class MyFlickr(object):

    def __init__(self):
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        self.authenticate()

    def authenticate(self):
        print 'Step 1: AUTHENTICATE'
        # Only do this if you don't have a valid token.
        if self.flickr.token_valid(perms=u'write'):  # Letter u is important!
            print 'You already have a valid token.'

        else:
            # Get a request token.
            self.flickr.get_request_token(oauth_callback='oob')

            # Open a brower at the authentication URL. Do this however
            # you want, as long as the user visits that URL.
            authorize_url = self.flickr.auth_url(perms=u'write')
            webbrowser.open_new_tab(authorize_url)

            # Get the verifier code from the user.
            verifier = to_unicode_or_bust(raw_input='Verifier code: ')

            # Trade the request token for an access token.
            self.flickr.get_access_token(verifier)
            if self.flickr.token_valid(perms=u'write'):
                print 'Authentication is OK.'

    def start_upload(self):
        folders = []
        for root, sub, filenames in os.walk(BASEPATH):
            # Get all the folders which are ready to be uploaded. flk file is
            # a custom file type for telling whether a folder(an item) is uploaded.
            if 'ready_to_upload.flk' in filenames:
                self.upload(root, filenames)
                # Change the flk filename avoiding repetitional uploading.
                os.rename(
                    os.path.join(root, 'ready_to_upload.flk'),
                    os.path.join(root, 'uploaded.flk')
                )
        # Add the uploaded photos to the specific alblum.
        self.add_to_photoset()

    def upload(self, path, filenames):
        # Get the data from the backup files.
        headline_file = [f for f in filenames if re.search(r'flk$', f)][0]
        headline = self.get_content(path, headline_file)

        desc_file = [f for f in filenames if re.search(r'txt$', f)][0]
        desc = self.get_content(path, desc_file)

        # Upload photos.
        print 'START UPLOADDING %s' % headline
        images = [f for f in filenames if re.search(r'(jpg|jpeg|png)$', f)]
        with progressbar.ProgressBar(max_value=len(images)) as bar:
            for i, image in enumerate(images, start=1):
                self.flickr.upload(
                    filename=os.path.join(path, image),
                    title=headline,
                    description=desc,
                    tags=date_tag,
                    is_friend='1',
                )
                bar.update(i)
                logger.info('%s uploaded.' % image)
        print 'DONE!'
        print '=' * 50 + '\n'

    def get_content(self, path, filename):
        with open(os.path.join(path, filename)) as f:
            content = f.read()
        return content

    def add_to_photoset(self):
        # Flickr cannot add photos to photoset while uploading photos by api.
        # Be careful: we need dada with parsed-json, here self.flickr format
        # changed, it is different from the initialization.
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        recent_photos_data = self.flickr.photos.search(
            user_id='me', tags=date_tag, per_page=200, min_upload_date=date_tag
        )
        photos = recent_photos_data[u'photos'][u'photo']

        print 'Start to add the latest upload photos to the photoset...\n'
        for photo in photos:
            with open('flickr_photosets.json') as f:
                photosets = json.loads(f.read())

            # ' - ' is the rule that names headline.
            brand = photo[u'title'].split(' - ')[0].upper()
            photo_id = photo[u'id']

            print photo['title']
            target_photosets = [brand, 'FOUND', date_photoset]
            with progressbar.ProgressBar(
                max_value=len(target_photosets), redirect_stdout=True
            ) as bar:

                for i, photoset in enumerate(target_photosets, start=1):
                    self.add_photo(photo, photo_id, photosets, photoset)
                    print '--> %s OK.' % photoset.encode('utf-8')
                    bar.update(i)

    def add_photo(self, photo, photo_id, photosets, photoset):
        if photoset not in photosets:
            self.update_photoset(photoset, photo_id)
            logger.info('Photo added to %s!\n+++ %s\n' % (photoset, photo))
        else:
            try:
                self.flickr.photosets.addPhoto(
                    photoset_id=photosets[photoset], photo_id=photo_id
                )
                logger.info('Photo added to %s!\n+++ %s\n' % (photoset, photo))
            except FlickrError as e:
                logger.info('REPETITION: %s %s\n--- %s\n' % (e, photoset, photo))

    def update_photoset(self, brand, photo_id):
        self.flickr.photosets.create(title=brand, primary_photo_id=photo_id)
        logger.warn('+++ Add a new photoset: %s\n' % brand)
        self.backup_photoset()
        logger.warn('+++ Local photosets data updated.\n')

    def backup_photoset(self):
        # Be careful: self.flickr format changed, it is different from the initialization.
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        photoset_list = self.flickr.photosets.getList()
        photosets = photoset_list[u'photosets'][u'photoset']

        # Keep photosets title-id relationship in a JSON file avoiding get it with
        # a request to interenet every time we need it.
        photosets_dict = {}
        for photoset in photosets:
            photosets_dict[photoset[u'title'][u'_content'].upper()] = photoset['id']
        if photosets_dict:
            with open('flickr_photosets.json', 'wb') as f:
                f.write(json.dumps(photosets_dict))
