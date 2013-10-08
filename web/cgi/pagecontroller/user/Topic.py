#coding=utf-8
import site_helper, web, page_helper
from User import User
import datetime
from controller import User as UserCtrl

# ../page/user/Topic.html

class Topic(User):

    def GET(self, user_id):
        user_id = int(user_id)
        user_model = site_helper.getModel('User')
        topic_model = site_helper.getModel('Topic')
        userimg_model = site_helper.getModel('UserImage')
        topic_comment_model = site_helper.getModel('TopicComment')
        group_model = site_helper.getModel('Groups')
        user = user_model.get(user_id)
        if user is not None:
            env = {'pagination':'thirty items', 'where': ('Userid=%s',[user_id]), 'orderby':'Topicid desc'}
            topics = topic_model.getAll(env)
            for topic in topics:
                topic.author = user_model.get(topic.Userid)
                topic.comments_sum = topic_comment_model.getCount({'where': ('Topicid=%s',[topic.Topicid])})
                topic.group = group_model.get(topic.Groupsid)
                topic.summary = site_helper.getUnicodeSummary(topic.content, 150)
                topic.upload_images = userimg_model.gets('Topic', topic.Topicid)


            pagination_html = topic_model.getPaginationHtml(env)
            UserCtrl().writeBaseInfo(user)
            sub_content = site_helper.page_render_nobase.user.Topic(topics, pagination_html, user_id, datetime.datetime.now())
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirect404()


