#!coding=utf-8
import unittest, test_helper, os
from site_helper import getDBHelper
from model import Category
from model import Model

class TestCategory(unittest.TestCase):

    def setUp(self):
        self.model = Category()
        test_helper.cleanTable(self.model.table_name, Model().table_name)

    def test_get(self):
        '''get函数返回的数据要包含model_name'''
        category_model = self.model
        model_model = Model()
        new_category_id = category_model.insert(test_helper.storage({'title':'cat1'}))
        new_model_id = model_model.insert(test_helper.storage({'Categoryid':new_category_id}))
        inserted_category = category_model.get(new_category_id)
        self.assertEqual(inserted_category.model_name,model_model.table_name)

    def test_getAll(self):
        '''getAll函数返回的数据只包含model_name，不包含models'''
        category_model = self.model
        model_model = Model()
        new_category_id = category_model.insert(test_helper.storage({'title':'cat1'}))
        new_model_id = model_model.insert(test_helper.storage({'Categoryid':new_category_id}))
        all_categorys = category_model.getAll()
        self.assertEqual(len(all_categorys),1)
        self.assertEqual(all_categorys[0].model_name,model_model.table_name)
        self.assertTrue(not all_categorys[0].has_key('models'))

    def test_delete(self):
        '''delete的同时要删除相关数据'''
        category_model = self.model
        model_model = Model()
        new_category_id = category_model.insert(test_helper.storage({'title':'cat1'}))
        new_model_id = model_model.insert(test_helper.storage({'Categoryid':new_category_id}))
        inserted_model = getDBHelper().fetchOne('select * from '+model_model.table_name+' where '+model_model.primary_key+'=%s',new_model_id)
        self.assertTrue(inserted_model is not None)
        category_model.delete(new_category_id)
        inserted_model = getDBHelper().fetchOne('select * from '+model_model.table_name+' where '+model_model.primary_key+'=%s',new_model_id)
        self.assertTrue(inserted_model is None)
