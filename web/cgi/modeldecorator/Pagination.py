#coding=utf-8
from Decorator import Decorator
import web, site_helper

class Pagination(Decorator):
    ''' example: decorator = [('Pagination',{})] '''

    rewrite_functions = ['getAll','getPaginationHtml']
    TEST = False

    def getAll(self,env=None):
        if env is None: env = {}
        new_env = site_helper.deepCopy(env)
        if env.get('pagination'):
            pagination_model = self._getModel()
            pagination_data = self._getPaginationData(new_env['pagination'])
            new_env['limit'] = pagination_model.getLimit(pagination_data, self._getPageNum(new_env), self._getCount(new_env))
        return self.model.getAll(new_env)

    def getPaginationHtml(self, env=None, others=None):
        if env is None: env = {}
        if others is None: others = {}
        if env.get('pagination'):
            pagination_model = self._getModel()
            pagination_data = self._getPaginationData(env['pagination'])
            return pagination_model.getHtml(pagination_data, self._getPageNum(env), self._getCount(env), others)
        else:
            return ''

    def _getPageNum(self, env=None):
        if env is None: env = {}
        if env.has_key('page_num'):
            return int(env['page_num'])
        else:
            return int(web.input().get('page_num',1))

    def _getCount(self,env):
        max_count = self.model.getCount(env)
        return max_count

    def _getModel(self):
        return site_helper.getModel('Pagination')

    def _getPaginationData(self, name):
        pagination_model = self._getModel()
        return pagination_model.getOneByWhere('name=%s',[name])

