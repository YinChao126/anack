# -*- coding:utf-8 -*- 

import App.IndustryEstimation
from SQL.sql import pymysql_connect
from SQL.update import get_interest_list

industry_check = []
dbconn=pymysql_connect()
filename = './SQL/感兴趣的个股列表.txt'

App.IndustryEstimation.CreateTable() #此处开启则清空此前所有内容
for stock_id in get_interest_list(filename):
    name = App.IndustryEstimation.GetIndustryName(stock_id) #根据id获取行业名
    
    if name in industry_check: #去重检查
        continue
    else:
        industry_check.append(name)
 
    App.IndustryEstimation.Estimation(dbconn,name,2017) #入库
 