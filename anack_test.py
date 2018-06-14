# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:12:12 2018

@author: 1707501
"""

import pymysql

conn = pymysql.connect(
        host = mysqlip,
        port = 3306,
        user = uusername,
        passwd = upassword,
        db = "test",
        charset = "utf8"
        )

cur = conn.cursor()
print("OK!")
# 查看库里的表
sql = "show tables;"
cur.execute(sql)
result = cur.fetchall()
print(result)

# 查询数据
sql = "select * from target limit 100;"
cur.execute(sql)
result = cur.fetchall()
print(result)