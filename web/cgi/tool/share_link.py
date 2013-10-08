#coding=utf-8
import model, time, web, MySQLdb, re
from site_helper import session
import site_helper

def saveShareUserid(handler):
    params = site_helper.getUrlParams()
    if params.has_key('shareUserid'):
        if params['shareUserid'].isdigit():
            session.share_user_id = int(params['shareUserid'])
            session.share_referer = site_helper.getEnv('HTTP_REFERER')

    return handler()
