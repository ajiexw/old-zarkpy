#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper
from model import ImgLink
from model import Image

class TestImgLink(unittest.TestCase):

    def setUp(self):
        self.model = ImgLink()
        test_helper.cleanTable(self.model.table_name)

    def test_insert(self):
        '''当插入的数据有imagefile时，ImgLink会自动插入一个Image数据，并与之关联'''
        imglink_model = self.model
        image_model = Image()
        max_image_id = getDBHelper().fetchFirst('select max('+image_model.primary_key+') from '+image_model.table_name)
        data = test_helper.storage({'imagefile':{'value':'imagefile_content', 'filename':'c://sdjl/lyh.png'}})

        self.assertTrue(not os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % (max_image_id+1)))
        inserted_image = getDBHelper().fetchOne('select * from '+image_model.table_name+' where '+image_model.primary_key+'=%s', max_image_id+1)
        self.assertTrue(inserted_image is None)

        new_imglink_id = imglink_model.insert(data) # insert imglink
        self.assertTrue(os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % (max_image_id+1)))
        inserted_image = getDBHelper().fetchOne('select * from '+image_model.table_name+' where '+image_model.primary_key+'=%s', max_image_id+1)
        self.assertTrue(inserted_image is not None)

        self.assertEqual(inserted_image.itemtype, imglink_model.table_name)
        self.assertEqual(inserted_image.itemid, new_imglink_id)

        inserted_imglink = getDBHelper().fetchOne('select * from '+imglink_model.table_name+' where '+imglink_model.primary_key+'=%s', new_imglink_id)
        self.assertEqual(inserted_imglink.Imageid, max_image_id+1)
        
    def test_update(self):
        '''update时如果有imagefile，则新建图片数据与文件给imglink，且不删除老数据与文件'''
        imglink_model = self.model
        image_model = Image()
        data = test_helper.storage({'imagefile':{'value':'imagefile_content', 'filename':'c://sdjl/lyh.png'}})

        new_imglink_id = imglink_model.insert(data) # insert imglink
        first_image_id = getDBHelper().fetchFirst('select max('+image_model.primary_key+') from '+image_model.table_name)

        imglink_model.update(new_imglink_id, data) # update imglink
        second_image = getDBHelper().fetchOne('select * from '+image_model.table_name+' where '+image_model.primary_key+'=%s', first_image_id+1)

        self.assertTrue(second_image is not None)
        self.assertTrue(os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % (second_image.get(image_model.primary_key))))

        first_image = getDBHelper().fetchOne('select * from '+image_model.table_name+' where '+image_model.primary_key+'=%s', first_image_id)
        self.assertTrue(first_image is not None)
        self.assertTrue(os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % (first_image.get(image_model.primary_key))))

    def test_get(self):
        '''get函数返回的数据要包含uri属性，表示图片的uri'''
        imglink_model = self.model
        image_model = Image()
        data = test_helper.storage({'imagefile':{'value':'imagefile_content', 'filename':'c://sdjl/lyh.png'}})
        new_imglink_id = imglink_model.insert(data) # insert imglink
        new_imglink = imglink_model.get(new_imglink_id)
        new_image_id = getDBHelper().fetchFirst('select max('+image_model.primary_key+') from '+image_model.table_name)
        self.assertEqual(new_imglink.uri, site_helper.config.UPLOAD_IMAGE_URL+'%d.png' % new_image_id)

    def test_getAll(self):
        '''getAll函数返回的数据要包含uri属性，表示图片的uri'''
        imglink_model = self.model
        image_model = Image()
        data = test_helper.storage({'imagefile':{'value':'imagefile_content', 'filename':'c://sdjl/lyh.png'}})
        new_imglink_id = imglink_model.insert(data) # insert imglink
        new_imglinks = imglink_model.getAll()
        new_image_id = getDBHelper().fetchFirst('select max('+image_model.primary_key+') from '+image_model.table_name)
        self.assertEqual(new_imglinks[0].uri, site_helper.config.UPLOAD_IMAGE_URL+'%d.png' % new_image_id)

    def test_getImageid(self):
        imglink_model = self.model
        image_model = Image()
        data = test_helper.storage({'imagefile':{'value':'imagefile_content', 'filename':'c://sdjl/lyh.png'}})
        new_imglink_id = imglink_model.insert(data) # insert imglink
        new_image_id = getDBHelper().fetchFirst('select max('+image_model.primary_key+') from '+image_model.table_name)
        self.assertEqual(imglink_model.getImageid(new_imglink_id), new_image_id)
        
