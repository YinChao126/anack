# -*- coding: utf-8 -*-
'''
类名：M1809_finance_crawling_target（财务分析数据爬虫）
作者：徐抒田
日期：2018-5-28
描述：
1、筛选17年和18年复合增长率大于10%的股票作为TARGET
2、选取close为当日的股价
3、年股价计算（12个月均价）
版本号：V0.1
'''

import tushare as ts
import pandas as pd

stock_code_num = ts.get_profit_data(2018,1)['code'].tolist()

a=[]
data = pd.DataFrame()
for j in stock_code_num:
    try:    
        df = ts.get_k_data(j,ktype = 'M')[['date','close','code']]
        for i in df['date']:
            a.append(i[0:4])
        df['date'] = a
        a=[]
        df = pd.concat([df[df.date == '2016'],df[df.date == '2017'],df[df.date == '2018']])
        data = pd.concat([data,df])
        print(j)
    except:
        stock_code_num.remove(j)
        print('error!')
        print(j)
    
data_mean = data.pivot_table('close',index='code',columns=['date'],aggfunc='mean',fill_value=0)  
data_var = data.pivot_table('close',index='code',columns=['date'],aggfunc='std',fill_value=0)  


df_final = pd.DataFrame({'code' : data_mean.index,
                   'yiliu_mean' : data_mean['2016'],
                   'yiqi_mean' : data_mean['2017'],
                   'yiba_mean' : data_mean['2018'],
                   'yiliu_var' : data_var['2016'],
                   'yiqi_var' : data_var['2017'],
                   'yiba_var' : data_var['2018']
                   })
    
df_final = df_final[df_final.yiliu_mean != 0]
df_final['firstincrase'] = (df_final['yiqi_mean'] - df_final['yiliu_mean'])/df_final['yiliu_mean']
df_final['secondincrase'] = (df_final['yiba_mean'] - df_final['yiqi_mean'])/df_final['yiba_mean']

df_final[(df_final.firstincrase > 0.1) & (df_final.secondincrase > 0.1)& (df_final.yiliu_var < 15)& (df_final.yiqi_var < 15)& (df_final.yiba_var < 15)]
df_final.to_csv('D:/999github/anack/M1809/target.csv',index =False)
