#!/usr/bin/env python
#coding=utf-8
if __name__ != "__main__":
    raise 'import test_all module is forbidden'

import os, re, sys, MySQLdb
sys.path.append(os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0])
import site_helper
import test_init
from unittest import TestLoader, TestSuite, TextTestRunner

# 文件夹的名称需要以"_testing"结尾，避免与cgi下的module重名而引起import同名module的错误
if len(sys.argv) > 1 and sys.argv[1]=='model':
    TEST_DIR = ['model_testing'] 
else:
    print 'Usage: python testing/test_all.py model'
    exit(0)

# delete all tables from database
assert(site_helper.config.DB_DATABASE.endswith('_test'))
db = MySQLdb.connect(host=site_helper.config.DB_HOST,user=site_helper.config.DB_USER,passwd=site_helper.config.DB_PASSWORD,charset=site_helper.config.DB_CHARSET)
db.query('drop database if exists %s;' % ( site_helper.config.DB_DATABASE))
db.query('create database %s;' % ( site_helper.config.DB_DATABASE))
db.close()
# create tabels for database
from tool import init_database
init_database.init()

#do test
for test_dir in TEST_DIR:
    files = os.listdir(site_helper.config.APP_ROOT_PATH+"web/cgi/testing/%s" % test_dir)
    modules = [re.sub(".py$", "", v) for v in files if re.match("^Test[A-Z].*\\.py$", v)]
    suites = []
    for v in modules:
        try:
            test_module = __import__('testing.%s.%s' % (test_dir, v) )
            test_class = eval("test_module.%s.%s.%s" % (test_dir, v, v))
        except:
            print 'try to import %s' % ('testing.%s.%s' % (test_dir, v) )
            raise
        suites.append( TestLoader().loadTestsFromTestCase(test_class))
    TextTestRunner().run( TestSuite(suites) )
