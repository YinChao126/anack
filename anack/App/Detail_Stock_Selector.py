# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:57:22 2018

@author: 10191773
"""

import sys
sys.path.append("..")
import pandas as pd
import pymysql
import tushare as ts
from SQL.sql import pymysql_connect
from SQL.sql import df_to_mysql


'''
code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数
'''

dbconn=pymysql_connect()

def create_stock_select_table():
    #db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    db = pymysql_connect()
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS all_stock_select') 
    stock_select_sql = """CREATE TABLE IF NOT EXISTS `all_stock_select` (
                `code`    varchar(255) DEFAULT NULL,
                `name`    varchar(255) DEFAULT NULL,
                `industry`  varchar(255) DEFAULT NULL, 
                `area`    varchar(255) DEFAULT NULL,
                `pe`    float(25) DEFAULT NULL,                       #市盈率
                `outstanding`    varchar(255) DEFAULT NULL, 
                `totals`    varchar(255) DEFAULT NULL,
                `totalAssets`    float(25) DEFAULT NULL,              #总资产(万)
                `liquidAssets`    varchar(255) DEFAULT NULL, 
                `fixedAssets`    varchar(255) DEFAULT NULL, 
                `reserved`    varchar(255) DEFAULT NULL, 
                `reservedPerShare`    varchar(255) DEFAULT NULL,
                `esp`    varchar(255) DEFAULT NULL,
                `bvps`    varchar(255) DEFAULT NULL,
                `pb`    float(25) DEFAULT NULL,                       #市净率
                `timeToMarket`    varchar(255) DEFAULT NULL,
                `undp`    varchar(255) DEFAULT NULL,
                `perundp`    varchar(255) DEFAULT NULL,
                `rev`    float(25) DEFAULT NULL,                      #收入同比
                `profit`    float(25) DEFAULT NULL,                   #利润同比
                `gpr`    float(25) DEFAULT NULL,                      #毛利率
                `npr`    float(25) DEFAULT NULL,                      #净利润率
                `holders` varchar(255) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(stock_select_sql)
    db.commit()
    cursor.close()
    db.close()


def create_stock_detail_select_table():
    #db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    db = pymysql_connect()
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS detail_stock_select') 
    stock_select_sql = """CREATE TABLE IF NOT EXISTS `detail_stock_select` (
                `code`    varchar(255) DEFAULT NULL,
                `name`    varchar(255) DEFAULT NULL,
                `industry`  varchar(255) DEFAULT NULL, 
                `area`    varchar(255) DEFAULT NULL,
                `pe`    float(25) DEFAULT NULL,                       #市盈率
                `outstanding`    varchar(255) DEFAULT NULL, 
                `totals`    varchar(255) DEFAULT NULL,
                `totalAssets`    float(25) DEFAULT NULL,              #总资产(万)
                `liquidAssets`    varchar(255) DEFAULT NULL, 
                `fixedAssets`    varchar(255) DEFAULT NULL, 
                `reserved`    varchar(255) DEFAULT NULL, 
                `reservedPerShare`    varchar(255) DEFAULT NULL,
                `esp`    varchar(255) DEFAULT NULL,
                `bvps`    varchar(255) DEFAULT NULL,
                `pb`    float(25) DEFAULT NULL,                       #市净率
                `timeToMarket`    varchar(255) DEFAULT NULL,
                `undp`    varchar(255) DEFAULT NULL,
                `perundp`    varchar(255) DEFAULT NULL,
                `rev`    float(25) DEFAULT NULL,                      #收入同比
                `profit`    float(25) DEFAULT NULL,                   #利润同比
                `gpr`    float(25) DEFAULT NULL,                      #毛利率
                `npr`    float(25) DEFAULT NULL,                      #净利润率
                `holders` varchar(255) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(stock_select_sql)
    db.commit()
    cursor.close()
    db.close()    
 
    
#初步筛选   
def stock_select_to_sql(PE,TotalAssists):
    create_stock_select_table()    
    
    df=ts.get_stock_basics()
    #df.to_excel('c:/python/all_stock_list.xlsx')
    df= df[df['pe'] < PE]
    df= df[df['pe'] > 0]
    print(df)
    #df.to_excel('c:/python/all_stock_pe50.xlsx')
    df= df[df['totalAssets'] >= TotalAssists]
    df= df[df['rev'] >= 0]
    df= df[df['profit'] >= 0]
    #df.to_excel('c:/python/all_stock_assets100.xlsx')
    print(df)  
    print('...........................before')
    #df=df.iloc[1:]
    #df.to_excel('c:/python/all_stock_assets100head.xlsx')
    #sql.df_to_mysql('all_stock_select',df)
    df_to_mysql('all_stock_select',df)
    print('...........................after')
    
def GetIndustryData(id):
    sqlcmd="select * from industry_estimation_avg where industry ='%s'" %(id)
    try:
        a=pd.read_sql(sqlcmd,dbconn)
        return a
    except:
        print('invalid  input')
        return pd.DataFrame()    
 
    
#仔细筛选并入库----执行前提是industry_estimation_avg表已存在
#PE,TotalAssists参数暂时没有用到   
def stock_detail_select(PE,TotalAssists):
    #stock_select_to_sql(PE,TotalAssists)
    create_stock_detail_select_table()
    #sqlcmd="select * from all_stock_select ORDER BY pe" 
    #try:
    #a=pd.read_sql(sqlcmd,dbconn)
    a=ts.get_stock_basics()
    target = pd.DataFrame() #创建一个空的dataframe
    i=0
    for i in range(0,len(a)):     
        '''     
        #测试输出某一个行业的所有股票数据
        c=a.iloc[i,1] 
        print('****',c)
        if (c=='元器件'):
            print('get---->',a.iloc[i],i)
        if(c=='农药化肥'):
            print('get...2>',a.iloc[i],i)
            
        '''           

        '''      
        #测试输出数据库（行业平均值数据库）中指定行业的平均统计数据
        c='农药化肥'
        result=GetIndustryData(c)
        if not result.empty:
            #print(result) 
            print(result.iloc[0]['avg_pe'],result.iloc[0]['avg_pb'],result.iloc[0]['avg_rev'], \
                  result.iloc[0]['avg_profit'],result.iloc[0]['avg_gpr'],result.iloc[0]['avg_npr'])  
            #print(result.iloc[0,5],result.iloc[0,6],result.iloc[0,7], \
            #      result.iloc[0,8],result.iloc[0,9],result.iloc[0,10])  
        else:
           print('找不到行业名称...',i)
        '''
                      
        #正式逻辑代码   
        c=a.iloc[i,1] 
        result=GetIndustryData(c)
        if not result.empty:
            cnt=0;
            #print('#########',result.iloc[0],'pe:',a.iloc[i].pe)
            
            #此处判断条件可调，eg:判断条件中5/6的数据优于平均水平则认为值得研究,此处判断条件可操作范围较大，可以再讨论
            if a.iloc[i].pe<result.iloc[0]['avg_pe']:
                cnt+=1
            if a.iloc[i].pb<result.iloc[0]['avg_pb']:
                cnt+=1
            if a.iloc[i].rev>result.iloc[0]['avg_rev']:
                cnt+=1
            if a.iloc[i].gpr>result.iloc[0]['avg_gpr']:
                cnt+=1
            if a.iloc[i].profit>result.iloc[0]['avg_profit']:
                cnt+=1
            if a.iloc[i].npr>result.iloc[0]['avg_npr']:
                cnt+=1
           
            # 5/6的参数优于平均水平，则认为值得研究，保存入库
            if cnt>=6:
                print('find industry data,avg ok data num is:',cnt)
                target = target.append(a.iloc[i])
            #else:
            #     print('item ok num not enogh,which is:',cnt)
                  
        #else:
        #    print('找不到行业名称...',i)
               
        i=i+1
        
    print(target)    
    df_to_mysql('detail_stock_select',target) #筛选结果入库
    return target   

#to test run this fun
#stock_detail_select(300,50)
