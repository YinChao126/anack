# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:21:14 2018

@author: Administrator
"""

import pandas as pd
import pymysql

import tushare as ts
import glo
import sql

#------------------------------------------------------------------------------
hosts = glo.get_value('host')
users = glo.get_value('user')
passwords = glo.get_value('passwd')
databases = glo.get_value('database')
#------------------------------------------------------------------------------

def create_classify_table():
    db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS anack_classify') 
    classify = """CREATE TABLE IF NOT EXISTS `anack_classify` (
                `code`    varchar(255) DEFAULT NULL,
                `name`    varchar(255) DEFAULT NULL,
                `industry`    varchar(255) DEFAULT NULL,
                `area`    varchar(255) DEFAULT NULL,
                `sz50`    varchar(255) DEFAULT NULL,
                `hs300_weight`    FLOAT(10) DEFAULT NULL,
                `zz500_weight`    FLOAT(10) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(classify)
    db.commit()
    cursor.close()
    db.close()
    
def classify_info_to_sql():
    create_classify_table()    
    
    a = ts.get_industry_classified()
    a.columns = ['code', 'name', 'industry']
    b = ts.get_area_classified()
    c = ts.get_sz50s()
    c = c.iloc[:,1::]
    c['sz50'] = '1'
    d = ts.get_hs300s()
    d = d.iloc[:,1::]
    d.columns = ['code','name','hs300_weight']
    e = ts.get_zz500s()
    e = e.iloc[:,1::]
    e.columns = ['code','name','zz500_weight']
    result = pd.merge(a, b, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=True,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    result = pd.merge(result, c, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=True,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    result = pd.merge(result, d, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=True,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    result = pd.merge(result, e, how='left', on=None, left_on=None, right_on=None,
             left_index=False, right_index=False, sort=True,
             suffixes=('_x', '_y'), copy=True, indicator=False)
    sql.df_to_mysql('anack_classify',result)
    
#    -------------------------------------------------------------
#classify_info_to_sql()#每次调用都会更新
