#coding=utf-8
from ImgLink import ImgLink

class IndexCycle(ImgLink):
    table_name = 'IndexCycle'
    column_names = ['title','tag','paragraph','href','alt','Imageid','target', 'imgorder']

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            href            varchar(500)  charset utf8 not null default '',
            target          ENUM('_blank','_self') not null default '_self',
            alt             varchar(100)  charset utf8 not null default '',
            title           varchar(100)  charset utf8 not null default '',
            tag             varchar(50)  charset utf8 not null default '',
            imgorder        int unsigned not null default 0,
            paragraph       varchar(4000) charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

