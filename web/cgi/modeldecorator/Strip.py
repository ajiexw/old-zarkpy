#coding=utf-8
from Decorator import Decorator
import copy, web

class Strip(Decorator):
    '''example: decorator = [('Strip',{'attrs':['title','url']})]'''
    rewrite_functions = ['insert','update']

    def insert(self, data):
        assert( type(self.arguments.attrs) is list and len(self.arguments.attrs)>0 )
        return self.model.insert(self.__stripAttr(data))

    def update(self,itemid, data):
        assert( type(self.arguments.attrs) is list and len(self.arguments.attrs)>0 )
        self.model.update(itemid,self.__stripAttr(data))

    def __stripAttr(self,data):
        ret_data = self.__copyData(data)
        for attr in self.arguments.attrs:
            if ret_data.has_key(attr):
                ret_data[attr] = ret_data[attr].strip()
        return ret_data

    def __copyData(self, data):
        ret_data = web.Storage({})
        for k in data.keys():
            ret_data[k] = copy.deepcopy(data[k])
        return ret_data

