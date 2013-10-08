#coding=utf-8
from Decorator import Decorator
import site_helper

class Orderby(Decorator):
    '''
        ('Orderby',{'orderby':'time desc'}),
    '''
    rewrite_functions = ['getAll']

    def getAll(self,env=None):
        assert( type(self.arguments.orderby) is str and len(self.arguments.orderby)>0 )
        if env is None: env = {}
        new_env = site_helper.deepCopy(env)
        if not new_env.has_key('orderby'):
            new_env['orderby'] = self.arguments.orderby
        return self.model.getAll(new_env)
