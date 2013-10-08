#coding=utf-8
import site_helper, web, page_helper

class SendACode:

    def GET(self):
        i = web.input()

        session = site_helper.session

        if session.is_login:
            user = site_helper.getModel('User').get(session.user_id)
            acode_model = site_helper.getModel('ACode')
            acode = acode_model.getACode(user.Userid)
            acode_model.updateACode(user.Userid, acode)
            acode_model.sendACode(user, acode)
            return page_helper.success('已向您的邮箱发送验证邮件,请查收,可能在垃圾邮件里.', site_helper.getUrlParams().get('referer','/'))
        else:
            return page_helper.redirectToLogin()
