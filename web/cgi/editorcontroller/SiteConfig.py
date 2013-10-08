#coding=utf-8
import site_helper, web, page_helper
from site_helper import getModel

class SiteConfig:

    def POST(self):
        inputs = web.input()
        model = getModel('SiteConfig')
        for k,v in inputs.items():
            model.replaceInsert({'name':k, 'value':v})

        return page_helper.refresh()
