#coding=utf-8
from Decorator import Decorator
import site_helper
from tool import search

class Category(Decorator):
    ''' example: decorator = [
        ('Category',{'cat_name':''}),
    ] '''

    rewrite_functions = ['getCategoryTitle']
    TEST = False

    def getCategoryTitle(self, item_id):
        item = self.model.get(item_id)
        ret = None
        if item.has_key('Categoryid'):
            cat = site_helper.getModel(self.arguments.cat_name).get(item.Categoryid)
            if cat is not None:
                ret = cat.title
        return ret


