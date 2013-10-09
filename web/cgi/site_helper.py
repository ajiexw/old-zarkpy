#coding=utf-8
import web, MySQLdb, glob, sys, os, socket, struct, copy as _copy
from urllib import quote as _quote, unquote as _unquote
from urlparse import urlparse
from PIL import Image

config = web.Storage({
        'APP_ROOT_PATH' : '/opt/songshu/',
        'APP_PORT' : 10000, # the port of application
        'SESSION_PATH' : '/opt/songshu/web/sessions',
        'DB_HOST' : '127.0.0.1',
        'DB_DATABASE' :'songshu',
        'DB_USER' : 'songshu',
        'DB_PASSWORD' :'*******************************',
        'DB_CHARSET' : 'utf8',
        'CGI_PATH' : '/opt/songshu/web',
        'UPLOAD_IMAGE_PATH' : '/opt/songshu/web/img/upload/', # relative to system root
        'UPLOAD_IMAGE_URL'  : '/img/upload/', # relative to site root
        'GOODS_COVER_PATH' : '/opt/songshu/web/img/goods/cover/',
        'GOODS_COVER_URL'  : '/img/goods/cover/',
        'USER_COVER_PATH': '/opt/songshu/web/img/user/cover/',
        'USER_COVER_URL' : '/img/user/cover/',
        'USER_IMAGE_PATH': '/opt/songshu/web/img/user/userupload/',
        'USER_IMAGE_URL' : '/img/user/userupload/',
        'IS_TEST': False,
        'MODIFY_TIME_LIMIT': 24 * 3600,
        'COOKIE_EXPIRES': 365 * 24 * 3600,
        'ERROR_LOG_PATH' :  '/opt/songshu/log/error.log',
        'FOOT_LOG_PATH' :   '/opt/songshu/log/foot.log',   # 访问log, 一般情况下可以不使用
        'HOST_NAME' : 'http://me.songshu.com',
})

global session,page_render,page_render_nobase,editor_render,editor_render_nobase,page_module
session = page_render = page_render_nobase = editor_render = editor_render_nobase = page_module = None

def getDirModules(dir_path, dir_name, except_files=[]):
    ''' import modules in model folder.
        only use in __init__.py file of direct subfolders of cgi folder.
    '''
    ret_modules = []
    for file_path in glob.glob(dir_path+'/*.py'):
        file_name = file_path.rpartition('/')[2].rpartition('.')[0]
        if file_name not in except_files:
            __import__(dir_name.strip('.')+'.'+file_name)
            if file_name in dir(getattr(sys.modules[dir_name.strip('.')],file_name)):
                ret_modules.append((file_name,getattr(getattr(sys.modules[dir_name.strip('.')],file_name),file_name)))
    return ret_modules

def getModel(model_name, decorator=[]):
    '''getModel函数从model中找到名称为model_name的model，然后得到他的一个实例并用modeldecorator装饰后返回. '''
    #此import语句不能放到函数外面去,否则会与其它module嵌套循环import
    import model, modeldecorator 
    try:
        for name in model_name.split('.'):
            assert( hasattr(model, name) )
            model = getattr(model, name)
    except:
        print 'the name is', name
        print 'the model name is', model_name
        raise
    model = model()
    for d,arguments in model.decorator + decorator:
        if not config.IS_TEST or getattr(modeldecorator,d).TEST: # 如果不是测试, 或者是测试且这个装饰需要测试
            model = getattr(modeldecorator,d)(model,arguments)
    return model

def getController(ctrl_name):
    import controller
    try:
        for name in ctrl_name.split('.'):
            assert( hasattr(controller, name) )
            controller = getattr(controller, name)
    except:
        print 'the name is', name
        print 'the controller name is', ctrl_name
        raise
    return controller()

def login(user, remember_me=False):
    global session
    session.user_id = user.Userid
    session.is_login = True
    session.activated = user.activated
    session.user_name = user.username
    # remember me
    if remember_me:
        web.setcookie('myid',  user.Userid, config.COOKIE_EXPIRES )
        web.setcookie('email', user.email, config.COOKIE_EXPIRES )
        web.setcookie('md5password',  user.password, config.COOKIE_EXPIRES )
        web.setcookie('name',  user.username, config.COOKIE_EXPIRES )
    else:
        web.setcookie('myid',  user.Userid )
        web.setcookie('email', user.email )
        web.setcookie('name',  user.username )
        #web.setcookie('md5password',  '' ) 不能set空, 否则会消除remember_me的效果

    getModel('User').increaseLoginCount(user.Userid)
    
def logout():
    global session
    session.is_login  = False
    session.activated = 'off'
    session.user_id   = 0
    session.user_name = ''
    web.setcookie('email',  '')
    web.setcookie('md5password',  '')

def loginAdmin(user):
    global session
    session.is_admin = True
    session.admin_user_id = user.AdminUserid
    session.admin_user_name = user.name

def logoutAdmin():
    global session
    session.is_admin = False
    session.admin_user_id = 0
    session.admin_user_name = ''

def getDB():
    return MySQLdb.connect(host=config.DB_HOST,user=config.DB_USER,passwd=config.DB_PASSWORD,charset=config.DB_CHARSET,db=config.DB_DATABASE)

def getDBHelper():
    from model import DBHelper
    return DBHelper()

def storage(data={}):
    return web.Storage(data)

def filterNone(l):
    return [i for i in l if i is not None]

