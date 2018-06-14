# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 01:44:29 2018

@author: yinchao
"""

 
# 远程数据库访问
import pandas as pd
import tushare as ts
import numpy as np
np.set_printoptions(suppress=True)
import Config


'''
list 对照表
0 总资产
1 净资产
2 流动资产
3 现金
4 一年内到期的长期负债
5 资产负债比
6 应收账款
7 预收账款
8 研发投入比
9 流动比率
10 资产周转率
11 存货周转率
12 现金增长净额
13 营收总额
14 支出总额
15 净利润
16 除非净利润
17 经营所得税

'''
def GetAllData(para, stock_id, year):
    '''
    返回一个series，
    '''
    cur = Config.Connect_sql()
    cmd = "select * from zichanfuzai where h79 = \'"+stock_id+"\' and h80 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
    p_len = len(para)
    
    info = []
    #此段用以实现result的字段填充，如需修改，请修改此处
    for s in range(p_len):
        info.append(-1)
    
    info[0] = float(data[37].replace(',',''))
    info[2] = float(data[16].replace(',',''))
    info[3] = float(data[0].replace(',',''))
    info[4] = float(data[12].replace(',',''))
    info[5] = float(data[65].replace(',',''))
    info[5] = round((info[5] / info[0]),2)
    info[6] = float(data[4].replace(',',''))
    
    cmd = "select * from Profit where h29 = \'"+stock_id+"\' and h30 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
#    print(data)
    info[13] = float(data[0].replace(',','')) #营收总额
    info[14] = float(data[2].replace(',','')) #费用总额
    info[15] = float(data[19].replace(',','')) #净利润
    info[17] = float(data[4].replace(',','')) #所得税

    cmd = "select * from cashFlow where h72 = \'"+stock_id+"\' and h73 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
#    print(data)
    info[12] = float(data[70].replace(',','')) #现金增长净额
#    info[3] = float(data[66].replace(',','')) #现金余额
        
    return pd.Series(info,index = para)










def GetSingleInfo(para, name, year):
    '''
    返回一个series，
    '''
    cur = Config.Connect_sql()
    cmd = "select * from anack_classify where name = \'"+name+"\';"
    cur.execute(cmd)
    result = cur.fetchall()
    id = result[0][0] 
    print(id)
    p_len = len(para)
    
    result = []
    #此段用以实现result的字段填充，如需修改，请修改此处
    for s in range(p_len):
        result.append(s)
        
    return pd.Series(result,index = para)

##############################################################################
#GetSingleInfo(parameter,'隆基股份',2016)
#print(company_id)
if __name__ =='__main__':
    parameter,company_id = Config.M1809_config() #获取配置信息
    s = GetAllData(parameter,company_id[0],2017)
    print(s)