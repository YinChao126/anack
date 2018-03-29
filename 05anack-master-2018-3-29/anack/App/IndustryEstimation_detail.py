# -*- coding:utf-8 -*- 
import sys
sys.path.append("..")
import pandas as pd
#import pymysql
#from sqlalchemy import create_engine
import tushare as ts  

# =============================================================================
# from SQL.sql import pymysql_connect
# from SQL.sql import df_to_mysql
# =============================================================================



#from SQL.glo import get_value
#import requests
## 加上字符集参数，防止中文乱码

#确定输出表头信息：
#基础：总市值、平均市值、市盈率、市净率、收入增长、净利增长、毛利率、净利率
#扩展：资产负债率、市净率、市现率、市销率（需要根据财务报表获取）
#自定义：
#sql语句示例
#select 字段 from 表名 where 条件;
#eg:select * from student where sex='男' and age>20; //查询性别是男，并且年龄大于20岁的人。

#创建industry_estimation表头    
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


#行业平均值明细数据入库
def CreateTable():
    db = pymysql_connect()
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS industry_estimation_detail')
    estimation = """CREATE TABLE IF NOT EXISTS `industry_estimation_detail` (
                `code`    varchar(25) DEFAULT NULL,
                `name`    varchar(25) DEFAULT NULL,
                `industry`    varchar(25) DEFAULT NULL,
                `area`    varchar(25) DEFAULT NULL,
                `pe`    varchar(25) DEFAULT NULL,
                `outstanding`    varchar(25) DEFAULT NULL,
                `totals`    varchar(25) DEFAULT NULL,
                `totalAssets`    varchar(25) DEFAULT NULL,
                `liquidAssets`    varchar(25) DEFAULT NULL,
                `fixedAssets`    varchar(25) DEFAULT NULL,
                `reserved`    varchar(25) DEFAULT NULL,
                `reservedPerShare`    varchar(25) DEFAULT NULL,
                `esp`    varchar(25) DEFAULT NULL,
                `bvps`    varchar(25) DEFAULT NULL,
                `pb`    varchar(25) DEFAULT NULL,
                `timeToMarket`    varchar(25) DEFAULT NULL,
                `undp`    varchar(25) DEFAULT NULL,
                `perundp`    varchar(25) DEFAULT NULL,
                `rev`    varchar(25) DEFAULT NULL,
                `profit`    varchar(25) DEFAULT NULL,
                `gpr`    varchar(25) DEFAULT NULL,
                `npr`    varchar(25) DEFAULT NULL,
                `holders`    varchar(25) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(estimation)
    db.commit()
    cursor.close()
    db.close()    
       
def Estimation(): 
               
    result_df = pd.DataFrame(ts.get_stock_basics().values,columns = ts.get_stock_basics().columns)
    df_to_mysql('industry_estimation_detail',result_df)
    
    return result_df



#作用：查看行业平均值统计
#输入：行业名称
#输出：行业平均统计数
def industry_stat(industry):    
    df = pd.DataFrame(ts.get_stock_basics().values,columns = ts.get_stock_basics().columns)   
    pe_stat = df[df.industry == industry].drop(['name','industry','area'], axis = 1).astype('float')
# =============================================================================
#     print(pe_stat.dtypes)
# =============================================================================
    result_df = pe_stat.describe()
    print(result_df)
    return result_df


# =============================================================================
# #调试使用
# CreateTable()
# Estimation()
# industry_stat('通信设备')
# =============================================================================











