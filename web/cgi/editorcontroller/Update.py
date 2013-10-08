#coding=utf-8
import page_helper, site_helper, web

class Update:

    def POST(self,i=None):
        if i is None: i = web.input(imagefile={})
        if i.has_key('imagefile'):
            if i.imagefile=={}:
                del i.imagefile
            else:
                i.imagefile = site_helper.storage({'filename':i.imagefile.filename, 'value':i.imagefile.value})

        assert(i.has_key('model_name'))
        assert(i.has_key('model_id'))
        model = site_helper.getModel(i.model_name)
        model.update(int(i.model_id),i)

        page_helper.refresh()
