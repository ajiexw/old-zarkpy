#coding=utf-8
import web, json

def render(data):
    assert(type(data) is dict)
    inputs = web.input()
    data = _removeUnjson(data)
    # 在API.js中必须使用callback形式, 否则无法
    if inputs.has_key('callback'):
        callback = inputs['callback']
        return '%s(%s);' % (callback, json.dumps(data)) 
    else:
        return json.dumps(data)

def _removeUnjson(data):
    '''过滤掉不能json化的数据'''
    newData = {}
    for k,v in data.items():
        if type(v) in [int,long,str,bool,list]:
            newData[k] = v
    return newData

