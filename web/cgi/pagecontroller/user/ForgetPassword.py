#coding=utf-8
import site_helper, web, page_helper
from .. import Update
from datetime import datetime

# ../page/user/ForgetPassword.html

class ForgetPassword(Update):

    def GET(self):
        i = web.input()
        return site_helper.page_render.user.ForgetPassword()

    def POST(self):
        i = web.input()
        if i.has_key('email'):
            user = site_helper.getModel('User').getByEmail(i.email.strip())
            if user is not None:
                reset_model = site_helper.getModel('ResetPasswdCode')
                reset = reset_model.getACode(user.Userid)
                reset_model.updateACode(user.Userid, reset)
                reset_model.sendACode(user, reset)
            return page_helper.success('发送成功,查收您的邮箱.', '/')
        elif i.has_key('password'):
            user_id = site_helper.getUrlParams(site_helper.getEnv('HTTP_REFERER'))['userid']
            post_code = site_helper.getUrlParams(site_helper.getEnv('HTTP_REFERER'))['rcode']

            user_model = site_helper.getModel('User')
            code_model = site_helper.getModel('ResetPasswdCode')
            user = user_model.get(user_id)

            if user is not None:
                code = code_model.getByUserid(user_id)
                if code is not None and code.acode == post_code and ((datetime.now() - code.created).seconds < 3600*24):
                    assert(len(i.password) > 0)
                    user_model.resetPassword(user_id, i.password)
                    code_model.deleteByUserid(user_id)
                    site_helper.login(user)
                    return page_helper.success('重设密码成功,已登录.', '/')
                else:
                    return page_helper.failed('本重置密码链接已使用或已过期,请重新申请.','/accounts/forget')
            else:
                return page_helper.redirectToLogin()
        else:
            return page_helper.redirect404();

