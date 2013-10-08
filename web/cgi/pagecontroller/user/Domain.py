#coding=utf-8
import site_helper, web, page_helper
from controller import User as UserCtrl
from site_helper import getModel
from pagecontroller import Friend

# htmlfile: ../../page/user/Base2.html
# htmlfile: ../../page/user/User.html
# ../Friend.py

class Domain(Friend):

    def GET(self, self_domain):
        i = web.input()
        self_domain = str(self_domain)
        user_model = getModel('User')
        review_model = getModel('Review')
        makeup_model = getModel('Makeup')
        wanted_model = getModel('Wanted')
        bought_model = getModel('Bought')
        brand_model = getModel('Brand')
        ulb_model = getModel('UserLikeBrand')
        feed_model = getModel('PullFeed')

        user = user_model.getBySelfDomain(self_domain)
        if user is not None:
            user_id = user.Userid
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

            #pull_feeds = self.getMyPullFeeds(user_id)
            #user_feeds = self.getUserFeeds(user_id)
            #self._writeFeedComments(pull_feeds, 'PullFeed')
            #self._writeFeedComments(user_feeds, 'UserFeed')
            #all_feeds = pull_feeds + user_feeds
            #all_feeds = [ (f.created, f ) for f in all_feeds ]
            #all_feeds.sort(reverse=True)
            #all_feeds = [f[1] for f in all_feeds]
            #first_page_feeds_html = site_helper.page_render_nobase.feed.MoreFeeds(all_feeds)
            
            pagination_html, feeds = self.getReviewAndTopicFeeds(user_id)
            feeds = [ (f.created, f ) for f in feeds ]
            feeds.sort(reverse=True)
            feeds = [f[1] for f in feeds]
            first_page_feeds_html = site_helper.page_render_nobase.feed.MoreFeeds(feeds)
            sub_content = site_helper.page_render_nobase.user.User(user, first_page_feeds_html, pagination_html)

            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirect404()

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
