# This tools used to update file "感兴趣的个股列表.txt"
# syntax:
# first line:   update time:<date>
# seconde line: total:<number of items>
# other line:   <id>/t<name>  
#
# eg:
# update time:2018/3/4
# total:33
# 000651  格力电器
# ... other 32 items

# -*- coding: utf-8 -*-
import pandas as pd

#------------------------------------------------------------------------------
# change here
# 用于筛选个股的各项参数
# 筛股逻辑：
# 1. 初筛：调用ts.get_stock_basics()即可
# 动态市盈率60以下，日成交量大于1亿，市值大于100亿，收入同比、净利润率为正
# 2. 仔细筛查：同行比对排名前5，个股历年同比连续增长
# 同行业对比（从大到小排列）：pe倒数前五，毛利率顺数前5。pb排名靠后，利润同比、
# 收入同比排名靠前
# 自己同比：现金流为正、利润同比有增长
# 
parameter = []
pe = 50
pb = 
and so on ...
#------------------------------------------------------------------------------

def update_interest_list():
  '''
  根据指定的逻辑遍历A股，找出符合条件的个股，更新“感兴趣的个股列表.txt”文件，
  同时以列表形式返回
  '''
  
  return interest_list
  
def get_interest_list():
    '''
    解析"感兴趣的个股列表.txt",返回list类型的数据供其他模块使用
    '''
    list_id = []
    with open('yourpath/感兴趣的个股列表.txt','r') as fh:
        s = fh.readline()   #获取更新时间
        s = fh.readline()   #获取目标长度  
        
        lines = fh.readlines()  #获取目标内容
    for s in lines:
        code = s[:6]
        list_id.append(code)    
    list_id.sort()
    return list_id  