#!/usr/bin/env python
import os
import re
import json

import flickrapi
from flickrapi.core import FlickrError
import webbrowser
from IPython import embed

import secret
from secret import BASEPATH, api_key, api_secret
import data


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
        # Get all the folders which are ready to be uploaded.
        folders = []
        for root, sub, files in os.walk(secret.BASEPATH):
            if 'ready_to_upload.flk' in files:
                self.upload(root, files)

    def upload(self, path, files):
        # Get the data from the backup files.
        headline_file = [f for f in files if re.search(r'flk$', f)][0]
        headline = self.get_content(path, headline_file)

        desc_file = [f for f in files if re.search(r'txt$', f)][0]
        desc = self.get_content(path, desc_file)

        print 'START UPLOADDING %s' % headline
        print '=' * 50

        # Upload photos.
        images = [f for f in files if re.search(r'(jpg|jpeg|png)$', f)]
        for image in images:
            self.flickr.upload(
                filename='/'.join((path, image)),
                title=headline,
                description=desc,
            )
            print '%s uploaded.' % image
        print 'WELL DONE!'
        print '=' * 50

    def get_content(self, path, _file):
        with open('/'.join((path, _file))) as f:
            content = f.read()
        return content

    def add_to_photoset(self):
        # Flickr cannot add photos to photoset while uploading photos by api.
        # Be careful: we need dada with parsed-json, here self.flickr format
        # changed, it is different from the initialization.
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        recent_photos_data = self.flickr.photos.recentlyUpdated(
            per_page=200, min_date='20170112'
        )
        photos = recent_photos_data[u'photos'][u'photo']

        print 'Start to add the latest upload photos to the photoset...\n'
        for photo in photos:
            with open('flickr_photosets.json') as f:
                photosets = json.loads(f.read())

            # ' - ' is the rule that names headline.
            if ' - ' in photo[u'title']:
                brand = photo[u'title'].split(' - ')[0].upper()
                photo_id = photo[u'id']

                if brand in photosets:
                    self.add_photo(photo, photo_id, photosets, brand)
                    self.add_photo(photo, photo_id, photosets, 'FOUND')
                    self.add_photo(photo, photo_id, photosets, 'FOUND-2017.01')
                else:
                    self.update_photoset(brand, photo_id)
                    print 'Photo added to %s!\n+++ %s\n' % (brand, photo)

    def add_photo(self, photo, photo_id, photosets, photoset):
        try:
            self.flickr.photosets.addPhoto(
                photoset_id=photosets[photoset], photo_id=photo_id
            )
            print 'Photo added to %s!\n+++ %s\n' % (photoset, photo)
        except FlickrError as e:
            print '%s %s\n--- %s\n' % (e, photoset, photo)

    def update_photoset(self, brand, photo_id):
        self.flickr.photosets.create(title=brand, primary_photo_id=photo_id)
        print '+++ Add a new photoset: %s\n' % brand
        self.backup_photoset()
        print '+++ Local photosets data updated.\n'

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
