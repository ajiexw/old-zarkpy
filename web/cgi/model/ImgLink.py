#coding=utf-8
from Model import Model
from Image import Image

class ImgLink(Model):
    '''ImgLink保存一个Imageid,且把model.table_name和modelid写入到对应图片的itemtype与itemid值中,以便关联 '''
    table_name = 'ImgLink'
    ''' read only属性: uri(图片地址,来自Image model) '''
    column_names = ['title','paragraph','href','alt','Imageid','target']

    #插入一个ImgLink和一个Image，然后关联Imageid的itemtype和itemid
    def insert(self, data):
        assert(self.table_name != '')
        data['itemtype'] = self.table_name # 设置Image表中的itemtype为self.table_name
        if data.has_key('imagefile'):
            data['Imageid'] = Image().insert(data)
        new_id = Model.insert(self,data)
        if data.get('Imageid',0) > 0: # 允许Imageid==0，使得更多的东西可以伪装成ImgLink, 比如Fleaflea
            Image().setItemID(data['Imageid'],new_id)
        return new_id

    def update(self, itemid, data):
        assert(self.table_name != '')
        if data.has_key('imagefile') and len(data.imagefile['value']) > 10:
            data['itemtype'] = self.table_name
            data.Imageid = new_image_id = Image().insert(data) # set Imageid for update
            Image().setItemID(new_image_id, itemid)
        Model.update(self,itemid,data)

    def get(self, itemid):
        imglink = Model.get(self,itemid)
        if imglink is not None:
            img = Image().get(imglink.Imageid)
            imglink['uri'] = img.uri if img is not None else ''
        return imglink

    def getAll(self, env=None):
        imglinks = Model.getAll(self,env)
        image_model = Image()
        for imglink in imglinks:
            img = image_model.get(imglink.Imageid)
            imglink['uri'] = img.uri if img is not None else ''
        return imglinks

    def getImageid(self, itemid):
        return self.get(itemid).Imageid

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            href            varchar(500)  charset utf8 not null default '',
            target          ENUM('_blank','_self') not null default '_self',
            alt             varchar(1000)  charset utf8 not null default '',
            title           varchar(100)  charset utf8 not null default '',
            paragraph       varchar(4000) charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
