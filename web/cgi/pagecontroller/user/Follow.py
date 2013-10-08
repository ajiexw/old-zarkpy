#coding=utf-8
import site_helper, web, page_helper
from User import User
from controller import User as UserCtrl

# ../page/user/Follow.html

class Follow(User):

    def GET(self, user_id):
        user_id = int(user_id)
        user_model = site_helper.getModel('User')
        user = user_model.get(user_id)

        if user is not None:
            my_follows = user_model.getMyFollows(user.Userid)
            follows_me = user_model.getFollowsMe(user.Userid)
            my_shares  = user_model.getMyShares(user.Userid)

            UserCtrl().writeBaseInfo(user)
            sub_content = site_helper.page_render_nobase.user.Follow(user, my_follows, follows_me, my_shares)
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            return page_helper.redirect404()
