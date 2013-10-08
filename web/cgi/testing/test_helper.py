#coding=utf-8
import web, site_helper

def storage(data):
    return web.Storage(data)

def cleanTable(*table_names):
    db = site_helper.getDB()
    for table_name in table_names:
        db.query('delete from %s' % table_name)
    db.commit()

def dropTable(*table_names):
    db = site_helper.getDB()
    for table_name in table_names:
        db.query('drop table if exists %s' % table_name)
    db.commit()

