#coding=utf-8
import page_helper, site_helper, web

class Insert:

    def GET(self):
        return self.POST()

    def POST(self, i=None):
        try:
            i = self.initInputs(i)
            model = site_helper.getModel(i.model_name)
            new_id = model.insert(i)
            return page_helper.refresh()
        except:
            if i.get('exception'):
                return page_helper.failed(i.get('exception'))
            else:
                raise

    def initInputs(self, i=None):
        if i is None: i = web.input(imagefile={})
        if i.has_key('imagefile'):
            if (not hasattr(i.imagefile, 'filename')) or len(i.imagefile.filename)==0 or len(i.imagefile.value) < 10:
                del i.imagefile
            else:
                i.imagefile = site_helper.storage({'filename':i.imagefile.filename, 'value':i.imagefile.value})

        assert(i.has_key('model_name'))
        session = site_helper.session
        assert(session.is_login)

        i.Userid = session.user_id
        i.ip = site_helper.ipToInt(session.ip)
        return i
