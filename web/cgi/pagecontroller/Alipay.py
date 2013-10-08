#coding=utf-8
import site_helper, web, page_helper
from site_helper import getModel
from tool import alipay
# ../page/Alipay.html

class Alipay:

    def GET(self):
        alipayTool=alipay()
        params={  
            '_input_charset':'utf-8',
            "body":"一翻",
            'logistics_fee':'0',
            'logistics_payment':'SELLER_PAY',
            'logistics_type':'EXPRESS',
            "notify_url":"http://me.aoaola.com/alipay-return",
            "out_trade_no":"f36474ca6749f653",
            "partner":"2088702246877050",
            "payment_type":"1",
            'price':'0.1',
            'quantity':'1',
            'receive_address':'无需收货地址',
            'receive_mobile':'13800138000',
            'receive_name':'无需收货人',
            'receive_phone':'02161686888',
            'receive_zip':'100000',
            "return_url":"http://me.aoaola.com/alipay-return", 
            "seller_id":"2088702246877050",
            "service":"trade_create_by_buyer",
            "show_url":"http://me.aoaola.com/alipay",
            "subject":"一翻",
            "sign":"gvvqfk1cecbxgdg4f8hp2p54xbv8gbdd",
            "sign_type":"MD5"
        }  
        payhtml=alipayTool.createPayForm(params) 
        return site_helper.page_render_nobase.Alipay(payhtml)


