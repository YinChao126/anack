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
    if id[:3] == '000' or id[:3] == '002' or id[:3] == '300': #如果是深市，则前缀为1
        nid = '1' + id
    else: #如果是沪市主板，则前缀为0
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
    
def get_period_k_day(id, start_day, stop_day = 0):
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

    if id[:3] == '000' or id[:3] == '002' or id[:3] == '300': #如果是深市，则前缀为1
        nid = '1' + id
    else: #如果是沪市主板，则前缀为0
        nid = '0' + id
    url = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&\
    fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;VOTURNOVER;VATURNOVER" %(nid, start_day, stop_day)


#    url = "http://quotes.money.163.com/service/chddata.html?code=0%s&start=%s&end=%s&\
#    fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;VOTURNOVER;VATURNOVER" %(id, start_day,stop_day)
    res = requests.get(url)
    res.raise_for_status()
#    playFile = open(file_name, 'wb')
    
    raw_data = []
    for chunk in res.iter_content(1000000):
#        playFile.write(chunk)
        chunk = chunk.decode('gbk')
        pattern = '[^,\r\n]+'
        obj = re.compile(pattern)
        match = obj.findall(chunk)
        if len(match) < 8: #如果没有数据
            return 0
        
    header = match[:10] #如果增加字段，则此处以下需要相应修改
#    print(header)
    raw_data = match[10:]
    date = raw_data[::10]
    idc = raw_data[1::10]
    name = raw_data[2::10]
    price = raw_data[3::10]
    high = raw_data[4::10]
    lopen = raw_data[5::10]
    yesterday_close = raw_data[6::10]
    low = raw_data[7::10]
    vol = raw_data[8::10]
    mount = raw_data[9::10]
    
    data = {
#            header[0]:date,
            header[1]:idc,
            header[2]:name,
            header[3]:price,
            header[4]:high,
            header[5]:lopen,
            header[6]:yesterday_close,
            header[7]:low,
            header[8]:vol,
            header[9]:mount
            }
    df = pd.DataFrame(data,index = date)
#    playFile.close()
    return df

    
def k_day_to_csv(code, stop_day = 0):
    '''
    更新k线数据，并保存到本地，默认为更新到昨天
    code：目标个股,只能为'000xxx'形式
    stop_day: 0->昨天，    20170101:更新到指定的一天
    @更新逻辑：
    1. 如果无记录，则自动创建csv文件，默认为：ID.kday
    2. 如果有部分记录，则自动分析，并将后续的内容更新
    3. 如果记录比需要更新的更新，则直接返回
    
    缺陷：得到的数据是没有复权的，应该进行前复权
    '''
    base_path = './'   #修改此处可以更改文件存放路径，可以考虑作为一个配置参数
    start_day = '19970101' #start时间统一从1997年开始
    #参数合法性检查
    if isinstance(code,list):
        print('is a list')
    elif isinstance(code,str):
        file_name = code + '.csv'
#        print(file_name)
    else:
        print('bad input. please check it')
        return
    
    file_name = base_path + file_name
#    print(file_name)
    
    update_flag = 1     #1代表重新生成，   2代表更新   3代表无需处理
    #判断最新的是第几天
    try:
        with open(file_name,'r') as fh:
            content = fh.readlines()
            if len(content) > 2: #获取最新记录，总是在第二行
                latest_record = content[1].split(',')
                
                from datetime import datetime
                from dateutil.parser import parse
                latest_day = parse(latest_record[0])
                now = datetime.now().strftime('%Y-%m-%d')
                yesterday = parse(now)
                
                if yesterday > latest_day:
                    update_flag = 2
                    print('not the latest')
                else:
                    update_flag = 3
                    print(code + ' already the latest')
                    return
    except:
        update_flag = 1
        print('no record')
        
    #不同的情况适用不同更新逻辑
    if update_flag == 1:    #完全更新
        r = get_period_k_day(code, start_day)
        r.to_csv(file_name, encoding= 'gbk') 
    elif update_flag == 2:
        r = get_period_k_day(code, start_day)    #此处没有办法在首部添加
        r.to_csv(file_name, encoding= 'gbk')      #如果可以的话，则不必每次重写
        return 
    print('finish ' + code + ' update')
    return

def k_day_update(id_list, stop_day = 0):
    '''
    用户API，更新个股的K线数据，可以是列表，也可以是str
    '''
    #参数合法性检查
    if isinstance(id_list,list):
        print('is a list')
        for s in id_list:
            k_day_to_csv(s,stop_day)
    elif isinstance(id_list,str):
        k_day_to_csv(id_list,stop_day)
    else:
        print('bad input. please check it')
        return
        
if __name__ == '__main__':
    id = '601012'
    start_day = '20100625'
    stop_day = '20180904'
    
    #获取昨天的收盘价
#    price = get_close_price(id) 
#    print(price)
    
#    #获取指定一天的收盘价
#    price = get_close_price('600660','20170209') 
#    print(price)
#    
#    #获取从start_day开始直到昨天的收盘价
#    s = get_period_price('600660',start_day)
#    print(s)
#    
#    #获取指定时间段内的收盘价
#    s = get_period_k_day('601012',start_day,stop_day)
#    print(s)
#    s.to_csv('test.csv', encoding= 'gbk') 
    
    #更新K线数据并存文档
    company_list = ['600660', '600066', '000651', '600522', '601012', '600887']
    k_day_update(company_list)
    k_day_update('600066')
    
    