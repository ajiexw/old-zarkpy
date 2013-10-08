#!/usr/bin/env python
#coding=utf-8
if __name__ != "__main__":
    raise 'import test_method module is forbidden'

import os, sys
sys.path.append(os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0])
import test_init

if len(sys.argv) != 3:
    print 'Usage: ./testing/test_method.py file method'
    exit(0)

#do test
import_module = sys.argv[1][:-3].replace('/','.')
if import_module.startswith('..'):
    import_module = import_module[2:]
test_module = __import__(import_module)
test_class = eval("test_module.%s.%s" % (import_module.partition('.')[2], import_module.rpartition('.')[2]))
#help( test_class(sys.argv[2].strip()))
print '====== TEST METHOD %s ======' % sys.argv[2]
test_class(sys.argv[2].strip()).run()

