#!coding=utf-8
import unittest, test_helper, os
from site_helper import getDBHelper
from model import AdminUser

class TestAdminUser(unittest.TestCase):

    def setUp(self):
        self.user_model = AdminUser()
        test_helper.cleanTable(self.user_model.table_name)
