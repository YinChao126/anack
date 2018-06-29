# -*- coding: utf-8 -*-
'''
类名：M1809_finance_crawling（财务分析数据爬虫）
作者：徐抒田
日期：2018-5-20
描述：
1、获取财务数据模块，存入本地CSV;
2、后续盈利表里增加：市盈率、市净率、PEG；现金流量增加：当期现金流入；
3、后续版本增加表入库，增加数据更新，模块化
方法：使用TUSHARE
版本号：V0.1
'''
import pandas as pd
import tushare as ts
'''
盈利能力表

code,代码
name,名称
roe,净资产收益率(%)
net_profit_ratio,净利率(%)
gross_profit_rate,毛利率(%)
net_profits,净利润(万元)
esp,每股收益
business_income,营业收入(百万元)
bips,每股主营业务收入(元)
season,年+季度
'''
result_yinli = ts.get_profit_data(2018,1).loc[:,['code','name']]
print(result_yinli)
for i in [2016,2017,2018]:
    if i != 2018:
        for j in [1,2,3,4]:
            columns = ['code','name','roe'+str(i)+str(j),'net_profit_ratio'+str(i)+str(j),'gross_profit_rate'+str(i)+str(j),'net_profits'+str(i)+str(j),'esp'+str(i)+str(j),'business_income'+str(i)+str(j),'bips'+str(i)+str(j)]
            result_1 = pd.DataFrame(ts.get_profit_data(i,j).values,columns = columns)
            result_1 = result_1.drop(['name'],axis=1)
            result_yinli = pd.merge(result_yinli, result_1, on='code',how='left')
            print(str(i)+str(j))
            print(len(result_yinli))
    if i == 2018:
        j = 1
        columns = ['code','name','roe'+str(i)+str(j),'net_profit_ratio'+str(i)+str(j),'gross_profit_rate'+str(i)+str(j),'net_profits'+str(i)+str(j),'esp'+str(i)+str(j),'business_income'+str(i)+str(j),'bips'+str(i)+str(j)]
        result_1 = pd.DataFrame(ts.get_profit_data(i,j).values,columns = columns)    
        result_1 = result_1.drop(['name'],axis=1)
        result_yinli = pd.merge(result_yinli, result_1, on='code',how='left')
        print(str(i)+str(j))
        print(len(result_yinli))
result_yinli = result_yinli.drop_duplicates()        
result_yinli.to_csv('D:/999github/anack/M1809/result_yinli.csv',index =False)
'''
营运能力表

code,代码
name,名称
arturnover,应收账款周转率(次)
arturndays,应收账款周转天数(天)
inventory_turnover,存货周转率(次)
inventory_days,存货周转天数(天)
currentasset_turnover,流动资产周转率(次)
currentasset_days,流动资产周转天数(天)
season,年+季度
'''
result_yingyun = ts.get_operation_data(2018,1).loc[:,['code','name']]
for i in [2016,2017,2018]:
    if i != 2018:
        for j in [1,2,3,4]:
            columns = ['code','name','arturnover'+str(i)+str(j),'arturndays'+str(i)+str(j),'inventory_turnover'+str(i)+str(j),'inventory_days'+str(i)+str(j),'currentasset_turnover'+str(i)+str(j),'currentasset_days'+str(i)+str(j)]
            result_1 = pd.DataFrame(ts.get_operation_data(i,j).values,columns = columns)
            result_1 = result_1.drop(['name'],axis=1)
            result_yingyun = pd.merge(result_yingyun, result_1, on='code',how='left')
    if i == 2018:
        j = 1
        columns = ['code','name','arturnover'+str(i)+str(j),'arturndays'+str(i)+str(j),'inventory_turnover'+str(i)+str(j),'inventory_days'+str(i)+str(j),'currentasset_turnover'+str(i)+str(j),'currentasset_days'+str(i)+str(j)]
        result_1 = pd.DataFrame(ts.get_operation_data(i,j).values,columns = columns)
        result_1 = result_1.drop(['name'],axis=1)
        result_yingyun = pd.merge(result_yingyun, result_1, on='code',how='left')
