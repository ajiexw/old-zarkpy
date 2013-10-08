#coding=utf-8
import page_helper, site_helper, web

class Logout:

    def GET(self):
        site_helper.logout()
        return page_helper.redirectTo('/')
