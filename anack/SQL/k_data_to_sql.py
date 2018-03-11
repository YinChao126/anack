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

def create_k_table():
    db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    cursor = db.cursor()
    
    sql1 = """CREATE TABLE IF NOT EXISTS `anack_d_k_data` (
`date`    varchar(255) DEFAULT NULL,
`open`    varchar(255) DEFAULT NULL,
`close`    varchar(255) DEFAULT NULL,
`high`    varchar(255) DEFAULT NULL,
`low`    varchar(255) DEFAULT NULL,
`volume`    varchar(255) DEFAULT NULL,
`code`    varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    
    sql2 = """CREATE TABLE IF NOT EXISTS `anack_m_k_data` (
`date`    varchar(255) DEFAULT NULL,
`open`    varchar(255) DEFAULT NULL,
`close`    varchar(255) DEFAULT NULL,
`high`    varchar(255) DEFAULT NULL,
`low`    varchar(255) DEFAULT NULL,
`volume`    varchar(255) DEFAULT NULL,
`code`    varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

    cursor.execute(sql1)
    cursor.execute(sql2)
    db.commit()
    cursor.close()
    db.close()
    
def k_data(index,mode='D'):

    if mode == 'D':
        sql.df_to_mysql('anack_d_k_data',ts.get_k_data(index))
    elif mode == 'M':
        sql.df_to_mysql('anack_m_k_data',ts.get_k_data(index,ktype='M'))
        
#------------------------------------------------------------------------------
#create_k_table()
#k_data('600660') 
#k_data('600660','M')   
