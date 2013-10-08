import site_helper, web

def login_by_cookie(handler):
    if not site_helper.session.is_login:
        email = web.cookies().get('email','')
        md5password = web.cookies().get('md5password','')
        if len(email) > 0 and len(md5password) > 0:
            user = site_helper.getModel('User').getOneByWhere('email=%s and password=%s', [email, md5password])
            if user is not None:
                site_helper.login(user)
    return handler()
