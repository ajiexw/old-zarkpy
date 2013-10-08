#coding=utf-8
import site_helper, web, page_helper

# ../page/Failed.html

class Failed:

    def GET(self):
        msg = web.input().get('msg', '')
        referer = web.input().get('referer', '')
        return site_helper.page_render.Failed(msg, referer)

