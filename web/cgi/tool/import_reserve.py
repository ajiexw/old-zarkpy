#!/usr/bin/env python
#coding=utf-8
'''根据MakeupReserveid批量导入数据'''

import sys, os
filePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(filePath + '/..')
import site_helper
from site_helper import getModel

def getChooses(matchs):
    chooses = []
    for match in matchs:
        for m in match.matchs.split(';'):
            m = m.strip()
            if len(m) > 0:
                chooses.append((len(m), m, match.name))
    chooses.sort(reverse=True)
    return chooses

def match(chooses, content):
    for l, m, name in chooses:
        if _getMatchString(m) in _getMatchString(content):
            return name
    return ''

def matchAttrs( chooses, content):
    matched = []
    for l, m, name in chooses:
        if _getMatchString(m) in _getMatchString(content):
            if name not in matched:
                matched.append(name)
    return matched

def _getMatchString( content):
    return content.replace(' ','').replace('\n','').replace('\r','').replace('\t','').lower()

def main():
    makeup_model    = getModel('Makeup')
    brand_model     = getModel('Brand')
    reserve_model   = getModel('MakeupReserve')
    cat_model       = getModel('MakeupCategory')
    attr_model      = getModel('Attribute')

    brand_matchs    = getModel('BrandMatch').getAll({'cache':True})
    category_matchs = getModel('MakeupCategoryMatch').getAll({'cache':True})
    attr_matchs     = getModel('AttributeMatch').getAll({'cache':True})

    brand_chooses    = getChooses(brand_matchs)
    category_chooses = getChooses(category_matchs)
    attr_chooses     = getChooses(attr_matchs)

    for id in sys.argv[1:]:
        reserve = None
        if id.isdigit():
            reserve = reserve_model.get(id)

        if reserve:

            # match brand id
            match_brand = match(brand_chooses, reserve.brand + reserve.name)
            if match_brand:
                match_brand  = brand_model.getOneByWhere('name=%s', [match_brand])
                reserve.Brandid   = match_brand.Brandid if match_brand else 0

            # match catetory id
            match_category = match(category_chooses, reserve.category + reserve.name)
            if match_category:
                match_category  = cat_model.getOneByWhere('name=%s', [match_category])
                reserve.MakeupCategoryid = match_category.MakeupCategoryid if match_category else 0

            # match attribute ids
            reserve.attributeids = []
            match_attrs = matchAttrs(attr_chooses, reserve.attrs + reserve.name)
            if match_attrs:
                for a in match_attrs:
                    a = a.strip()
                    match_attr  = attr_model.getOneByWhere('name=%s', [a])
                    if match_attr is not None:
                        reserve.attributeids.append(match_attr.Attributeid)

            # insert
            assert(reserve.has_key('MakeupReserveid'))
            if reserve_model.get(reserve.MakeupReserveid):
                makeup_model.insert(reserve)
                reserve_model.delete(reserve.MakeupReserveid)

        else:
            print 'Warning: MakeupReserve is not found by id', id

if __name__=='__main__':
    if len(sys.argv) > 1:
        main()
    else:
        print 'Usage: python import_reserve.py makeup_reserve_id [makeup_reserve_id..]'
else:
    raise Exception('Import error, just run it!')
