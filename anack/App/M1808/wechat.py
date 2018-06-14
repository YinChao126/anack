# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 10:08:24 2018

@author: Administrator
"""
import time
import itchat
from protocol import *
#import imp #防止重复调用导致全局变量设置无效
#try:
#    imp.find_module('protocol')
#    found = True
#    print('arleady imported protocol')
#except ImportError:
#    from protocol import *
'''
1. 给单个人发消息
2. 给指定群发消息
3. 实现消息注册
4. 显示当前可用的群聊
'''
def WechatLogin():
    itchat.auto_login(hotReload=True)
    
def SendText2Friend(msg,nick_name='filehelper'): #已经测试成功，可用
    '''
    @ 发送文本消息给指定好友，如果不指定nick_name则发送给自己的文件助手
    '''
    if nick_name == 'filehelper':
        itchat.send(msg,toUserName = 'filehelper')
    else:
        
        users = itchat.search_friends(name=nick_name)
#        print(users)
        who = users[0]['UserName']
#        print(who)
        itchat.send(msg,toUserName = who)
    
def SendText2ChatRoom(context, name):
    '''
    @ 发送消息到特定群聊内
    @ 备注：1.确定该群聊存在（可调用PrintChatRoomList查看）
    @      2.切记把群聊加入通讯录，否则只能显示活跃的前几个群聊
    '''
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        if room['NickName'] == name:
            userName = room['UserName']
            break
    try:
        itchat.send_msg(context, userName)
    except:
        print('warning: no this chatrooms')
        
def PrintChatRoomList():
    '''
    @ 显示当前可见的群聊名
    '''
    rooms = itchat.get_chatrooms(update=True)
    for s in rooms:
        print(s['NickName'])
    
@itchat.msg_register('Text',isGroupChat = True)#群回复
def text_reply(msg):
#    msg.user.send('%s: %s' % (msg.type, msg.text))  #终于发出消息了
    who = msg['ActualNickName']    #获取发送人的名称
    content = msg['Text']
    print(who,'call me')
    if content == 'logout' or content == 'quit' or content == 'exit':
        itchat.logout()
        return
    ### 发送内容有三种方式：给自己、给别人、给群聊(示例程序),测试成功
#    if who == '尹超': 
#        SendText2Friend('yc send')    #给自己(文件助手)
#        SendTxet2ChatRoom('yc send','啊啊啊') #给指定群聊
#    else:
#        SendText2Friend('ali send','阿狸')   #给指定的人
#        SendTxet2ChatRoom('ali send','啊啊啊') #给指定群聊
        
    #-------------------------------------------------
    authority = ['尹超','徐抒田','李航','李繁','鹏','顾秋杨']
#    if who in authority: #此处有bug，自己先发送的话who为空，必须别人先发信息
    if 1:
#        print(content)
        result = ATDecoder(content)
#        print(result)
        if result != None:
            SendText2ChatRoom(result,'啊啊啊') #给指定群聊
#    else:
#        print('no reply')
    #-------------------------------------------------------------------    
    time.sleep(1)
########################################################################
#WechatLogin()
#SendText2Friend('test')
#SendText2Friend('test','阿狸')
#SendTxet2ChatRoom('test','啊啊啊')
#itchat.run()
