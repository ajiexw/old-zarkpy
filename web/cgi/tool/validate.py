#coding=utf-8
import site_helper, web, page_helper

def validate(handler):
    request_uri = site_helper.getEnv('REQUEST_URI')

    is_login  = site_helper.session.get('is_login', False)
    is_admin  = site_helper.session.get('is_admin', False)
    activated = site_helper.session.get('activated', 'off') == 'on'

    # 禁止非admin用户访问admin页面
    if request_uri.startswith('/admin') and request_uri != '/admin/login' and (not is_admin):
        return web.seeother('/admin/login')

    # 禁止未登录用户post数据
    if request_uri.startswith('/post') and (not is_login):
        # 允许flash不登录
        if request_uri == '/post/userimage':
            pass
        else:
            return page_helper.redirectToLogin()

    # 禁止未验证邮件的用户post数据
    if request_uri.startswith('/post') and (not activated):
        # 允许flash及第三方登录不验证
        if request_uri == '/post/userimage':
            pass
        elif 'model_name=oauth' in request_uri:
            pass
        else:
            referer = site_helper.getEnv('HTTP_REFERER')
            return web.seeother('/noactivate?referer=%s' % referer)

    return handler()

def forbiddenIP(handler):
    content = site_helper.getModel('LevelTable').getContentByPage('forbidden-ip')
    ip = site_helper.session.ip
    for l in content.split('\n'):
        if ip == l.strip():
            return None
    else:
        return handler()

