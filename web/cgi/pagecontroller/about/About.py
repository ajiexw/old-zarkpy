#coding=utf-8
import site_helper, web, page_helper

class About:

    def GET(self, page):
        page = page.title()
        if hasattr(site_helper.page_render_about, page):
            return getattr(site_helper.page_render.about, page)()
        else:
            return page_helper.redirect404()

