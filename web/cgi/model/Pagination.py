#coding=utf-8
from Model import Model
import math

ZARKFX = '''<div class="pagination02" fx="pagination[max=%d;displaycount=%d;firsttext=%s;lasttext=%s;%s]"></div>'''

class Pagination(Model):
    table_name = 'Pagination'
    column_names = ['name','firsttext', 'lasttext', 'displaycount', 'itemcount',]
    
    def getHtml(self, pagination, page_num, max_count, others=None):
        #if max_count is 0, then page_max = 1
        if others is None: others = {}
        page_max = max(1,math.ceil(max_count * 1.0 / pagination.itemcount))
        return ZARKFX % (page_max, pagination.displaycount, pagination.firsttext, pagination.lasttext, ';'.join(['%s=%s' % (k,v) for k,v in others.items()]))

    def getLimit(self,pagination,page_num,max_count):
        '''return [start,length]'''
        try:
            return (pagination.itemcount * (page_num -1), pagination.itemcount)
        except:
            print 'Please insert these datas which in sql/init_database.sql file into your database.'
            raise

    table_template = ''' \
        CREATE TABLE Pagination (
            Paginationid        int unsigned not null auto_increment,
            name                varchar(100) not null default '',
            firsttext           varchar(100) charset utf8 not null default '',
            lasttext            varchar(100) charset utf8 not null default 'None',
            displaycount        int unsigned not null default 10 comment '显示的页数',
            itemcount           int unsigned not null default 10 comment '每页显示的item数',
            primary key (Paginationid),
            unique key (name)
        )ENGINE=InnoDB;
        '''
