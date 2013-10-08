#coding=utf-8
import site_helper, web
from site_helper import getModel

class Index:
    def GET(self):
        return site_helper.editor_render.Index()

