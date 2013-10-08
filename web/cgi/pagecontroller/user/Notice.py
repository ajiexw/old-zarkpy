#coding=utf-8
import site_helper, web, page_helper, math
from .. import Update
from controller import User as UserCtrl
from site_helper import getModel, filterNone

ITEM_COUNT_PER_PAGE = 20
# ../page/user/Notice.html

class Notice(Update):

    def GET(self):
        i = web.input()
        model = site_helper.getModel('User')
        session = site_helper.session
        page_num = int(i.get('page_num',1))
        if session.is_login:
            user = model.get(session.user_id)
            UserCtrl().writeBaseInfo(user)
            notices = self.getAllNotices(user.Userid)
            notices = [ (n.created, n ) for n in notices ]
            notices.sort(reverse=True)
            notices = [f[1] for f in notices]

            pagination_html = self.getNoticePaginationHtml(len(notices),ITEM_COUNT_PER_PAGE)
            notices = notices[ITEM_COUNT_PER_PAGE * (page_num-1): (ITEM_COUNT_PER_PAGE * page_num)]

            sub_content = site_helper.page_render_nobase.user.Notice(notices, pagination_html)
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirectToLogin()

    def getAllNotices(self,user_id):
        '''获得所有notice，去除重复'''
        pullfeed_notices = self.getReplyNotices(user_id)
        comment_notices = self.getReviewCommentNotices(user_id, pullfeed_notices) + self.getTopicCommentNotices(user_id, pullfeed_notices) # 回复你的心得及话题的提示feed
        follow_notices = self.getFollowsNotices(user_id) # 有了新的粉丝
        return  pullfeed_notices + comment_notices + follow_notices

    def getAnyNotices(self,user_id):
        '''获得所有notice，包含重复的'''
        pullfeed_notices = self.getReplyNotices(user_id)
        comment_notices = self.getReviewCommentNotices(user_id) + self.getTopicCommentNotices(user_id)
        follow_notices = self.getFollowsNotices(user_id) 
        return  pullfeed_notices + comment_notices + follow_notices

    def getUnReadNotices(self,user_id):
        unread_notices = []
        notices = self.getAllNotices(user_id)
        for notice in notices:
            if notice.is_read == 0:
                unread_notices.append(notice)
        return unread_notices

    def getUnReadNoticeSum(self,user_id):
        unread_notices = self.getUnReadNotices(user_id)
        return len(unread_notices)

    def setNoticeIsRead(self,user_id):
        unread_notices = self.getUnReadNotices(user_id)
        notice_model = getModel('Notice')
        for notice in unread_notices:
             notice_model.setToRead(notice.Noticeid)

    def delAllNotices(self,user_id):
        notices = self.getAnyNotices(user_id)
        notice_model = getModel('Notice')
        for notice in notices:
            notice_model.delete(notice.Noticeid)

    def getReplyNotices(self,user_id):
        reply_to_me_notices = self._getReplyToMeNotices(user_id)
        set_to_best_notices = self._getSetToBestNotices(user_id)  #我的心得被推送至逛街或话题被设为精华
        group_create_notices = self._getGroupsCreateNotices(user_id)
        set_group_manager_notices = self._getSetGroupsManagerNotices(user_id)
        return self.__setHtmlForNotice(reply_to_me_notices + set_to_best_notices + group_create_notices + set_group_manager_notices)

    def getReviewCommentNotices(self, user_id, filter_notices=None):
        '''获得你发布的心得的回复, filter_notices主要用于避免重复notice'''
        notice_model = getModel('Notice')
        env = {'orderby':'Noticeid desc'}
        env['select'] = 'distinct n.*'
        env['from'] = 'Notice n join Comment c on n.item_id=c.Commentid join Review r on c.Reviewid=r.Reviewid join User u on r.Userid=%s' % user_id
        env['where'] = ('n.item_type=%s and n.source=%s and r.Userid <> c.Userid', ['Comment', 'User'])
        comment_notices = notice_model.getAll(env)
        if filter_notices:
            filter_notice_ids = [n.item_id for n in filter_notices if n.has_key('item_id') and n.source=='Reply' and n.item_type=='Comment']
            comment_notices = [n for n in comment_notices if n.item_id not in filter_notice_ids]

        return self.__setHtmlForReviewCommentNotice(comment_notices)

    def getTopicCommentNotices(self, user_id, filter_notices=None):
        '''获得你发布的话题的回复, filter_notices主要用于避免重复notice'''
        notice_model = getModel('Notice')
        env = {'orderby':'Noticeid desc'}
        env['select'] = 'distinct n.*'
        env['from'] = 'Notice n join TopicComment c on n.item_id=c.TopicCommentid join Topic t on c.Topicid=t.Topicid join User u on t.Userid=%s' % user_id
        env['where'] = ('n.item_type=%s and n.source=%s and t.Userid <> c.Userid', ['TopicComment', 'User'])
        comment_notices = notice_model.getAll(env)
        if filter_notices:
            filter_notice_ids = [n.item_id for n in filter_notices if n.has_key('item_id') and n.source=='Reply' and n.item_type=='TopicComment']
            comment_notices = [n for n in comment_notices if n.item_id not in filter_notice_ids]

        return self.__setHtmlForTopicCommentNotice(comment_notices)


    def getFollowsNotices(self, user_id):
        '''有了新的粉丝'''
        user_model = getModel('User')
        user = user_model.get(user_id)
        notice_model = getModel('Notice')
        env = {'orderby':'Noticeid desc'}
        env['select'] = 'distinct f.*'
        env['from'] = 'Notice f join Follow fo on f.item_id=fo.Followid'
        env['where'] = ('f.item_type=%s and fo.followed_id=%s', ['Follow', user_id])
        follow_notices = notice_model.getAll(env)

        return self.__setHtmlForFollowNotice(user,follow_notices)

    def _getReplyToMeNotices(self, user_id):
        '''获得回复我的Notice, 它是getNoticeNotices的一部分.'''
        notice_model = getModel('Notice')
        env = {'where':('source=%s and source_id =%s',['Reply', user_id]), 'orderby':'Noticeid desc'}
        reply_notices = notice_model.getAll(env)
        return reply_notices


    def _getSetToBestNotices(self, user_id):
        '''获得被推送至逛街的心得或设为精华的话题的相关Notice, 它是getNotices的一部分.'''
        notice_model = getModel('Notice')
        env = {'where':('source=%s and source_id =%s',['FindOrBest', user_id]), 'orderby':'Noticeid desc'}
        return notice_model.getAll(env)

    def _getGroupsCreateNotices(self, user_id):
        '''获得创建小组后收到的管理员审核Notice, 它是getNotices的一部分.'''
        notice_model = getModel('Notice')
        env = {'where':('source=%s and source_id =%s',['GroupsCreate', user_id]), 'orderby':'Noticeid desc'}
        return notice_model.getAll(env)

    def _getSetGroupsManagerNotices(self, user_id):
        '''设置用户为小组管理员的Notice, 它是getNotices的一部分.'''
        notice_model = getModel('Notice')
        env = {'where':('source=%s and source_id =%s',['SetGroupsManager', user_id]), 'orderby':'Noticeid desc'}
        return notice_model.getAll(env)


    def __setHtmlForNotice(self, notices):
        ''' 求notice.html'''
        ret_notices = {}
        for notice in notices:
            key = (notice.item_type, notice.item_id)
            if not ret_notices.has_key(key):
                item = getModel(notice.item_type).get(notice.item_id)
                notice.html = getattr(self,'getNoticeHtml_%s_%s' % (notice.source, notice.item_type))(notice, item) if item else None
                ret_notices[key] = notice
        ret_notices = self.filterNotices(ret_notices.values())
        # 对ret_notices按照时间排序
        ret_notices = [(notice.created, notice) for notice in ret_notices]
        ret_notices.sort(reverse=True)
        ret_notices = [f[1] for f in ret_notices]
        return ret_notices

    def __setHtmlForReviewCommentNotice(self, comment_notices):
        user_model = site_helper.getModel('User')
        comment_model = site_helper.getModel('Comment')
        review_model = site_helper.getModel('Review')
        for notice in comment_notices:
            author = user_model.get(notice.source_id)
            comment = comment_model.get(notice.item_id)
            review = review_model.get(comment.Reviewid)
            notice.html = site_helper.page_render_nobase.user.notices.ReviewCommentNotice(author, comment, review, notice)
        return comment_notices

    def __setHtmlForTopicCommentNotice(self, comment_notices):
        user_model = site_helper.getModel('User')
        comment_model = site_helper.getModel('TopicComment')
        topic_model = site_helper.getModel('Topic')
        for notice in comment_notices:
            author = user_model.get(notice.source_id)
            comment = comment_model.get(notice.item_id)
            topic = topic_model.get(comment.Topicid)
            notice.html = site_helper.page_render_nobase.user.notices.TopicCommentNotice(author, comment, topic, notice)
        return comment_notices

    def __setHtmlForFollowNotice(self,user,follow_notices):
        user_model = site_helper.getModel('User')
        for notice in follow_notices:
            follow_you_user = user_model.get(notice.source_id)
            notice.html = site_helper.page_render_nobase.user.notices.FollowNotice(user,follow_you_user, notice)
        return follow_notices

    def getNoticeHtml_Reply_TopicComment(self, notice, topic_comment):
        ''' ../page/user/notices/ReplyTopicComment.html '''
        check = self.writeTopicCommentInfos(notice, topic_comment)
        return site_helper.page_render_nobase.user.notices.ReplyTopicComment(notice, topic_comment) if check else None

    def getNoticeHtml_Reply_Comment(self, notice, comment):
        ''' ../page/user/notices/ReplyComment.html '''
        check = self.writeCommentInfos(notice, comment)
        return site_helper.page_render_nobase.user.notices.ReplyComment(notice, comment) if check else None

    def getNoticeHtml_Reply_NewsComment(self, notice, news_comment):
        ''' ../page/user/notices/ReplyNewsComment.html '''
        check = self.writeNewsCommentInfos(notice, news_comment)
        return site_helper.page_render_nobase.user.notices.ReplyNewsComment(notice, news_comment) if check else None

    def getNoticeHtml_Reply_PkComment(self, notice, pk_comment):
        ''' ../page/user/notices/ReplyPkComment.html '''
        check = self.writePkCommentInfos(notice, pk_comment)
        return site_helper.page_render_nobase.user.notices.ReplyPkComment(notice, pk_comment) if check else None


    def getOfficialNoticeHtml_Event(self, notice):
        ''' ../page/user/notices/OfficialEvent.html'''
        event = getModel('Event').get(notice.item_id)
        if event:
            notice.source = 'Official'
        return site_helper.page_render_nobase.user.notices.OfficialEvent(notice, event) if notice else None

    def getOfficialNoticeHtml_News(self, notice):
        ''' ../page/user/notices/OfficialNews.html'''
        news = getModel('News').get(notice.item_id)
        if news:
            notice.source = 'Official'
        return site_helper.page_render_nobase.user.notices.OfficialNews(notice, news) if notice else None

    def getOfficialNoticeHtml_Review(self, notice):
        ''' ../page/user/notices/OfficialReview.html'''
        review = getModel('Review').get(notice.item_id)
        if review:
            notice.source = 'Official'
            review.summary = site_helper.getUnicodeSummary(review.content, 100)
        return site_helper.page_render_nobase.user.notices.OfficialReview(notice, review) if notice else None

    def getOfficialNoticeHtml_Topic(self, notice):
        ''' ../page/user/notices/OfficialTopic.html'''
        topic = getModel('Topic').get(notice.item_id)
        if topic:
            notice.source = 'Official'
            topic.summary = site_helper.getUnicodeSummary(topic.content, 100)
        return site_helper.page_render_nobase.user.notices.OfficialTopic(notice, topic) if notice else None

    def getNoticeHtml_FindOrBest_Topic(self, notice, topic):
        ''' ../page/user/notices/BestTopic.html '''
        check = self.writeTopicInfos(notice, topic)
        return site_helper.page_render_nobase.user.notices.BestTopic(notice, topic) if check else None

    def getNoticeHtml_GroupsCreate_Groups(self, notice, group):
        ''' ../page/user/notices/GroupsCreate.html '''
        check = self.writeGroupsInfos(notice, group)
        return site_helper.page_render_nobase.user.notices.GroupsCreate(notice, group) if check else None

    def getNoticeHtml_SetGroupsManager_Groups(self, notice, group):
        ''' ../page/user/notices/SetGroupsManager.html '''
        check = self.writeGroupsInfos(notice, group)
        return site_helper.page_render_nobase.user.notices.SetGroupsManager(notice, group) if check else None

    def getNoticeHtml_FindOrBest_Review(self, notice, review):
        ''' ../page/user/notices/FindReview.html '''
        check = self.writeReviewInfos(notice, review)
        return site_helper.page_render_nobase.user.notices.FindReview(notice, review) if check else None

    def writeTopicInfos(self, notice, topic):
        user_model = getModel('User')
        author = user_model.get(topic.Userid)
        if author:
            topic.author = author
        else:
            return False
        
        return True

    def writeTopicCommentInfos(self, notice, topic_comment):
        user_model = getModel('User')
        author = user_model.get(topic_comment.Userid)
        if author:
            topic_comment.author = author
        else:
            return False

        topic_model = getModel('Topic')
        topic = topic_model.get(topic_comment.Topicid)
        if topic:
            topic.user = user_model.get(topic.Userid)
            topic.summary = site_helper.getUnicodeSummary(topic.content, 100)
            topic_comment.topic = topic
        else:
            return False

        topic_comment.summary = site_helper.getUnicodeSummary(topic_comment.content, 100)

        return True

    def writeCommentInfos(self, notice, comment):
        user_model = getModel('User')
        author = user_model.get(comment.Userid)
        if author:
            comment.author = author
        else:
            return False

        review_model = getModel('Review')
        review = review_model.get(comment.Reviewid)
        review.user = user_model.get(review.Userid)
        review.summary = site_helper.getUnicodeSummary(review.content, 100)
        if review:
            comment.review = review
        else:
            return False

        comment.summary = site_helper.getUnicodeSummary(comment.content, 100)

        return True
    
    def writeNewsCommentInfos(self, notice, news_comment):
        user_model = getModel('User')
        author = user_model.get(news_comment.Userid)
        if author:
            news_comment.author = author
        else:
            return False

        news_model = getModel('News')
        news = news_model.get(news_comment.Newsid)
        if news:
            news_comment.news = news
        else:
            return False

        news_comment.summary = site_helper.getUnicodeSummary(news_comment.content, 100)

        return True

    def writePkCommentInfos(self, notice, pk_comment):
        user_model = getModel('User')
        author = user_model.get(pk_comment.Userid)
        if author:
            pk_comment.author = author
        else:
            return False

        pk_model = getModel('Pk')
        pk = pk_model.get(pk_comment.Pkid)
        if pk:
            pk_comment.pk = pk
        else:
            return False

        pk_comment.summary = site_helper.getUnicodeSummary(pk_comment.content, 100)

        return True

    
    def writeReviewInfos(self, notice, review):
        user_model = getModel('User')
        author = user_model.get(review.Userid)
        if author:
            review.author = author
        else:
            return False
        
        makeup_model = getModel('Makeup')
        makeup = makeup_model.get(review.Makeupid)
        if  makeup:
            review.makeup = makeup
            brand_model = getModel('Brand')
            brand = brand_model.get(makeup.Brandid)
            if brand:
                makeup.brand = brand
        else:
            return False

        return True

    def writeTopicInfos(self, notice, topic):
        user_model = getModel('User')
        author = user_model.get(topic.Userid)
        if author:
            topic.author = author
        else:
            return False
        
        return True

    def writeGroupsInfos(self, notice, group):
        user_model = getModel('User')
        author = user_model.get(group.Userid)
        if author:
            group.author = author
        else:
            return False
        
        return True

    def filterNotices(self, notices):
        # 过滤掉相关数据已被删除的notice
        return [notice for notice in notices if notice.get('html', None)]

    def getNoticePaginationHtml(self, total, item_count):
        page_max = max(1, math.ceil(total * 1.0 / item_count))
        return '''<div fx="pagination[max=%d;displaycount=10;firsttext=第一页;lasttext=末页;]"></div>''' % (page_max)



