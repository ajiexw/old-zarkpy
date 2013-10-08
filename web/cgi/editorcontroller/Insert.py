#coding=utf-8
import page_helper, site_helper, web

class Insert:

    def POST(self,i=None):
        if i is None: i = web.input(imagefile={}) #记得在form中添加 enctype="multipart/form-data" 

        if i.has_key('imagefile'):
            if (not hasattr(i.imagefile, 'filename')) or len(i.imagefile.filename)==0 or len(i.imagefile.value) < 10:
                del i.imagefile
            else:
                i.imagefile = site_helper.storage({'filename':i.imagefile.filename, 'value':i.imagefile.value})

        assert(i.has_key('model_name'))
        model = site_helper.getModel(i.model_name)

        new_id = model.insert(i)

        return page_helper.refresh()

