#coding=utf8
import site_helper, sys, glob, re

def _sort(file_paths, preference_list):
    '''把file_paths中的preference_list值排到前面来，满足自动创建数据库表时的外键依赖'''
    ret_pre_paths = []
    ret_other_paths = []
    for file_path in file_paths:
        model_name = file_path.rpartition('/')[2].rpartition('.')[0]
        if model_name in preference_list:
            ret_pre_paths.append(file_path)
        else:
            ret_other_paths.append(file_path)
    return ret_pre_paths + ret_other_paths

def initTables():
    ''' 用model和advmodel中名字不已“_”开头的model的table_template新建表 '''
    exists_tables = _getExistsTables()

    for dir_name in 'model','model/oauth':
        file_paths = glob.glob(site_helper.config.APP_ROOT_PATH+('web/cgi/%s/*.py' % dir_name))
        file_paths = _sort(file_paths,['Page'])
        for file_path in file_paths:
            model_name = file_path.rpartition('/')[2].rpartition('.')[0]
            if model_name[0] != '_': #去掉__init__等,任何hasattr(module,'__init__')都等于True
                try:
                    __import__(dir_name.replace('/', '.').strip('.')+'.'+model_name)
                except:
                    print 'try to import %s' % (dir_name.replace('/', '.').strip('.')+'.'+model_name)
                    raise
                if hasattr(sys.modules[dir_name.replace('/', '.').strip('.')], model_name):
                    model_class = getattr(sys.modules[dir_name.replace('/', '.').strip('.')],model_name)
                    if hasattr(model_class, 'table_template') and len(model_class.table_name) > 0:
                        try:
                            model_instance = model_class()
                            if model_class.table_name not in exists_tables:
                                model_instance.createTable()
                            else:
                                model_instance.increaseCreateTable()
                        except:
                            print 'model_class is:', model_class
                            print 'table_name is:', model_class.table_name
                            raise

def _getExistsTables():
    db = site_helper.getDB()
    cursor = db.cursor()
    cursor.execute('show tables')
    return [one[0].encode('utf-8') for one in cursor.fetchall()]

def initDatas():
    query = open(site_helper.config.APP_ROOT_PATH + 'web/cgi/tool/init_datas.sql').read().strip()
    assert('insert' not in query.lower()) # 请用replace, 否则会导致重复插入数据
    site_helper.getDBHelper().executeQuery(query)

