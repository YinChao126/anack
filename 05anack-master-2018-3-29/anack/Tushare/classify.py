# -*- coding:utf-8 -*- 
import tushare as ts

def info():
    '''
    本模块用于获取分类信息
    '''
    print('本模块用于获取分类信息')
    print('industry 行业分类数据')
    print('concept 概念分类数据')
    print('area 地域分类数据')
    print('zxb 中小板列表')
    print('cyb 创业板列表')
    print('st ST列表')
    print('hs300 沪深300列表')
    print('sz50 上证50列表')
    print('zz500 中证500列表')
    
def industry():
    return ts.get_industry_classified()
  
def concept():
    return ts.get_concept_classified()
  
def area():
    return ts.get_area_classified()
  
def zxb():
    return ts.get_sme_classified()
  
def cyb():
    return ts.get_gme_classified()
  
def st():
    return ts.get_st_classified()
  
def hs300():
    return ts.get_hs300s()
  
def sz50():
    return ts.get_sz50s()
  
def zz500():
    return ts.get_zz500s()