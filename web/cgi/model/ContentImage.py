#coding=utf-8
from Image import Image
import site_helper, os, time

# 创建保存图片的文件夹
if not os.path.exists(site_helper.config.USER_IMAGE_PATH + 'ContentImage/'):
    os.mkdir(site_helper.config.USER_IMAGE_PATH + 'ContentImage/')

class ContentImage(Image):
    table_name    = 'ContentImage'
    column_names  = ['title', 'tag', 'alt', 'uri', ]
    decorator = [('Pagination',{})]

    def update(self, item_id , data):
        '''允许修改图片'''
        if data.has_key('imagefile'):
            assert(data.imagefile.has_key('filename') and data.imagefile.has_key('value'))
            data.imagefile['filetype'] = data.imagefile['filename'].rpartition('.')[2].lower()
            validated_msg = self._insertValidate(data)
            # 如果validated_msg is not None, 则post的图片数据有错
            if validated_msg is not None:
                raise Exception(validated_msg)
            # 更新数据库中的uri字段
            file_path = '%s%d.%s' % (self._getSaveDir(data), item_id, data.imagefile['filetype'])
            self._getDB().update('update '+self.table_name+' set uri=%s where '+self.table_name+'id=%s' ,('%s%d.%s' % (self._getUriBase(data), item_id, data.imagefile['filetype']) ,item_id))
            # 创建文件夹
            if not os.path.exists(file_path.rpartition('/')[0]):
                os.mkdir(file_path.rpartition('/')[0])
            # 保存图片
            with open(file_path,'w') as f:
                f.write(data.imagefile['value'])
            # 压缩图片
            self.resizeImage(file_path)
        return Image.update(self, item_id, data)

    def _getSaveDir(self, data):
        return site_helper.config.USER_IMAGE_PATH + 'ContentImage/'

    def _getUriBase(self, data):
        return site_helper.config.USER_IMAGE_URL + 'ContentImage/'


    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id     int unsigned not null auto_increment,
            title               varchar(50) charset utf8 not null default '',
            tag                 varchar(60) charset utf8 not null default '',
            alt                 varchar(300) charset utf8 not null default '',
            uri                 varchar(50) not null default '',
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            key (tag)
        )ENGINE=InnoDB; '''
