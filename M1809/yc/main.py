# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 00:26:21 2018

@author: yinchao
"""
import pandas as pd
from datetime import datetime
import time

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
#    result.to_csv('compare_self.csv')
#    
#    
#    '''
#    个股纵向对比绘图分析
#    '''
#    Pictrue1 = result.iloc[:,[0,1,3]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('元') #纵坐标标签
#    plt.title('体量')
#    
#    Pictrue1 = result.iloc[:,[2]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('') #纵坐标标签
#    plt.title('安全性检查')
#    
#    Pictrue1 = result.iloc[:,[22,23,24]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('') #纵坐标标签
#    plt.title('营运情况')
#    
#    Pictrue1 = result.iloc[:,[16,19,20]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('') #纵坐标标签
#    plt.title('现金情况')
#    
#    Pictrue1 = result.iloc[:,[12,11]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('') #纵坐标标签
#    plt.title('盈利质量')
#    
#    Pictrue1 = result.iloc[:,[26,30,31]]
#    Pictrue1.plot()
#    plt.xlabel('年份')  #横坐标标签
#    plt.ylabel('') #纵坐标标签
#    plt.title('重要参数对比')
#    plt.show()
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
    
    Pictrue1 = data.iloc[:,[16,19,20]]
    Pictrue1.plot()
    plt.xlabel('年份')  #横坐标标签
    plt.ylabel('') #纵坐标标签
    plt.title('现金情况')
    
    Pictrue1 = data.iloc[:,[12,9,11]]
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
    
def GetGrowth(data, column):
    '''
    辅助函数：获取年复合增长率和去年的增长率
    data:输入的dataframe
    column:第几列数据对比（查看GetItemInfo或者Parameter_list.txt
    '''
    years = len(data)
    a = data.iloc[-1][column] / data.iloc[0][column]
    avg_growth = pow(a, 1/(years-1)) - 1 #年均复合增长率
    last_growth = (data.iloc[-1][column]-data.iloc[-2][column]) / data.iloc[-2][column]
    
    diff = last_growth - avg_growth #0-10%低速增长， 10-20%中速增长
    if abs(diff) < 0.1:
        level = 0
    elif abs(diff) < 0.2:
        level = 1
    else:
        level = 2
    if diff < 0:
        level = level * -1
    return round(avg_growth,3), round(last_growth,3) , level

def GetAverage(data, column):
    '''
    辅助函数：获取年平均水平并与去年做比较
    '''
    years = len(data)
    sum_data = 0
    for s in range(years):
        sum_data = sum_data + data.iloc[s][column]
    avg = sum_data / years
    return round(avg,3), data.iloc[-1][column]
    
def GetRate(df, target, base):
    '''
    辅助函数，获取最近一年target参数占base参数的比率
    '''
    rate = df.iloc[-1][target] / df.iloc[-1][base]
    return round(rate,3)

def FileOutGrowth(fh, comment, avg, last, level):
    fh.write(comment)
    fh.write(str(avg) + ',' + str(last) + '\t')
    if avg > 0.2:
        fh.write('长期高速增长，')
    elif avg > 0.1:
        fh.write('长期中速增长，')
    elif avg > 0:
        fh.write('长期稳定发展，')
    elif avg > -0.1:
        fh.write('长期缓慢衰退')
    else:
        fh.write('长期加速衰退，')
        
    if level == 2:
        fh.write('去年加速增长\n')
    elif level == 1:
        fh.write('去年增速放缓\n')
    elif level == 0:
        fh.write('去年无明显变化\n')
    elif level == -1:
        fh.write('去年缓慢衰退\n')
    else:
        fh.write('去年加速衰退\n')
def FileOutAverage(fh, comment, avg, last):
    fh.write(comment + ':\t')
    fh.write(str(avg) + ',\t' + str(last) + '\n')
    
    diff = last -avg
    
    #手工分析结果   
def SelfAnalyse(fh, data, mode = 0):
    '''
    分析自身连续数年的财务报表
    增长定义： 0-7 低速增长， 8-15 中速增长  >15 高速增长
    '''
#    years = len(data) #一共几年的数据？  
#    sum_data = data.copy() #带sum的datafram
#    sum_data.loc['sum'] = sum_data.apply(lambda x: x.sum()) #增加一行求和，方便计算
    
    #1.资产分析
    fh.write('\n--------------------------------------------\n')
    fh.write('**同比结果**\n')
    fh.write('--------------------------------------------\n')
#    print('1. 资产水平分析')
    fh.write('1.资产水平分析：\n')
    avg, last, level = GetGrowth(data,0)    #总资产_复合增长率
#    print(avg, last)
    FileOutGrowth(fh, '总资产增长率:',avg,last,level)
    avg, last, level = GetGrowth(data,1)    #净资产_复合增长率
#    print(avg, last)
    FileOutGrowth(fh, '净资产增长率:',avg,last,level)
    rate = GetRate(data, 3, 0) #流动资产_总资产占比
    fh.write('流动资产占比：'+str(rate) + '(需增加行业对比)\n')
#    print(rate)
    debt_avg, debt_last = GetAverage(data,2) #资产负债比_平均水平
#    print(debt_avg, debt_last,'\n')
    fh.write('资产负债比：'+ str(debt_avg) + ',' + str(debt_last) + '(需增加行业对比)\t')
    if rate > 0.65:
        fh.write(',属于轻资产结构\n')
    elif rate > 0.4:
        fh.write(',属于正常水平\n')
    else:
        fh.write(',属于重资产结构\n')
    
    #2.营收分析
    fh.write('--------------------------------------------\n')    
#    print('经营质量分析')
    fh.write('2.经营质量分析：\n')
    avg, last, level = GetGrowth(data,8)        #营业收入_复合增长率
    FileOutGrowth(fh, '营收增长率:',avg,last,level)
#    print(avg, last)  
    avg, last = GetAverage(data,30)        #毛利率
    FileOutAverage(fh, '毛利率', avg, last)
#    print(avg, last) 
    avg, last, level = GetGrowth(data,14)        #除非净利润
    FileOutGrowth(fh, '除非净利润增长率:',avg,last,level)
#    print(avg, last)
    avg, last, level = GetGrowth(data,10)        #营业税
    FileOutGrowth(fh, '营业税增长率:',avg,last,level)
#    print(avg, last)
    rate = GetRate(data,12,8) #现金与净资产的占比关系
    fh.write('现金/净资产:\t'+str(rate*100)+'%\n')
#    print(rate, '\n')
    
    #3.现金流分析
    fh.write('--------------------------------------------\n') 
#    print('现金流分析')
    fh.write('3.现金流分析：\n')
    avg, last, level = GetGrowth(data,16)        #营业现金
    FileOutGrowth(fh, '营业现金增长率:',avg,last,level)
#    print(avg, last)    
    avg, last, level = GetGrowth(data,20)        #增加的现金
    FileOutGrowth(fh, '现金增长净额:',avg,last,level)
#    print(avg, last)    
    avg, last, level = GetGrowth(data,21)        #期末现金
    FileOutGrowth(fh, '期末现金:',avg,last,level)
#    print(avg, last)     
    rate = GetRate(data,21,1) #现金与净资产的占比关系
#    print(rate, '\n')
    
    #4.营运参数分析
    fh.write('--------------------------------------------\n') 
#    print('营运质量分析')
    fh.write('4.营运质量分析\n')
    avg, last = GetAverage(data,22) #流动比率
    FileOutAverage(fh, '流动比率', avg, last)
#    print(avg, last)
    avg, last = GetAverage(data,23) #资产周转率
    FileOutAverage(fh, '资产周转率', avg, last)
#    print(avg, last)
    avg, last = GetAverage(data,24) #存货周转率
    FileOutAverage(fh, '存货周转率', avg, last)
#    print(avg, last, '\n')



## 同行业对比

def CompareItem(fh, comment, data, column, pole = 1):
    '''
    辅助函数：用于实现column字段的同行业对比，并直接输出到文档
    pole: 1->高于对比值为良好）  其他任意值->低于对比值为良好
    '''
    fh.write(comment)
    t = data.iloc[1][column]
    c = data.iloc[2][column]
    a = data.iloc[-1][column]
    
    rate1 = round((t - c) / c,3)
    rate2 = round((t - a) / a,3)
    fh.write(str(rate1)+',\t'+str(rate2)+'\t')
    
    cnt = 0
    if pole == 1:
        if rate1 > 0:
            fh.write(' ')
            cnt = cnt + 1
        else:
            fh.write('劣于竞争对手，')
            cnt = cnt - 1
        if rate2 > 0:
            fh.write(' ')
            cnt = cnt + 1
        else:
            fh.write('劣于平均水平，')
            cnt = cnt - 1
    else:
        if rate1 < 0:
            fh.write(' ')
            cnt = cnt + 1
        else:
            fh.write('劣于竞争对手，')
            cnt = cnt - 1
        if rate2 < 0:
            fh.write(' ')
            cnt = cnt + 1
        else:
            fh.write('劣于平均水平.')
            cnt = cnt - 1
    if cnt < 0:
        fh.write('该指标异常，请格外注意！\n')
    else:
        fh.write('\n')
    
    
    return data.iloc[1][column], data.iloc[2][column], data.iloc[-1][column]

def CompareAnalyse(fh, data, mode = 0):
    fh.write('\n--------------------------------------------\n')
    fh.write('**同行业对比结果**\n')
    fh.write('--------------------------------------------\n')
    fh.write('1.资产类对比\n')
    CompareItem(fh, '总资产对比：', data, 1)
    CompareItem(fh, '净资产对比：', data, 1)
    CompareItem(fh, '资产负债比：', data, 2, 0)
    CompareItem(fh, '应收款：', data, 5,0)
    CompareItem(fh, '预收款：', data, 6)
    CompareItem(fh, '存货：', data, 7)
    
    fh.write('--------------------------------------------\n') 
    fh.write('2.经营类对比\n')
    CompareItem(fh, '营收', data, 8)
    CompareItem(fh, '营业外收入', data, 12, 0)
    CompareItem(fh, '除非净利润：', data, 14)
    
    fh.write('--------------------------------------------\n') 
    fh.write('3.现金流对比\n')
    CompareItem(fh, '经营净额：', data, 16)
    CompareItem(fh, '汇率影响：', data, 19, 0)
    CompareItem(fh, '现金净增加额：', data, 20)
    CompareItem(fh, '期末现金余额：', data, 21)
    
    fh.write('--------------------------------------------\n') 
    fh.write('4.营运质量对比\n')
    CompareItem(fh, '流动比率：', data, 22)
    CompareItem(fh, '资产周转率：', data, 23)
    CompareItem(fh, '存货周转率：', data, 24)
    
    fh.write('--------------------------------------------\n') 
    fh.write('5.重要指标对比\n')
    CompareItem(fh, '估值比：', data, 25, 0)
    CompareItem(fh, '市盈率：', data, 26, 0)
    CompareItem(fh, '市净率：', data, 27, 0)
    CompareItem(fh, 'ROE：', data, 28, 0)
    CompareItem(fh, '毛利率：', data, 30)
    CompareItem(fh, '营收增长率：', data, 31)
    CompareItem(fh, '除非净利润增长率：', data, 32)

def ComprehensiveResult(fh):
    '''
    综合结论输出：自动输出，手工修正（不要忘记了）
    '''
    fh.write('\n--------------------------------------------\n')
    fh.write('**综合结论与评级报告**\n')
    fh.write('--------------------------------------------\n')
    
## API接口函数    
def Analyse(self_data, total_data):
    '''
    API函数
    直接根据配置信息，从云端获取数据，填充字段，输出原始csv文件，txt分析文件，绘图
    '''
    s = time.strftime("_%Y%m%d")
    s1 = time.strftime("%Y-%m-%d")
    file_name = 'output/' + '诊断报告_' + company[0] + s + '.txt'
    with open(file_name, 'w') as fh:
        fh.write('版本号：V1.0\n')
        fh.write('诊断时间：'+ s1 +'\n')
        fh.write('诊断个股：'+ '隆基股份-' + '601012' + '\n')
        SelfAnalyse(fh, self_data)
        CompareAnalyse(fh, total_data)
        ComprehensiveResult(fh)

###############################################################################
if __name__ =='__main__':
    # 1. 初始化配置
    parameter,company = Config.M1809_config() #获取配置信息 
    a = Compare2Themself('601012')
    a.to_csv('compare_self.csv', encoding = 'gbk')
    b = Compare2Industry(company)
    b.to_csv('compare_industry.csv', encoding = 'gbk')
    Analyse(a,b)
    
    
#    PlotAnalyse(a)
