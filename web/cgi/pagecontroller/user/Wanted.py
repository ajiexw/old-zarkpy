#coding=utf-8
import site_helper, web, page_helper
from User import User
from site_helper import getModel
from controller import User as UserCtrl

# ../page/user/Wanted.html

class Wanted(User):

    def GET(self, user_id):
        user_id = int(user_id)
        user_model = site_helper.getModel('User')
        user = user_model.get(user_id)
        if user is not None:
            wanteds = self.getWanteds(user_id)
            recommends = self.getRecommendMaps()
            levels = self.getLevels(wanteds, recommends)

            UserCtrl().writeBaseInfo(user)
            sub_content = site_helper.page_render_nobase.user.Wanted(levels)
            site_helper.printDictOrList(levels)
            return site_helper.page_render.user.Base2(user, sub_content)
        else:
            page_helper.redirect404()

    def getLevels(self, wanteds, recommends):
        '''返回这种格式的数据:
        {level1:{
            level2: {'wanteds':[makeup1, makeup2], 'recommends':[makeup1, makeup2]},
            level2: {...}
            },
         level1:{...},
        }   
        '''
        '''返回这种格式的数据:
        {level1:[
            (level2: {'wanteds':[makeup1, makeup2], 'recommends':[makeup1, makeup2]}),
            (level2: {...})
            ],
         level1:[...],
        }   
        '''

        makeup_model = site_helper.getModel('Makeup')
        setting_model = site_helper.getModel('WantedSetting')
        settings = setting_model.getAll()
        catid_key_maps = dict([(setting.MakeupCategoryid, (setting.level1, setting.level2)) for setting in settings])

        dict_wanteds = {}
        for wanted in wanteds:
            cat_id = wanted.makeup.MakeupCategoryid
            if catid_key_maps.has_key(cat_id):
                key = catid_key_maps[cat_id]
                dict_wanteds.setdefault(key, [])
                dict_wanteds[key].append(wanted)
        
        levels = {}
        for setting in settings:
            level1 = setting.level1
            level2 = setting.level2
            levels.setdefault(level1, [])
            item = (level2,{'wanteds':dict_wanteds.get((level1, level2), []), 'recommends':recommends.get((level1, level2), [])})
            if item not in levels[level1]:
                levels[level1].append(item)

            #原来的代码
            #levels.setdefault(level1, {})
            #levels[level1].setdefault(level2, {'wanteds':[], 'recommends':[]})
            #levels[level1][level2]['wanteds']    = dict_wanteds.get((level1, level2), [])
            #levels[level1][level2]['recommends'] = recommends.get((level1, level2), [])
            

        return levels

    def getRecommendMaps(self):
        '''返回推荐的产品, 格式为:  {(level1, level2):[makeup1, makeup2], (level1, level2):[...] }'''
        table_model   = getModel('LevelTable')
        reco_setting  = table_model.getContentByPage('wanted-recommend')
        makeup_model  = getModel('Makeup')
        levels = table_model.getLevels(reco_setting)
        lines  = table_model.levelsToLines(levels)

        ret_recommends = {}
        for line in lines:
            if len(line)==3:
                key = (line[0], line[1])
                ret_recommends.setdefault(key, [])
                makeup = makeup_model.getWithAll(line[2])
                score = makeup_model.calcScore(makeup.Makeupid)
                if score is not None:
                    makeup.score = '%.1f' % score
                else:
                    makeup.score = '未知'

                if makeup is not None:
                    ret_recommends[key].append(makeup)

        return ret_recommends

    def getWanteds(self, user_id):
        wanted_model = site_helper.getModel('Wanted')
        makeup_model = site_helper.getModel('Makeup')
        wanteds = wanted_model.getWantedsByUserid(user_id)
        for wanted in wanteds:
            wanted.makeup = makeup_model.getWithAll(wanted.Makeupid)
            score = makeup_model.calcScore(wanted.Makeupid)
            if score is not None:
                wanted.makeup.score = '%.1f' % score
            else:
                wanted.makeup.score = '未知'

        return filter(lambda w:w.makeup is not None, wanteds)

