#coding=utf-8
import web, json
from urllib import quote 

def JsonRender(data):
    data = _removeUnjson(data)
    return json.dumps(data)

def _removeUnjson(data):
    '''过滤掉不能json化的数据'''
    newData = {}
    for k,v in data.item():
        if type(v) in [int,long,str,bool]:
            newData[k] = v
    return newData

def refresh(referer=None):
    if referer is None:
        referer = web.input().get('referer', None)
    if referer is None:
        referer = web.ctx.env['HTTP_REFERER']
    web.seeother(referer)

def refreshParent():
    return '<script>window.parent.location.reload();</script>'

def close():
    return '<script>window.close();</script>'

def back():
    return '<script>history.go(-1);</script>'

def redirect404():
    web.seeother('/404.html')

def getSidebarHtml(*sidebars):
    from site_helper import page_render_nobase
    return ''.join([str(getattr(page_render_nobase.sidebar, name)(args)) for (name, args) in sidebars])

def redirectToLogin(referer=None):
    if referer is None and web.ctx.env.has_key('HTTP_REFERER'):
        url = '/login?referer=%s' % web.ctx.env['HTTP_REFERER']
    elif referer != '':
        url = '/login?referer=%s' % referer
    else:
        url = '/login'
    web.seeother(url)

def redirectTo(url):
    referer = web.input().get('referer', None)
    if url:
        web.seeother(url)
    else:
        web.seeother(referer)

def success(msg, referer=None):
    if referer is None:
        referer = web.ctx.env['HTTP_REFERER']
    web.seeother('/success?msg=%s&referer=%s' % ( quote(msg),  referer))

def failed(msg, referer=None):
    if type(msg) == unicode:
        msg = msg.encode('utf-8')
    if referer is None:
        referer = web.ctx.env['HTTP_REFERER']
    web.seeother('/failed?msg=%s&referer=%s' % ( quote(msg),  referer))
