#coding=utf-8
import site_helper
import web

class GetSiteInfo:

    def GET(self,i=None):
        if i is None: i = web.input()
        assert(i.has_key('name'))
        info = site_helper.getModel('SiteConfig').getOneByWhere('name=%s',[i.name])
        if info is not None:
            return str(info.value)
        else:
            return ''
