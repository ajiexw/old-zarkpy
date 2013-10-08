#coding=utf-8
from Model import Model
import site_helper

class Category(Model):
    table_name = 'Category'
    relative_model_name = 'Model' # 相关的model名, 即哪一个model使用此Category
    column_names = ['title', 'intro']

    def getAll(self,env=None):
        assert(len(self.table_name) > 0)
        assert(len(self.relative_model_name) > 0)
        assert(len(self.column_names) > 0)
        categorys = Model.getAll(self,env)
        for category in categorys:
            category['model_name'] = self.relative_model_name
            category['Categoryid'] = category.get(self.primary_key)
        return categorys

    def get(self,itemid):
        '''给get到的数据添加model_name Categoryid={$table_name}id'''
        assert(len(self.table_name) > 0)
        assert(len(self.relative_model_name) > 0)
        assert(len(self.column_names) > 0)
        category = Model.get(self,itemid)
        category['model_name'] = self.relative_model_name
        category['Categoryid'] = category.get(self.primary_key)
        return category

    def getWithAll(self,itemid):
        '''给get到的数据添加models model_name Categoryid={$table_name}id'''
        assert(len(self.table_name) > 0)
        assert(len(self.relative_model_name) > 0)
        assert(len(self.column_names) > 0)
        category = Model.get(self, itemid)
        relative_model = site_helper.getModel(self.relative_model_name)
        category['models'] = relative_model.getAll({'where':('Categoryid=%s',[itemid])})
        category['model_name'] = self.relative_model_name
        category['Categoryid'] = category.get(self.primary_key)
        return category

    def delete(self,itemid):
        assert(type(itemid) in [int,long])
        assert(len(self.table_name) > 0)
        assert(len(self.relative_model_name) > 0)
        assert(len(self.column_names) > 0)
        self._getDB().delete('delete from '+self.relative_model_name+' where Categoryid=%s',itemid)
        Model.delete(self,itemid)
        
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            title           varchar(30)  charset utf8 not null default '',
            intro           varchar(150) charset utf8 not null default '',
            primary key ({$table_name}id),
            unique key (title)
        )ENGINE=InnoDB; '''
