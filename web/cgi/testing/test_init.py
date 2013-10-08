import site_helper, os

# set config for test
site_helper.config.IS_TEST = True
for url in ['UPLOAD_IMAGE_PATH', 'UPLOAD_IMAGE_URL', 'MAKEUP_COVER_PATH', 'MAKEUP_COVER_URL', 'RESERVE_COVER_PATH', 'RESERVE_COVER_URL','USER_COVER_PATH','USER_COVER_URL']:
    assert(site_helper.config[url][-1] == '/')
    site_helper.config[url] = site_helper.config[url][:-1] + '-testing/'

site_helper.config.DB_DATABASE += '_test'

# delete testing files
for path in ['UPLOAD_IMAGE_PATH','MAKEUP_COVER_PATH','RESERVE_COVER_PATH',]:
    assert(site_helper.config[path].endswith('-testing/'))
    os.system( 'rm %s/* 2>/dev/null' % site_helper.config[path])
    if not os.path.exists(site_helper.config[path]):
        print 'mkdir %s -p' % site_helper.config[path]
        os.system('mkdir %s -p' % site_helper.config[path])

