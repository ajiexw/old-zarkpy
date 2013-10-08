#coding=utf-8
from Model import Model
import model
import web

class SiteConfig(Model):
    table_name = 'SiteConfig'
    column_names = ['name','value']

    table_template = \
            '''CREATE TABLE SiteConfig (
               SiteConfigid INT UNSIGNED NOT NULL AUTO_INCREMENT,
               name  VARCHAR(100) NOT NULL DEFAULT '',
               value text CHARSET UTF8 NOT NULL,
               PRIMARY KEY (SiteConfigid),
               UNIQUE KEY name (name)
            )ENGINE=InnoDB; '''
