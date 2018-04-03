# -*- coding:utf-8 -*- 
import pymysql
from sqlalchemy import create_engine
#import glo
#
#glo._init()

hosts = ' '
users = ' '
passwds = ' '
databases = ' '

#glo.set_value('host',host)
#glo.set_value('user',user)
#glo.set_value('passwd',passwd)
#glo.set_value('database',database)
#glo.set_value('charset','utf8')
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

def df_to_mysql(table,df):
    connect = connect_sql()
    df.to_sql(name=table,con=connect,if_exists='append',index=False,index_label=False)