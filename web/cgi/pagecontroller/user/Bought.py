#coding=utf-8
import site_helper, web, page_helper
from User import User
from controller import User as UserCtrl

# ../page/user/Bought.html

class Bought(User):

    def GET(self, user_id):
        user_id = int(user_id)
        user_model = site_helper.getModel('User')
        user = user_model.get(user_id)
        if user is not None:
            boughts, bought_pagination = self._getBoughts(user_id)
            UserCtrl().writeBaseInfo(user)
            sub_content = site_helper.page_render_nobase.user.Bought(boughts, bought_pagination)
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirect404()

    def _getBoughts(self, user_id):
        bought_model = site_helper.getModel('Bought')
        makeup_model = site_helper.getModel('Makeup')
        env = {'pagination':'fifty items', 'where':('Userid=%s',[user_id]), 'orderby':'Boughtid desc'}
        boughts = map(makeup_model.get, [i.Makeupid for i in bought_model.getAll(env)])
        for makeup in boughts:
            makeup.bought = bought_model.getBought(user_id,makeup.Makeupid)
        pagination_html = bought_model.getPaginationHtml(env)
        return boughts, pagination_html

