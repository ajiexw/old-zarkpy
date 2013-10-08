#coding=utf-8
import site_helper, web, page_helper, os
from site_helper import getModel
from controller import User as UserCtrl

# ../../page/oauth/Login.html

class Login:

    def GET(self):
        i = web.input()
        session = site_helper.session
        assert(i.has_key('state'))
        assert(i.has_key('token'))
        if not session.is_login: # 没有登录, 要求用户输入email和password
            return self.getThisPage(i.token.strip(), i.state.strip(), '')
        else: # 已经登录, 直接绑定当前帐号
            user_model = getModel('User')
            exists_user = user_model.get(session.user_id)
            site_name = i.state.partition('_')[0]
            oauth_ctrl  = site_helper.getController('oauth.' + site_name)
            error = oauth_ctrl.bindUserid(i.token.strip(), exists_user.Userid)
            if not error:
                self.shareThisSite(oauth_ctrl, session.user_id, i.token.strip(), '【来凹凹啦,找到最漂亮的自己】经常听姐妹们提起@凹凹啦, 今天我也终于注册啦! 大家一起来逛吧 ', pic='/img/page/ad_weibo.jpg', url='/find' )
                UserCtrl().checkConnectMedal(session.user_id)
                return page_helper.success('成功绑定' + oauth_ctrl.CN_SITE_NAME, '/oauth/setting&check_task=oauth_bind_sina|oauth_bind_qq|oauth_bind_renren')
            else:
                return self.getThisPage(i.token.strip(), i.state.strip(), error, i.get('email'))

    def POST(self):
        i = web.input()
        session = site_helper.session
        assert(not session.is_login)
        assert(i.has_key('state'))
        assert(i.has_key('access_token'))
        assert(i.has_key('email'))
        assert(i.has_key('password'))
        email = i.email.strip()
        password = i.password
        site_name = i.state.partition('_')[0]

        user_model = getModel('User')
        oauth_model = getModel('oauth.%sOAuth2' % site_name)
        oauth_ctrl  = site_helper.getController('oauth.' + site_name)

        exists_user = user_model.getByEmail(email)

        if exists_user is None: # 如果邮箱没有注册过, 那么新建用户绑定第三方帐号
            user_data = site_helper.storage({'email':email, 'password':password, 'activated': 'on' })
            user_data = oauth_ctrl.assignUserInfo(user_data, i.access_token)
            new_id = user_model.insert(user_data)
            new_user = user_model.get(new_id)
            if new_user and new_user.cover_url:
                user_model.update(new_id, {'small_portrait':'0 0 %d %d' % site_helper.getImageSize(new_user.cover_url)})
            oauth_ctrl.bindUserid(i.access_token, new_user.Userid)
            site_helper.login(new_user, True)
            UserCtrl().checkConnectMedal(session.user_id)
            # 分享本站
            if i.get('share_this', 'off') == 'on':
                self.shareThisSite(oauth_ctrl, new_user.Userid, i.access_token, i.get('share_comment').encode('utf-8','ignore'), pic='/img/page/ad_weibo.jpg', url='/find')
            return page_helper.success('成功绑定' + oauth_ctrl.CN_SITE_NAME, '/?check_task=oauth_bind_sina|oauth_bind_qq|oauth_bind_renren')
        else: # 否则邮箱已经注册过
            exists_user = UserCtrl().loginByEmail(i.email, i.password)
            if exists_user: # 如果密码正确
                error = oauth_ctrl.bindUserid(i.access_token, exists_user.Userid)
                if not error:
                    site_helper.login(exists_user, True)
                    UserCtrl().checkConnectMedal(session.user_id)
                    if i.get('share_this', 'off') == 'on':
                        self.shareThisSite(oauth_ctrl, exists_user.Userid, i.access_token, i.get('share_comment').encode('utf-8','ignore'), pic='/img/page/ad_weibo.jpg', url='/find' )
                    return page_helper.success('成功绑定' + oauth_ctrl.CN_SITE_NAME, '/?check_task=oauth_bind_sina|oauth_bind_qq|oauth_bind_renren')
                else:
                    return self.getThisPage(i.access_token.strip(), i.state.strip(), error, i.email)
            else: # 提示密码错误
                return self.getThisPage(i.access_token.strip(), i.state.strip(), '您的邮箱已经注册过, 但您输入的密码不正确, 请重新输入', i.email)

    def shareThisSite(self, oauth_ctrl, user_id, access_token, comment, **options):
        if options.get('url', None) and not options['url'].startswith('http://'):
            options['url'] = site_helper.config.HOST_NAME.rstrip('/') + options['url']
        oauth_ctrl.share(user_id, access_token, comment, **options)

    def getThisPage(self, token, state, error_msg, email=''):
        site_name = state.partition('_')[0]
        oauth_ctrl  = site_helper.getController('oauth.' + site_name)
        return  site_helper.page_render.oauth.Login(token.strip(), state.strip(), oauth_ctrl.CN_SITE_NAME, error_msg, email)

