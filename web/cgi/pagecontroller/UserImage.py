#coding=utf-8
import site_helper
import web, json

class UserImage:

    def POST(self):
        i= web.input()
        assert(i.has_key('userid'))
        #assert(i.has_key('email'))
        #assert(i.has_key('md5password'))
        #user = site_helper.getModel('User').getByEmail(i.email)
        user = site_helper.getModel('User').get(i.userid)
        assert(user is not None)
        #assert(user.password == i.md5password)

        i.imagefile = site_helper.storage({'filename':i['Filename'], 'value':i['Filedata']})
        i.filetype = i['Filename'].rpartition('.')[2].lower()
        del i['Filename']
        del i['Filedata']
        i.Userid = user.Userid

        model = site_helper.getModel('UserImage')
        new_id = model.insert(i)
        uri = model.get(new_id).uri
        return 'success;%d;%s' % (new_id, uri)

