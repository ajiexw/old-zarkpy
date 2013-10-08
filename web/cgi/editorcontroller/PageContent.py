#coding=utf-8
import site_helper, web, page_helper

# ../editor/PageContent.html

class PageContent:

    def GET(self, page_name):
        i = web.input()
        content = i.get('content', '')
        model_name = i.get('model_name', '')
        title = i.get('title', '')
        tip = i.get('tip', '')
        ids = site_helper.getModel('PageContent').getModelids(page_name, content)
        return site_helper.editor_render.PageContent(ids, page_name, content, model_name, title, tip)

    def POST(self, i=None):
        if i is None: i = web.input(imagefile={})
        assert(i.has_key('page'))
        assert(i.has_key('content'))
        assert(i.has_key('model_ids'))
        assert(i.has_key('model_name'))

        content_model = site_helper.getModel('PageContent')
        content_model.cleanModelids(i.page, i.content)

        ids = [int(j.strip()) for j in i.model_ids.strip().split('\n') if j.strip().isdigit()]
        for id in ids:
            data = site_helper.extend(i, {'model_id': id})
            content_model.insert(data)

        page_helper.refresh()

