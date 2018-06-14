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
0   总资产
1   净资产
2   资产负债比
3   流动资产
4   一年内到期的长期负债
5   应收账款
6   预收账款
7   存货

8   营业收入
9   营业成本
10  营业税金及附加
11  财务费用
12  营业外收入
13  净利润
14  除非净利润
15  每股收益

16  经营净额
17  投资净额
18  筹资净额
19  汇率影响
20  现金净增加额
21  期末现金余额

22  流动比率
23  资产周转率
24  存货周转率

25  总市值/净资
26  市盈率
27  市净率
28  名义净资产收益率
29  真实净资产收益率
30  毛利率
31  营收增长率
32  除非净利润增长率
'''
def GetSingleItem(para, stock_id, year):
    '''
    返回一个series，
    '''
    
    #
    p_len = len(para) #自动计算参数列表长度
    info = []   #实际待填充的字段，最后用于生成Series的value部分
  
    for s in range(p_len):
        info.append(-1) #初始化为-1，代表还未填充
        
    cur = Config.Connect_sql()
    
    #资产负债表中查询与填充
    cmd = "select * from zichanfuzai where h79 = \'"+stock_id+"\' and h80 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
    
    info[0] = float(data[37].replace(',','')) #总资产
    debt = float(data[65].replace(',','')) #总负债
    info[2] = round((debt / info[0]),2)     #资产负债比
    info[1] = info[0] - debt #净资产
    info[3] = float(data[16].replace(',','')) #流动资产
    info[4] = float(data[52].replace(',','')) #一年内到期的长期负债
    info[5] = float(data[4].replace(',',''))  #应收账款
    info[6] = float(data[42].replace(',',''))  #预收账款
    info[7] = float(data[10].replace(',',''))  #存货
    
    #利润表查询与填充
    cmd = "select * from Profit where h29 = \'"+stock_id+"\' and h30 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
#    print(data)
    info[8] = float(data[1].replace(',','')) 
    info[9] = float(data[3].replace(',',''))  
    

    #现金流量表查询与填充
    cmd = "select * from cashFlow where h72 = \'"+stock_id+"\' and h73 = \'2017-12-31\';"
    cur.execute(cmd)
    result = cur.fetchall()
    data = result[0] #获得资产负债表信息
    
        
    #指标计算，可能还需要获取额外的数据如实时股价等。。。
    info[8] = float(data[1].replace(',','')) 
    
    
    return pd.Series(info,index = para)


###############################################################################
if __name__ =='__main__':
    parameter,company_id = Config.M1809_config() #获取配置信息
    s = GetSingleItem(parameter,company_id[0],2017)
    print(s)