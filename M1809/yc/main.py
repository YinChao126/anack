# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:26:21 2018

@author: yinchao
"""
import GetItemInfo
import Config

# 1. 初始化配置
parameter,company = Config.M1809_config() #获取配置信息 

# 2.形成标准表头和DataFrame块,按年份比对
import pandas as pd
header = parameter
para_len = len(header)
item1 = pd.Series(range(para_len),index = parameter)
item2 = pd.Series(range(para_len),index = parameter)
item2 = pd.Series(range(para_len),index = parameter)
result = pd.DataFrame([item1,item2])
result.to_csv('out.csv',encoding = 'utf-8')
#print(result)

# 3.数据获取与填充        
a = GetItemInfo.GetSingleInfo(parameter,'隆基股份',1)
#print(a)

