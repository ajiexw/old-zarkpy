#coding=utf-8
from Model import Model
import hashlib, site_helper
import socket, struct, os
import random
import PIL.Image
from site_helper import getModel, getController

class User(Model):
    table_name = 'User'
    column_names = ['email','password','username','realname','address','intro','phone_number','cover_url','birthday','sex', 'register_ip','login_ip', 'login_count', 'created','activated']
    decorator = [('Pagination',{}),
        ('Orderby',{'orderby':'Userid desc'}),
        ('NoNone',{'attrs':['username']}),
        ('Cache',{'clear_functions':'all'}),
        ('Search',{'index':'user', 'display_page':10, 'max': 1000, 'page_count': 30, 'firsttext':'第一页', 'lasttext':'末页'}),
        ('Has',{'relate_key':'Has', 'revert':False}),
    ]
    resize_width  = 600
    resize_height = 810

    def getByEmail(self,email):
        return self.getOneByWhere('email=%s',[email])

    def getByUsername(self, name):
        return self.getOneByWhere('username=%s',[name])
    

    def insert(self, data):
        new_id = Model.insert(self, data)
        if data.has_key('imagefile'):
            self._savePortraitImg(new_id, data.imagefile)
            self._setPortraitDefault(new_id)

        return new_id

    def update(self, item_id, data):
        from controller import ImageConvert #  放到这里是为了避免在import model时中途import controller.* 导致import依赖
        # 成为达人时同步到第三方网站, 这是逻辑代码, 但是放到这里了
        old_item = self.get(item_id)
        daren_title = data.get('daren_title','').encode('utf-8','ignore').strip()
        if old_item and old_item.has_key('daren_title') and (old_item.daren_title.strip() != daren_title) and len(daren_title) > 0:
            user = self.get(item_id)
            if user and user.cover_url:
                pic = ImageConvert().getSmallPortrait(user.cover_url, user.small_portrait, 150)
            else:
                pic = None

            getController('Share').shareAll(old_item.Userid,
                    '【来凹凹啦, 找到最漂亮的自己】@凹凹啦 美妆前沿 我是凹凹啦美妆达人了, 我分享的美妆心得都在这里哦! 求围观, 求关注! 我的美妆主页',
                    url='/user/'+str(old_item.Userid), pic=pic )
            # 设置用户的达人勋章
            if user:
                self._getDB().delete("delete from UserHasMedal where Userid = %s and Medalid in (select Medalid from Medal where name like 'daren_')", (user.Userid, ))
                daren_medal_id = self._getDB().fetchFirst("select Medalid from Medal where name=%s ", ('daren_' + daren_title,))
                if daren_medal_id:
                    self._getDB().insert('insert into UserHasMedal (Userid, Medalid ) values (%s, %s);', (user.Userid, daren_medal_id))
            

        # 更新图片
        ret = Model.update(self, item_id, data)
        if data.has_key('imagefile'):
            self._savePortraitImg(item_id, data.imagefile)
            self._setPortraitDefault(item_id)
        if data.has_key('imagefile') or data.has_key('small_portrait') or data.has_key('big_portrait'):
            self._removeSmallFiles(item_id)

        return ret

    def _setPortraitDefault(self, item_id):
        fp = os.popen('ls %s%d-*'%(site_helper.config.USER_COVER_PATH,item_id)).read()[:-1]
        img = PIL.Image.open(fp)
        w,h = img.size
        if w < h:
            if w > h/1.35:
                self.update(item_id, {'big_portrait':'%d 0 %d %d'%((w-h/1.35)/2,h/1.35,h), 'small_portrait':'0 %d %d %d'%((h-w)/2,w,w)})
            else:
                self.update(item_id, {'big_portrait':'0 %d %d %d'%((h-1.35*w)/2,w,1.35*w), 'small_portrait':'0 %d %d %d'%((h-w)/2,w,w)})

        elif w == h:
            self.update(item_id, {'big_portrait':'%d 0 %d %d'%((w-h/1.35)/2,h/1.35,h), 'small_portrait':'0 0 %d %d'%(w,w)})
        else:
            self.update(item_id, {'big_portrait':'%d 0 %d %d'%((w-h/1.35)/2,h/1.35,h), 'small_portrait':'%d 0 %d %d'%((w-h)/2,h,h)})


    def getRandom(self):
        return random.randint(0, 1000000)

    def _savePortraitImg(self, item_id, imagefile):
        #删除旧文件
        rm_old_img = r'rm %s%d-*' % (site_helper.config.USER_COVER_PATH, item_id)
        os.system(rm_old_img)

        assert( imagefile.has_key('filename') and imagefile.has_key('value'))
        filetype = imagefile['filename'].rpartition('.')[2].lower()
        assert(filetype in ['jpg','png','jpeg'])
        assert(len(imagefile['value'])>10) # 插入的头像文件过小
        randint = self.getRandom()
        saved_file_path = '%s%d-%d.%s' % (site_helper.config.USER_COVER_PATH, item_id, randint, filetype)
        with open(saved_file_path, 'w') as f:
            f.write(imagefile['value'])
        self.update(item_id, {'cover_url':'%s%d-%d.%s' % (site_helper.config.USER_COVER_URL, item_id, randint, filetype)})
        os.system('convert "%s" -resize "%dx%d>" +profile "*" "%s"' % (saved_file_path, self.resize_width, self.resize_height, saved_file_path))

    def _removeSmallFiles(self, user_id):
        '''删除旧的大/小图片, 避免随机数相同时使用老的缓存文件'''
        rm_old_cmd = r'rm %s%d-*_* 2>/dev/null' % (site_helper.config.USER_COVER_PATH, user_id)
        os.system(rm_old_cmd)

    def _formatInsertData(self,data):
        ret_data = self._copyData(data)
        #assert(ret_data.has_key('password') and len(ret_data.password)>0)
        if ret_data.has_key('password'):
            ret_data.password = self.getMD5Password(ret_data.password)
            assert(len(ret_data.password) == 32)
        assert(ret_data.has_key('username'))
        #assert(ret_data.has_key('email'))
        if ret_data.has_key('email'):
            ret_data.email = ret_data.email.strip()
        ret_data.username = ret_data.username.strip()
        assert(len(ret_data.username) > 0)
        #assert(len(ret_data.email) > 0)
        ret_data = self._ipToInt(ret_data)
        if not ret_data.has_key('imagefile'):
            ret_data.cover_url = '/img/page/default_user.png'
        return ret_data

    def getMD5Password(self, password):
        m = hashlib.md5()
        if type(password) is unicode:
            password = password.encode('utf-8')
        try:
            m.update('songshu_ajie'+password)
        except:
            print 'Debug info: password\'s type is', type(password)
            raise
        return m.hexdigest()

    def activate(self, userid):
        self.update(userid, {'activated':'on'})

    def resetPassword(self, user_id, new_password):
        '''new_password是没有加密过的'''
        self.update(user_id, {'password': self.getMD5Password(new_password)})

    def _ipToString(self, data):
        if data is not None:
            newUser = site_helper.deepCopy(data)
            if data.has_key('register_ip'):
                self._assertLongInput(data['register_ip'])
                newUser['register_ip'] = socket.inet_ntoa(struct.pack('=L',newUser['register_ip']))
            if data.has_key('login_ip'):
                self._assertLongInput(data['login_ip'])
                newUser['login_ip'] = socket.inet_ntoa(struct.pack('=L',newUser['login_ip']))
            return newUser
        else:
            return None

    def _ipToInt(self, data):
        if data is not None:
            newUser = site_helper.deepCopy(data)
            if data.has_key('register_ip'):
                self._assertStrInput(data['register_ip'])
                newUser['register_ip'] =struct.unpack('=L',socket.inet_aton(newUser['register_ip']))[0]
            if data.has_key('login_ip'):
                self._assertStrInput(data['login_ip'])
                newUser['login_ip'] =struct.unpack('=L',socket.inet_aton(newUser['login_ip']))[0]
            return newUser
        else:
            return None

    def increaseLoginCount(self, user_id):
        self._getDB().update('update User set login_count = login_count +1 where Userid=%s', user_id)


    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            email           varchar(100) not null default '',
            password        varchar(32)  not null default '',
            username        varchar(32)  charset utf8 not null,
            realname        varchar(100) charset utf8 not null default '',
            address         varchar(1000) charset utf8 not null default '',
            intro           varchar(1000) charset utf8 not null default '',
            phone_number    varchar(20) not null default '',
            cover_url       varchar(300)  not null default '/img/page/default_user.png',
            birthday        date         not null default '1000-01-01',
            sex             enum('男','女','unknown') charset utf8 not null default 'unknown',
            activated       enum('off','on') not null default 'off',
            register_ip     bigint(20)   unsigned not null default 0,
            login_ip        bigint(20)   unsigned not null default 0,
            login_count     int unsigned  not null default 0,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id)
        )ENGINE=InnoDB;
        '''
