#coding=utf-8
import site_helper, web, page_helper
from User import User
import datetime
from controller import User as UserCtrl

# ../page/user/Review.html

class Review(User):

    def GET(self, user_id):
        user_id = int(user_id)
        user_model = site_helper.getModel('User')
        user = user_model.get(user_id)
        if user is not None:
            reviews, review_pagination = self._getReviews(user_id)
            UserCtrl().writeBaseInfo(user)
            sub_content = site_helper.page_render_nobase.user.Review(reviews, review_pagination, datetime.datetime.now() )
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirect404()

    def _getReviews(self, user_id):
        review_model = site_helper.getModel('Review')
        makeup_model = site_helper.getModel('Makeup')
        user_model = site_helper.getModel('User')
        env = {'pagination':'ten items',  'where':('Userid=%s',[user_id]), 'orderby':'Reviewid desc'}
        reviews = review_model.getAll(env)
        for review in reviews:
            review.username = user_model.get(review.Userid)
            review.makeup = makeup_model.get(review.Makeupid)
            review.comment_count = review_model.getCommentCount(review.Reviewid)
            review.content_summary = site_helper.getUnicodeSummary(review.content, 100)
            review.wanted_count = review_model.getWantedCount(review.Reviewid)
            review.upload_image_count = site_helper.getModel('UserImage').getCount({'where':('itemtype=%s and itemid=%s',['Review', review.Reviewid])})

        pagination_html = review_model.getPaginationHtml(env)
        return reviews, pagination_html

