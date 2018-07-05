# -*- coding: utf-8 -*-
"""
从163网址上获取指定ID指定时间段的K线数据
"""
import requests
import re
import datetime 
import pandas as pd
'''

完整网址：
http://quotes.money.163.com/service/chddata.html?code=0%06d&start=%d&end=%d&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;VOTURNOVER;VATURNOVER
'''


def get_close_price(id, day = 0):
    '''
    获取指定ID指定日期的收盘价
    输入：id -> str形式的ID号： '600660'
         day -> str形式的日期： '20180626'
    返回值：str形式的价格： '25.54'， 如果当天为节假日，则返回0
    '''
    if day == 0:
        day = datetime.datetime.now() - datetime.timedelta(days=1)
        day = day.strftime("%Y%m%d")
    if id[:3] == '000' or id[:3] == '002' or id[:3] == '300': #如果非主板，则前缀为1
        nid = '1' + id
    else: #如果是主板，则前缀为0
        nid = '0' + id
    url = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&\
    fields=TCLOSE" %(nid, day,day)
    res = requests.get(url)
    res.raise_for_status()
    
    for chunk in res.iter_content(100000):
#        print(chunk)
        pattern = '[^,\r\n]+'
        obj = re.compile(pattern)
        match = obj.findall(chunk.decode('gbk'))
        #print(match)
        if len(match) < 8:
            return 0
        else:
            return match[-1]
    
def get_period_price(id, start_day, stop_day = 0):
    '''
    获取指定ID一个时间段内的K线数据
    输入：id -> str形式的ID号： '600660'
         start_day -> str形式的日期： '20180626'
         stop_day -> 同上， 默认到昨天
    返回值：一个dataframe
    '''
    if stop_day == 0:
        day = datetime.datetime.now() - datetime.timedelta(days=1)
        day = day.strftime("%Y%m%d")
#    file_name = id + '.csv'
    url = "http://quotes.money.163.com/service/chddata.html?code=0%s&start=%s&end=%s&\
    fields=TCLOSE" %(id, start_day,stop_day)
    res = requests.get(url)
    res.raise_for_status()
#    playFile = open(file_name, 'wb')
    
    raw_data = []
    for chunk in res.iter_content(100000):
#        playFile.write(chunk)
        chunk = chunk.decode('gbk')
        pattern = '[^,\r\n]+'
        obj = re.compile(pattern)
        match = obj.findall(chunk)
        if len(match < 8): #如果没有数据
            return 0
        
    header = match[:4] #如果增加字段，则此处以下需要相应修改
#    print(header)
    raw_data = match[4:]
    date = raw_data[::4]
#    idc = raw_data[1::4]
#    name = raw_data[2::4]
    price = raw_data[3::4]
    data = {
#            header[0]:date,
#            header[1]:idc,
#            header[2]:name,
            header[3]:price
            }
    df = pd.DataFrame(data,index = date)
#    playFile.close()
    return df

if __name__ == '__main__':
    id = '300124'
    start_day = '20170625'
    stop_day = '20180625'
    
    #获取昨天的收盘价
    price = get_close_price(id) 
    print(price)
    
#    #获取指定一天的收盘价
#    price = get_close_price('600660','20171009') 
#    print(price)
#    
#    #获取从start_day开始直到昨天的收盘价
#    s = get_period_price('600660',start_day)
#    print(s)
#    
#    #获取指定时间段内的收盘价
#    s = get_period_price('600660',start_day,stop_day)
#    print(s)
    
    