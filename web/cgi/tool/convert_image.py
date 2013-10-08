#!/usr/bin/env python
#coding=utf-8
import os, copy

''' convert env help:
    crop:   widthxheight+start_x+start_y (宽x高+x坐标+y坐标)
    resize: widthxheight
    resize: widthx> (压缩width为某个值)
    profile: * (删除附加信息)

    remove help:
    append_name:    将要删除文件的resize值(比如25*25), 或者一个字符串名称(比如small)
'''

def convert(image_path, env={}, use_exists=True, async=True):
    env = _initEnv(env)
    assert( ' ' not in image_path )
    if os.path.exists(image_path):
        new_path = _newPath(image_path, env)
        if not use_exists or not os.path.exists(new_path):
            cmd = _cmd(image_path, new_path, env, async)
            os.system(cmd)
        return new_path
    else:
        return image_path

def _newPath(image_path, env):
    a,b,c = image_path.rpartition('.')
    assert('/' not in c)
    if env.has_key('appendName'):
        return a + str(env['appendName']) + '.' + c
    else:
        assert(env.has_key('resize'))
        return '%s_%s.%s' % (a, env['resize'].strip('!<>'), c)

def _cmd(image_path, new_path, env, async):
    cmd = ['convert']

    if env.get('first_image', True):
        cmd.append('"' + image_path + '[0]"')
    else:
        cmd.append('"' + image_path + '"')

    if env.has_key('format'):
        cmd.append('-format ' + env['format'])
    else:
        filetype = image_path.rpartition('.')[2]
        cmd.append('-format %s' % filetype)

    for arg in 'crop', 'resize', 'profile': # resize要在crop之后
        if env.has_key(arg):
            assert( ' ' not in env[arg] )
            if arg in ['profile',]:
                cmd.append('+' + arg)
            else:
                cmd.append('-' + arg)
            cmd.append('"' + env[arg] + '"')

    cmd.append('"' + new_path + '"')

    if async:
        cmd.append('&')
    return ' '.join(cmd)

def _initEnv(env):
    new_env = copy.copy(env)
    new_env.setdefault('profile', '*')
    return new_env

def remove(image_path, append_name, async=True):
    new_path = _newPath(image_path, {'appendName': append_name})
    if os.path.exists(new_path):
        cmd = 'rm "%s" ' % new_path
        if async:
            cmd += ' &'
        os.system(cmd)

if __name__ == '__main__':
    env = {'crop': '174x174+219+29', 'resize': '25x25', }
    convert('/home/sdjl/tmp/crop/IMG_7470.jpg', env)
