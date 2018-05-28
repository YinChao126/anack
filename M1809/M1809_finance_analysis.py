# -*- coding: utf-8 -*-
'''
类名：M1809_finance_analysis（财务数据分析）
作者：徐抒田
日期：2018-5-28
描述：
1、初步调试机器学习方法

版本号：V0.1
'''


import pandas as pd

result_yinli = pd.read_csv('D:/999github/anack/M1809/result_yinli.csv')
result_yingyun = pd.read_csv('D:/999github/anack/M1809/result_yingyun.csv')
result_chengzhang = pd.read_csv('D:/999github/anack/M1809/result_chengzhang.csv')
result_changzhai = pd.read_csv('D:/999github/anack/M1809/result_changzhai.csv')
result_xianjin = pd.read_csv('D:/999github/anack/M1809/result_xianjin.csv')


result_target = pd.read_csv('D:/999github/anack/M1809/target.csv')



data = result_yinli
data = pd.merge(data, result_yingyun, on=['code','name'])
data = pd.merge(data, result_chengzhang, on=['code','name'])
data = pd.merge(data, result_changzhai, on=['code','name'])
data = pd.merge(data, result_xianjin, on=['code','name'])

