# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 14:21:14 2018

@author: Administrator
"""

import tushare as ts
from SQL.sql import pymysql_connect
from SQL.sql import df_to_mysql

def create_k_table():
    db = pymysql_connect()
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
        df_to_mysql('anack_d_k_data',ts.get_k_data(index))
    elif mode == 'M':
        df_to_mysql('anack_m_k_data',ts.get_k_data(index,ktype='M'))
        
#------------------------------------------------------------------------------
#create_k_table()
#k_data('600660') 
#k_data('600660','M')   
