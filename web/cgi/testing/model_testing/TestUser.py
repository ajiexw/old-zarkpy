#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper
from datetime import date

class TestUser(unittest.TestCase):

    def setUp(self):
        self.model = site_helper.getModel('User')
        test_helper.cleanTable(self.model.table_name)

    def test_insert(self):
        '''保存图片, 验证加密方式, 生日格式'''
        user_model = self.model
        data = test_helper.storage({'username':'sdjl', 'email':'sdjllyh@gmail.com', 'password':'sdjllyh', 'birthday':'1985-10-17'})
        data.imagefile = site_helper.storage({'filename':'sdjl.jpg', 'value':'shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!'})
        new_id   = user_model.insert(data)
        new_user = getDBHelper().fetchOne('select * from '+user_model.table_name+' where '+user_model.primary_key+'=%s',new_id)
        self.assertEqual(new_user.password, 'dab61a7c59b7d5f2e9fd22c85f6aa03c') # 不允许改变加密方式
        self.assertEqual(new_user.cover_url, '%s%d.jpg' % (site_helper.config.USER_COVER_URL, new_id)) # 保存图片
        self.assertEqual(open('%s%d.jpg' % (site_helper.config.USER_COVER_PATH, new_id)).read().strip(), 'shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!')
        self.assertEqual(new_user.birthday, date(1985,10,17) )

    def test_getByEmail(self):
        user_model = self.model
        data = test_helper.storage({'email':'  sdjllyh@gmail.com  ','username':'sdjl', 'password':'sdjllyh'})
        new_id = user_model.insert(data)
        self.assertEqual(user_model.getByEmail('sdjllyh@gmail.com').get(user_model.primary_key),new_id)

    def test_validatePassword(self):
        user_model = self.model
        data = test_helper.storage({'username':'sdjl', 'email':'sdjllyh@gmail.com', 'password':'sdjllyh', 'birthday':'1985-10-17'})
        new_id   = user_model.insert(data)
        new_user = getDBHelper().fetchOne('select * from '+user_model.table_name+' where '+user_model.primary_key+'=%s',new_id)
        self.assertTrue(user_model.validatePassword(new_id, 'sdjllyh'))

    def test_update(self):
        '''更新头像内容'''
        user_model = self.model
        data = test_helper.storage({'username':'sdjl', 'email':'sdjllyh@gmail.com', 'password':'sdjllyh', 'birthday':'1985-10-17'})
        data.imagefile = site_helper.storage({'filename':'sdjl.jpg', 'value':'shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!shuai!'})
        new_id   = user_model.insert(data)
        data.imagefile = site_helper.storage({'filename':'sdjl.jpg', 'value':'chou!chou!chou!chou!chou!chou!chou!chou!chou!chou!'})
        user_model.update(new_id, data)
        self.assertEqual(open('%s%d.jpg' % (site_helper.config.USER_COVER_PATH, new_id)).read().strip(), 'chou!chou!chou!chou!chou!chou!chou!chou!chou!chou!')
