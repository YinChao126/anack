# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:23:28 2018

@author: YinChao
@date: 20180520
"""

import urllib.request as request  
import datetime 
import time 
'''  
@query a single date: string '20170401';  
@api return day_type: 0 workday 1 weekend 2 holiday -1 err  
@function return day_type: 1 workday 0 weekend&holiday  
'''  
  
  
def get_day_type(query_date): 
    '''
    节假日求取辅助函数，从指定网址上获取当日状态
    0工作日    1周末     2节假日
    http://tool.bitefu.net/jiari/?d=20181009  返回0（工作日）
    http://tool.bitefu.net/jiari/?d=20181014  返回1（周末）
    http://tool.bitefu.net/jiari/?d=20181001  返回2（国庆节）
    '''
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date  
    resp = request.urlopen(url)  
    content = resp.read()  
    if content:  
        try:  
            day_type = int(content)  
        except ValueError:  
            return -1  
        else:  
            return day_type  
    else:  
        return -1  


def isWorkingTime():
    '''
    判断当前时刻是否工作日上班时间（未考虑节假日影响）
    '''
    workTime=['09:00:00','18:00:00']
    dayOfWeek = datetime.datetime.now().weekday()
    beginWork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[0]
    endWork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[1]
    beginWorkSeconds=time.time()-time.mktime(time.strptime(beginWork, '%Y-%m-%d %H:%M:%S'))
    endWorkSeconds=time.time()-time.mktime(time.strptime(endWork, '%Y-%m-%d %H:%M:%S'))
    if (int(dayOfWeek) in range(5)) and int(beginWorkSeconds)>0 and int(endWorkSeconds)<0:
        return 1
    else:
        return 0   

def isWorkingDay():
    '''
    判断今天是否工作日
    '''
    dayOfWeek = datetime.datetime.now().weekday()   #今天星期几？
    if dayOfWeek < 6:
        return 1
    else:
        return 0     
    
  
def is_tradeday(query_date):  
    '''
    判断给定日期是否股市交易日（考虑了节假日的影响）
    '''
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()  
    if weekday <= 5 and get_day_type(query_date) == 0:  
        return 1  
    else:  
        return 0  
  
  
def today_is_tradeday():
    '''
    判断今天是否股市交易日（考虑了节假日的影响）
    '''  
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')  
    return is_tradeday(query_date)  
  
  
if __name__ == '__main__':  
    print(is_tradeday('20171229'))  
    print(today_is_tradeday()) 