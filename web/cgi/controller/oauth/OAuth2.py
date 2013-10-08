#coding=utf-8
import site_helper, json, hashlib
from site_helper import getModel
import httplib2, httplib, mimetypes

class OAuth2:
    SITE_NAME = ''
    MODEL_NAME = ''
    CN_SITE_NAME = ''
    APP_ID = ''
    SECRET_KEY = ''
    MAX_BINDING = 1
    REDIRECT_AUTHORIZATION_CODE = site_helper.config.HOST_NAME + '/oauth/authorize'
    ACCESS_TOKEN_METHOD = 'GET'

    def getUrl(self, request_uri, querys):
        query = '&'.join(['%s=%s' % ( str(querys[i*2]), site_helper.quote(str(querys[i*2+1])) ) for i in range(len(querys) / 2) if querys[i*2+1]])
        return request_uri + '?' + query

    def getState(self):
        return self.SITE_NAME

    def pickAccessTokenAndExpires(self, content):
        content = self.loadsJson(content)
        return content.access_token, content.expires_in

    def assignUserInfo(self, data):
        return data

    def requestImageFile(self, url):
        response, content =  self.getHtmlContent(url)
        if response.status == 200:
            ret_image_file = site_helper.storage()
            ret_image_file.filename = url + '.jpeg'
            ret_image_file.value = content
            return ret_image_file
        else:
            return None

    def getLoginUrl(self, state=None):
        if state is None:
            state = self.getState()

        return self.getUrl(self.REQUEST_AUTHORIZATION_CODE, (
            'response_type', 'code',
            'client_id', self.APP_ID,
            'redirect_uri', self.REDIRECT_AUTHORIZATION_CODE,
            'scope', self.SCOPE,
            'state', state,
            ))

    def getAccessTokenUrl(self, authorization_code, state):
        return self.getUrl(self.REQUEST_ACCESS_TOKEN, (
            'grant_type', 'authorization_code',
            'client_id', self.APP_ID,
            'client_secret', self.SECRET_KEY,
            'code', authorization_code,
            'state', state,
            'redirect_uri', self.REDIRECT_AUTHORIZATION_CODE,
            ))

    def getOpenIdUrl(self, access_token):
        return self.getUrl(self.REQUEST_OPEN_ID, (
            'access_token', access_token,
            ))

    def getOpenId(self, access_token):
        open_id_url = self.getOpenIdUrl(access_token)
        response, content =  self.getHtmlContent(open_id_url)
        return self.pickOpenId(content)

    def bindUserid(self, access_token, user_id):
        model = getModel(self.MODEL_NAME)
        exists_count = len(model.getsByUserid(user_id))
        if exists_count < self.MAX_BINDING:
            model.bindUserid(access_token, user_id)
            return ''
        else:
            return '您的邮箱已绑定了%d个%s帐号,请重新输入' % (exists_count, self.CN_SITE_NAME)


    def share(self, user_id, access_token, comment, **options):
        pass

    def shareAll(self, user_id, comment, **options):
        user = getModel('User').get(user_id)
        if user:
            model = getModel(self.MODEL_NAME)
            for o in model.getsByUserid(user_id):
                if o.get('share','') == 'on':
                    self.share(user_id, o.access_token, comment, **options)

    def loadsJson(self, content):
        return site_helper.storage(json.loads(content))

    def sign(self, data, secret_key):
        l = ['%s=%s' % (k,v) for k,v in data.items()]
        l = [i if type(i) is str else i.encode('utf-8','ignore') for i in l]
        l.sort()
        l.append(secret_key)
        md5 = hashlib.md5()
        md5.update(''.join(l))
        return md5.hexdigest()

    def getHtmlContent(self, url, method='GET'):
        h = httplib2.Http()
        h.timeout = 5
        response, content = h.request(url, method=method)
        return response, content

    def post_multipart(self, host, url, fields, files):
        content_type, body = self.encode_multipart_formdata(fields, files)
        h = httplib.HTTPSConnection(host)
        h.putrequest('POST', url)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        return h.getresponse().read()

    def encode_multipart_formdata(self, fields, files):
        BOUNDARY = '----------lImIt_of_THE_fIle_eW_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            if type(value) is unicode:
                value = value.encode('utf-8', 'ignore')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            if type(value) is unicode:
                value = value.encode('utf-8', 'ignore')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
