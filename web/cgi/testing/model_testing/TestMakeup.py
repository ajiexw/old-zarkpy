#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper
from model import Makeup

# modelfile: ../../model/Makeup.py

class TestMakeup(unittest.TestCase):

    def setUp(self):
        self.model = site_helper.getModel('Makeup')
        test_helper.cleanTable(self.model.table_name, 'MakeupHasAttribute')

    def test_insert(self):
        makeup_model = self.model
        data = test_helper.storage({'name':'面膜', 'enname':'mianmo', 'brand':'sdjlbrand', 'category':'good', 'score':'5.5', 'attributeids':[10,1,1017], 'release_time':'2011-10-17', 'intro':'haobao','cover_url':'/img/makeupreserve/cover/1.jpg' })

        new_makeup_id = makeup_model.insert(data)
        inserted_makeup = makeup_model.get(new_makeup_id)
        self.assertEqual(inserted_makeup.name, '面膜')
        self.assertEqual(inserted_makeup.enname, 'mianmo')
        self.assertEqual(inserted_makeup.cover_url, '/img/makeupreserve/cover/1.jpg')

    def test_insert_saveimage(self):
        '''插入makeup时, 如果有imagefile,就把文件保存在config.MAKEUP_COVER_PATH中, 并且以Makeupid命名, 修改cover_url指向图片文件'''
        makeup_model = self.model
        db_helper = getDBHelper()
        data = test_helper.storage({'name':'面膜', 'cover_url':'/img/makeupreserve/cover/1.jpg' })
        data.imagefile = site_helper.storage({'filename':'c://sdjl.jpg', 'value':'liuyonghui'})
        new_makeup_id = makeup_model.insert(data)

        self.assertTrue(os.path.exists('%s%d.jpg' % (site_helper.config.MAKEUP_COVER_PATH, new_makeup_id)))
        self.assertEqual(db_helper.fetchFirst('select cover_url from Makeup where Makeupid=%s', new_makeup_id), site_helper.config.MAKEUP_COVER_URL+str(new_makeup_id)+'.jpg')
        self.assertEqual(open('%s%d.jpg' % (site_helper.config.MAKEUP_COVER_PATH, new_makeup_id)).read().strip(), 'liuyonghui')

    def test_insert_write_attributeids(self):
        '''insert要插入attributes的id'''
        makeup_model = self.model
        data = test_helper.storage({'name':'面膜', 'enname':'mianmo', 'brand':'sdjlbrand', 'category':'good', 'score':'5.5', 'attributeids':[10,1,1017], 'release_time':'2011-10-17', 'intro':'haobao','cover_url':'/img/makeupreserve/cover/1.jpg' })
        new_makeup_id = makeup_model.insert(data)
        inserted_makeup = makeup_model.getWithAll(new_makeup_id)
        self.assertEqual(inserted_makeup.attributeids, [10,1,1017])
        self.assertEqual(inserted_makeup.cover_url, '/img/makeupreserve/cover/1.jpg')

    def test_update_saveimage(self):
        '''更新的时候要替换原来的图片文件'''
        makeup_model = self.model
        db_helper = getDBHelper()
        data = test_helper.storage({'name':'面膜', 'cover_url':'/img/makeupreserve/cover/1.jpg' })
        data.imagefile = site_helper.storage({'filename':'c://sdjl.jpg', 'value':'liuyonghui'})
        new_makeup_id  = makeup_model.insert(data)
        data.imagefile = site_helper.storage({'filename':'c://wx.jpg', 'value':'wangxuan'})
        makeup_model.update(new_makeup_id, data)
        self.assertEqual(open('%s%d.jpg' % (site_helper.config.MAKEUP_COVER_PATH, new_makeup_id)).read().strip(), 'wangxuan')

    def test_update_change_attributeids(self):
        makeup_model = self.model
        data = test_helper.storage({'name':'面膜', 'attributeids':[10,1,1017]})
        new_makeup_id = makeup_model.insert(data)
        data.attributeids = [23,1]
        makeup_model.update(new_makeup_id, data)
        inserted_makeup = makeup_model.getWithAll(new_makeup_id)
        self.assertEqual(inserted_makeup.attributeids, [23,1])

    def test_delete(self):
        '''删除的时候要级联删除MakeupHasAttribute'''
        makeup_model = self.model
        data = test_helper.storage({'name':'面膜', 'enname':'mianmo', 'brand':'sdjlbrand', 'category':'good', 'score':'5.5', 'attributeids':[10,1,1017], 'release_time':'2011-10-17', 'intro':'haobao','cover_url':'/img/makeupreserve/cover/1.jpg' })

        new_makeup_id = makeup_model.insert(data)
        makeup_model.delete(new_makeup_id)
        db_helper = getDBHelper()
        self.assertEqual(db_helper.fetchSome('select * from MakeupHasAttribute where Makeupid=%s', new_makeup_id), [])

