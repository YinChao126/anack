# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 21:02:35 2018

@author: Administrator
"""
from datetime import datetime
from datetime import timedelta
import time
import threading
from threading import Thread
L = threading.Lock() # 引入锁

#import imp #防止重复调用导致全局变量设置无效
#try:
#    imp.find_module('protocol')
#    found = True
#    print('arleady imported protocol')
#except ImportError:
#    from protocol import *

from protocol import ATDecoder

#try:
#    imp.find_module('wechat')
#    found = True
#    print('arleady imported wechat')
#except ImportError:
#    from wechat import *
# 参数初始化设置
now = datetime.now()
open_call_time = datetime(now.year,now.month,now.day,9,15)
close_call_time = datetime(now.year,now.month,now.day,9,25)
morning_open_time = datetime(now.year,now.month,now.day,9,30)
morning_close_time = datetime(now.year,now.month,now.day,11,30)
afternoon_open_time = datetime(now.year,now.month,now.day,13,00)
afternoon_close_time = datetime(now.year,now.month,now.day,23,00)

# 周期性调用该函数以实现完整的预警监测功能
def watch_dog_one_time():
    now = datetime.now()
    if now == close_call_time: # 获取大盘和个股的开盘信息并输出
        print(str(now)+'快开盘了')
    elif (now >= morning_open_time and now < morning_close_time) or \
    (now >= afternoon_open_time and now < afternoon_close_time):
        # 获取
#        rand = ran      
        print('主线程休眠')
        time.sleep(get_sleep_time() * 60) #休眠
        clear_sleep_time()
        print('主线程休眠完毕')
        print(str(now)+'检查一次')  
        test_str='AT:run'
        result = ATDecoder(test_str)
#        print(result)
        SendText2ChatRoom(result,'啊啊啊') #给指定群聊
    elif now >= afternoon_close_time: #3点以后停止运行
        print(str(now)+'停止运行')
        return 1
    else: #中场休息，直接sleep
        time.sleep(1)
        print(str(now)+'休息')
    return 0

# 外界的API接口，调用run函数以实现完整的监测
def M1808_run():
    while 1:
        L.acquire()
        ret = watch_dog_one_time()
        L.release()
#        if ret == 1:
#            return
#        else:
        time.sleep(30)

###############################################################################
#import imp #官方提供的加载方法，仍然没用
#import sys
#def __import__(name, globals=None, locals=None, fromlist=None):
#    try:
#        return sys.modules['wechat']
#    except KeyError:
#        pass    
#        
#    fp,pathname,description = imp.find_module('wechat')
#    try:
#        imp.load_module('wechat',fp,pathname,description)
#    finally:
#        if fp:
#            fp.close()
#            
#itchat.auto_login(hotReload=True)
            
            
###############################################################################

from wechat import *
def test():
    n = 1
    while n > 0:
        print(n)
        n = n + 1
        time.sleep(2)
#t1 = Thread(target=M1808_run, args=())
itchat.auto_login(hotReload=True)
#t1 = Thread(target=test, args=()) #仅供测试
t1 = Thread(target=M1808_run, args=())
t2 = Thread(target=itchat.run,args=())
t1.start()
t2.start()
###############################################################################
#from wechat import *
#from protocol import *
#import itchat
#
#itchat.auto_login(hotReload=True)
#itchat.run()

#cmd='AT:set_target_id=600660,000651,601012,000002,000333'
#ATDecoder(cmd)
#cmd='AT:run'
#s = ATDecoder(cmd)
#cmd='AT:get_target_id?'
#s = ATDecoder(cmd)
###############################################################################