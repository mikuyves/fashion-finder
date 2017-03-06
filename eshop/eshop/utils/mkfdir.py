# -*- coding: utf-8 -*-
import os


# Define your own BASEPATH which is a ABS-PATH for saving the data.
from secret import BASEPATH


flickr_headline = raw_input('Enter flickr headline: ')
base_filename = flickr_headline.replace(' ', '_')

folderpath = os.path.join(BASEPATH, base_filename)
os.mkdir(folderpath)
print 'FOLDER: %s is created' % folderpath

with open(folderpath + '/ready_to_upload.flk', 'w') as f:
    f.write(flickr_headline.encode('utf8'))
print 'Made a flk file for flickr uploading.'

with open(folderpath + '/%s.txt' % base_filename, 'w') as f:
    f.write(flickr_headline.encode('utf8'))
print 'Made a txt file for item content.'
