#!/usr/bin/env python
#coding=utf-8
import sys, os
filePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(filePath + '/..')
import site_helper
from site_helper import getModel

def getDBHelper():
    from model import DBHelper
    return DBHelper()

def getSinsitiveKeys():
    return [a for a,b in getModel('LevelTable').getLevelsByPage('sinsitive-table')]

def check(sinsitive_keys, table_name, id_col_name, mark_col_name, content_col_name):
    db = getDBHelper()
    rows = db.fetchSome('select * from ' + table_name + ' where ' + mark_col_name + '=0 ')
    for row in rows:
        content = row.get(content_col_name)
        is_sinsitive = 1
        for key in sinsitive_keys:
            if key in content:
                is_sinsitive = 2
                break
        db.update('update '+table_name+' set '+mark_col_name+'=%s where ' + id_col_name + '=%s', (is_sinsitive, row.get(id_col_name)))


if __name__ == '__main__':
    db = getDBHelper()
    if len(sys.argv) < 5:
        print """usage: python sinsitive_check.py <table_name> <id_col_name> <mark_col_name> <content_col_name> <content_col_name> ... """
        exit(1)

    table_name = sys.argv[1]
    id_col_name = sys.argv[2]
    mark_col_name = sys.argv[3]

    # check arguments
    if not db.isTableExists(table_name):
        sys.stderr.write("Database table name error.\n")
        exit(1)

    col_list = db.getTableColumns(table_name)
    for col in sys.argv[2:]:
        if col not in col_list:
            sys.stderr.write("Database column name error.\n")
            exit(1)

    # check
    sinsitive_keys = getSinsitiveKeys()
    for content_col_name in sys.argv[4:]:
        check(sinsitive_keys, table_name, id_col_name, mark_col_name, content_col_name)

