#coding=utf-8
import site_helper, web, page_helper

# ../../editor//content/SearchBox.html

class SearchBox:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        brand_ids = content_model.getModelids('searchbox', 'brand')
        cat_face_ids = content_model.getModelids('searchbox', 'catface')
        cat_cos_ids = content_model.getModelids('searchbox', 'catcos')
        cat_body_ids = content_model.getModelids('searchbox', 'catbody')
        attr_ids = content_model.getModelids('searchbox', 'attr')

        return site_helper.editor_render.content.SearchBox(brand_ids , cat_face_ids , cat_cos_ids , cat_body_ids , attr_ids )

        
