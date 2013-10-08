#coding=utf-8
import  web, copy, site_helper, re
from DBHelper import DBHelper

class Model:
    table_name = 'Model'
    column_names = ['Categoryid']
    default_values = {}
    primary_key = None
    decorator = []
    get_all_env = {}

    def __init__(self):
        if self.primary_key == None:
            self.primary_key = self.table_name+'id'
        try:
            assert(type(self.table_name) is str)
            assert(len (self.table_name) > 0)
            assert(' ' not in self.table_name )
        except:
            print 'the table_name is:',self.table_name
            print 'and the class is:',self.__class__
            raise
        assert(type(self.primary_key) is str)
        assert(len (self.primary_key) > 0)
        assert(type(self.column_names) is list)
        assert(len (self.column_names) > 0)
        assert(type(self.default_values) is dict)

    '''assertInput函数主要用于验证insert的数据'''
    def _assertLongInput(self,data):
        '''使用_assertLongInput(obj['key'])，可以同时验证:obj.has_key(key),type(obj['key']) is long, obj['key'] >= 0'''
        try:
            assert(type(data) in [int,long] and data>=0)
        except:
            print '==========the value\'s type is %s,and the value is %s  ===============' % (type(data),data)
            raise

    def _assertStrInput(self,data):
        '''使用_assertStrInput(obj['key'])，可以同时验证:obj.has_key(key),type(obj['key']) is str, len(obj['key']) > 0'''
        try:
            assert(type(data) in [str,unicode] and len(data)>0)
        except:
            print '==========the value\'s type is %s,and the value is %s  ===============' % (type(data),data)
            raise

    def _getDB(self):
        return DBHelper()

    def insert(self,data):
        data = self._formatInsertData(data)
        data = self._removeNone(data)
        assert(data is not None)
        self._insertValidate(data)
        insert_cols =   [c       for c in self.column_names if c in data.keys()]
        insert_values = [data[c] for c in self.column_names if c in data.keys()]
        query = 'insert into %s (%s) values (%s)' % (self.table_name,','.join(insert_cols),','.join(len(insert_cols)*['%s']))
        return self._getDB().insert(query,tuple(insert_values))

    def replaceInsert(self,data):
        data = self._formatInsertData(data)
        data = self._removeNone(data)
        assert(data is not None)
        self._insertValidate(data)
        insert_cols =   [c       for c in self.column_names if c in data.keys()]
        insert_values = [data[c] for c in self.column_names if c in data.keys()]
        query = 'replace into %s (%s) values (%s)' % (self.table_name,','.join(insert_cols),','.join(len(insert_cols)*['%s']))
        return self._getDB().insert(query,tuple(insert_values))

    def update(self,itemid,data):
        try:
            data = self._formatUpdateData(data)
            data = self._removeNone(data)
            assert(data is not None)
            self._updateValidate(data)
            update_cols =   [c       for c in self.column_names if c in data.keys()]
            update_values = [data[c] for c in self.column_names if c in data.keys()]
            assert(len(update_cols) == len(update_values) > 0 )
            query = 'update '+self.table_name \
                    + ' set '+','.join([c+'=%s' for c in update_cols]) \
                    + ' where '+self.table_name+'id=%s'
            self._getDB().update(query,(update_values + [itemid]))
        except:
            print 'ERROR INFO:'
            print 'data is :', data
            raise

    def delete(self,itemid):
        self._getDB().delete('delete from '+self.table_name+' where '+self.table_name+'id=%s',itemid)

    def _spliceQuery(self, env):
        query_string = 'select '
        argv = []
        if env is None: env = self.get_all_env
        assert(type(env) in [dict, web.Storage])

        if env.get('select', None):
            query_string += env['select'] + ' '
        else:
            if env.get('distinct',None):
                query_string += 'distinct '
            query_string += '* '

        if env.get('from', None):
            query_string += 'from '+ env['from'] + ' '
        else:
            query_string += 'from '+ self.table_name + ' '

        if env.get('where',None) != None: # { 'where': ('title=%s',['test']) }
            assert( type(env['where']) in (tuple,list) and  len(env['where']) == 2 )
            assert( type(env['where'][0]) is str )
            assert( type(env['where'][1]) in (tuple,list) )
            query_string += ' where ' + env['where'][0] + ' '
            argv.extend(env['where'][1])

        if env.get('orderby',None):
            query_string += ' order by '+env.get('orderby')

        if env.get('limit',None):
            assert( type(env['limit']) in (tuple,list) and  len(env['limit']) == 2 )
            #assert( (type(env['limit'][0]) and type(env['limit'][1])) in [int,long] )
            query_string += ' limit %s,%s'
            argv.append(env['limit'][0])
            argv.append(env['limit'][1])

        return query_string, argv

    def getAll(self,env=None):
        query_string, argv = self._spliceQuery(env)
        return self._getDB().fetchSome(query_string,argv)

    def getCount(self,env={}):
        new_env = self._copyData(env)
        new_env['select'] = 'count(*)' 
        # mysql 语法中, count(*) 和 limit 不能一起用
        if new_env.has_key('limit'):
            del new_env['limit']
        query_string, argv = self._spliceQuery(new_env)
        return self._getDB().fetchFirst(query_string, argv)

    def get(self,itemid):
        return self._getDB().fetchOne('select * from '+self.table_name+' where '+self.table_name+'id=%s limit 1',itemid)

    def gets(self,ids):
        assert(type(ids) is list)
        if len(ids) > 0:
            where = ' or '.join([self.table_name+'id=%s'] * len(ids))
            return self._getDB().fetchSome('select * from '+self.table_name+' where ' + where, ids)
        else:
            return []

    def getOneByWhere(self,where,argv=[]):
        assert(type(argv) in [list,tuple]) #getOneByWhere的第二个参数类型应该是list
        return self._getDB().fetchOne('select * from '+self.table_name+' where '+where+' limit 1',argv)

    def _formatInsertData(self,data):
        return data

    def _formatUpdateData(self,data):
        return data

    def _insertValidate(self,data):
        pass

    def _updateValidate(self,data):
        pass

    def _removeNone(self,data):
        ret_data = self._copyData(data)
        for k,v in data.items():
            if v is None:
                del ret_data[k]
        return ret_data

    def _copyData(self, data):
        ret_data = web.Storage({})
        for k in data.keys():
            ret_data[k] = copy.copy(data[k])
        return ret_data

    def getDecoratorAttr(self,attr):
        '''获得带装饰的函数'''
        if hasattr(self, '_decorator_model'):
            assert(self._decorator_model is not None)
            return getattr(self._decorator_model, attr)
        else:
            return getattr(self,attr)

    def createTable(self):
        assert(len(self.table_name)>0)
        assert(len(self.table_template)>0)
        assert(not DBHelper().isTableExists(self.table_name))
        try:
            db = site_helper.getDB()
            formated_creat_query = self._getCreateTableQuery()
            db.cursor().execute(formated_creat_query)
            db.commit()
        except:
            print formated_creat_query
            raise

    def increaseCreateTable(self):
        '''根据table_template在原有表上添加新字段, 但不添加新的索引.'''
        assert(len(self.table_name)>0)
        assert(len(self.table_template)>0)
        assert(DBHelper().isTableExists(self.table_name))
        def getColumnsFromSQL(sql):
            sql = sql.partition('(')[2].rpartition(')')[0].replace('\n', ' ').replace('\r', ' ')
            columns = []
            column = []
            bracket_count = 0
            for c in sql+',':
                if c == '(':
                    bracket_count += 1
                    column.append(c)
                elif c == ')':
                    bracket_count -= 1
                    column.append(c)
                elif bracket_count == 0 and c==',':
                    column = ''.join(column)
                    if column.strip().split()[0].lower() not in ['key', 'primary','unique'] and column.strip().split('(')[0].lower() not in ['key', 'primary','unique']:
                        columns.append((column.strip().split()[0], column))
                    column = []
                else:
                    column.append(c)
                if bracket_count < 0:
                    raise Exception('table template is invalid. model name is: ' + self.table_name)
            return columns
        try:
            exists_columns = site_helper.getDBHelper().getTableColumns(self.table_name)
            formated_creat_query = self._getCreateTableQuery()
            columns = getColumnsFromSQL(formated_creat_query)
            db = site_helper.getDB()
            for column_name, query  in columns:
                if column_name.lower() not in map(str.lower, exists_columns):
                    try:
                        db.cursor().execute('alter table %s add %s' % (self.table_name, query))
                    except:
                        print 'alter query is:'
                        print 'alter table %s add %s' % (self.table_name, query)
                        raise
            db.commit()
        except:
            print 'formated creat query is:'
            print formated_creat_query
            raise

    def _getCreateTableQuery(self):
        ret_query = self.table_template
        for variable in re.compile('{\$\w+}').findall(self.table_template):
            ret_query = ret_query.replace(variable,getattr(self,variable[2:-1]))
        return ret_query

    def toHtml(self, paras={}):
        '''读取数据，然后生成一定格式的html，至于外观则留给css和js来渲染'''
        raise Exception('调用了不应该调用的函数，请确保此model overwrite了toHtml函数')

    #table_template变量名不能以下划线"_"开头，因为_开头的“类静态”数据将不会被overwrite,也就是说每个py文件会调用自己的"类静态"变量，而不使用子类的.
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Categoryid int unsigned not null default 0,
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
