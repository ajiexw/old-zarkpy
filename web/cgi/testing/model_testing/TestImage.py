#!coding=utf-8
import unittest, test_helper, site_helper, os
from model import Image

class TestImage(unittest.TestCase):

    def setUp(self):
        self.image_model = Image()
        test_helper.cleanTable(self.image_model.table_name)

    def test_insert(self):
        image_model = self.image_model
        data = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id = image_model.insert(data)
        # save image file success
        self.assertTrue(os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % new_image_id))
        # file content
        self.assertEqual(open(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % new_image_id).read().strip(),'image_file_content')
        # data value
        new_image = site_helper.getDBHelper().fetchOne('select uri,itemtype,itemid,alt from '+image_model.table_name+' where '+image_model.primary_key+'=%s',new_image_id)
        self.assertEqual(new_image.uri,'%s%d.png' % (site_helper.config.UPLOAD_IMAGE_URL, new_image_id))
        self.assertEqual(new_image.itemtype,'AImage')
        self.assertEqual(new_image.itemid,1017)
        self.assertEqual(type(new_image.itemid),long)
        self.assertEqual(new_image.alt,' image alt ') # don't strip

    def test_delete(self):
        '''Image的delete函数仅删除表数据，而不删除图片文件'''
        image_model = self.image_model
        data = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id = image_model.insert(data)
        image_model.delete(new_image_id)
        # delete data
        new_image = site_helper.getDBHelper().fetchOne('select uri,itemtype,itemid,alt from '+image_model.table_name+' where '+image_model.primary_key+'=%s',new_image_id)
        self.assertEqual(new_image,None)
        # don't delete image file
        self.assertTrue(os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % new_image_id))
        self.assertEqual(open(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % new_image_id).read().strip(),'image_file_content')

    def test_update(self):
        '''Image的update函数只能更新数据库表的值，而不创建、删除或修改图片文件。 '''
        image_model = self.image_model
        data = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id = image_model.insert(data)
        update_data = test_helper.storage({'imagefile':{'value':'image_file_content2','filename':'c://my files/sdjl2.png'},'itemtype':'AImage2','itemid':10172,'alt':' image alt2 ',})
        image_model.update(new_image_id,update_data)
        updated_image = site_helper.getDBHelper().fetchOne('select uri,itemtype,itemid,alt from '+image_model.table_name+' where '+image_model.primary_key+'=%s',new_image_id)
        self.assertEqual(updated_image.itemtype,'AImage2')
        self.assertEqual(updated_image.itemid,10172)
        self.assertEqual(updated_image.alt,' image alt2 ') # don't strip
        self.assertEqual(updated_image.uri,'%s%d.png' % (site_helper.config.UPLOAD_IMAGE_URL, new_image_id)) # has the old image uri
        self.assertTrue(not os.path.exists(site_helper.config.UPLOAD_IMAGE_PATH+'/%d.png' % (new_image_id+1))) # don't create new image file
        new_image2 = site_helper.getDBHelper().fetchOne('select uri,itemtype,itemid,alt from '+image_model.table_name+' where '+image_model.primary_key+'=%s',new_image_id+1)
        self.assertTrue(new_image2 is None) # don't insert new image data

    def test_getUri(self):
        image_model = self.image_model
        data = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id = image_model.insert(data)
        self.assertEqual(image_model.getUri(new_image_id),'%s%d.png' % (site_helper.config.UPLOAD_IMAGE_URL, new_image_id))

    def test_setItemID(self):
        image_model = self.image_model
        data = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id = image_model.insert(data)
        image_model.setItemID(new_image_id,801)
        new_image = site_helper.getDBHelper().fetchOne('select uri,itemtype,itemid,alt from '+image_model.table_name+' where '+image_model.primary_key+'=%s',new_image_id)
        self.assertEqual(new_image.itemid, 801)

    def test_getByItemid(self):
        '''Image表支持插入多个(itemtype,itemid)相同的数据，表示一个item可以有多个Image'''
        image_model = self.image_model
        data1 = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        data2 = test_helper.storage({'imagefile':{'value':'image_file_content','filename':'c://my files/sdjl.png'},'itemtype':'AImage','itemid':1017,'alt':' image alt ',})
        new_image_id1 = image_model.insert(data1)
        new_image_id2 = image_model.insert(data2)
        images = image_model.getByItemid('AImage',1017)
        self.assertTrue(type(images) is list)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0][image_model.primary_key],new_image_id1)
        self.assertEqual(images[1][image_model.primary_key],new_image_id2)

