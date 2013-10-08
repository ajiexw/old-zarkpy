#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper

class TestPageContent(unittest.TestCase):

    def setUp(self):
        self.model = site_helper.getModel('PageContent')
        test_helper.cleanTable('PageContent', 'PageContentType')

    def test_insert(self):
        '''插入的数据, 如果type表中没有相关数据, 要先插入type'''
        content_model = self.model
        data = test_helper.storage({'page':'brand-list', 'content':'brandshow', 'model_name':'Brand', 'model_id':1, })

        exists_content = getDBHelper().fetchOne("select * from PageContentType where page='brand-list' and content='brandshow' ")
        self.assertEqual(exists_content, None)

        new_id = content_model.insert(data)

        exists_content = getDBHelper().fetchOne("select * from PageContentType where page='brand-list' and content='brandshow' ")
        self.assertEqual(exists_content.model_name, 'Brand')

    def test_getModelidsByTypeid(self):
        content_model = self.model
        data = test_helper.storage({'page':'brand-list', 'content':'brandshow', 'model_name':'Brand', 'model_id':1, })

        new_id = content_model.insert(data)
        type_id = getDBHelper().fetchFirst("select PageContentTypeid from PageContentType")

        contents = content_model.getModelidsByTypeid(type_id)
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0], 1)

    def test_getModelids(self):
        content_model = self.model
        data = test_helper.storage({'page':'brand-list', 'content':'brandshow', 'model_name':'Brand', 'model_id':1, })
        new_id = content_model.insert(data)
        contents = content_model.getModelids('brand-list', 'brandshow')
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0], 1)

    def test_cleanModelids(self):
        content_model = self.model
        data = test_helper.storage({'page':'brand-list', 'content':'brandshow', 'model_name':'Brand', 'model_id':1, })
        new_id = content_model.insert(data)
        content_model.cleanModelids('brand-list', 'brandshow')
        contents = content_model.getModelids('brand-list', 'brandshow')
        self.assertEqual(len(contents), 0)

