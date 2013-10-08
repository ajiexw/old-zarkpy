#coding=utf-8
import site_helper, web, page_helper
from controller import User as UserCtrl

# ../../page/user/Login.html

class Login:

    def GET(self):
        referer = site_helper.getEnv('HTTP_REFERER')
        if not referer.startswith(site_helper.config.HOST_NAME):
            referer = ''
        return site_helper.page_render.user.Login('', '', referer)

    def POST(self, i=None):
        if i is None: i = web.input()
        assert(len(i.get('email','')) > 0)
        assert(len(i.get('password','')) > 0)

        user = UserCtrl().loginByEmail(i.email, i.password)
        if user:
            if user.dead == 'off':
                site_helper.login(user, i.get('rememberme', False) == 'on')
                # 根据当前url中的referer跳转
                params = site_helper.getUrlParams()
                if params.get('referer', False):
                    return page_helper.redirectTo(params['referer'])

                # 根据上一个页面地址中的referer跳转
                params = site_helper.getUrlParams(site_helper.getEnv('HTTP_REFERER'))
                if params.get('referer', False):
                    return page_helper.redirectTo(params['referer'])

                return page_helper.success('登录成功. 欢迎回来', i.get('referer', '/'))
            else:
                return page_render.failed('登录失败,你已被管理员列入黑名单,请联系我们.', '/')

        else:
            return site_helper.page_render.user.Login('用户名或密码错误, 请重新输入', i.get('email', ''), i.get('referer',''))
