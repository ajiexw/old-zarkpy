#coding=utf-8
import page_helper, site_helper, web

class LogoutAdmin:

    def GET(self):
        site_helper.logoutAdmin()
        return page_helper.refresh()
