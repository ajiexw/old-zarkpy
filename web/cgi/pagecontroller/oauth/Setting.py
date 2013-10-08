#coding=utf-8
import site_helper, web, page_helper

# ../../page/oauth/Setting.html

class Setting:

    def GET(self):
        i = web.input()
        model = site_helper.getModel('User')
        renren_model = site_helper.getModel('oauth.RenRenOAuth2')
        qq_model = site_helper.getModel('oauth.QQOAuth2')
        sina_model = site_helper.getModel('oauth.SinaOAuth2')

        session = site_helper.session
        if session.is_login:
            user_id = session.user_id
            user = model.get(user_id)
            user.renren_connections = renren_model.getsByUserid(user_id)
            user.qq_connections = qq_model.getsByUserid(user_id)
            user.sina_connections = sina_model.getsByUserid(user_id)
            sub_content = site_helper.page_render_nobase.oauth.Setting(user)
            return site_helper.page_render.user.Base3(user, sub_content)

        else:
            page_helper.redirectToLogin()

    def POST(self):
        i = web.input()
        for k,v in i.items():
            if k.startswith('share_'):
                model = site_helper.getModel('oauth.%sOAuth2' % k.split('_')[1])
                id    = k.split('_')[2]
                model.update(id, {'share': v})
        return page_helper.success('修改成功')
    
