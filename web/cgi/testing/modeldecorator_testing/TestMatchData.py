#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper

class TestMatchData(unittest.TestCase):

    def setUp(self):
        test_helper.cleanTable('Model', 'Category')

    def test_equal(self):
        getDBHelper().insert('insert into Category (Categoryid, title) values (1017, %s)', 'sdjl')
        getDBHelper().insert('insert into Category (Categoryid, title) values (801, %s)', 'wx')
        decorator = [('MatchData',{'matchs':[{'table_name':'Category','match_key':'datatitle','type':'equal','match_column':'title','add':'Categoryid','functions':'insert update'}]}), ]
        model = site_helper.getModel('Model', decorator )
        data = test_helper.storage({'datatitle':'sdjl'})
        new_id = model.insert(data)
        self.assertEqual(getDBHelper().fetchOne('select * from Model where Modelid=%s',new_id).Categoryid, 1017)
        data = test_helper.storage({'datatitle':'wx'})
        model.update(new_id, data)
        self.assertEqual(getDBHelper().fetchOne('select * from Model where Modelid=%s',new_id).Categoryid, 801)

