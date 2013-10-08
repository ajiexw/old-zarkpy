#coding=utf-8
from Decorator import Decorator
import web

class Cache(Decorator):
    '''example: decorator = [('Cache',{'clear_functions':'all'})]'''
    '''env = {'cache':True} '''
    rewrite_functions = ['getAll', 'update', 'insert', 'delete']
    cache_datas = {}

    def getAll(self,env=None):
        if env is None: env = {}
        assert( type(self.arguments.clear_functions) is str and len(self.arguments.clear_functions)>0 )
        if env.get('cache', None):
            table_name = self.getModelTableName()
            env_hash = self.__envToHash(env)
            Cache.cache_datas.setdefault(table_name, {})
            if not Cache.cache_datas[table_name].has_key(env_hash):
                Cache.cache_datas[table_name][env_hash] = self.model.getAll(env)
            return Cache.cache_datas[table_name][env_hash]
        else:
            return self.model.getAll(env)

    def insert(self, data):
        if self.arguments.clear_functions == 'all' or 'insert' in self.arguments.clear_functions.split(' '):
            table_name = self.getModelTableName()
            if Cache.cache_datas.has_key(table_name):
                del Cache.cache_datas[table_name]
        return self.model.insert(data)

    def update(self, item_id,  data):
        if self.arguments.clear_functions == 'all' or 'update' in self.arguments.clear_functions.split(' '):
            table_name = self.getModelTableName()
            if Cache.cache_datas.has_key(table_name):
                del Cache.cache_datas[table_name]
        return self.model.update(item_id, data)

    def delete(self, item_id):
        if self.arguments.clear_functions == 'all' or 'delete' in self.arguments.clear_functions.split(' '):
            table_name = self.getModelTableName()
            if Cache.cache_datas.has_key(table_name):
                del Cache.cache_datas[table_name]
        return self.model.delete(item_id)

    def __envToHash(self, env):
        '''计算hash值要同时考虑到env和web.input()两个变量'''
        ret_hash = []

        keys = env.keys()
        keys.sort()
        for k in keys:
            ret_hash.append('%s\t%s' % (k, str(env[k])))

        i = web.input()
        keys = i.keys()
        keys.sort()
        for k in keys:
            ret_hash.append('%s\t%s' % (k, i[k].encode('utf-8')))

        return '\n'.join(ret_hash)

