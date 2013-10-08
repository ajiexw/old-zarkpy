#coding=utf-8
from User import User

class AdminUser(User):
    table_name = 'AdminUser'
    column_names = ['email', 'name','password', 'portait_url',]

    table_template = \
            ''' CREATE TABLE {$table_name} (
                {$table_name}id int unsigned  not null auto_increment,
                email           varchar(100) not null,
                name            varchar(32)  charset utf8 not null,
                password        varchar(32)  not null,
                portait_url     varchar(50)  not null default '',
                created         timestamp not null default current_timestamp,
                primary key ({$table_name}id),
                unique key (email)
            )ENGINE=InnoDB; '''
