#coding=utf-8
from OAuth2 import OAuth2
import site_helper
from site_helper import getModel
import urllib, httplib, urllib2, mimetypes

# OAuth2.py
''' help: http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3_V2 '''

class Sina(OAuth2):
    SITE_NAME = 'Sina'
    MODEL_NAME = 'oauth.SinaOAuth2'
    CN_SITE_NAME = '新浪微博'
    APP_ID = '1268783154'
    SECRET_KEY = 'bab8198d96685d6be1df88f0534c5918'
    SCOPE = ''
    REQUEST_AUTHORIZATION_CODE = 'https://api.weibo.com/oauth2/authorize'
    REQUEST_ACCESS_TOKEN = 'https://api.weibo.com/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    REQUEST_OPEN_ID = 'https://api.weibo.com/2/account/get_uid.json'
    SHARE_URL = 'https://api.weibo.com/2/statuses/update.json'
    SHARE_URL_PIC = 'https://upload.api.weibo.com/2/statuses/upload.json'
    
    def pickOpenId(self, content):
        content = self.loadsJson(content)
        return content.uid

    def assignUserInfo(self, data, access_token):
        new_data = site_helper.copy(data)
        model = getModel(self.MODEL_NAME)
        open_id = model.getOpenIdByAccessToken(access_token)
        if open_id is None:
            return new_data

        url = self.getUrl('https://api.weibo.com/2/users/show.json', (
            'access_token', access_token,
            'oauth_consumer_key', self.APP_ID,
            'uid', open_id,
            'format', 'json',
            ))
        
        response, content =  self.getHtmlContent(url)
        if response.status != 200:
            return new_data

        content = self.loadsJson(content)

        if content.get('error_code', None):
            return new_data

        new_data['username'] = content.screen_name

        if content.gender == 'm':
            new_data['sex'] = '男'
        elif content.gender == 'f':
            new_data['sex'] = '女'
        else:
            new_data['sex'] = '保密'

        image_file = self.requestImageFile(content.avatar_large)
        if image_file is None:
            return new_data
        new_data['imagefile'] = image_file

        return new_data

    def share(self, user_id, access_token, comment, **options):
        open_id = getModel(self.MODEL_NAME).getOpenIdByAccessToken(access_token)
        url = options.get('url', None)
        if url:
            comment = comment + ' ' + url

        if open_id:
            params = {
                'access_token': access_token,
                'oauth_consumer_key': self.APP_ID,
                'uid': open_id,
                'status': comment,
            }

            if options.get('pic', None):
                path = site_helper.config['APP_ROOT_PATH'] + 'web' + options['pic']
                content = self.post_multipart('upload.api.weibo.com','/2/statuses/upload.json',params.items(), [('pic', path, open(path, 'rb').read())])
            else:
                params = urllib.urlencode(params)
                content = urllib.urlopen(self.SHARE_URL, params).read()

