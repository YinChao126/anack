# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:21:14 2018

@author: Administrator
"""

import pandas as pd
import pymysql

import tushare as ts
from SQL.sql import pymysql_connect
from SQL.sql import df_to_mysql
#    
def create_classify_table():
    db = pymysql_connect()
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS anack_macro_data') 
    macro = """CREATE TABLE IF NOT EXISTS `anack_macro_data` (
                `month`    varchar(255) DEFAULT NULL,
                `cpi`    varchar(16) DEFAULT NULL,
                `ppi`    varchar(16) DEFAULT NULL,
                `m2`    varchar(16) DEFAULT NULL,
                `m1`    varchar(16) DEFAULT NULL,
                `m0`    varchar(16) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(macro)
    db.commit()
    cursor.close()
    db.close()
    
def macro_info_to_sql():
    create_classify_table()    
    
    a = ts.get_cpi()
    b = ts.get_ppi()
    c = ts.get_money_supply()
    c = c.iloc[:,[0,1,3,5]]
    b = b.iloc[:,[0,2]]
    result = pd.merge(a, b, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=False,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    result = pd.merge(result, c, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=False,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    df_to_mysql('anack_macro_data',result)
    
    
#    -------------------------------------------------------------
macro_info_to_sql() #每次调用都会更新