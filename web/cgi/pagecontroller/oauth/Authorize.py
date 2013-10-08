#coding=utf-8
import site_helper, page_helper, web
from controller import User as UserCtrl

'''用户在第三方网站输入密码后返回到Authorize, 然后获取access_token后跳转到/oauth/login'''
class Authorize:

    def GET(self):
        i = web.input()
        session = site_helper.session
        assert(i.has_key('code'))
        assert(i.has_key('state'))

        #if session.is_login: # 如果已经登录, 直接跳转到/oauth/login
        #    return page_helper.redirectTo('/oauth/login?token=%s&state=%s' % (i.code, i.state))

        site_name = i.state.partition('_')[0]

        authorization_code = i.code.strip()
        oauth_ctrl  = site_helper.getController('oauth.' + site_name)
        oauth_model = site_helper.getModel('oauth.%sOAuth2' % site_name)
        user_model = site_helper.getModel('User')

        token_url = oauth_ctrl.getAccessTokenUrl(authorization_code, oauth_ctrl.getState())

        response, content =  oauth_ctrl.getHtmlContent(token_url, oauth_ctrl.ACCESS_TOKEN_METHOD)

        if response.status == 200:
            try:
                access_token, access_expires = oauth_ctrl.pickAccessTokenAndExpires(content)
                open_id = oauth_ctrl.getOpenId(access_token)
                assert( len(str(open_id)) > 0 )
                item = oauth_model.getBy(open_id)
                if item: # 如果此用户已经用第三方帐号登录过
                    oauth_model.updateAccessToken(open_id, access_token, access_expires)
                    if item.Userid != 0: # 如果已绑定本站帐号
                        user = user_model.get(item.Userid)
                        site_helper.login(user, True)
                        return page_helper.redirectTo('/')
                    else: # 他登录过本站, 但是没有绑定帐号, 叫他绑定(注册)
                        if site_name == 'QQ':
                            return self.loginByQQOAuth(access_token, site_name)
                        else:
                            return self.redirectToLogin(access_token, oauth_ctrl.getState())
                else: # 否则这是第一次用第三方帐号登录本站, 叫他绑定(注册)帐号
                    oauth_model.insertBy(open_id, access_token, access_expires)
                    if site_name == 'QQ':
                        if session.is_login:
                            oauth_ctrl.bindUserid(access_token, session.user_id)
                            UserCtrl().checkConnectMedal(session.user_id)
                            page_helper.redirectTo('/')
                        else:
                            return self.loginByQQOAuth(access_token, site_name)
                    else:
                        return self.redirectToLogin(access_token, oauth_ctrl.getState())
            except:
                raise
                return page_helper.redirect404()
        else:
            print 'get access_token error, content is:'
            print content

    def redirectToLogin(self, access_token, state):
        return page_helper.redirectTo('/oauth/login?token=%s&state=%s' % (access_token, state))

    def loginByQQOAuth(self, access_token, site_name):
        session = site_helper.session
        oauth_ctrl  = site_helper.getController('oauth.' + site_name)
        oauth_model = site_helper.getModel('oauth.%sOAuth2' % site_name)
        user_model = site_helper.getModel('User')

        user_data = site_helper.storage({'activated': 'on' })
        user_data = oauth_ctrl.assignUserInfo(user_data, access_token)
        new_id = user_model.insert(user_data)
        new_user = user_model.get(new_id)
        if new_user and new_user.cover_url:
            user_model.update(new_id, {'small_portrait':'0 0 %d %d' % site_helper.getImageSize(new_user.cover_url)})
        oauth_ctrl.bindUserid(access_token, new_user.Userid)

        site_helper.login(new_user, True)
        UserCtrl().checkConnectMedal(session.user_id)
        page_helper.redirectTo('/')



