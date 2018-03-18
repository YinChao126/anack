# -*- coding:utf-8 -*- 

import App.IndustryEstimation
from SQL.sql import pymysql_connect

dbconn=pymysql_connect()

def get_interest_list():
    '''
    解析"感兴趣的个股列表.txt",返回list类型的数据供其他模块使用
    '''
    list_id = []
    with open('./SQL/感兴趣的个股列表.txt','r') as fh:
        s = fh.readline()   #获取更新时间
        s = fh.readline()   #获取目标长度  
        
        lines = fh.readlines()  #获取目标内容
    for s in lines:
        code = s[:6]
        list_id.append(code)    
    list_id.sort()
    return list_id 

App.IndustryEstimation.CreateTable() #此处开启则清空此前所有内容
industry_check = []
for stock_id in get_interest_list():
    name = App.IndustryEstimation.GetIndustryName(stock_id) #根据id获取行业名
    
    if name in industry_check: #去重检查
        continue
    else:
        industry_check.append(name)
 
    App.IndustryEstimation.Estimation(dbconn,name,2017) #入库
 