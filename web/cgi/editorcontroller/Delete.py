#coding=utf-8
import page_helper, site_helper, web

class Delete:

    def POST(self,i=None):
        if i is None: i = web.input()

        assert(i.has_key('model_name'))
        assert(i.has_key('model_id'))
        assert(site_helper.session.is_admin)

        model = site_helper.getModel(i.model_name)

        model.delete(int(i.model_id))

        page_helper.refresh()

