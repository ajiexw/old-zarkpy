#!coding=utf-8
import unittest, test_helper, os, site_helper
from site_helper import getDBHelper

class TestLevelTable(unittest.TestCase):
    '''../../model/LevelTable.py'''

    def setUp(self):
        self.model = site_helper.getModel('LevelTable')
        test_helper.cleanTable(self.model.table_name)

    def test_getContentByPage(self):
        table_model = self.model
        data = test_helper.storage({'page':'sdjl', 'content':'lyh'})
        new_id = table_model.insert(data)
        content = table_model.getContentByPage('sdjl')
        self.assertEqual(content, 'lyh')

    def test_getLevels_1(self):
        '''getLevels函数根据有层级关系的content, 获得list嵌套的python对象'''
        table_model = self.model
        content = '''
        aaa
            bb
            cc
        '''
        level_content = [
            ('aaa',[
                ('bb',[]),
                ('cc',[])
            ]),
        ]
        data = test_helper.storage({'page':'sdjl', 'content':content})
        table_model.insert(data)
        self.assertEqual(table_model.getLevelsByPage('sdjl'), level_content )

    def test_getLevels_2(self):
        table_model = self.model
        content = '''
        aaa
            bb
            cc
        dd
        '''
        level_content = [
            ('aaa',[
                ('bb',[]),
                ('cc',[])
            ]),
            ('dd',[])
        ]
        data = test_helper.storage({'page':'sdjl', 'content':content})
        table_model.insert(data)
        self.assertEqual(table_model.getLevelsByPage('sdjl'), level_content )

    def test_getLevels_3(self):
        table_model = self.model
        content = '''
        aaa
            bb
            cc
        ddd
            ee
                ff
            gg
            hh
        ll
        '''
        level_content = [
            ('aaa',[
                ('bb',[]),
                ('cc',[])
            ]),
            ('ddd', [
                ('ee',[
                    ('ff',[])
                ]),
                ('gg', []),
                ('hh', [])
            ]),
            ('ll',[])
        ]
        data = test_helper.storage({'page':'sdjl', 'content':content})
        table_model.insert(data)
        self.assertEqual(table_model.getLevelsByPage('sdjl'), level_content )

    def test_getLevels_4(self):
        table_model = self.model
        content = '''
        aaa
            bb
                lyh
                ll
            cc
        ddd
            ee
                ff
            gg
                jj
                k


        ll

            887

        99
            
        '''
        level_content = [
            ('aaa',[
                ('bb',[
                    ('lyh',[]),
                    ('ll',[]),
                ]),
                ('cc',[])
            ]),
            ('ddd', [
                ('ee',[
                    ('ff',[])
                ]),
                ('gg', [
                    ('jj',[]),
                    ('k',[]),
                ]),
            ]),
            ('ll',[
                ('887', []),
            ]),
            ('99',[]),
        ]
        data = test_helper.storage({'page':'sdjl', 'content':content})
        table_model.insert(data)
        self.assertEqual(table_model.getLevelsByPage('sdjl'), level_content )

    def test_LevelsToLines(self):
        content = '''
        aaa
            bb
                lyh
                ll
            cc
        ddd
            ee
                ff
            gg
                jj
                k


        ll

            887

        99
            
        '''
        lines = [['aaa'],
                ['aaa','bb'],
                ['aaa','bb','lyh'],
                ['aaa','bb','ll'],
                ['aaa','cc'],
                ['ddd'],
                ['ddd','ee'],
                ['ddd','ee','ff'],
                ['ddd','gg'],
                ['ddd','gg','jj'],
                ['ddd','gg','k'],
                ['ll'],
                ['ll','887'],
                ['99'],]
        table_model = self.model
        levels = table_model.getLevels(content)
        self.assertEqual(table_model.levelsToLines(levels), lines)
