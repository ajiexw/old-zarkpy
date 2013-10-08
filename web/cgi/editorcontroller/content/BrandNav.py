#coding=utf-8
import site_helper, web, page_helper

# ..content/BrandNav.html

class BrandNav:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        hot_brand_ids = content_model.getModelids('brandnav', 'hotbrand')
        hot_makeup_ids = content_model.getModelids('brandnav', 'hotmakeup')
        counter_ids = content_model.getModelids('brandnav', 'counter')
        open_shelf_ids = content_model.getModelids('brandnav', 'openshelf')
        other_brand_ids = content_model.getModelids('brandnav', 'otherbrand')

        return site_helper.editor_render.content.BrandNav(hot_brand_ids , hot_makeup_ids , counter_ids , open_shelf_ids , other_brand_ids ,)
