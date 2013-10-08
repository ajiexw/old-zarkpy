#coding=utf-8
import site_helper, web, page_helper
from site_helper import getModel

# ../../editor/content/IndexCycle.html

class IndexCycle:

    def GET(self):
        i = web.input()

        cycle_model = getModel('IndexCycle')
        cycles = cycle_model.getAll({'orderby':'imgorder'})

        return site_helper.editor_render.content.IndexCycle(cycles)

