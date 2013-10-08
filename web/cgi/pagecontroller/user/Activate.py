#coding=utf-8
import site_helper, web, page_helper

class Activate:

    def GET(self):
        i = web.input() 
        assert(i.has_key('userid'))
        assert(i.has_key('acode'))
        user_id = int(i.userid)

        acode_model = site_helper.getModel('ACode')
        exists_acode = acode_model.getOneByWhere('Userid=%s and acode=%s', [user_id, i.acode])

        if exists_acode is not None:
            user_model = site_helper.getModel('User')
            user = user_model.get(user_id)
            assert(user is not None)
            user_model.activate(user_id)
            site_helper.login(user)
            site_helper.session.activated = 'on'
            acode_model.deleteByUserid(user_id)
            return site_helper.page_render.user.ActivateSuccess(user)
        else:
            page_helper.redirect404()

