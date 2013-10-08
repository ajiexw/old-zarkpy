#coding=utf-8
from Decorator import Decorator
import site_helper
from tool import search

class Has(Decorator):
    ''' example: decorator = [
        ('Has',{'relate_key':'Has', 'revert':False}),
    ] '''

    rewrite_functions = ['getHavs']
    TEST = False

    def getHavs(self, item_id, relation_table, env=None):
        if env is None: env = {}
        new_env = site_helper.deepCopy(env)

        if new_env.has_key('where'):
            new_env['where'][0] = '('+ new_env['where'][0] +') and '+self.primary_key+'=%s'
            new_env['where'][1].append(item_id)
        else:
            new_env['where'] = (self.primary_key+'=%s', [item_id])

        if self.arguments.get('revert', False) == False:
            middle_table = self.table_name + self.arguments.relate_key + relation_table
        else:
            middle_table = relation_table + self.arguments.relate_key + self.table_name
            
        return map(site_helper.getModel(relation_table).get, [i.get(relation_table+'id') for i in site_helper.getModel(middle_table).getAll(new_env)])
