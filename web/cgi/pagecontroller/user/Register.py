#coding=utf-8
import site_helper, web, page_helper
from site_helper import session, getModel
from controller import User as UserCtrl, DoTask
from .. import Insert
import time

# ../../page/user/Register.html

class Register(Insert):

    def GET(self):
        return site_helper.page_render.user.Register()

    def POST(self, i=None):
        #if i is None: i = web.input(imagefile={})
        i = web.input()
        has_portrait = False
        i.login_ip = i.register_ip = site_helper.session.ip

        assert(i.has_key('email') and len(i.email.strip()) < 100 )
        assert(i.has_key('username') and 2 <= len(i.username.strip()) <= 24 )
        assert(i.has_key('password') and len(i.password)<60 )
        i.email = i.email.strip()
        i.username = i.username.strip()
        user_model = getModel('User')

        if UserCtrl().isExists(i.email):
            return page_helper.failed('注册失败, 邮箱已被占用 :(')

        # 管理员注册不需要验证
        if site_helper.session.is_admin:
            i.activated = 'on'

        new_id = user_model.insert(i)
        user = user_model.get(new_id)
        site_helper.login(user)
        
        self.processShareLink(user)

        acode_model = site_helper.getModel('ACode')
        acode = acode_model.getACode(user.Userid)
        acode_model.updateACode(user.Userid, acode)
        acode_model.sendACode(user, acode)
        
        if has_portrait:
            #return site_helper.page_render.user.ModifyPortrait(user)
            raise web.seeother('/accounts/portrait?hideupload=true')
        else:
            # 根据当前url中的referer跳转
            params = site_helper.getUrlParams()
            if params.get('referer', False):
                return site_helper.page_render.Success('注册成功! 请打开您的Email进行验证, 只有验证后才能发表心得哦!', params['referer'])


            # 根据上一个页面地址中的referer跳转
            params = site_helper.getUrlParams(site_helper.getEnv('HTTP_REFERER'))
            if params.get('referer', False):
                return site_helper.page_render.Success('注册成功! 请打开您的Email进行验证, 只有验证后才能发表心得哦!', params['referer'])


            return site_helper.page_render.Success('注册成功! 请打开您的Email进行验证, 只有验证后才能发表心得哦!', '/')

    def processShareLink(self, user):
        session = site_helper.session
        if session.has_key('share_user_id'):
            share_link_model = getModel('ShareLink')
            ip = site_helper.ipToInt(site_helper.session.ip)
            share_limit = site_helper.getSiteConfig('share_link_ip_limit')
            ip_count = share_link_model.getTodayCountByIP(ip)

            if share_limit.isdigit() and ip_count < int(share_limit):
                source = ''
                if session.has_key('share_referer'):
                    for key in ['qq.com', 'weibo.com', 'renren.com']:
                        if key in session.share_referer:
                            source = key

                share_link_model.insert({'Userid': session.share_user_id, 'register_user_id': user.Userid, 'ip':ip, 'source': source, 'referer': session.get('share_referer', '') })

                follow_model = getModel('Follow')
                follow_model.replaceInsert({'Userid':session.share_user_id, 'followed_id':user.Userid})
                follow_model.replaceInsert({'Userid':user.Userid, 'followed_id':session.share_user_id})

            if DoTask().doTask(session.share_user_id, 'share_link'):
                append_score = getModel('GoalTask').getGoalByName('share_link')
                user_model = getModel('User')
                user_model.addShareScore(session.share_user_id, append_score)
                share_count = user_model.addShareCount(session.share_user_id)
                requirement = site_helper.getSiteConfig('share_link_medal_requirement')
                if requirement.isdigit() and share_count >= int(requirement):
                    medal = getModel('Medal').getOneByWhere('name=%s', ['share_daren'])
                    if medal:
                        getModel('UserHasMedal').insert({'Userid':session.share_user_id, 'Medalid':medal.Medalid, })

            if session.has_key('share_user_id'):
                del session.share_user_id
            if session.has_key('share_referer'):
                del session.share_referer


    def calcAge(self, birthday):
        age = time.localtime().tm_year - time.strptime(birthday,'%Y-%m-%d').tm_year
        if age <= 20:
            return '20岁以下'
        elif age <= 25:
            return '21-25'
        elif age <= 30:
            return '26-30'
        elif age <= 35:
            return '31-35'
        else:
            return '36以上'
