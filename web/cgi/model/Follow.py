#coding=utf-8
from Model import Model

class Follow(Model):
    table_name = 'Follow'
    column_names = ['Userid',      # 关注者id
                    'followed_id', # 被关注者id
                    'created']
    decorator = [
        ('PullFeed', {'insert':[('User', 'fromFollowGetUserids'), ],
                      'delete':['Follow', ],
        }),
        
        ('Notice', {'insert':[('User', 'fromFollowGetUserids'), ],
                      'delete':['Follow', ],
        }),


    ]

    def insert(self, data):
        # 不能自己follow自己
        if data.has_key('Userid') and data.has_key('followed_id'):
            assert(str(data['Userid']) != str(data['followed_id']))
        return Model.insert(self, data)

    def getBy(self, user_id, followed_id):
        return self.getOneByWhere('Userid=%s and followed_id=%s', (user_id, followed_id))

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid          int unsigned not null,
            followed_id     int unsigned not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (Userid, followed_id),
            key (followed_id)
        )ENGINE=InnoDB;
        '''
