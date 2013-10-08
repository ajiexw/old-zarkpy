#!/usr/bin/env python
#coding=utf-8
import sys, os
filePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(filePath+'/..')

USAGE = 'python excute_sql.py file_name1.sql file_name2.sql ..'

import site_helper


if __name__=='__main__':
    if len(sys.argv) <= 1:
        print USAGE
        exit(0)

    for file_name in sys.argv[1:]:
        if not os.path.exists(file_name):
            print USAGE
            exit(0)

    db = site_helper.getDBHelper()
    for file_name in sys.argv[1:]:
        sql = open(file_name).read()
        db.executeQuery(sql)
