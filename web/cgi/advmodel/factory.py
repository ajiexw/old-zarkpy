#coding=utf-8
import advmodel

def getInstance(model_name, new_table_name):
    exec('ret_model = advmodel.%s()' % model_name)
    ret_model.table_name = new_table_name
    return ret_model

