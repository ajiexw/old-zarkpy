#!/usr/bin/env python
#coding=utf-8

print 'Connecting DataBase'
import web, os
from tool import nginx_uwsgi
import site_helper
import pagecontroller, editorcontroller, api, datetime, random
from urllib import quote as urlencode

web.config.debug = False # the default value is true and sessions doesn't work in debug mode
web.config.session_parameters['timeout'] = 86400

urls = (
    # error
    '/cgi/js/(.*)','pagecontroller.Error',
    '/cgi/css/(.*)','pagecontroller.Error',
    '/cgi/img/(.*)','pagecontroller.Error',
    '/cgi/swf/(.*)','pagecontroller.Error',
    '/cgi/plugins/(.*)','pagecontroller.Error',
    '/cgi/sessions/(.*)','pagecontroller.Error',
    '/cgi/html/(.*)','pagecontroller.Error',

    # users
    '/cgi/user/(\d*)','pagecontroller.user.User', # pagecontroller/user/User.py
    '/cgi/register','pagecontroller.user.Register', # pagecontroller/user/Register.py
    '/cgi/register-activate','pagecontroller.user.Activate', # pagecontroller/user/Activate.py
    '/cgi/login','pagecontroller.user.Login', # pagecontroller/user/Login.py
    '/cgi/logout','pagecontroller.user.Logout', # pagecontroller/user/Logout.py
    '/cgi/noactivate','pagecontroller.user.NoActivate', # pagecontroller/user/NoActivate.py
    '/cgi/sendacode','pagecontroller.user.SendACode', # pagecontroller/user/SendACode.py

    '/cgi/accounts','pagecontroller.user.Modify', # pagecontroller/user/Modify.py
    '/cgi/accounts/portrait','pagecontroller.user.ModifyPortrait', 
            # pagecontroller/user/ModifyPortrait.py
    '/cgi/accounts/password','pagecontroller.user.ModifyPassword', 
            # pagecontroller/user/ModifyPassword.py
    '/cgi/accounts/forget','pagecontroller.user.ForgetPassword', 
            # pagecontroller/user/ForgetPassword.py
    '/cgi/notice','pagecontroller.user.Notice', # pagecontroller/user/Notice.py


    # pages
    '/cgi/index','pagecontroller.Index', # pagecontroller/Index.py
    '/cgi/success','pagecontroller.Success', # pagecontroller/Success.py
    '/cgi/failed','pagecontroller.Failed', # pagecontroller/Failed.py
    '/cgi/alipay','pagecontroller.Alipay', # pagecontroller/Alipay.py
    '/cgi/alipay-return','pagecontroller.AlipayReturn', # pagecontroller/AlipayReturn.py

    # user post
    '/cgi/post/insert','pagecontroller.Insert', # pagecontroller/Insert.py
    '/cgi/post/replaceinsert','pagecontroller.ReplaceInsert', # pagecontroller/ReplaceInsert.py
    '/cgi/post/delete','pagecontroller.Delete', # pagecontroller/Delete.py
    '/cgi/post/update','pagecontroller.Update', # pagecontroller/Update.py
    '/cgi/post/comment','pagecontroller.Comment', # pagecontroller/Comment.py
    '/cgi/post/userimage','pagecontroller.UserImage', # pagecontroller/UserImage.py

    # admin user
    '/cgi/admin','editorcontroller.Index', # editorcontroller/Index.py
    '/cgi/admin/register','editorcontroller.RegisterAdmin', # editorcontroller/RegisterAdmin.py
    '/cgi/admin/logout','editorcontroller.LogoutAdmin', # editorcontroller/LogoutAdmin.py
    '/cgi/admin/login','editorcontroller.LoginAdmin', # editorcontroller/LoginAdmin.py
    '/cgi/admin/update','editorcontroller.Update', # editorcontroller/Update.py
    '/cgi/admin/insert','editorcontroller.Insert', # editorcontroller/Insert.py
    '/cgi/admin/delete','editorcontroller.Delete', # editorcontroller/Delete.py
    '/cgi/admin/select','editorcontroller.Select', # editorcontroller/Select.py get json datas
    '/cgi/admin/site-config','editorcontroller.SiteConfig',
            # editorcontroller/SiteConfig.py

    # admin editor page
    '/cgi/admin/imagecenter/pagecontent','editorcontroller.imagecenter.PageContent', 
            # editorcontroller/imagecenter/PageContent.py
    '/cgi/admin/manage-feedback','editorcontroller.ManageFeedback', # editorcontroller/ManageFeedback.py 

    # admin page content

    '/cgi/admin/pagecontent-index-cycle','editorcontroller.content.IndexCycle', 
            # editorcontroller/content/IndexCycle.py
    '/cgi/admin/pagecontent-sidebar','editorcontroller.content.Sidebar', 
            # editorcontroller/content/Sidebar.py
    # api
    '/api/delete','api.Delete', # api/Delete.py
    '/api/profile','api.Profile', # api/Profile.py
    '/api/getuseridbyname','api.GetUseridByName', # api/GetUseridByName.py
    '/api/manage-notice','api.ManageNotice', # api/ManageNotice.py

    # others
    '/cgi/admin/leveltable','editorcontroller.LevelTable', # editorcontroller/LevelTable.py
    '/cgi/admin/leveltable/(.+)','editorcontroller.LevelTable', # editorcontroller/LevelTable.py
    '/cgi/admin/pagecontent','editorcontroller.PageContent', # editorcontroller/PageContent.py
    '/cgi/admin/pagecontent/(.+)','editorcontroller.PageContent', # editorcontroller/PageContent.py
    '/cgi/admin/send-mail','editorcontroller.SendMail', # editorcontroller/SendMail.py
    '/cgi/admin/modify-password','editorcontroller.ModifyPassword', # editorcontroller/ModifyPassword.py
    '/cgi/tinymceimageinsert','editorcontroller.TinymceImageInsert', # editorcontroller/TinymceImageInsert.py
    '/cgi/test','pagecontroller.Test', # pagecontroller/Test.py

    # oauth
    '/cgi/oauth/authorize','pagecontroller.oauth.Authorize', # pagecontroller/oauth/Authorize.py
    '/cgi/oauth/login','pagecontroller.oauth.Login', # pagecontroller/oauth/Login.py
    '/cgi/oauth/setting','pagecontroller.oauth.Setting', # pagecontroller/oauth/Setting.py

    # others
    '/cgi/about/(.+)','pagecontroller.about.About', # pagecontroller/about/About.py
    '/cgi/weixin','pagecontroller.weixin.Weixin', # pagecontroller/weixin/Weixin.py

    #'','',
)

