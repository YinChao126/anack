# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:54:14 2018

@author: Administrator
# note: key 可以从"http://www.tuling123.com/"处免费注册获得
"""

import itchat
import requests
import json
key = ''

# 1. 单独发送
#itchat.auto_login()
#users = itchat.search_friends(name=u'阿狸')
#print(users)
#who = users[0]['UserName']
#print(who)
#itchat.send('进入自动回复模式，和我对话试试看',toUserName = who)

#2. 自动回复

#itchat.auto_login()
#@itchat.msg_register('Text',isGroupChat = True)#群回复
#def text_reply(msg):
#    return '新年快乐！（回复群消息）'
#@itchat.msg_register('Text')#个人回复
#def text_reply(msg):
#    print(msg['Text'])
#    print(type(msg))
#    return '新年快乐！（回复好友消息）'
#itchat.auto_login(hotReload=True)
#itchat.run()


#3. 实现了机器人对话
#import requests
#import json
#key = 'aa7ab198e85e4ba3bec6622654789472'
#while True:
#    info = input('\n我：')
#    url = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+info
#    res = requests.get(url)
#    res.encoding = 'utf-8'
#    jd = json.loads(res.text)#将得到的json格式的信息转换为Python的字典格式
#    print('\nTuling: '+jd['text'])#输出结果


#4. 个人图灵测试成功 
itchat.auto_login()
@itchat.msg_register('Text')#个人回复
def text_reply(msg):
#    print(msg['Text'])
    url = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+msg['Text']
    res = requests.get(url)
    res.encoding = 'utf-8'
    jd = json.loads(res.text)#将得到的json格式的信息转换为Python的字典格式
    return jd['text'] #输出结果
itchat.auto_login(hotReload=True)
itchat.run()

#5. 群回复测试成功
#itchat.auto_login()
#@itchat.msg_register('Text',isGroupChat = True)#群回复
#def text_reply(msg):
##    print(msg['Text'])
#    url = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+msg['Text']
#    res = requests.get(url)
#    res.encoding = 'utf-8'
#    jd = json.loads(res.text)#将得到的json格式的信息转换为Python的字典格式
#    return jd['text'] #输出结果
#itchat.auto_login(hotReload=True)
#itchat.run()