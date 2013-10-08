#coding=utf-8
import page_helper, site_helper, web
from Insert import Insert

class ReplaceInsert(Insert):

    def GET(self):
        return self.POST()

    def POST(self, i=None):
        i = self.initInputs(i)
        model = site_helper.getModel(i.model_name)
        new_id = model.replaceInsert(i)
        return page_helper.refresh()

