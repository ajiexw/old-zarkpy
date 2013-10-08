#coding=utf-8
import site_helper, web, page_helper

# ../../editor//content/Review.html

class Review:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        attr_ids = content_model.getModelids('makeup', 'attributes')
        return site_helper.editor_render.content.Review(attr_ids)

