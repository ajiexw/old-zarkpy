#coding=utf-8
import web

class Decorator:
    TEST = True #指明装饰是否需要测试, 比如Pagination这种视觉性的就不需要测试

    # 参数model可以是一个model.Model的实例，也可以是Decorator的实例。
    # client可以在arguments参数中指明rewrite_functions来选择使用哪些decorator functions
    def __init__(self, model, arguments):
        assert( type(arguments) is dict )
        self.model = model
        self.__getRealModel()._decorator_model = self # 只允许这一行引用model的_decorator_model
        self.arguments = web.Storage(arguments)
        if arguments.has_key('rewrite_functions'):
            self.rewrite_functions = arguments.rewrite_functions

    def __getattr__(self, attr):
        assert(len(self.rewrite_functions) > 0)
        # 注意,在Decorator的继承类中,overwrite的method必须同时出现在rewrite_functions中.
        # 因为,如果rewrite_functions中缺少的话就过不了下面这个if的判断,就不能返回正确的method
        # 而如果出现了在rewrite_functions中又没有被overwrite的话,if就会错误的截断
        # 同时注意,如果你在这里引言self或self.model的属性的话,就会产生递归调用本函数
        if attr in self.rewrite_functions:
            return getattr(self, attr)
        else:
            return getattr(self.model, attr)

    def __getRealModel(self):
        if isinstance(self.model, Decorator):
            return self.model.__getRealModel()
        else:
            return self.model

    def getModelTableName(self):
        model = self
        while isinstance(model, Decorator):
            model = model.model
        return model.table_name

