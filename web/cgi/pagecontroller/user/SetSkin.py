#coding=utf-8
import site_helper, web, page_helper
from .. import Update

# ../../page/user/SetSkin.html

class SetSkin(Update):

    def GET(self):
        i = web.input()
        model = site_helper.getModel('User')
        session = site_helper.session
        if session.is_login:
            user = model.get(session.user_id)
            sub_content = site_helper.page_render_nobase.user.SetSkin(user)
            return site_helper.page_render.user.Base3(user, sub_content)
        else:
            page_helper.redirectToLogin()

