# -*- coding:utf-8 -*- 
import tushare as ts

def info():
    '''
    
    '''
    print('本模块用于获取宏观经济数据')
    print('deposit 存款利率一览表')
    print('loan 贷款利率一览表')
    print('rrr 存款准备金率')
    print('money_supply 货币供应量')
    print('gdp 国内生产总值')
    print('cpi 居民消费价格指数')
    print('ppi 工业品出厂价格指数')
    print('gdp_contribute 三大产业对GDP的贡献率')
    
def deposit():
  return ts.get_deposit_rate()
  
def loan():
  return ts.get_loan_rate()
  
def rrr():
  return ts.get_rrr()
  
def money_supply():
  return ts.get_money_supply()
  
def gdp():
  return ts.get_gdp_year()
  
def cpi():
  return ts.get_cpi()
  
def ppi():
  return ts.get_ppi()
  
def gdp_contribute():
  return ts.get_gdp_contrib()
  