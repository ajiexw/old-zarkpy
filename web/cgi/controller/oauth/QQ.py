#coding=utf-8
from OAuth2 import OAuth2
import site_helper
from site_helper import getModel

# OAuth2.py
''' help: http://wiki.opensns.qq.com/wiki/%E3%80%90QQ%E7%99%BB%E5%BD%95%E3%80%91Qzone_OAuth2.0%E7%AE%80%E4%BB%8B '''

class QQ(OAuth2):
    SITE_NAME = 'QQ'
    MODEL_NAME = 'oauth.QQOAuth2'
    CN_SITE_NAME = '腾讯QQ'
    APP_ID = '100277538'
    SECRET_KEY = '34380d499d0c5a9d83659fbd449b85f0'
    SCOPE = 'get_user_info,add_share,check_page_fans,add_t,add_pic_t,del_t,get_info'
    REQUEST_AUTHORIZATION_CODE = 'https://graph.qq.com/oauth2.0/authorize'
    REQUEST_ACCESS_TOKEN = 'https://graph.qq.com/oauth2.0/token'
    REQUEST_OPEN_ID = 'https://graph.qq.com/oauth2.0/me'
    SHARE_URL = 'https://graph.qq.com/share/add_share'

    def pickAccessTokenAndExpires(self, content):
        if 'access_token=' in content:
            access_token = content.partition('access_token=')[2].partition('&')[0]
            expires_in = content.partition('expires_in=')[2]
        else:
            access_token = ''
            expires_in = ''
        return access_token, expires_in

    def pickOpenId(self, content):
        return content.partition('"openid":"')[2].partition('"')[0]

    def assignUserInfo(self, data, access_token):
        new_data = site_helper.copy(data)
        model = getModel(self.MODEL_NAME)
        open_id = model.getOpenIdByAccessToken(access_token)
        if open_id is None:
            return new_data

        url = self.getUrl('https://graph.qq.com/user/get_user_info', (
            'access_token', access_token,
            'oauth_consumer_key', self.APP_ID,
            'openid', open_id,
            'format', 'json',
            ))

        response, content =  self.getHtmlContent(url)
        if response.status != 200:
            return new_data

        content = self.loadsJson(content)
        if content.ret != 0:
            return new_data

        new_data['username'] = content.nickname
        new_data['sex'] = content.gender

        image_file = self.requestImageFile(content.figureurl_2)
        if image_file is None:
            return new_data
        new_data['imagefile'] = image_file

        return new_data


    def share(self, user_id, access_token, comment, **options):

        open_id = getModel(self.MODEL_NAME).getOpenIdByAccessToken(access_token)
        url = options.get('url', None)

        comment = comment.replace('【','"').replace('】','"')

        pic = options.get('pic', None)
        if pic and not pic.startswith('http://'):
            pic = site_helper.config.HOST_NAME + pic

        if open_id:
            url = self.getUrl(self.SHARE_URL, (
                'access_token', access_token,
                'oauth_consumer_key', self.APP_ID,
                'openid', open_id,
                'title', comment,
                'url', url,
                'comment', None,
                'summary', None,
                'images', pic,
                'source', 1,
                ))
            response, content =  self.getHtmlContent(url)
            print pic

