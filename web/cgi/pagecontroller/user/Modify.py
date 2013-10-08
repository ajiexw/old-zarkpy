#coding=utf-8
import site_helper, web, page_helper
from .. import Update
from Register import Register

# ../../page/user/Modify.html
# ../../page/user/ModifyPortrait.html

class Modify(Update, Register):

    def GET(self):
        i = web.input()
        model = site_helper.getModel('User')
        session = site_helper.session
        if session.is_login:
            user = model.get(session.user_id)
            sub_content = site_helper.page_render_nobase.user.Modify(user)
            return site_helper.page_render.user.Base3(user, sub_content)
        else:
            page_helper.redirectToLogin()

    def POST(self):
        i = web.input(imagefile={})
        assert(not i.has_key('email'))
        assert(not i.has_key('password'))
        if i.has_key('birthday'):
            try:
                i.age = self.calcAge(i.birthday)
            except:
                return page_helper.failed('修改失败,生日格式填写错误 ')
        session = site_helper.session
        if session.is_login:
            if i.has_key('username'):
                user_name = i.username.encode('utf-8', 'ignore')
                if self.existsUsername(user_name, session.user_id):
                    return page_helper.failed('修改失败, 用户名 ' +user_name+ ' 已被使用')
                web.setcookie('name',  user_name)
                site_helper.session.user_name = user_name
            if i.has_key('self_domain'):
                self_domain = i.self_domain.encode('utf-8', 'ignore')
                if self.existsDomain(self_domain, session.user_id):
                    return page_helper.failed('修改失败, 域名' +self_domain+ ' 已被使用')
            i.model_name = 'User'
            i.model_id = session.user_id
            return Update.POST(self, i, )
        else:
            return page_helper.redirectToLogin()

    def existsUsername(self, user_name, user_id):
        item = site_helper.getDBHelper().fetchFirst('select Userid from User where LOWER(username)=%s and Userid<>%s', [user_name.lower(), user_id])
        return item is not None

    def existsDomain(self, self_domain, user_id):
        item = site_helper.getDBHelper().fetchFirst('select Userid from User where LOWER(self_domain)=%s and Userid<>%s', [self_domain.lower(), user_id])
        return item is not None

