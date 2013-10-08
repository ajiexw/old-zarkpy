#coding=utf-8
import site_helper, web
from controller import User as UserCtrl

class LoginAdmin:
    def GET(self):
        return site_helper.editor_render_nobase.adminuser.Login()

    def POST(self,i=None):
        if i is None: i = web.input()
        assert(len(i.get('email','')) > 0)
        assert(len(i.get('password','')) > 0)
        user = UserCtrl().loginAdminByEmail(i.email, i.password)
        if user:
            site_helper.loginAdmin(user)
            web.seeother('/admin')
        else:
            web.seeother('/admin/login')

