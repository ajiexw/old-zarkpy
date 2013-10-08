#!/usr/bin/env python
#coding=utf-8
if __name__ != "__main__":
    raise 'import test_one module is forbidden'

import os, sys
sys.path.append(os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0])
import site_helper
import test_init
from unittest import TestLoader, TestSuite, TextTestRunner

if len(sys.argv) != 2:
    print 'Usage: ./testing/test_one.py file'
    exit(0)

#do test
suites = []
import_module = sys.argv[1][:-3].replace('/','.')
if import_module.startswith('..'):
    import_module = import_module[2:]
try:
    test_module = __import__(import_module)
    test_class = eval("test_module.%s.%s" % (import_module.partition('.')[2], import_module.rpartition('.')[2]))
except:
    print 'inport module name:', import_module
    raise

suites.append( TestLoader().loadTestsFromTestCase(test_class))
TextTestRunner().run( TestSuite(suites) )
