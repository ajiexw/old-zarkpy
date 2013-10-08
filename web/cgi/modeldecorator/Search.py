#coding=utf-8
from Decorator import Decorator
import site_helper
from tool import search

ZARKFX = '''<div fx="pagination[max=%d;displaycount=%d;firsttext=%s;lasttext=%s]"></div>'''

class Search(Decorator):
    ''' example: decorator = [
        ('Search',{'index':'', 'max': 1000, 'display_page':10, 'page_count': 30, 'firsttext':'第一页', 'lasttext':'末页'}),
    ] '''

    rewrite_functions = ['search']
    TEST = False

    def search(self, env=None):
        if env is None: env = {}
        env = site_helper.extend(env, self.arguments)
        assert(len(env.index)>0)
        assert(env.has_key('searchword'))
        assert(env.has_key('page_num') and type(env.page_num) == int)
        page_num = env.page_num
        start = (page_num - 1) * env.page_count
        search_ids = search.search(query = env.searchword, index=env.index, start=start, limit = env.max - start)
        model = site_helper.getModel(self.getModelTableName())
        items = []
        for id in search_ids:
            item = model.get(id)
            if item is not None:
                items.append(item)
            if len(items) == env.page_count:
                break
        return items

    def getSearchPaginationHtml(self,env=None):
        if env is None: env = {}
        env = site_helper.extend(env, self.arguments)
        assert(len(env.index)>0)
        assert(env.has_key('searchword'))
        amount = len(search.search(query=env.searchword, index=env.index, limit=env.max ))
        max_page = amount / env.page_count
        if amount % env.page_count != 0: max_page += 1
        return ZARKFX % (max_page, env.display_page, env.firsttext, env.lasttext)

    def getSearchAllIds(self, env):
        if env is None: env = {}
        env = site_helper.extend(env, self.arguments)
        assert(len(env.index)>0)
        assert(env.has_key('searchword'))
        return search.search(query = env.searchword, index=env.index, start=0, limit=1000)

