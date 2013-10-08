#coding=utf-8
from ImgLink import ImgLink

class Article(ImgLink):
    table_name = 'Article'
    category_table_name = 'ArticleCategory'
    column_names = ['title','paragraph','Categoryid','time','Imageid']
    decorator = [('Orderby',{'orderby':'time desc'}),('Pagination',{})]

    def insert(self,data):
        if len(self.category_table_name) > 0:
            # 断言当使用category_table时，Categoryid对应的数据必须已经存在
            assert(data.has_key('Categoryid'))
            assert(self._getDB().fetchFirst('select count(*) from ' + self.category_table_name+' where '+self.category_table_name+'id=%s',data.Categoryid) == 1)
        else:
            print 'WARNING: self.category_table_name is empty in model/Article.py'
        return ImgLink.insert(self,data)

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            title           varchar(200)  charset utf8 not null default '',
            paragraph       text charset utf8 not null,
            Categoryid      int unsigned  not null default 0,
            time            date not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            key (time)
        )ENGINE=InnoDB; '''
