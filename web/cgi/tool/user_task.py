#coding=utf-8
import site_helper
from site_helper import getModel
from controller import *

def check(handler):
    html = handler()
    if site_helper.session.is_login:
        _check(site_helper.session.user_id)
    return html

def _check(user_id):
    do_tash = DoTask()
    task_names = site_helper.getUrlParams().get('check_task','').split('|')
    task_names = [task_name.strip() for task_name in task_names if len(task_name.strip()) > 0]
    for task_name in task_names:
        do_tash.doStatusTask(user_id, task_name.strip())
    # 如果取消了绑定第三方帐号，就重新计算绑定勋章
    if 'oauth' in site_helper.getUrlParams().get('check_task',''):
        User().checkConnectMedal(user_id)

def doLoginTask(handler):
    if site_helper.session.is_login:
        DoTask().doLogin(site_helper.session.user_id)
    return handler()
