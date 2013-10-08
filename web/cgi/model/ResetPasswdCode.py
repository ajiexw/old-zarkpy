#coding=utf-8
from ACode import ACode
import hashlib, site_helper, time
import subprocess


class ResetPasswdCode(ACode):  
    '''Reset Password Code: 找回密码验证码'''
    table_name = 'ResetPasswdCode'
    column_names = ['Userid','acode','created']
    secret_key = '64c730d81ad293156a8f1d3'
    mail_subject = '凹凹啦密码重置邮件'
    mail_template = site_helper.page_render_nobase.mail.ResetPassword if site_helper.page_render_nobase is not None else None

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Userid          varchar(100) not null,
            acode            varchar(32)  not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (Userid)
        )ENGINE=InnoDB;
        '''
