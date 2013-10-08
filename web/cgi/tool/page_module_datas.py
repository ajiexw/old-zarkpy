import site_helper
from site_helper import getModel

def getSearchBoxDatas(cat):
    content_model = getModel('PageContent')

    if cat == 'brand':
        brand_model = getModel('Brand')
        brand_ids = content_model.getModelids('searchbox', 'brand')
        brands = map(brand_model.get, brand_ids)
        for brand in brands:
            brand.show_name = brand_model.getShowName(brand)
        datas = brands
    elif cat == 'catface':
        cat_model = getModel('MakeupCategory')
        cat_ids = content_model.getModelids('searchbox', 'catface')
        datas = map(cat_model.get, cat_ids)
    elif cat == 'catcos':
        cat_model = getModel('MakeupCategory')
        cat_ids = content_model.getModelids('searchbox', 'catcos')
        datas = map(cat_model.get, cat_ids)
    elif cat == 'catbody':
        cat_model = getModel('MakeupCategory')
        cat_ids = content_model.getModelids('searchbox', 'catbody')
        datas = map(cat_model.get, cat_ids)
    elif cat == 'attr':
        attr_model = getModel('Attribute')
        attr_ids = content_model.getModelids('searchbox', 'attr')
        datas = map(attr_model.get, attr_ids)
    else:
        datas = []

    datas = site_helper.filterNone(datas)
    return datas


def getHotTags():
    content = getModel('LevelTable').getContentByPage('index-hottag')
    content = content.replace('\t',' ')
    ret_links = []
    for a,b,c in [line.partition(' ') for line in content.split('\n')]:
        a = a.strip()
        c = c.strip()
        if len(a) > 0 and len(c) > 0:
            ret_links.append((a, c))
    return ret_links

def getAdDatas(page_name):
    ret_datas = []
    level_model = getModel('LevelTable')
    levels = level_model.getLevelsByPage('ad')

    if levels:
        d = level_model.levelsToDict(levels)
        if d and d.has_key(page_name):
            ret_datas = [(v['__index'], k, v) for k, v in d[page_name].items() if not k.startswith('__')]
            ret_datas.sort()
    return ret_datas
        
