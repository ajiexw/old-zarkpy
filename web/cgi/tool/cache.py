#coding=utf-8
import model, time, web, MySQLdb, re
from site_helper import config, session

global cache_datas, cache_rule
cache_datas  = {}
cache_rule = ( #配置url缓存时间, 单位秒
    r'/book',     36000,
    r'/catalog',    36000,
    r'/pk',         36000,
    r'/',               0,
    r'/index',          0,
    r'/logout',         0,
    r'/admin.*',        0,
    r'/post.*',         0,
    r'/accounts.*',     0,
    r'/edit.*',         0,
    r'/tinymceimageinsert',     0,
    r'/test',           0,
    r'/aoaolaapi/.*',   0,
    r'/api/.*',         0,
    r'.*',              0,
)

def cachePage(handler):
    global cache_datas
    uri = web.ctx.env['REQUEST_URI']
    method = web.ctx.env['REQUEST_METHOD']
    retention = getCacheRetention(uri)
    now = time.time()

    if method == 'GET':
        # 如果处于缓存有效期
        if (now - getLastCachedTime(uri) < retention) and cache_datas.has_key(uri):
            html = cache_datas[uri]['html']
        else:
            html = handler()
            if retention > 0:
                cacheData(uri, html)
    else: # POST 请求不缓存
        html = handler()

    return html

def getCacheRetention(uri):
    '''获得某个uri的缓存时间, 单位秒, 0代表不缓存'''
    global cache_rule
    uri = uri.partition('?')[0]
    assert(len(cache_rule) % 2 == 0)

    for i in range(len(cache_rule)):
        if i % 2 == 0:
            assert(type(cache_rule[i]) is str)
            assert(type(cache_rule[i+1]) is int)
            matched = re.match(cache_rule[i], uri)
            if matched is not None and matched.group() == uri:
                return cache_rule[i+1]

    raise Exception('tool/cache.py can not match this request uri: %s' % uri)

def getLastCachedTime(uri):
    global cache_datas
    if cache_datas.has_key(uri) and cache_datas[uri].has_key('last_cached_time'):
        return cache_datas[uri]['last_cached_time']
    else:
        return 0

def cacheData(uri, html):
    global cache_datas
    cache_datas.setdefault(uri, {})
    cache_datas[uri]['last_cached_time'] = time.time()
    cache_datas[uri]['html'] = html

def clearAll():
    global cache_datas
    del cache_datas
    cache_datas = {}

def clear(uri):
    global cache_datas
    del cache_datas[uri]
    print 'clear cache:',uri

