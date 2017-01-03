#!/usr/bin/env python
import flickrapi
import webbrowser
from IPython import embed

import secret
import data

pic_to_upload = raw_input('Enter what you need to upload:')
title = 'BRAND - TITLE'
description = 'This is some text about picture upload function.'
tags = 'test python flickrapi'

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

flickr = flickrapi.FlickrAPI(secret.api_key, secret.api_secret, format='parsed-json')

print 'Step 1: AUTHENTICATE'

# Only do this if you don't have a valid token.
if flickr.token_valid(perms=u'write'):  # Notice: letter u is important!
    print 'You already have a valid token.'

else:
    # Get a request token.
    flickr.get_request_token(oauth_callback='oob')

    # Open a brower at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=u'write')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user.
    verifier = to_unicode_or_bust(raw_input='Verifier code: ')

    # Trade the request token for an access token.
    flickr.get_access_token(verifier)
    if flickr.token_valid(perms=u'write'):
        print 'Authentication is OK.'

embed()

print 'Step 2: Use flickr'
flickr.upload(
    filename=pic_to_upload,
    title=title,
    description=description,
    tags=tags
    )

# Search the recently uploaded photos.
# new_pictures = flickr.photos.search(user_id='me', text='brand', min_upload_date='today')

# Search photoset id of the brand photoset
def get_photoset_id(brand):
    photoset_list = flickr.photosets.getList()
    photosets = photoset_list[u'photosets'][u'photoset']
    for photoset in photosets:
        if brnad in photoset[u'title'][u'_content']:
            return photoset[u'id']
        else:
            # If no photoset matches, then create a photoset.
            return none

# Add the recently uploaded photos to the photoset of brand.
# flickr.photosets.addPhoto(photoset_id='brand_photoset_id', photo_id='per_new_picture_id')
