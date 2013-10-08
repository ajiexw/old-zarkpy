#coding=utf-8
import page_helper, site_helper, web
import socket, struct
from Insert import Insert

class RegisterAdmin(Insert):
    def GET(self):
        return site_helper.editor_render.adminuser.Register()

    def POST(self,i=None):
        if i is None: i = web.input()
        assert(len(i.get('username','')) > 0)
        assert(len(i.get('email','')) > 0)
        assert(len(i.get('password','')) > 0)
        i.register_ip = i.login_ip = self._ipToInt(site_helper.session.ip)
        new_id = site_helper.getModel('AdminUser').insert(i)
        user = site_helper.getModel('AdminUser').get(new_id)
        assert(user is not None)
        site_helper.loginAdmin(user)
        return page_helper.refreshParent()

    def _ipToInt(self,ipstring):
        return struct.unpack('=L',socket.inet_aton(ipstring))[0]

