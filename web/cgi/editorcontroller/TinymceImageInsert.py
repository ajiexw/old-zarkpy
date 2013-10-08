#coding=utf-8
import page_helper, site_helper, web
from Insert import Insert

class TinymceImageInsert(Insert):

    def POST(self,i=None):
        if i is None: i= web.input(imagefile={})
        assert(i.has_key('imagefile'))
        if '.' in i.imagefile.filename and len(i.imagefile.value)>10:
            i.imagefile = site_helper.storage({'filename':i.imagefile.filename, 'value':i.imagefile.value})
            upload_filetype = i.imagefile.filename.rpartition('.')[2]
            assert(upload_filetype.lower() in ['jpg','png','gif','jpeg'])
            new_id = site_helper.getModel('Image').insert(i)

            return site_helper.editor_render_nobase.tinymce.imagemanager_insertcallback('<img src="%s%d.%s" />' % (site_helper.config.UPLOAD_IMAGE_URL, new_id, upload_filetype))
        else:
            return page_helper.close()
