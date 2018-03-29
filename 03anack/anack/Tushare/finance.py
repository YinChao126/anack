# -*- coding:utf-8 -*- 
import tushare as ts
def info():
  '''
  '''
    print('本模块用于获取基本面信息')
    print('basic_info 获取股票列表')
    print('finance_report 所有季度报表')
    print('area 地域分类数据')
    print('zxb 中小板列表')
    print('cyb 创业板列表')
    print('st ST列表')
    print('hs300 沪深300列表')
    print('sz50 上证50列表')
    print('zz500 中证500列表')
  
def basic_info():
    '''
    获取股票列表
    '''
    return ts.get_stock_basics()

def finance_report(year, month):
    '''
    季度报主表
    '''
    return ts.get_report_data(year,month)

def profit(year, month):
    return ts.get_profit_data(year, month)
    
def cashflow(year, month):
    return ts.get_cashflow_data(year, month)
