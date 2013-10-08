#coding=utf-8
import site_helper, web, page_helper

# ../../editor//content/ReviewNav.html

class ReviewNav:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        show_brand_ids = content_model.getModelids('reviewnav', 'showbrand')

        table_model = site_helper.getModel('LevelTable')
        review_categorys = table_model.getContentByPage('reviewnav-categorys')
        review_attributes = table_model.getContentByPage('reviewnav-attributes')
        recommends = table_model.getContentByPage('reviewnav-recommend_brands')

        return site_helper.editor_render.content.ReviewNav(show_brand_ids,   review_categorys, review_attributes, recommends)

