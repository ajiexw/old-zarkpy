#coding=utf-8
import unittest
import site_helper, test_helper, model
from model import factory as ModelFactory

class TestFactory(unittest.TestCase):

    def test_getInstance(self):
        '''ModelFactory可以根据class名和新表名动态生成新model，此新model类似继承了class，但使用了新的table_name, 因此它会链接另外一个数据表，而和原class的数据互不影响。'''
        test_helper.dropTable('your_table')
        new_image = ModelFactory.getInstance('Image','your_table')
        self.assertTrue(isinstance(new_image, model.Image))
        self.assertTrue(not site_helper.getDBHelper().isTableExists('your_table'))
        self.assertEqual(new_image.table_name, 'your_table')
