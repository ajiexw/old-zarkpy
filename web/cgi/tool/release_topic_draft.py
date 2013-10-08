#!/usr/bin/env python
#coding=utf-8
import sys, os
filePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(filePath+'/..')

import site_helper
from site_helper import getModel

if __name__=='__main__':

    topic_model = getModel('Topic')
    topic_draft_model = getModel('TopicDraft')
    userimg_model = getModel('UserImage')

    drafts = topic_draft_model.getTopicDraftOfCurdate()
    if drafts:
        for draft in drafts:
            new_id = topic_model.insert(draft)
            userimg_model.updateTopicDraftType('Topic', new_id, draft.TopicDraftid) 
            topic_draft_model.delete(draft.TopicDraftid)


