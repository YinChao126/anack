# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 10:23:33 2018

@author: Administrator
"""
import time
import re

from early_warning import *
#import imp #防止重复调用导致全局变量设置无效
#try:
#    imp.find_module('early_warning')
#    found = True
#    print('arleady imported early_warning')
#except ImportError:
#    from early_warning import *

def ATDecoder(strin):
    pattern_id = '(?<=AT:)[^=?]+'
    reobj = re.compile(pattern_id)
    cmd = reobj.findall(strin)
    cmd = "".join(cmd)  #list to str
    print('\ncmd =',cmd)  #该句话只做调试用
        
#    if cmd in cmd_list: #找到合适的命令
    if cmd == 'set_target_id':  #设置感兴趣的股票列表
#        print('set target_id\n')
        pattern_id = '\d{6}'
        reobj = re.compile(pattern_id)
        stock_id = reobj.findall(strin)
        set_target_id(stock_id)
        return ('stock id set ok')
        
    elif cmd == 'get_target_id':    #显示股票列表
#        print(show_target_id())
        return show_target_id()
        
    elif cmd == 'clear_target': #清空股票列表
        clear_target_id()
        return 'target id cleared'
        
    elif cmd == 'set_para': #设置参数
        pattern_id = '[0-9.]+'
        reobj = re.compile(pattern_id)
        result = reobj.findall(strin)
        if len(result) == 1:
            set_param(float(result[0]))    
        else:
            set_param(float(result[0]),float(result[1]))    
        return 'set para th = %s, quantity = %s' % (result[0],result[1])
        
    elif cmd == 'get_para': #查看设置的预警参数
        th, quantity = get_param()
        return 'rase th, quantity = %.2f, %.2f' % (th, quantity)
        
    elif cmd == 'check': #主动查询当前个股状态
        r = str(get_main_market())
        r += '\n\n'
        r += str(get_stock_market())
        return r
        
    elif cmd == 'sleep': #让主机休眠x分钟
        pattern_id = '(?<=sleep=)[0-9]+'
        reobj = re.compile(pattern_id)
        result = reobj.findall(strin)
        result = "".join(result)  #list to str  
        print('主机休眠',result,'分钟\n')
        set_sleep_time(int(result))
#        time.sleep(int(result)*60)
        
        return '开始休眠'   #仅供测试
        
    elif cmd == 'level': #设置预警模式
        pattern_id = '(?<=level=)[0-9]'
        reobj = re.compile(pattern_id)
        result = reobj.findall(strin)
        result = "".join(result)  #list to str  
        set_warning_level(int(result))
        return ('设置预警模式')
        
    #测试指令，正式使用时请注释--------------------------------------------------
    elif cmd == 'run':
        init()
        market_info = get_stock_market()
#        print(market_info)
        warning_info = check(market_info)
        print(warning_info)
        return warning_info
    
    elif cmd == 'test':
        return 'still connecting...'

###############################################################################
#test_str='AT:set_target_id=600660,000651,601012,000002,000333'
#print(ATDecoder(test_str))
#
#test_str='AT:get_target_id?'
#print(ATDecoder(test_str))

#test_str='AT:clear_target'
#print(ATDecoder(test_str))

#test_str='AT:get_target_id?'
#print(ATDecoder(test_str))

#test_str='AT:set_para=1.0,0.9'
#print(ATDecoder(test_str))
#
#test_str='AT:get_para?'
#print(ATDecoder(test_str))

#test_str='AT:sleep=1'
#print(ATDecoder(test_str))

#test_str='AT:check?'    
#print(ATDecoder(test_str))

#test_str='AT:level=3'
#print(ATDecoder(test_str))
#
#test_str='AT:run'
#print(ATDecoder(test_str))
#
#test_str='AT:test'
#print(ATDecoder(test_str))

#print(get_main_market())
#print(get_stock_market())
###################################
#from test import * #此处就是设置的全局变量不起作用的原因
#import test
#test.set_a()
#test.a = 1
#print(test.a)