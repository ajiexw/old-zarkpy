#coding=utf-8
import site_helper, web, page_helper

# ../page/Success.html

class Success:

    def GET(self):
        msg = web.input().get('msg', '')
        referer = web.input().get('referer', '')
        return site_helper.page_render.Success(msg, referer)