mysql_errors = web.Storage({
        'IntegrityError' : MySQLdb.IntegrityError, # 主键冲突
})

def deepCopy(obj):
    '''已知问题, 不能对post的file进行deepCopy'''
    return _copy.deepcopy(obj)

def copy(obj):
    return _copy.copy(obj)

def extend(old, new):
    ret = deepCopy(old)
    for k,v in new.items():
        if not ret.has_key(k):
            ret[k] = v
    return storage(ret)

def getEnv(key):
    if web.ctx.env.has_key(key):
        return web.ctx.env[key]
    else:
        return ''

def setEnv(key, value):
    web.ctx.env[key] = value

def rmEnv(key):
    if web.ctx.env.has_key(key):
        del web.ctx.env[key] 

def ipToInt(ip_str):
    return struct.unpack('=L',socket.inet_aton(ip_str))[0]

def ipToStr(ip_int):
    return socket.inet_ntoa(struct.pack('=L',ip_int))

def getIntIP():
    return ipToInt(session.ip)

def getRelation(item, relation_name):
    if item.has_key(relation_name+'id'):
        return getModel(relation_name).get(item[relation_name+'id'])
    else:
        return None

def setRelations(items, *relations):
    for relation in relations:
        if relation.count(' '):
            k1, k2  = relation.split(' ')
        else:
            k1 = k2 = relation

        model = getModel(k1)
        assert(model is not None)
        if type(items) is not list:
            items = [items]
        for item in items:
            if item is not None and item.has_key(k1+'id'):
                item[k2] = model.get(item[k1+'id'])

def quote(string):
    try:
        if type(string) is unicode:
            string = string.encode('utf-8')
        return _quote(string)
    except:
        print 'quoted string is:', string
        raise

def unquote(string):
    if type(string) is unicode:
        string = string.encode('utf-8')
    return _unquote(string)

def getUrlParams(url=None):
    if url is None:
        url = getEnv('REQUEST_URI')
    url = urlparse(url)
    return dict([(part.split('=')[0], _unquote(part.split('=')[1])) for part in url[4].split('&') if len(part.split('=')) == 2])

def calcTimeInterval(late, early):
    '''也可以理解为(now, created)'''
    diff = late - early
    if diff.days > 30:
        return '%d月%d日' % (early.month, early.day)
    elif diff.days > 0:
        return '%s天前' % diff.days
    elif diff.seconds > 3600:
        return '%s小时前' % (diff.seconds / 3600)
    elif diff.seconds > 600:
        return '%s分钟前' % (diff.seconds / 60)
    else:
        return '刚刚'

def calcTimeIntervalClass(late, early):
    diff = late - early
    if diff.days > 7:
        return 'gray'
    elif diff.days > 0:
        return 'green'
    else:
        return 'red'

def calcTimeIntervalSimple(late, early):
    diff = late - early
    if diff.days > 30:
        return None
    elif diff.days > 0:
        return '%sdays' % diff.days
    elif diff.seconds > 3600:
        return '%sh' % (diff.seconds / 3600)
    elif diff.seconds > 600:
        return '%smin' % (diff.seconds / 60)
    else:
        return '刚刚'

def getUnicodeSummary(string, length):
    if len(string.decode('utf-8')) > length:
        content_summary = string.decode('utf-8')[:length].encode('utf-8')
    else:
        content_summary = None
    return content_summary

def getImageSize(image_url):
    path = config['APP_ROOT_PATH'] + 'web' + image_url
    if os.path.exists(path):
        try:
            return Image.open(path).size
        except:
            return 0, 0
    else:
        return 0, 0

def doStatusTask(user_id, task_name):
    from controller import DoTask
    DoTask().doStatusTask(user_id, task_name)

def splitAndStrip(string, chars=' '):
    return [s.strip() for s in string.split(chars) if len(s.strip()) > 0]

def resizeImage(url, resize):
    from controller import ImageConvert
    return ImageConvert().resize(url, resize)

def getSmallPortrait(cover_url,  small_portrait, size):
    from controller import ImageConvert
    return ImageConvert().getSmallPortrait(cover_url, small_portrait, size)

def getBigPortrait(cover_url,  big_portrait, width, height):
    from controller import ImageConvert
    return ImageConvert().getBigPortrait(cover_url, big_portrait, width, height)

def toUrl(*argvs):
    return '/' + '/'.join(filter(lambda x:len(x)>0, argvs)).rstrip('/')

def getHtmlContent(url, headers=None):
    import httplib2
    h = httplib2.Http()
    h.timeout = 60 # 单位秒
    response, content = h.request(url, headers = headers)
    return response, content

def printDictOrList(d, index=0):
    if type(d) is dict or type(d) is web.Storage:
        for k, v in d.items():
            print ' ' * index + k, ':'
            printDictOrList(v, index+4)
    elif type(d) is list or type(d) is tuple:
        for i in d:
            printDictOrList(i, index+4)
    else:
        print ' ' * index + str(d)

def getSiteConfig(key):
    model = getModel('SiteConfig')
    item = model.getOneByWhere('name=%s', [key])
    return item.value if item else ''


def getLovelys():
    users = filterNone(map(getModel('User').get, getModel('PageContent').getModelids('aoaoquan','lovely')))
    return users

def getRecommendNews():
    level_model = getModel('LevelTable')
    levels = level_model.getLevelsByPage('gift-recommend-news')
    return level_model.levelsToList(levels)
