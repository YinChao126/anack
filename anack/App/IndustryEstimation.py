# -*- coding:utf-8 -*- 
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import tushare as ts  
#import requests
## 加上字符集参数，防止中文乱码

#确定输出表头信息：
#基础：总市值、平均市值、市盈率、市净率、收入增长、净利增长、毛利率、净利率
#扩展：资产负债率、市净率、市现率、市销率（需要根据财务报表获取）
#自定义：

#
hosts="localhost"
databases="anack_sql"
users="yinchao"
passwords="yc5315558"
  
dbconn=pymysql.connect(
  host="localhost",
  database="anack_sql",
  user="yinchao",
  password="yc5315558",
  port=3306,
  charset='utf8'
 )
      
clm = ['行业','年度','企业数量','总市值','平均市值','平均市盈率','平均市净率',
          '收入增长率','利润增长率','毛利率','净利润率']
headers = ['name','industry','totalAssets','pe','pb','rev','profit','gpr','npr']
#sql语句示例
#select 字段 from 表名 where 条件;
#eg:select * from student where sex='男' and age>20; //查询性别是男，并且年龄大于20岁的人。

#创建industry_estimation表头
def df_to_mysql(table,df):
    connect = create_engine("mysql+pymysql://"+ users + ":"+ passwords + "@" + hosts + ":3306/" + databases + "?charset=utf8")
    df.to_sql(name=table,con=connect,if_exists='append',index=False,index_label=False)
    
