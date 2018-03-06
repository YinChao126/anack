# -*- coding:utf-8 -*- 
import tushare as ts
def info():
    print('本模块用于获取实时交易信息')
    print('k_day 获取个股的K线图')
    print('k_today 获取当日所有股票的K线图')
    print('index 获取今日指数信息')
    print('ddjy 获取指定日期下的大单交易信息')
    
def k_day(index,mode='D'):

    if mode == 'D':
        return ts.get_k_data(index)
    elif mode == 'M':
        return ts.get_k_data(index,ktype='M')

def k_today():

    return ts.get_today_all()

def index():

    return ts.get_index()

def ddjy(id,time,hand=400):

    return ts.get_sina_dd(id, date=time, vol=hand)

