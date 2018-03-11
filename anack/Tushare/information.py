# -*- coding:utf-8 -*- 
    
import tushare as ts


def info():
    '''
    
    '''
    print('本模块用于输出各种消息')
    print('fund_holdings 基金持股')
    print('forecast_info 业绩预告')
    print('xsg_info 限售股信息')
    
def fund_holdings(year,month):
    '''
    基金持股消息披露
    year:年
    month：季度    只可取【1,2,3,4】
    '''
    try:
        return ts.fund_holdings(year,month)
    except:
        print('error, month=[1,4], please check your parameter')
        
def forecast_info(year,month):
    '''
    业绩预告
    '''
    try:
        return ts.forecast_data(year,month)
    except:
        print('error, month=[1,4], please check your parameter')
        
def xsg_info():
    '''
    限售股信息
    '''
    return ts.xsg_data()