result_yingyun = result_yingyun.drop_duplicates()
result_yingyun.to_csv('D:/999github/anack/M1809/result_yingyun.csv',index =False)
'''
成长能力表

code,代码
name,名称
mbrg,主营业务收入增长率(%)
nprg,净利润增长率(%)
nav,净资产增长率
targ,总资产增长率
epsg,每股收益增长率
seg,股东权益增长率
season,年+季度
'''
result_chengzhang = ts.get_growth_data(2018,1).loc[:,['code','name']]
for i in [2016,2017,2018]:
    if i != 2018:
        for j in [1,2,3,4]:
            columns = ['code','name','mbrg'+str(i)+str(j),'nprg'+str(i)+str(j),'nav'+str(i)+str(j),'targ'+str(i)+str(j),'epsg'+str(i)+str(j),'seg'+str(i)+str(j)]
            result_1 = pd.DataFrame(ts.get_growth_data(i,j).values,columns = columns)
            result_1 = result_1.drop(['name'],axis=1)
            result_chengzhang = pd.merge(result_chengzhang, result_1, on='code',how='left')
    if i == 2018:
        j = 1
        columns = ['code','name','mbrg'+str(i)+str(j),'nprg'+str(i)+str(j),'nav'+str(i)+str(j),'targ'+str(i)+str(j),'epsg'+str(i)+str(j),'seg'+str(i)+str(j)]
        result_1 = pd.DataFrame(ts.get_growth_data(i,j).values,columns = columns)
        result_1 = result_1.drop(['name'],axis=1)
        result_chengzhang = pd.merge(result_chengzhang, result_1, on='code',how='left')
result_chengzhang = result_chengzhang.drop_duplicates()
result_chengzhang.to_csv('D:/999github/anack/M1809/result_chengzhang.csv',index =False)
'''
偿债能力表

code,代码
name,名称
currentratio,流动比率
quickratio,速动比率
cashratio,现金比率
icratio,利息支付倍数
sheqratio,股东权益比率
adratio,股东权益增长率
season,年+季度
'''
result_changzhai = ts.get_debtpaying_data(2018,1).loc[:,['code','name']]
for i in [2016,2017,2018]:
    if i != 2018:
        for j in [1,2,3,4]:
            columns = ['code','name','currentratio'+str(i)+str(j),'quickratio'+str(i)+str(j),'cashratio'+str(i)+str(j),'icratio'+str(i)+str(j),'sheqratio'+str(i)+str(j),'adratio'+str(i)+str(j)]
            result_1 = pd.DataFrame(ts.get_debtpaying_data(i,j).values,columns = columns)
            result_1 = result_1.drop(['name'],axis=1)
            result_changzhai = pd.merge(result_changzhai, result_1, on='code',how='left')
    if i == 2018:
        j = 1
        columns = ['code','name','currentratio'+str(i)+str(j),'quickratio'+str(i)+str(j),'cashratio'+str(i)+str(j),'icratio'+str(i)+str(j),'sheqratio'+str(i)+str(j),'adratio'+str(i)+str(j)]
        result_1 = pd.DataFrame(ts.get_debtpaying_data(i,j).values,columns = columns)
        result_1 = result_1.drop(['name'],axis=1)
        result_changzhai = pd.merge(result_changzhai, result_1, on='code',how='left')
result_changzhai = result_changzhai.drop_duplicates()
result_changzhai.to_csv('D:/999github/anack/M1809/result_changzhai.csv',index =False)
'''
现金流量表

code,代码
name,名称
cf_sales,经营现金净流量对销售收入比率
rateofreturn,资产的经营现金流量回报率
cf_nm,经营现金净流量与净利润的比率
cf_liabilities,经营现金净流量对负债比率
cashflowratio,现金流量比率
season,年+季度
'''
result_xianjin = ts.get_cashflow_data(2018,1).loc[:,['code','name']]
for i in [2016,2017,2018]:
    if i != 2018:
        for j in [1,2,3,4]:
            columns = ['code','name','cf_sales'+str(i)+str(j),'rateofreturn'+str(i)+str(j),'cf_nm'+str(i)+str(j),'cf_liabilities'+str(i)+str(j),'cashflowratio'+str(i)+str(j)]
            result_1 = pd.DataFrame(ts.get_cashflow_data(i,j).values,columns = columns)
            result_1 = result_1.drop(['name'],axis=1)
            result_xianjin = pd.merge(result_xianjin, result_1, on='code',how='left')
    if i == 2018:
        j = 1
        columns = ['code','name','cf_sales'+str(i)+str(j),'rateofreturn'+str(i)+str(j),'cf_nm'+str(i)+str(j),'cf_liabilities'+str(i)+str(j),'cashflowratio'+str(i)+str(j)]
        result_1 = pd.DataFrame(ts.get_cashflow_data(i,j).values,columns = columns)
        result_1 = result_1.drop(['name'],axis=1)
        result_xianjin = pd.merge(result_xianjin, result_1, on='code',how='left')
result_xianjin = result_xianjin.drop_duplicates()
result_xianjin.to_csv('D:/999github/anack/M1809/result_xianjin.csv',index =False)

