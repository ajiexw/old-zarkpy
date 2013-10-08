#coding=utf-8
from Decorator import Decorator
import copy, web

class NoNone(Decorator):
    '''
        ('NoNone',{'attrs':['title','url']}),
    '''
    rewrite_functions = ['insert']

    def insert(self,data):
        assert( type(self.arguments.attrs) is list and len(self.arguments.attrs)>0 )
        self.__NoNoneValidate(data)
        return self.model.insert(data)

    '''
    def update(self,itemid,data):
        assert( type(self.arguments.attrs) is list and len(self.arguments.attrs)>0 )
        self.__NoNoneValidate(data)
        self.model.update(itemid,data)
    '''

    def __NoNoneValidate(self,data):
        for k in self.arguments.attrs:
            if not data.has_key(k):
                raise self.noNoneError("%s can't none or empty" % k)
            if data[k] is None:
                raise self.noNoneError("%s can't none or empty" % k)
            if type(data[k]) is str and len(data[k].strip()) == 0:
                raise self.noNoneError("%s can't none or empty" % k)

    class noNoneError(Exception):
        pass
