#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper

# ../../model

class TestComment(unittest.TestCase):

    def setUp(self):
        self.model = site_helper.getModel('Comment')
        test_helper.cleanTable(self.model.table_name, 'Review')

