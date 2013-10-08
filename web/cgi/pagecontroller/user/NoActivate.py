#coding=utf-8
import site_helper, web, page_helper

class NoActivate:

    def GET(self):
        return site_helper.page_render.user.NoActivate()
