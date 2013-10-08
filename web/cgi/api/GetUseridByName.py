#coding=utf-8
import site_helper, web, page_helper, api_helper

class GetUseridByName:

    def GET(self):
        i = web.input()
        user_model = site_helper.getModel('User')
        assert( i.has_key('user_name') )
        user_name = i.user_name.encode('utf-8', 'ignore')
        user = user_model.getByUsername(user_name)

        if user is not None:
            return api_helper.render({'userid':user.Userid})
        else:
            return api_helper.render({'userid':None})



