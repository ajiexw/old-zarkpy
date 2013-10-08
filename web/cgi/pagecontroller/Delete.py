#coding=utf-8
import page_helper, site_helper, web

class Delete:

    def GET(self, i=None):
        return self.POST(i)

    def POST(self,i=None):
        if i is None: i = web.input()

        assert(i.has_key('model_name'))
        assert(i.has_key('model_id'))
        assert(site_helper.session.is_login)
        model = site_helper.getModel(i.model_name)

        #只允许删除自己的东西
        item = model.get(i.model_id)
        if (item and item.has_key('Userid') and item.Userid == int(site_helper.session.user_id))\
            or (i.get('model_name', '') == 'UserFeedComment') or (i.get('model_name', '') == 'PullFeedComment')\
            or (i.get('model_name', '') == 'BrandCycle') or (i.get('model_name', '') == 'BrandLinkCycle')\
            or (i.get('model_name', '') == 'Topic' and  site_helper.getModel('Groups').get(item.Groupsid).Userid == int(site_helper.session.user_id)):
            model.delete(i.model_id)

        page_helper.refresh()


