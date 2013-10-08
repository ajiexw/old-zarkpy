#coding=utf-8
from tool import convert_image
from site_helper import config

class ImageConvert:

    def getSmallPortrait(self, cover_url, small_portrait, size):
        crops = small_portrait.split()
        assert(len(crops) == 4)
        crops = crops[2:] + crops[:2]
        env = {'resize':'%sx%s' % (size, size), 'crop':'%sx%s+%s+%s' % tuple(crops), 'format':'jpg'}
        path = config['APP_ROOT_PATH'] + 'web' + cover_url
        new_path = convert_image.convert(path, env)
        return new_path.partition(config['APP_ROOT_PATH'] + 'web')[2]

    def getBigPortrait(self, cover_url, big_portrait, width, height):
        crops = big_portrait.split()
        assert(len(crops) == 4)
        crops = crops[2:] + crops[:2]
        env = {'resize':'%sx%s' % (width, height), 'crop':'%sx%s+%s+%s' % tuple(crops), 'format':'jpg'}
        path = config['APP_ROOT_PATH'] + 'web' + cover_url
        new_path = convert_image.convert(path, env)
        return new_path.partition(config['APP_ROOT_PATH'] + 'web')[2]

    def getFindReviewUrl(self, cover_url):
        env = {'resize':'206x>', 'format':'jpg'}
        path = config['APP_ROOT_PATH'] + 'web' + cover_url
        new_path = convert_image.convert(path, env)
        return new_path.partition(config['APP_ROOT_PATH'] + 'web')[2]

    def getFindMakeupUrl(self, cover_url):
        env = {'resize':'32x32>', 'format':'jpg'}
        path = config['APP_ROOT_PATH'] + 'web' + cover_url
        new_path = convert_image.convert(path, env)
        return new_path.partition(config['APP_ROOT_PATH'] + 'web')[2]

    def resize(self, cover_url, resize):
        env = {'resize':resize, 'format':'jpg'}
        path = config['APP_ROOT_PATH'] + 'web' + cover_url
        new_path = convert_image.convert(path, env)
        return new_path.partition(config['APP_ROOT_PATH'] + 'web')[2]
        
