# -*- coding:utf-8 -*- 
import pymysql
from sqlalchemy import create_engine
import glo

glo._init()

host = 'localhost'
user = 'root'
passwd = '123456'
database = 'anack_sql'

glo.set_value('host',host)
glo.set_value('user',user)
glo.set_value('passwd',passwd)
glo.set_value('database',database)
glo.set_value('charset','utf8')

def df_to_mysql(table,df):
    connect = create_engine("mysql+pymysql://"+ user + ":"+ passwd + "@" + host + ":3306/" + database + "?charset=utf8")
    df.to_sql(name=table,con=connect,if_exists='append',index=False,index_label=False)