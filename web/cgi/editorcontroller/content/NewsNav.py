#coding=utf-8
import site_helper, web, page_helper

# ../../editor//content/NewsNav.html

class NewsNav:

    def GET(self):
        i = web.input()
        content_model = site_helper.getModel('PageContent')
        latest_news_ids = content_model.getModelids('newsnav', 'latestnews')
        latest_makeup_ids = content_model.getModelids('newsnav', 'latestmakeup')
        current_month_makeup_ids = content_model.getModelids('newsnav', 'currentmonth')
        last_month_makeup_ids = content_model.getModelids('newsnav', 'lastmonth')

        return site_helper.editor_render.content.NewsNav(latest_news_ids, latest_makeup_ids, current_month_makeup_ids, last_month_makeup_ids)


