#coding=utf-8
from OAuth2 import OAuth2
import site_helper
from site_helper import getModel
import urllib

# OAuth2.py
''' help: http://wiki.dev.renren.com/wiki/Web%E7%BD%91%E7%AB%99%E6%8E%A5%E5%85%A5 '''

class RenRen(OAuth2):
    SITE_NAME = 'RenRen'
    MODEL_NAME = 'oauth.RenRenOAuth2'
    CN_SITE_NAME = '人人网'
    APP_ID = '6e533046dbd64fc1bfca05449cbaf12f'
    SECRET_KEY = '65b8d0e9a3ad4a038b72d2ca33fd07bd'
    SCOPE = 'publish_share publish_feed publish_comment'
    REQUEST_AUTHORIZATION_CODE = 'https://graph.renren.com/oauth/authorize'
    REQUEST_ACCESS_TOKEN = 'https://graph.renren.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REQUEST_OPEN_ID = 'http://api.renren.com/restserver.do'
    SHARE_URL = ''

    def _request(self, params):
        params = site_helper.copy(params)
        params['v'] = '1.0'
        params['format'] = 'JSON'
        params['sig'] = self.sign(params, self.SECRET_KEY)
        content = urllib.urlopen(self.REQUEST_OPEN_ID, urllib.urlencode(params)).read()
        return content

    def getOpenId(self, access_token):
        params = {
            'method':   'users.getLoggedInUser',
            'access_token':   access_token,
        }
        content = self.loadsJson(self._request(params))
        return content.uid

    def pickOpenId(self, content):
        content = self.loadsJson(content)
        return content.uid

    def assignUserInfo(self, data, access_token):
        params = {
            'method':   'users.getInfo',
            'access_token':   access_token,
            'fields': 'name,sex,mainurl'
        }
        content = self._request(params).partition('[')[2].rpartition(']')[0]
        content = self.loadsJson(content)

        new_data = site_helper.copy(data)
        model = getModel(self.MODEL_NAME)

        new_data['username'] = content.name

        if str(content.sex) == '1':
            new_data['sex'] = '男'
        elif str(content.sex) == '2':
            new_data['sex'] = '女'

        image_file = self.requestImageFile(content.mainurl)
        if image_file:
            new_data['imagefile'] = image_file

        return new_data

    def share(self, user_id, access_token, comment, **options):
        url = options.get('url', None)
        comment = comment.replace('@','')
        params = {
            'method':   'share.share',
            'type':     6,
            'comment':  comment,
            'access_token':  access_token,
            'url':  url if url else site_helper.config.HOST_NAME,
        }
        self._request(params)
