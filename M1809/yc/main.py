# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:26:21 2018

@author: yinchao
"""
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
#from pylab import *  
#mpl.rcParams['font.sans-serif'] = ['SimHei'] 

import GetItemInfo
import Config


def Compare2Themself(target_id, start_year = 2010):   
    '''
    个股连续多年的对比分析
    输入：开始时间（可选）
    输出：DataFrame形式的结果
    '''
    result = []
    index_id = []
    for year in range(start_year, datetime.now().year):
        try:
            a = GetItemInfo.GetSingleItem(parameter,target_id,year)
            result.append(a)
            index_id.append(year)
        except:
            pass
    result = pd.DataFrame(result,index = index_id)
    result.to_csv('compare_self.csv')
    
    
    '''
    个股纵向对比绘图分析
    '''
    Pictrue1 = result.iloc[:,[0,1,3]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('元') #纵坐标标签
    plt.title('体量')
    
    Pictrue1 = result.iloc[:,[2]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('安全性检查')
    
    Pictrue1 = result.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('营运情况')
    
    Pictrue1 = result.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('现金情况')
    
    Pictrue1 = result.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('盈利质量')
    
    Pictrue1 = result.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('重要参数对比')
    plt.show()
    return result

#绘图分析

# 3. 同行业对比
def Compare2Industry(company):
    '''
    同行业的对比分析
    输入：行业对比
    输出：DataFrame形式的结果（最后一行是输入的平均水平）
    '''
    result = []
    index_id = []
    for individual in company:
        try:
            a = GetItemInfo.GetSingleItem(parameter,individual,datetime.now().year - 1)
            result.append(a)
            index_id.append(individual)
        except:
            pass
    result = pd.DataFrame(result,index = index_id)
    result.loc['avarage'] = result.apply(lambda x: x.sum()/len(index_id))
#    result.to_csv('compare_industry.csv')
    return result

# 4. 绘图分析 

def PlotAnalyse(data):
    '''
    个股纵向对比绘图分析
    '''
    Pictrue1 = data.iloc[:,[0,1,3]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('元') #纵坐标标签
    plt.title('体量')
    
    Pictrue1 = data.iloc[:,[2]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('安全性检查')
    
    Pictrue1 = data.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('营运情况')
    
    Pictrue1 = data.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('现金情况')
    
    Pictrue1 = data.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('盈利质量')
    
    Pictrue1 = data.iloc[:,[22,23,24]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('重要参数对比')
    plt.show()
    
    #手工分析结果
    
###############################################################################
if __name__ =='__main__':
    # 1. 初始化配置
    parameter,company = Config.M1809_config() #获取配置信息 
    a = Compare2Themself(company[0])
#    b = Compare2Industry(company)
#    b.to_csv('compare_industry.csv')
    
#    PlotAnalyse(a)
