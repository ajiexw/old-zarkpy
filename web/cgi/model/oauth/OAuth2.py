#coding=utf-8
from .. import Model
import datetime, hashlib

class OAuth2(Model):
    table_name = ''
    column_names = ['Userid', 'access_token', 'open_id', 'access_expires', 'access_token_md5_int', 'open_id_md5_int', 'share', ]

    def insert(self, data):
        raise 'donnot use method OAuth2.insert'

    def getOpenIdByAccessToken(self, access_token):
        return self._getDB().fetchFirst('select open_id from '+self.table_name+' where access_token=%s order by '+self.table_name+'id desc limit 1', [access_token])

    def getBy(self, open_id):
        md5_int = self.getMD5Int(open_id)
        return self.getOneByWhere('open_id_md5_int=%s and open_id=%s', [md5_int, open_id])

    def getMD5Int(self, key):
        md5 = hashlib.md5()
        md5.update(str(key))
        return int(md5.hexdigest(), 16) % 4000000000 # 因为mysql中的unsigned int最大值约为40亿

    def insertBy(self, open_id, access_token, access_expires, user_id=None):
        self.deleteByAccessToken(access_token)
        new_data = {'open_id':open_id, 'access_token':access_token, 'access_expires':access_expires}
        if user_id:
            new_data['Userid'] = user_id

        new_data['open_id_md5_int'] = self.getMD5Int(open_id)
        new_data['access_token_md5_int'] = self.getMD5Int(access_token)

        return Model.insert(self, new_data)

    def updateAccessToken(self, open_id, access_token, access_expires):
        access_token_md5_int = self.getMD5Int(access_token)
        now = datetime.datetime.now()
        self._getDB().update('update '+self.table_name+' set access_token=%s, access_token_md5_int=%s, access_expires=%s, updated=%s where open_id=%s', [access_token, access_token_md5_int, access_expires, now, open_id])

    def deleteByAccessToken(self, access_token):
        self._getDB().delete('delete from '+self.table_name+' where access_token=%s', access_token)

    def bindUserid(self, access_token, user_id):
        self._getDB().update('update ' + self.table_name + ' set Userid=%s where access_token=%s', [user_id, access_token])

    def getsByUserid(self, user_id):
        return self._getDB().fetchSome('select * from ' + self.table_name + ' where Userid=%s', [user_id])

    def existsByUserid(self, user_id):
        item = self._getDB().fetchFirst('select Userid from ' + self.table_name + ' where Userid=%s limit 1', [user_id])
        return item is not None

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,

            Userid int unsigned not null default 0,
            access_token varchar(100) not null default '',
            open_id varchar(100) not null default '',
            access_expires int unsigned not null default 0,
            share enum('off','on') not null default 'on',
            open_id_md5_int         int unsigned not null,
            access_token_md5_int    int unsigned not null,
            updated         timestamp not null default current_timestamp,

            primary key ({$table_name}id),
            unique key (access_token_md5_int, access_token),
            unique key (open_id_md5_int, open_id)

        )ENGINE=InnoDB;
        '''
