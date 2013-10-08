#coding=utf-8
from Model import Model
import site_helper, os, time

'''
图片是不能修改和删除的,因此请勿在重写update函数时修改图片内容
'''

class Image(Model):
    table_name = 'Image'
    column_names = ['uri','itemtype','itemid','alt',]
    resize_width = None
    resize_height = None

    def insert(self,data):
        if data.has_key('imagefile'):
            assert(data.imagefile.has_key('filename') and data.imagefile.has_key('value'))
            data.imagefile['filetype'] = data.imagefile['filename'].rpartition('.')[2].lower()
            validated_msg = self._insertValidate(data)
            # 如果validated_msg is not None, 则post的图片数据有错
            if validated_msg is not None:
                raise Exception(validated_msg)
            # 插入数据
            new_id = Model.insert(self,data)
            file_path = '%s%d.%s' % (self._getSaveDir(data), new_id, data.imagefile['filetype'])
            # 更新数据库中的uri字段
            self._getDB().update('update '+self.table_name+' set uri=%s where '+self.table_name+'id=%s' ,('%s%d.%s' % (self._getUriBase(data), new_id, data.imagefile['filetype']) ,new_id))
            # 创建文件夹
            if not os.path.exists(file_path.rpartition('/')[0]):
                os.mkdir(file_path.rpartition('/')[0])
            # 保存图片
            with open(file_path,'w') as f:
                f.write(data.imagefile['value'])
            # 压缩图片
            if data.has_key('ifResize'):
                pass
            else:
                self.resizeImage(file_path)
        else:
            new_id = Model.insert(self, data)
        return new_id

    def resizeImage(self, file_path):
        if self.resize_width is not None and self.resize_height is not None:
            os.system('convert "%s" -resize "%dx%d>" +profile "*" "%s" ' % (file_path, self.resize_width, self.resize_height, file_path))

    def _getSaveDir(self, data):
        '''因为不同的表会有相同的主键值, 所以必须不同的model放到不同的文件夹中, 否则会互相overwrite'''
        #return site_helper.config.UPLOAD_IMAGE_PATH + self.table_name + '/'  应该使用这个版本
        return site_helper.config.UPLOAD_IMAGE_PATH

    def _getUriBase(self, data):
        #return site_helper.config.UPLOAD_IMAGE_URL + self.table_name + '/'   应该使用这个版本
        return site_helper.config.UPLOAD_IMAGE_URL

    def _insertValidate(self,data):
        if not data.has_key('imagefile'):
            return '插入的data没有imagefile数据'
        if len(data.imagefile['filetype']) == 0:
            return '图片的类型未知'
        if len(data.imagefile['value']) < 10:
            return '没有上传图片或上传的图片太小'
        return None

    def getUri(self,itemid):
        return self._getDB().fetchFirst('select uri from '+self.table_name+' where '+self.table_name+'id=%s limit 1',itemid)

    def setItemID(self,image_id,itemid):
        self._getDB().update('update '+self.table_name+' set itemid=%s where '+self.table_name+'id=%s',(itemid,image_id))

    def getByItemid(self,itemtype,itemid):
        return self._getDB().fetchSome('select * from '+self.table_name+' where itemtype=%s and itemid=%s',(itemtype,itemid))

    table_template = \
            ''' CREATE TABLE {$table_name} (
                {$table_name}id     int unsigned not null auto_increment,
                uri                 varchar(50) not null default '',
                itemtype            varchar(20)  not null default '',
                itemid              int unsigned not null default 0,
                alt                 varchar(1000) charset utf8 not null default '',
                primary key ({$table_name}id),
                key (itemtype,itemid)
            )ENGINE=InnoDB; '''