# init app
app = web.application(urls, {'pagecontroller':pagecontroller, 'editorcontroll-commenter':editorcontroller})

# init session
site_helper.session = web.session.Session(app, web.session.DiskStore(site_helper.config.SESSION_PATH), initializer={'is_login': False,'is_admin':False,'user_id': 0,'admin_user_id':0, 'user_name': '','admin_user_name':''})

# init template
from tool import page_module_datas
template_functions = {
    'str':          str,
    'int':          int,
    'len':          len,
    'type':         type,
    'dir':          dir,
    'map':          map,
    'hasattr':      hasattr,
    'getattr':      getattr,
    'web_ctx':      web.ctx,
    'input':        web.input,
    'session':      site_helper.session,
    'page_module_datas':page_module_datas,
    'config':       site_helper.config,
    'site_helper':  site_helper,
    'ipToStr':  site_helper.ipToStr,
    'urlencode':  urlencode,
    'getNow':   datetime.datetime.now,
    'getUrlParams': site_helper.getUrlParams,
    'randint': random.randint,
    'datetime': datetime.datetime,
}

# 为了能在page_module中使用page_module, 所以这里有两次调用
page_module_path = site_helper.config.APP_ROOT_PATH + 'web/cgi/page/module'
assert os.path.exists(page_module_path)
template_functions['page_module'] = web.template.render(loc=page_module_path, globals=template_functions)
template_functions['page_module'] = web.template.render(loc=page_module_path, globals=template_functions)
site_helper.page_module = template_functions['page_module']

page_sidebar_path = site_helper.config.APP_ROOT_PATH + 'web/cgi/page/sidebar'
assert os.path.exists(page_sidebar_path)
template_functions['page_sidebar'] = web.template.render(loc=page_sidebar_path,globals=template_functions)
page_render_path = site_helper.config.APP_ROOT_PATH + 'web/cgi/page'
assert os.path.exists(page_render_path)
site_helper.page = web.template.render(loc=page_render_path, base='Base', globals=template_functions)
site_helper.page_render_nobase = web.template.render(loc=page_render_path, globals=template_functions)

page_render_about_path = site_helper.config.APP_ROOT_PATH + 'web/cgi/page/about'
assert os.path.exists(page_render_about_path)
site_helper.page_render_about = web.template.render(loc=page_render_about_path, base='Base', globals=template_functions)

editor_render_path = site_helper.config.APP_ROOT_PATH + 'web/cgi/editor'
assert os.path.exists(editor_render_path)
site_helper.editor_render = web.template.render(loc=editor_render_path, base='Base', globals=template_functions)
site_helper.editor_render_nobase = web.template.render(loc=editor_render_path, globals=template_functions)

# add processor
from tool import validate, auto_login, cache, user_task, share_link, profiler, judge_device
app.add_processor(profiler.profiler)
app.add_processor(user_task.check)
app.add_processor(user_task.doLoginTask)
app.add_processor(validate.validate)
app.add_processor(validate.forbiddenIP)
app.add_processor(auto_login.login_by_cookie)
app.add_processor(share_link.saveShareUserid)

app.notfound = lambda:web.seeother('/html/404.html')

if __name__ == "__main__":
    from tool import init_database
    init_database.initTables()
    init_database.initDatas()
    print 'Ok'
    app.run()
