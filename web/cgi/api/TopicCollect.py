#coding=utf-8
import site_helper, web, page_helper, api_helper

class TopicCollect:

    def GET(self):
        i = web.input()
        model = site_helper.getModel('TopicCollect')
        assert( i.has_key('Topicid') )
        if site_helper.session.is_login:
            assert(i.has_key('action'))
            user_id = site_helper.session.user_id
            topic_id = int(i.Topicid)
            item = model.getTopicCollect(user_id, topic_id)
            if i.action == 'add':
                if item is None:
                    model.insert({'Userid': user_id, 'Topicid': topic_id})
                    topic_html = str(site_helper.page_render_nobase.module.MakeupWantedBought('成功收藏!'))
                    return api_helper.render({'msg':topic_html})
                else:
                    topic_html = str(site_helper.page_render_nobase.module.MakeupWantedBought('您已收藏过该话题!'))
                    return api_helper.render({'msg':topic_html})
            elif i.action == 'del':
                if item is not None:
                    model.delete(item.TopicCollectid)
                    return api_helper.render({'msg':'已成功取消收藏'})
                else:
                    return api_helper.render({'msg':'您还未收藏该话题!'})
        else:
            page_helper.redirectToLogin()
