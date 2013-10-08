#coding=utf-8
from Model import Model
import hashlib, site_helper, time
import subprocess

# ../page/mail/Activate.html

class ACode(Model):  
    '''Activate Code: 邮箱验证码'''
    table_name = 'ACode'
    column_names = ['Userid','acode','created']
    secret_key = '6c31db57530094a8b48fdaa053b'
    mail_subject = '欢迎加入凹凹啦'
    #mail_template = site_helper.page_render_nobase.mail.Activate if site_helper.page_render_nobase is not None else None # 运行testing代码时,render等于None

    def getACode(self, userid):
        m = hashlib.md5()
        m.update(self.secret_key + str(userid) + str(time.time()))
        return m.hexdigest()

    def updateACode(self, userid, acode):
        self.replaceInsert({'Userid':userid, 'acode':acode})

    def deleteByUserid(self, userid):
        acode = self.getOneByWhere('Userid=%s',[userid])
        if acode is not None:
            self.delete(acode.get(self.table_name+'id'))

    def sendACode(self, user, acode):
        '''使用heirloom-mailx发送邮件'''
        p = subprocess.Popen(['mail','-s',self.mail_subject,'-r','noreply','-B',user.email],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        #assert(self.mail_template is not None)
        content = str(site_helper.page_render_nobase.mail.Activate(user, acode))
        p.stdin.write(content)
        p.communicate()
        p.stdin.close()

    def getByUserid(self, user_id):
        return self._getDB().fetchOne('select * from '+self.table_name+' where Userid=%s', user_id)

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Userid          varchar(100) not null,
            acode           varchar(32)  not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (Userid)
        )ENGINE=InnoDB;
        '''
