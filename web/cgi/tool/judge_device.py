#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web,  page_helper

mob_markers = ['ios', 'iphone', 'android', 'adr', 'windows phone', 'mqqbrowser', 'uc', 'UC']

def JudgeDevice(handler):
    ua = web.ctx.env.get('HTTP_USER_AGENT', '')
    ua = ua.lower()
    device = ''
    for i in mob_markers:
        if i in ua and 'ipad' not in ua:
            device = 'mob'
        
    if device == 'mob':
        return page_helper.redirectTo('http://m.aoaola.com' + web.ctx.env.get('REQUEST_URI', ''))
    else:
        return handler()

