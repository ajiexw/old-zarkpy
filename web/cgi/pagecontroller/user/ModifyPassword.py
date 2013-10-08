#coding=utf-8
import site_helper, web, page_helper
from .. import Update

# ../page/user/ModifyPassword.html

class ModifyPassword(Update):

    def GET(self):
        i = web.input()
        model = site_helper.getModel('User')
        session = site_helper.session
        if session.is_login:
            user = model.get(session.user_id)
            sub_content = site_helper.page_render_nobase.user.ModifyPassword(user, '')
            return site_helper.page_render.user.Base3(user, sub_content)
        else:
            page_helper.redirectToLogin()


    def POST(self):
        i = web.input()
        model   = site_helper.getModel('User')
        session = site_helper.session
        if session.is_login:
            assert(i.has_key('oldpassword'))
            assert(i.has_key('newpassword'))
            user = model.get(session.user_id)
            if user.password == model.getMD5Password(i.oldpassword):
                model.update(session.user_id, {'password': model.getMD5Password(i.newpassword)})
                return page_helper.redirectTo('/success?msg=%E4%BF%AE%E6%94%B9%E6%88%90%E5%8A%9F&referer=/accounts')
            else:
                return site_helper.page_render.user.ModifyPassword(user, '原密码输入错误, 请重新输入')
        else:
            page_helper.redirectToLogin()

