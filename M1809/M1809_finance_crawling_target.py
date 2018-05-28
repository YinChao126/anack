# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:13:36 2018

@author: 1707500
"""


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
    
data = data.pivot_table('close',index='code',columns=['date'],aggfunc='mean',fill_value=0)  

print(len(data['2016']))
print(len(data['2017']))
print(len(data['2018']))
print(len(stock_code_num))

df_final = pd.DataFrame({'code' : data.index,
                   '2016' : data['2016'],
                   '2017' : data['2017'],
                   '2018' : data['2018']
                   })

df_final['firstincrase'] = (df_final['2017'] - df_final['2016'])/df_final['2016']
df_final['secondincrase'] = (df_final['2018'] - df_final['2017'])/df_final['2018']

df_final[(df_final.firstincrase > 0.1) & (df_final.secondincrase > 0.1)]
    
df_final.to_csv('D:/999github/anack/M1809/target.csv',index =False)    