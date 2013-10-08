#coding=utf-8
import site_helper, web, page_helper
from User import User
from controller import User as UserCtrl
from site_helper import session, getModel
import datetime

# ../page/user/Share.html

class Share(User):

    def GET(self):
        session = site_helper.session
        if session.is_login:
            user_id = int(session.user_id)
            user_model = site_helper.getModel('User')
            medal_model = site_helper.getModel('Medal')
            share_link_model = site_helper.getModel('ShareLink')
            uhm_model = site_helper.getModel('UserHasMedal')
            user = user_model.get(user_id)

            if user is not None:
                share_count = share_link_model.getCountByUserid(user.Userid)
                UserCtrl().writeBaseInfo(user)
                oauth_status = self._getOAuthStatus(user_id)
                exists_medal = uhm_model.getByUserAndName(user_id, 'share_daren')
                share_medal = medal_model.getOneByWhere('name=%s', ['share_daren'])
                if share_medal:
                    share_medal = medal_model.get(share_medal.Medalid)
                winner_settings = self._getWinnerSettings('share_link_winner')
                latest_winner_settings = self._getWinnerSettings('share_link_latest_winner')
                sub_content = site_helper.page_render_nobase.user.Share(user, share_count, oauth_status, exists_medal, winner_settings, latest_winner_settings, share_medal)
                return site_helper.page_render.user.Base3(user, sub_content)
            else:
                return page_helper.redirect404()
        else:
            page_helper.redirectToLogin()

    def _getOAuthStatus(self, user_id):
        oauth_status = site_helper.storage({})
        for site, model_name in [('qq', 'oauth.QQOAuth2'), ('sina', 'oauth.SinaOAuth2'), ('renren', 'oauth.RenRenOAuth2'),]:
            model = getModel(model_name)
            item = model.getsByUserid(user_id)
            if not item:
                oauth_status[site] = 'no binding'
            elif self._isOverdue(item[0].updated, item[0].access_expires):
                oauth_status[site] = 'expires'
            else:
                oauth_status[site] = 'enable'
        return oauth_status

    def _isOverdue(self, created, expires):
        return created + datetime.timedelta(seconds=expires-600) < datetime.datetime.today()

    def _getWinnerSettings(self, which_month):
        winner_settings = site_helper.getSiteConfig(which_month).split('\n')
        winner_settings = [(w.partition(':')[0].strip(), w.partition(':')[2].strip())
                for w in winner_settings]
        winner_settings = dict(winner_settings)
        if winner_settings.get('winner_id'):
            winner_settings['winner_user'] = getModel('User').get(winner_settings['winner_id'])
        return winner_settings

