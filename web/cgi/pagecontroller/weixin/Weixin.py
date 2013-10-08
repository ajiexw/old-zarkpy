#coding=utf-8
import os, hashlib, web, site_helper
from lxml import etree
from site_helper import getModel 
from controller import Event as EventCtrl

CONFIG = { "TOKEN":'aoaola_weixin', 'HOST':'http://m.aoaola.com'}
HEADER_XML = """<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType>"""
TEXT_XML = """<Content><![CDATA[%s]]></Content>"""
PIC_HEADER_XML = """<ArticleCount>%s</ArticleCount><Articles>"""
PIC_XML = """<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"""
PIC_FOOTER_XML = """</Articles>"""
FOOTER_XML = """<FuncFlag>0</FuncFlag></xml>"""
ARTICLE_COUNT = 5

class Weixin:       
    def GET(self):
        i = web.input()
        signature, timestamp, nonce, echostr = i.signature, i.timestamp, i.nonce, i.echostr
        tmplist = [CONFIG['TOKEN'], timestamp, nonce]
        tmplist.sort()
        tmpstr = "%s%s%s" % tuple(tmplist)
        hashstr = hashlib.sha1(tmpstr).hexdigest()
 
        if hashstr == signature:
            return echostr
        else: 
            return 'Error' + echostr
 
    def POST(self):
        data = web.data()
        root = etree.fromstring(data)
        child = list(root)
        recv = {}
        for i in child:
            recv[i.tag] = i.text
        from_username,to_username,create_time,msg = recv['FromUserName'],recv['ToUserName'],recv['CreateTime'],recv['Content']

        msg = msg.encode('utf-8', 'ignore')
        article_count = 5
        env = {'limit':(0,article_count)}
        content = ''

        if msg == '今日话题':
            topic = getModel('Topic').getTopicOfToday('19')
            content = '<a href="%s/topic/%s">点击参与->%s</a>' % (CONFIG["HOST"], topic.Topicid, topic.title)
            msg_type = 'text'
        elif msg == '主题':
            newss = getModel('News').getAll(env)
            for news in newss:
                pic_url = 'http://m.aoaola.com'+site_helper.resizeImage(news.uri, '180x140>')
                content += PIC_XML % (news.title, news.summary, pic_url, 'http://m.aoaola.com/news/%s' % int(news.Newsid))  
            msg_type = 'news'
        elif msg == '逛街' or msg == '2':
            reviews = getModel('Review').getAll(env)
            for r in reviews:
                user = getModel('User').get(r.Userid)
                if r == reviews[0]:
                    pic_url = 'http://m.aoaola.com'+user.cover_url
                else:
                    pic_url = 'http://m.aoaola.com'+site_helper.getSmallPortrait(user.cover_url, user.small_portrait, 80)
                content += PIC_XML % (r.title, r.content, pic_url, 'http://m.aoaola.com/review/%s' % int(r.Reviewid))  
            msg_type = 'news'
        elif msg == '试用' or msg == '3':
            events = getModel('Event').getAll(env)
            article_count = 0
            for e in events:
                e.status = EventCtrl().getStatus(e.start_time, e.end_time)
                if e.status == 'running':
                    article_count = article_count + 1
                    pic_url = 'http://m.aoaola.com' + e.big_image_url
                    content += PIC_XML % (e.title, e.title, pic_url, 'http://m.aoaola.com/event/%s' % int(e.Eventid))  
            msg_type = 'news'
        elif msg == '新贴' or msg == '4':
            env['orderby'] = 'Topicid desc'
            topics = getModel('Topic').getAll(env)
            for t in topics:
                user = getModel('User').get(t.Userid)
                if t == topics[0]:
                    pic_url = 'http://m.aoaola.com'+user.cover_url
                else:
                    pic_url = 'http://m.aoaola.com'+site_helper.getSmallPortrait(user.cover_url, user.small_portrait, 80)
                content += PIC_XML % (t.title, t.content, pic_url, 'http://m.aoaola.com/topic/%s' % int(t.Topicid))  
            msg_type = 'news'
        elif msg == '帮助' or msg == 'help' or msg == '0':
            content = '凹凹啦美妆社区手机站：<a href="http://m.aoaola.com">http://aoaola.com</a>\n \n回复"帮助"或"help"即可查看此帮助信息。\n \n目前处于开发测试状态'
            msg_type = 'text'
        elif msg == '兑奖码':
            content = '你的兑奖码是：%s' % (from_username)
            msg_type = 'text'

        header = HEADER_XML % (from_username, to_username, create_time, msg_type) 
        if msg_type == 'text':
            echostr = header + TEXT_XML%(content) + FOOTER_XML
        elif msg_type == 'news': 
            echostr = header + PIC_HEADER_XML%(article_count) + content + PIC_FOOTER_XML + FOOTER_XML

        return echostr
