#coding=utf-8
import site_helper, web, page_helper
from controller import User as UserCtrl
from site_helper import getModel
from pagecontroller import Friend

# htmlfile: ../../page/user/Base2.html
# htmlfile: ../../page/user/User.html
# ../Friend.py

class User(Friend):

    def GET(self, user_id):
        inp = web.input()
        user_id = int(user_id)
        user_model = getModel('User')
        review_model = getModel('Review')
        makeup_model = getModel('Makeup')
        wanted_model = getModel('Wanted')
        bought_model = getModel('Bought')
        brand_model = getModel('Brand')
        ulb_model = getModel('UserLikeBrand')
        feed_model = getModel('PullFeed')

        user = user_model.get(user_id)
        if user is not None:
            if user.self_domain:
                web.seeother(site_helper.config.HOST_NAME+'/u/'+user.self_domain)
            else:
                wanteds = wanted_model.getAll({'where':('Userid=%s', [user_id]), 'orderby':'Wantedid desc', 'limit':(0, 9)})
                boughts = bought_model.getAll({'where':('Userid=%s', [user_id]), 'orderby':'Boughtid desc', 'limit':(0, 9)})
                brands = ulb_model.getAll({'where':('Userid=%s', [user_id]), 'orderby':'UserLikeBrandid desc'})

                user.latest_wanteds = site_helper.filterNone(map(makeup_model.get, [i.Makeupid for i in wanteds]))
                user.latest_boughts = site_helper.filterNone(map(makeup_model.get, [i.Makeupid for i in boughts]))
                user.latest_reviews = review_model.getAll({'where':('Userid=%s', [user_id]), 'orderby':'Reviewid desc', 'limit':(0, 9)})

                for review in user.latest_reviews:
                    review.makeup = makeup_model.get(review.Makeupid)
                user.liked_brands = map(brand_model.get, [i.Brandid for i in brands])
                UserCtrl().writeBaseInfo(user)

                pagination_html, feeds = self.getReviewAndTopicFeeds(user_id)
                feeds = [ (f.created, f ) for f in feeds ]
                feeds.sort(reverse=True)
                feeds = [f[1] for f in feeds]
                first_page_feeds_html = site_helper.page_render_nobase.feed.MoreFeeds(feeds)
                sub_content = site_helper.page_render_nobase.user.User(user, first_page_feeds_html, pagination_html)

                return site_helper.page_render.user.Base2(user, sub_content)
        else:
            return page_helper.redirect404()

    def _getReviews(self, user_id, inp):
        reviews, review_pagination = self._getReviews(user_id, inp)
        wanteds, wanted_pagination = self._getWanteds(user_id, inp)
        review_model = getModel('Review')
        makeup_model = getModel('Makeup')
        page_num = int(web.input().get('rpn',1)) # rpn is review page number
        env = {'pagination':'ten items', 'page_num':page_num, 'where':('Userid=%s',[user_id]), 'orderby':'Reviewid desc'}
        reviews = review_model.getAll(env)
        for review in reviews:
            review.makeup = makeup_model.get(review.Makeupid)
        pagination_html = review_model.getPaginationHtml(env, {'para_name':'rpn'})
        return reviews, pagination_html

