#!/usr/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS

import os
import sys

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value

    ret['Size'] = i.size

    return ret


def main():

    dname = sys.argv[1]

    fields = ('FileName', 'ImageDescription', 'DateTimeOriginal', 'Size')

    photos = []
    width = 0
    for fname in os.listdir(dname):
        exif = get_exif(os.path.join(dname, fname))
        info = ("'%s'" % fname,
                "'%s'" % exif['ImageDescription'],
                "'%s'" % exif['DateTimeOriginal'],
                str(exif['Size'][0]),
                str(exif['Size'][1]))

        photos.append("    [%s]" % ',\n     '.join(info))
        width += exif['Size'][0]

    print '    photos: [\n%s\n    ]' % (',\n'.join(photos))
    print '    width: %d' % width


if __name__ == '__main__':
    main()
