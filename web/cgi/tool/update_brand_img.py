#!/usr/bin/env python
#coding=utf-8
import sys, os
sys.path.append('.')
import site_helper

if __name__=='__main__':

    if len(sys.argv) == 3:
        model = site_helper.getModel('Brand')
        brand_id = int(sys.argv[1])
        image_file = sys.argv[2]

        brand = model.get(brand_id)
        if brand is None:
            sys.stderr.write('brand is not exists\n')
            exit(1)

        if not os.path.exists(image_file):
            sys.stderr.write('image file is not exists\n')
            exit(1)

        imagefile = site_helper.storage({'filename':image_file, 'value':open(image_file).read()})
        data = site_helper.storage({'cnname':brand.cnname , 'imagefile':imagefile })
        model.update(brand_id, data)
    else:
        print 'Usage: python update_brand_img.py brand_id image_file'

else:
    raise Exception('Import error, just run it!')
