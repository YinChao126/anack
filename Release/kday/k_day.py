# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 20:46:24 2018
本模块用于实现k线数据的入库/本地存储
@author: yinchao
"""
# =============================================================================
# 1. sql账户配置
# 2. k_day数据更新
# 3. k_day数据提取
# =============================================================================

import get_price
import pymysql
import os
from sqlalchemy import create_engine


hosts = '47.98.216.118'
users = 'yc'
passwds = 'yc123!'
databases = 'test'
def pymysql_connect():
  return pymysql.connect(
  host=hosts,
  database=databases,
  user=users,
  password=passwds,
  port=3306,
  charset='utf8'
 )
def connect_sql():
    return create_engine("mysql+pymysql://"+ users + ":"+ passwds + "@" + hosts + ":3306/" + databases + "?charset=utf8")

def df_to_mysql(table, code_id, start_day = '19970101'):
    connect = connect_sql()
    df = get_price.get_period_k_day(code_id, start_day)
    df.to_sql(name=table,con=connect,if_exists='append')


def get_data_from_mysql(code_id):
    try:
        cmd = "select * from k_day2 where 股票代码 = \'"+code_id+"\';"
        print(cmd)
        conn = pymysql.connect(
            host = hosts,
            port = 3306,
            user = users,
            passwd = passwds,
            db = databases,
            charset = "utf8"
            )
        
        cur = conn.cursor()
        cur.execute(cmd)
        result = cur.fetchall()
        print(result)   #此处无法获取正确的数据
        return result
    except:
        print('get nothing')
        
# =============================================================================
# 
# =============================================================================
if __name__ == '__main__':
#    df_to_mysql('k_day2', '601012', '20180801')
    get_data_from_mysql('601012')