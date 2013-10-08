#coding=utf-8
import site_helper, web, page_helper

#  ../../editor/imagecenter/PageContent.html

class PageContent:

    def GET(self):
        i = web.input()
        image_model = site_helper.getModel('ContentImage')
        env = {'pagination':'thirty items', 'orderby':'ContentImageid desc'}

        tag = i.get('tag', None)
        if tag is not None:
            env['where'] = ('tag=%s', [tag])

        images = image_model.getAll(env)
        pagination_html = image_model.getPaginationHtml(env)

        return site_helper.editor_render.imagecenter.PageContent(images, pagination_html)

    def POST(self):
        pass
