# 本模块实现全局变量
# -*- coding:utf-8 -*- 
 
def _init():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    _global_dict[key] = value

def get_value(key, default_value = None):
    try:
        return _global_dict[key]
    except KeyError:
        return default_value