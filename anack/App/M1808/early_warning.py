# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 07:31:22 2018

@author: Administrator
"""

# 本模块用于实现一个实时预警器
 
import requests
import tushare as ts
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = 'GB2312'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


###############################################################################
###############################################################################
# 自动预警逻辑
'''
 1.实现对大盘的跟踪观测
 2.实现对指定个股的跟踪
 3.实现整个市场资金异动的发掘（暂时不实现）
'''
###############################################################################
# 用户配置参数，可手动修改或者通过AT指令实时修改
global target_id
global rase_th
global volume_rate
global warning_level
global sleep_time

target_id = [] #感兴趣的个股列表
rase_th = 2.5 #涨跌幅预警阈值（%）
volume_rate = 1 #量比阈值
quantity_th = 15 #成交量预警阈值（亿），暂时不管
sleep_time = 0 #用于控制主线程休眠

'''
warning_level 用来实现预警等级
0 关闭预警功能
1 只预警实时价格（默认最少会监控大盘状态，如果不设置target_id的话）
2 预警实时价格+量比
3 预警实时价格+量比+年月周线
'''
warning_level = 3 #价格预警开关（0：全部关闭，1：只预警实时价格，1：预警周线
###############################################################################
# 全局变量区
global avg_info
avg_info = pd.DataFrame(columns=['id', 'avg_price_week', 'avg_price_month'
                                 'avg_price_year','volume_min']) #保存平均值
global morning_open_time    #用以指示交易时间
global morning_close_time
global afternoon_open_time
global afternoon_close_time
###############################################################################
# 系统参数：不可随意更改
price_line = 0
volume_line = 3
rate_line = 2
stock_info = [] #定义的消息类型：[0]当前股价，[1]涨跌幅，[2]成交量

avg_line_m = 0
avg_line_w = 1
avg_line_y = 2
id_line = 3
avg_vol_min = 4
###############################################################################
#初始化时获取个股的历史平均水平
def init():
    '''
        根据target_id获取历史平均成交量、均线水平等参数，作为后续check的比对依据
        id:
        avg_price_week:周线
        avg_price_month:月线
        avg_price_year:年线
        volume_min:5日内平均每分钟成交量（用于计算量比）
    '''
    global avg_info
    global morning_open_time
    global morning_close_time
    global afternoon_open_time
    global afternoon_close_time
#    input_id = ['000651','600887','600066','600660']
    input_id = target_id
    
    avg_price_week = []    #周均线，5天
    avg_price_month = []   #月均线，22天
    avg_price_year = [] #年线，250天
    avg_volumn_min = []
    for id_name in input_id:
        a = ts.get_k_data(id_name)  #获取基础信息
        temp = a.iloc[-5:]['close']
        avg_price_week.append(temp.sum()/5)
        temp = a.iloc[-22:]['close']
        avg_price_month.append(temp.sum()/22)    
        if len(a) > 250:
            temp = a.iloc[-250:]['close']
            avg_price_year.append(temp.sum()/250)
        else:
            temp = a.iloc[:]['close']
            avg_price_year.append(temp.sum()/len(a))     
        a = a[-5:]  #计算过去5天内的平均成交量
        b = a.iloc[:]['volume']
        c = b.sum() / len(b) / 240
        avg_volumn_min.append(c)
        
    data = {'id':input_id,
            'avg_price_week':avg_price_week,
            'avg_price_month':avg_price_month,
            'avg_price_year':avg_price_year,
            'volume_min':avg_volumn_min
            }
    avg_info = pd.DataFrame(data)
    
    
    now = datetime.now()
    morning_open_time = datetime(now.year,now.month,now.day,9,30)
    morning_close_time = datetime(now.year,now.month,now.day,11,30)
    afternoon_open_time = datetime(now.year,now.month,now.day,13,00)
    afternoon_close_time = datetime(now.year,now.month,now.day,15,00)
#    return pd.DataFrame(data)

def get_main_market():
    #监测大盘
    url = 'http://hq.sinajs.cn/list=s_sh000001'
    html = get_one_page(url)
    pattern_data = '-?[\d.]+'
    reobj = re.compile(pattern_data)
    r1 = reobj.findall(html)    

    url = 'http://hq.sinajs.cn/list=s_sz399001'
    html = get_one_page(url)
    pattern_data = '-?[\d.]+'
    reobj = re.compile(pattern_data)
    r2 = reobj.findall(html)
    
    name = ['上证综指','深成指数']
    price = [r1[1],r2[1]]
    rise = [r1[3],r2[3]]
    quantity = [round(float(r1[5])/10000,2),round(float(r2[5])/10000,2)]
    data = {'name':name,
         'price':price,
         'rise_rate':rise,
         'quantity':quantity
        }
    r = pd.DataFrame(data)
    return r
    
def get_stock_market():
    global target_id
    if len(target_id) < 1:
        return 0
    s = ''
    for l in target_id:
        if (int(l) < 600000) and (int(l) != 1):
            s += 's_sz'     #如果此处换为 'sz',则对应详细买卖量信息
        else:
            s += 's_sh'
        s += l
        s += ','
    result = s[:-1]
#    print(result)    
    url = 'http://hq.sinajs.cn/list=' + result
#    print(url)
#    url = 'http://hq.sinajs.cn/list=sh600660,sh600006'
    html = get_one_page(url)
    pattern_data = '-?[\d.]+'
    reobj = re.compile(pattern_data)
    data = reobj.findall(html)
#    print('个股数据'+ str(data))

    name = data[::6]
    cur_price = data[1::6]
    rise_rate = data[3::6]
    volume = data[4::6]     
    data = {'id':name,
         'cur_price':cur_price,
         'rise_rate':rise_rate,
         'volume':volume
        }
    r = pd.DataFrame(data)
#    print(r)
    return r

def check(df):
    '''
    1. 判断涨跌
    2. 判断成交量
    3. 判断是否突破各级均线水平
    '''
    global volume_rate
    global morning_open_time
    global morning_close_time
    global afternoon_open_time
    global afternoon_close_time
    global warning_level
    
    # 如果关闭了预警功能，则直接退出
    if warning_level == 0:
        return 'close warning mode'
    total_info_buff = ''
    
    #监测大盘
    market_th = 1.5 #大盘预警门限比个股要低，而且禁止配置
    
    info = get_main_market()
    rate = float(info.iloc[0]['rise_rate'])
    if abs(rate) >= market_th:
        total_info_buff += '沪市预警：'
        total_info_buff += info.iloc[0]['price']
        total_info_buff += '\t涨跌(%)：'
        total_info_buff += info.iloc[0]['rise_rate']
        total_info_buff += '\t成交量(亿)'
        total_info_buff += str(info.iloc[0]['quantity'])
        total_info_buff += '\n\n'
        
    rate = float(info.iloc[1]['rise_rate'])
    if abs(rate) >= market_th:
        total_info_buff += '深市预警：'
        total_info_buff += info.iloc[1]['price']
        total_info_buff += '\t涨跌(%)：'
        total_info_buff += info.iloc[1]['rise_rate']
        total_info_buff += '\t成交量(亿)'
        total_info_buff += str(info.iloc[1]['quantity'])
        total_info_buff += '\n\n'
           
    # 监测个股
    try:
        s = len(df)
    except:
         return total_info_buff    
    
#    if df == 0: #如果没有设置target_id,则只监控大盘状态
#        return total_info_buff
    for indexs in df.index:
        #涨跌判断
        if abs(float(df.loc[indexs].values[rate_line])) > rase_th:
#            print(df.loc[indexs].values[:])
            total_info_buff += '涨跌预警：ID=' + df.loc[indexs].values[1] + \
            ', 涨跌幅：' + df.loc[indexs].values[2] + '%\n'  
        #均线判断     
        if warning_level > 2:           
            if float(df.loc[indexs].values[price_line]) < \
               float(avg_info.iloc[indexs].values[avg_line_w]):
                total_info_buff += '周线预警：ID=' + df.loc[indexs].values[1] + \
                ',（当前价<周线):(' + df.loc[indexs].values[0] + '<' + \
                str(avg_info.iloc[indexs].values[avg_line_w]) + ')\n'  
    #            print('week error')
            if float(df.loc[indexs].values[price_line]) < \
               float(avg_info.iloc[indexs].values[avg_line_m]):
                total_info_buff += '月线预警：ID=' + df.loc[indexs].values[1] + \
                ',（当前价<月线):(' + df.loc[indexs].values[0] + '<' + \
                str(round(avg_info.iloc[indexs].values[avg_line_m],2)) + ')\n'  
    #            print('month error')
            if float(df.loc[indexs].values[price_line]) < \
               float(avg_info.iloc[indexs].values[avg_line_y]):
                total_info_buff += '年线预警：ID=' + df.loc[indexs].values[1] + \
                ',（当前价<年线):(' + df.loc[indexs].values[0] + '<' + \
                str(round(avg_info.iloc[indexs].values[avg_line_y],2)) + ')\n'  
#            print('year error')
        #量比判断
        if warning_level > 1:
            now = datetime.now()
            if now < morning_close_time:
                diff = now - morning_open_time
                time_elapse = diff.seconds / 60
            elif now <= afternoon_open_time:
                time_elapse = 120
            elif now < afternoon_close_time:
                diff = now - afternoon_open_time
                time_elapse = 120 + diff.seconds / 60
            else:
                time_elapse = 240  
            cur_vol = float(df.loc[indexs].values[volume_line])
            vol_rate = cur_vol / (time_elapse * avg_info.iloc[indexs].values[avg_vol_min])
    
            if  vol_rate > volume_rate :  #成交量
                total_info_buff += '量比异常：ID=' + df.loc[indexs].values[1] + \
                ',量比=' + str(round(vol_rate,2)) + ')\n'
            total_info_buff += '\n'
    return total_info_buff
            
###############################################################################
# API
# 
###############################################################################
def set_target_id(set_id):
    global target_id
    if isinstance(set_id, (list)):
        for i in set_id:
            if i not in target_id:
                target_id.append(i)
    elif isinstance(set_id, (str)):
        if set_id not in target_id:
            target_id.append(set_id)  
    else:
        print('input invalid, only support list or str type')              
            
def del_target_id(rm_id):
    global target_id
    if isinstance(rm_id, (list)):
        for i in rm_id:
            if i in target_id:
                target_id.append(i)
    elif isinstance(rm_id, (str)):
        if rm_id in target_id:
            target_id.remove(rm_id)  
    else:
        print('input invalid, only support list or str type')
    
def show_target_id():
    global target_id
    msg = '当前个股列表：'
    for i in target_id:
#        print(i)
        msg += i
        msg += ','
    return msg

def clear_target_id():
    global target_id
#    print(target_id)
#    print(len(target_id))
    while len(target_id) > 0:
        target_id.pop()
#------------------------------------------------------------------------------            
def set_param(r_th, v_th = volume_rate):#设置预警阈值
    global rase_th
    global volume_rate
    rase_th = r_th
    volume_rate = v_th     
def get_param():
    global rase_th
    global volume_rate
    return rase_th,volume_rate   

def set_warning_level(level):
    global warning_level
    if level > 3:
        level = 3
    elif level < 0:
        level = 0
    warning_level = level
    print('全局预警等级设置为',level,'\n')

def set_sleep_time(set_time):
    global sleep_time
    sleep_time = set_time
    print('休眠 %s ' % set_time, '分钟')
    return sleep_time

def get_sleep_time():
    global sleep_time
    return sleep_time
    
def clear_sleep_time():
    global sleep_time
    sleep_time = 0
#最终的信息输出，发送给微信端
#def output_msg():
#    global out_buff    
#    out_buff = total_info_buff + individual_info_buff
#    return out_buff
###############################################################################
###############################################################################
#init()  #不初始化会出问题
#l = ['000001','600066','000651','601012']
#result = get_stock_market(l)
#set_param(1,10)
#check(result)
#l = get_param()

#clear_target_id()
#l = ['00031','2']
#set_target_id('000665')
#set_target_id(l )
#show_target_id()
#del_target_id('00031')
#del_target_id('2')
#show_target_id()
###############################################################################
###############################################################################
###############################################################################
#l = ['600066','000651','601012']
#set_target_id(l)
#init() #此处逻辑有问题，必须先执行此句才能实现初始化
#c = get_stock_market()
#check(c)
#print(show_target_id())
