#coding=utf-8
from Model import Model
from copy import copy
from site_helper import getModel

# ../testing/model_testing/TestLevelTable.py

class LevelTable(Model):
    table_name = 'LevelTable'
    column_names = ['page', 'content']

    def getContentByPage(self, page):
        one = self.getOneByWhere('page=%s', [page])
        return one.content if one is not None else ''

    def levelsToLines(self, levels):
        '''把levels数据变成行数据, 详见测试: test_LevelsToLines'''
        ret_list = []
        queue = []
        def _levelsToLines(levels):
            for a,b in levels:
                ret_list.append(copy(queue+[a]))
                if len(b) != 0:
                    queue.append(a)
                    _levelsToLines(b)
                    queue.pop()
        _levelsToLines(levels)
        assert(len(queue) == 0)
        return ret_list

    def levelsToDict(self, levels):

        def _levelsToDict(key, values):
            if len(values) == 0:
                if ':' not in key:
                    return str(key)
                else:
                    a,b,c = key.partition(':')
                    return (a, c)
            else:
                ret_dict = {'__index': _levelsToDict.index}
                _levelsToDict.index += 1
                for a,b in values:
                    sub = _levelsToDict(a, b)
                    if type(sub) is str:
                        ret_dict[sub] = ''
                    elif type(sub) is tuple:
                        ret_dict[sub[0]] = sub[1]
                    else:
                        ret_dict[a] = sub
                return ret_dict
        _levelsToDict.index = 0

        return _levelsToDict('root', levels) if len(levels) > 0 else None

    def levelsToList(self, levels):
        def _levelsToList(key, values):
            if len(values) == 0:
                if ':' not in key:
                    return str(key)
                else:
                    a,b,c = key.partition(':')
                    return (a, c)
            else:
                ret_list = []
                ret_dict = {}
                for a,b in values:
                    sub = _levelsToList(a, b)
                    if type(sub) is tuple:
                        ret_dict[sub[0]] = sub[1]
                    else:
                        ret_list.append(sub)
                return [key, ret_dict] if ret_dict else [key, ret_list]

        root = _levelsToList('root', levels) if len(levels) > 0 else None
        return root[1] if root and len(root) == 2 and root[0]=='root' else root

    def getLevels(self, content):
        '''根据content返回递归的二元组组成的list, 详见测试: test_getLevels_4'''
        queue = []
        ret_list = []
        for l in content.replace('\r','').split('\n'):
            assert('\t' not in l)
            if l.strip() == '': continue
            space_len = len(l)-len(l.lstrip())
            l = l.strip()
            if len(queue) == 0:
                next_level = []
                ret_list.append((l, next_level))
                queue.append((space_len, next_level))
            else:
                if space_len > queue[-1][0]:
                    next_level.append((l, []))
                    next_level = next_level[-1][1]
                    queue.append((space_len, next_level))
                elif space_len == queue[-1][0] and space_len != 0:
                    assert(len(queue) > 1)
                    queue.pop()
                    next_level = queue[-1][1]
                    next_level.append((l, []))
                    next_level = next_level[-1][1]
                    queue.append((space_len, next_level))
                else:
                    while len(queue)>1 and space_len < queue[-1][0]:
                        queue.pop()
                    queue.pop()
                    if len(queue) > 0:
                        next_level = queue[-1][1]
                        next_level.append((l, []))
                        next_level = next_level[-1][1]
                        queue.append((space_len, next_level))
                    else:
                        next_level = []
                        ret_list.append((l, next_level))
                        queue.append((space_len, next_level))

        return ret_list

    def getLevelsByPage(self, page):
        return self.getLevels(self.getContentByPage(page))

    def getThreeLayerDatas(self, content, model_name, default_values = {}):
        '''获得三级分类数据, 其中第一级为分类, 第二级为model_id, 第三级为属性重写.'''
        model  = getModel(model_name)
        levels = getModel('LevelTable').getLevels(content)
        for a,b in levels:
            if len(b) > 0:
                for c,d in b:
                    item = model.get(c)
                    if item is not None:
                        for k,v in default_values.items():
                            if not item.has_key(k):
                                item[k] = v
                        for overwrite, none in d:
                            p1,p2,p3 = overwrite.partition(':')
                            item[p1.strip()] = p3.strip()
                        del d[:]
                        d.append(item)
                    else:
                        del d[:]
                    assert(len(d) <= 1)
        return levels

    def getTwoLayerDatas(self, content, model_name, default_values = {}):
        '''获得二级分类数据, 第一级为model_id, 第二级为属性重写.'''
        model  = getModel(model_name)
        levels = getModel('LevelTable').getLevels(content)
        for a,b in levels:
            item = model.get(a)
            if item is not None:
                for k,v in default_values.items():
                    if not item.has_key(k):
                        item[k] = v
                for overwrite, none in b:
                    p1,p2,p3 = overwrite.partition(':')
                    item[p1.strip()] = p3.strip()
                del b[:]
                b.append(item)
            else:
                del b[:]
            assert(len(b) <= 1)
        return levels

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            page    varchar(100)  charset utf8 not null,
            content text charset utf8 not null default '',
            primary key ({$table_name}id),
            unique key (page)
        )ENGINE=InnoDB;
        '''
