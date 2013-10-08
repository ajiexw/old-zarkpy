#coding=utf-8
from Model import Model
import site_helper
from site_helper import config
import datetime

class Comment(Model):
    table_name = 'Comment'
    column_names = ['Reviewid','Userid','content','sinsitive_mark','status', 'toReplyUserids', 'hide_name']
    decorator = [
        ('Pagination',{}),
        ('UserGoal',{'insert_inc_tasks':'post_comment,be_commented', 'delete_dec_tasks':'post_comment,be_commented', }),
        ('PullFeed', {'insert':[('User', 'fromCommentGetUserids'), ],
                      'delete':['Comment', ],
        }),
        ('Notice', {'insert':[('User', 'fromCommentGetUserids'), ],
                      'delete':['Comment', ],
        }),

        ('Search',{'index':'comment', 'display_page':10, 'max': 1000, 'page_count': 30, 'firsttext':'第一页', 'lasttext':'末页'}),
    ]

    def setToPass(self, comment_id):
        self.update(comment_id, {'status':'judged'})

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Reviewid    int unsigned not null,
            Userid      int unsigned not null,
            content     varchar(4000) charset utf8 not null default '',
            sinsitive_mark  tinyint unsigned not null default 0,
            status      enum('unjudged','judged','sensitive','deleted') not null default 'unjudged',
            created     timestamp not null default current_timestamp,
            toReplyUserids  varchar(100) charset utf8 not null default '',
            hide_name       boolean not null default 0,
            primary key ({$table_name}id),
            key (Reviewid, Userid)
        )ENGINE=InnoDB;
        '''
