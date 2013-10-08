#coding=utf-8
import site_helper, web, page_helper, datetime
from site_helper import config, getModel, filterNone

class User:

    def writeBaseInfo(self, user):
        if user:
            user_model = site_helper.getModel('User')


    def isExists(self, email=''):
        email = email.strip().lower()
        user = getModel('User').getOneByWhere('LOWER(email)=%s', [email])
        return user is not None

    def loginByUsername(self, username, password):
        username  = username.strip().lower()
        user = getModel('User').getOneByWhere('LOWER(username)=%s', [username])
        if user and self.validatePassword(user.password, password):
            return user
        else:
            return None

    def loginByEmail(self, email, password):
        email  = email.strip().lower()
        user = getModel('User').getOneByWhere('LOWER(email)=%s', [email])
        if user and self.validatePassword(user.password, password):
            return user
        else:
            return None

    def loginAdminByEmail(self, email, password):
        email  = email.strip().lower()
        user = getModel('AdminUser').getOneByWhere('LOWER(email)=%s', [email])
        if user and self.validatePassword(user.password, password):
            return user
        else:
            return None

    def validatePassword(self, md5_password, input_password):
        return getModel('User').getMD5Password(input_password) == md5_password


    def updateUserImages(self, item_type, item_id, image_values, del_image_values):
        userimg_model = site_helper.getModel('UserImage')
        userimg_model.deleteByIDs(filter(lambda x:len(x)>0, del_image_values.split(';')))
        image_ids = filter(lambda x:len(x)>0 and userimg_model.get(x).Userid == site_helper.session.user_id, image_values.split(';'))
        userimg_model.updateTypes(item_type, item_id, image_ids)

