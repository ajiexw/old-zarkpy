#coding=utf-8
import site_helper, web, page_helper

# ../../editor//content/Sidebar.html

class Sidebar:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        latest_news_ids = content_model.getModelids('sidebar', 'latestnews')
        popular_makeup_ids = content_model.getModelids('sidebar', 'popularmakeup')

        return site_helper.editor_render.content.Sidebar( latest_news_ids, popular_makeup_ids)
