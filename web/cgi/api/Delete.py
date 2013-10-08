#coding=utf-8
import page_helper, site_helper, web, api_helper

class Delete:

    def GET(self, i=None):
        return self.POST(i)

    def POST(self,i=None):
        if i is None: i = web.input()

        assert(i.has_key('model_name'))
        assert(i.has_key('model_id'))

        model = site_helper.getModel(i.model_name)

        session = site_helper.session
        #只允许删除自己的东西
        item = model.get(i.model_id)
        if item is not None:
            if (session.is_login and item.get('Userid', None) == int(session.user_id)) or site_helper.session.is_admin:
                model.delete(i.model_id)
                return api_helper.render({'success':True})
            else:
                return api_helper.render({'success':False, 'msg':'尝试删除不属于你的东西.'})
        else:
            return api_helper.render({'success':False, 'msg':'尝试删除不存在的东西.'})
