import site_helper, os

EXCEPT_FILES = ['__init__', 'api_helper']
for module_name, module in site_helper.getDirModules(os.path.split(os.path.realpath(__file__))[0], __name__, except_files=EXCEPT_FILES):
    exec('%s = module' % module_name)
