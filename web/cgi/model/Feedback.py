#coding=utf-8
from ImgLink import ImgLink
import site_helper

class Feedback(ImgLink):
    table_name = 'Feedback'
    category_table_name = 'FeedbackCategory'
    column_names = ['Userid','Imageid','type','position','content','created','status','ip']
    decorator = [
        ('Pagination',{}),
    ]

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Userid          int unsigned not null default 0,
            Imageid         int unsigned not null default 0,
            type            varchar(30)  charset utf8 not null default '',
            position        varchar(100) charset utf8 not null default '',
            content         varchar(4000) charset utf8 not null default '',
            status          enum('unviewed','viewed') not null default 'unviewed',
            created         timestamp not null default current_timestamp,
            ip              bigint(20)   unsigned not null default 0,
            primary key ({$table_name}id),
            key (type),
            key (position)
        )ENGINE=InnoDB; '''

