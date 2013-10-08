#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper

class TestBrand(unittest.TestCase):

    def setUp(self):
        self.model = site_helper.getModel('Brand')
        test_helper.cleanTable(self.model.table_name)

    def test_update(self):
        '''禁止修改name(修改时无效)'''
        brand_model = self.model
        data = test_helper.storage({'name':'sdjl', 'cnname':'闪电精灵', 'enname':'SDJL', 'Imageid':0})
        new_id = brand_model.insert(data)
        data.name = 'sparker5'
        brand_model.update(new_id, data)

        db_helper = getDBHelper()
        self.assertEqual(db_helper.fetchFirst('select name from Brand where Brandid=%s', new_id), 'sdjl')
        self.assertEqual(data.name, 'sparker5')

