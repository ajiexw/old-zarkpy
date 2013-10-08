#coding=utf-8
import site_helper, web, page_helper
from site_helper import getModel
from tool import alipay
# ../page/AlipayReturn.html

class AlipayReturn:

    def GET(self,f):
        alipayTool=alipay()
        rlt=alipayTool.notifiyCall(f,verify=True)  
        if rlt=='success':  
            return page_helper.redirectTo('/')


