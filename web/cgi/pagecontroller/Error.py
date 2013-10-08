#coding=utf-8
import site_helper, web

class Error:
    def GET(self):
        raise Exception('访问到了pagecontroller/Error!')

    def POST(self):
        raise Exception('访问到了pagecontroller/Error!')

