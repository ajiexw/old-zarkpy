#coding=utf-8
from Image import Image
import site_helper, os, time

class UserImage(Image):
    table_name    = 'UserImage'
    column_names  = ['Userid', 'uri','itemtype','itemid','alt','imgorder']
    resize_width  = 600
    resize_height = 4000

    def _getSaveDir(self, data):
        assert(data.has_key('Userid'))
        dir_path = site_helper.config.USER_IMAGE_PATH + str(data['Userid']) + '/'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def _getUriBase(self, data):
        assert(data.has_key('Userid'))
        return site_helper.config.USER_IMAGE_URL + str(data['Userid']) + '/'

    def deleteByIDs(self, ids):
        map(self.delete, ids)

    def updateTypes(self, itemtype, itemid, ids):
        for id in ids:
            self._getDB().update('update '+self.table_name+' set itemtype=%s, itemid=%s where '+self.table_name+'id=%s',(itemtype, itemid, id))

    def updateType(self, itemtype, itemid, id):
        self._getDB().update('update '+self.table_name+' set itemtype=%s, itemid=%s where '+self.table_name+'id=%s',(itemtype, itemid, id))

    def updateTopicDraftType(self, itemtype, itemid, id):
        self._getDB().update('update '+self.table_name+' set itemtype=%s, itemid=%s where itemtype=%s and itemid=%s',(itemtype, itemid, 'TopicDraft', id))

    def gets(self, itemtype, itemid):
        ordered_img = self._getDB().fetchSome('select * from '+self.table_name+' where itemtype=%s and itemid=%s and imgorder!=%s order by imgorder', (itemtype, itemid, 0))
        unordered_img = self._getDB().fetchSome('select * from '+self.table_name+' where itemtype=%s and itemid=%s and imgorder=%s order by UserImageid', (itemtype, itemid, 0))
        return ordered_img + unordered_img

    def updateAlts(self, data):
        for key, value in data.items():
            if key.startswith('user_image_alt_') and value!='为图片说点什么吧':
                id = int(key.rpartition('_')[2])
                self._getDB().update('update '+self.table_name+' set alt=%s where '+self.table_name+'id=%s',(value, id))
            if key.startswith('alt_align_'):
                id = int(key.rpartition('_')[2])
                self._getDB().update('update '+self.table_name+' set alt_align=%s where '+self.table_name+'id=%s',(value, id))


    def updateOrders(self, data):
        for key, value in data.items():
            if key.startswith('user_image_order_'):
                id = int(key.rpartition('_')[2])
                self._getDB().update('update '+self.table_name+' set imgorder=%s where '+self.table_name+'id=%s',(value, id))

    def getBgByBrandid(self, itemtype, brand_id):
        return self._getDB().fetchFirst('select uri from UserImage where itemtype=%s and itemid=%s', [itemtype, brand_id])

    def deleteBgByBrandid(self, itemtype, brand_id):
        self._getDB().delete('delete from UserImage where itemtype=%s and itemid=%s', (itemtype, brand_id))


    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id     int unsigned not null auto_increment,
            Userid              int unsigned not null,
            uri                 varchar(50) not null default '',
            itemtype            varchar(20)  not null default '',
            itemid              int unsigned not null default 0,
            alt                 varchar(1000) charset utf8 not null default '',
            alt_align           enum('left','center') not null default 'left',
            imgorder            int unsigned not null default 0,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            key (itemtype, itemid),
            key (Userid)
        )ENGINE=InnoDB; '''