def CreateTable():
    db = pymysql.connect(host = hosts,user = users, password = passwords, 
                         database = databases,charset='utf8')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS industry_estimation') 
    estimation = """CREATE TABLE IF NOT EXISTS `industry_estimation` (
                `行业`    varchar(25) DEFAULT NULL,
                `年度`    varchar(25) DEFAULT NULL,
                `企业数量`    int(25) DEFAULT NULL,
                `总市值`    float(25) DEFAULT NULL,
                `平均市值`    float(25) DEFAULT NULL,
                `平均市盈率`    float(25) DEFAULT NULL,
                `平均市净率`    float(25) DEFAULT NULL,
                `收入增长率`    float(25) DEFAULT NULL,
                `利润增长率`    float(25) DEFAULT NULL,
                `毛利率`    float(25) DEFAULT NULL,
                `净利润率`    float(25) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cursor.execute(estimation)
    db.commit()
    cursor.close()
    db.close()    

#描述：输入ID或者股票名称，查看其在anack_classify数据库中所在的行业名
#输入：股票名称或者代码， 比如 "福耀玻璃"或者"600660"都可以
#输出：行业名称    比如：汽车制造
#异常处理：如果没有对应信息，输出invalid id input错误提示信息
def GetIndustryName(id):
    sqlcmd="select code,name,industry from anack_classify where code ='%s'" %(id)
    try:
        a=pd.read_sql(sqlcmd,dbconn)
        return a.iloc[0]['industry']
    except:
        sqlcmd="select code,name,industry from anack_classify where name ='%s'" %(id)
        try:
            a=pd.read_sql(sqlcmd,dbconn)
            return a.iloc[0]['industry']
        except:
            print('invalid id input')
            return 
 
#描述：输入行业名，计算出该行业的平均水平
#输入：数据库用户信息， 行业名， 年度     
def IndustryEstimation(dbconn,industry_name, year):
#    industry_name = '汽车制造'   #此处的var如何写到select语句中？   
    #sqlcmd="select code,name from anack_classify where '&var&' in industry"
#    sqlcmd="select code,name from anack_classify where industry ='汽车制造'"
#    print(sqlcmd)
#    print(type(sqlcmd))
    sqlcmd="select code,name from anack_classify where industry ='%s'" %(industry_name)
#    print(sqlcmd)
#    print(type(sqlcmd))
      
    #利用pandas 模块导入mysql数据
    a=pd.read_sql(sqlcmd,dbconn)
    #取前5行数据
    industry_id_list=a[:]
#    print(a)
    
    if len(a) == 0:
        print('行业名称输入错误，请重试')
    else: 
        a = ts.get_stock_basics()   #获取的数据
        tushare_data=a.loc[:,headers]
        target = pd.DataFrame(columns = ['行业','industry','totalAssets','pe','pb','rev','profit','gpr','npr']) #创建一个空的dataframe
        
        for names in industry_id_list.name:
            target = target.append(tushare_data.loc[tushare_data.name == names], ignore_index=True)
        #print(target)
        
        总市值 = 0
        企业数量 = 0
        for sums in target.totalAssets:
            总市值 += sums
            企业数量 += 1  
        print('行业名：' + industry_name)
        print('行业数量(家) = ' + str(企业数量))
        print('行业总市值(万) = ' + str(总市值))   
        平均市值 = 总市值/企业数量
        print('平均市值(万) = ' + str(平均市值)) 
        
        weight = []
        for each in target.totalAssets:
            weight.append(each/总市值)
        target['weight'] = weight    
        
        # 求平均市盈率
        平均市盈率  = 0
        num = 企业数量
        i = 0
        for each in target.pe:
            if each == 0 or each > 100: #排除异常情况
                num -= 1
            else:
                平均市盈率 += each * target.iloc[i]['weight']
            i+=1
        print('平均市盈率(%) = ' + str(平均市盈率))
        
        平均市净率 = 0
        num = 企业数量
        i = 0
        for each in target.pb:
            if each < 0 or each > 10: #排除异常情况
                num -= 1
            else:
                平均市净率 += each * target.iloc[i]['weight']
            i+=1
        print('平均市净率(%) = ' + str(平均市净率))
        
        收入增长率 = 0
        num = 企业数量
        i = 0
        for each in target.rev:
            if each < -1000 or each > 1000: #排除异常情况
                num -= 1
            else:
                收入增长率 += each * target.iloc[i]['weight']
            i+=1
        print('收入增长率(%) = '+str(收入增长率))
        
        利润增长率 = 0
        num = 企业数量
        i = 0
        for each in target.profit:
            if each < -1000 or each > 1000: #排除异常情况
                num -= 1
            else:
                利润增长率 += each * target.iloc[i]['weight']
            i+=1
        print('利润增长率(%) = ' + str(利润增长率))
        
        
        毛利率 = 0
        num = 企业数量
        i = 0
        for each in target.gpr:
            if each < -1000 or each > 1000: #排除异常情况
                num -= 1
            else:
                毛利率 += each * target.iloc[i]['weight']
            i+=1
        print('毛利率(%) = ' + str(毛利率))
        
        净利润率 = 0
        num = 企业数量
        i = 0
        for each in target.npr:
            if each < -1000 or each > 1000: #排除异常情况
                num -= 1
            else:
                净利润率 += each * target.iloc[i]['weight']
            i+=1
        print('净利润率(%) = ' + str(净利润率))
        data = {'行业':industry_name,'年度':str(year),'企业数量':企业数量,
                '总市值':round(总市值/10000,4),'平均市值':round(平均市值/10000,4),'平均市盈率':round(平均市盈率,2),
                '平均市净率':round(平均市净率,2),'收入增长率':round(收入增长率,2),'利润增长率':round(利润增长率,2),
                '毛利率':round(毛利率,2),'净利润率':round(净利润率,2)}      
        result_df = pd.DataFrame(data,columns = clm, index=["0"])
#        print(result_df)
        df_to_mysql('industry_estimation',result_df)
    return result_df
#IndustryEstimation(dbconn,'家电行业')
#print(GetIndustryName('福耀玻璃')) 
CreateTable()
IndustryEstimation(dbconn,GetIndustryName('宁沪高速'),2017)  
IndustryEstimation(dbconn,GetIndustryName('格力电器'),2017)   
IndustryEstimation(dbconn,GetIndustryName('福耀玻璃'),2017)   
IndustryEstimation(dbconn,GetIndustryName('隆基股份'),2017)   


#keys = ['name','age']
#values=[1,2]
#print(zip(keys,values))
#dic = dict('name'=1,'age'=2)
 
#d = pd.DataFrame(dic, columns=columns,index=['1'])
#d.ix[0]




#获取DataFrame中一类数据的标准语法：df.loc[df.property == value]
#example = pd.DataFrame()
#for content in tushare_data:
#    example = example.append(tushare_data.loc[tushare_data.industry == '汽车配件'])
#print(example)



#3. 总市值
#         name industry area       pe  outstanding  totals   totalAssets  \
#code                                                                      
#002226   江南化工     化工原料   安徽    72.51         9.11   12.49  5.143744e+05