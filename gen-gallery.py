#!/usr/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

import os
import glob
import sys

def get_exif(im):
    ret = {}
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value

    ret['Size'] = im.size

    return ret


def main():

    thumb_dir = "thumbs"
    m = 540.0

    if not os.path.isdir(thumb_dir):
        os.mkdir(thumb_dir)

    photos = []
    for fname in glob.glob("*.jpg"):
        im = Image.open(fname)
        im_w, im_h = im.size
        thumb_size = (int(m), int(im_h*(m/im_w))) if im_w > im_h else (int(im_w*(m/im_h)),int(m))
        im.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_fname = os.path.join(thumb_dir, os.path.splitext(fname)[0] +
                ".thumbnail.jpg")
        im.save(thumb_fname)

        exif = get_exif(im)
        date = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        desc = exif['ImageDescription'] if 'ImageDescription' in exif else ''
        photos.append((fname, thumb_fname, desc, thumb_size[0], thumb_size[1], date))

    photos.sort(key=lambda p: p[5])

    print '''
---
  title: <TITLE>
  layout: post
  imagedir: /images/projects/<PROJECT>
  photos:'''

    for photo in photos:
        print '  - url: %s' % photo[0]
        print '    thumbnail: %s' % photo[1]
        print '    label: %s' % photo[2]
        print '    width: %s' % photo[3]
        print '    height: %s' % photo[4]

    print '---'
    print ''

if __name__ == '__main__':
    main()
