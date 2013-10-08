#coding=utf-8
import site_helper, web, page_helper

# ../editor/LevelTable.html

class LevelTable:

    def GET(self, page_name):
        i = web.input()
        content = site_helper.getModel('LevelTable').getContentByPage(page_name)
        title = i.get('title', '')
        tip = i.get('tip', '')
        return site_helper.editor_render.LevelTable(page_name, content, title, tip)

    def POST(self, i=None):
        if i is None: i = web.input(imagefile={})
        assert(i.has_key('page'))
        assert(i.has_key('content'))
        assert('\t' not in i.content)
        table_model = site_helper.getModel('LevelTable')
        table_model.replaceInsert(i)
        page_helper.refresh()
