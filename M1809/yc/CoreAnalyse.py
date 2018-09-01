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
import txttoexcel
import PlotAnalyse

## API接口函数
def Analyse(self_data, total_data):
    '''
    API函数，用户可调用
    直接根据配置信息，从云端获取数据，填充字段，输出txt分析文件，并得到统计分数
    '''
    s = time.strftime("_%Y%m%d")
    s1 = time.strftime("%Y-%m-%d")
    file_name = '../output/' + '诊断报告_' + Config.company_id_list[0] + s + '.txt'#形成文件名
    with open(file_name, 'w') as fh:
        fh.write('版本号：V1.0\n')
        fh.write('诊断时间：'+ s1 +'\n')
        fh.write('诊断个股：'+ Config.company_id_list[0] + '\n')
        SelfAnalyse(fh, self_data) #同比分析并写文件
        CompareAnalyse(fh, total_data) #同行业对比分析并写文件
        ComprehensiveResult(fh) #手动分析部分（不用关心）

    # write excel
    file_list = txttoexcel.read_txt(file_name)
    txttoexcel.generate_excel(file_list,file_name)

#手工分析结果
def SelfAnalyse(fh, data):
    '''
    同比分析的逻辑实现
    分析自身从2010年开始到去年的财务报表
    进行平均年复合增长率和去年增长率的统计，并比较增速幅度
    输入： fh->文件句柄，用于写txt文件
            data->同比的数据，默认从2010年开始，到去年截至，都是年报数据（DataFrame)
    '''

    #1.资产分析
    print('start self analyse')
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
    avg, last = GetAverage(data,33) #股息率
    FileOutAverage(fh, '股息率', avg, last)
    avg, last = GetAverage(data,34) #分红率
    FileOutAverage(fh, '分红率', avg, last)

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

def CompareAnalyse(fh, data):
    '''
    同行业对比分析的逻辑实现
    输入： fh->文件句柄，用于写txt文件
            data->同行业的数据（DataFrame)
    '''
    print('start compare analyse')
    fh.write('\n--------------------------------------------\n')
    fh.write('**同行业对比结果与评级输出**\n')
    fh.write('--------------------------------------------\n')
    fh.write('1.资产类对比\n')
    score = 0 #初始分数100分
    score += CompareItem(fh, '总资产对比：', data, 0)
    score += CompareItem(fh, '净资产对比：', data, 1)
    score += CompareItem(fh, '资产负债比：', data, 2, -1)
    score += CompareItem(fh, '应收款：', data, 5,-1)
    score += CompareItem(fh, '预收款：', data, 6)
    score += CompareItem(fh, '存货：', data, 7)

    fh.write('--------------------------------------------\n')
    fh.write('2.经营类对比\n')
    score += CompareItem(fh, '营收', data, 8)
    score += CompareItem(fh, '营业外收入', data, 12, -1) #没意义啊
    score += CompareItem(fh, '除非净利润：', data, 14)
    score += CompareItem(fh, '股息率', data, 33)
    score += CompareItem(fh, '分红率', data, 34)

    fh.write('--------------------------------------------\n')
    fh.write('3.现金流对比\n')
    score += CompareItem(fh, '经营净额：', data, 16)
    score += CompareItem(fh, '汇率影响：', data, 19, -1)
    score += CompareItem(fh, '现金净增加额：', data, 20)
    score += CompareItem(fh, '期末现金余额：', data, 21)

    fh.write('--------------------------------------------\n')
    fh.write('4.营运质量对比\n')
    score += CompareItem(fh, '流动比率：', data, 22)
    score += CompareItem(fh, '资产周转率：', data, 23)
    score += CompareItem(fh, '存货周转率：', data, 24)
    #自动评级结论在此处输出
    score += CompareItem(fh, 'ROE：', data, 28)
    score += CompareItem(fh, '毛利率：', data, 30)
    score += CompareItem(fh, '营收增长率：', data, 31)
    score += CompareItem(fh, '除非净利润增长率：', data, 32)
    print(score)
    stra = '---->>|同行业对比得分：\t' + str(score) + '\t|<----\n'
    fh.write(stra)
    fh.write('\n')


    fh.write('--------------------------------------------\n')
    fh.write('--------------------------------------------\n')
    fh.write('重要指标对比\n')
    CompareItem(fh, '估值比：', data, 25, -1)
    CompareItem(fh, '市盈率：', data, 26, -1)
    CompareItem(fh, '市净率：', data, 27, -1)


def ComprehensiveResult(fh):
    '''
    综合结论输出：自动输出，手工修正（不要忘记了）
    '''
    fh.write('\n--------------------------------------------\n')
    fh.write('**综合结论与评级报告**\n')
    fh.write('--------------------------------------------\n')


## 以下均为辅助函数，用户不用关心
###############################################################################
def Compare2Themself(target_id, start_year = 2010):
    '''
    辅助函数：获取target_id从2010年开始直到去年的财务数据，形成DataFrame并输出（用户不必关心）
    输入：开始时间（可选）
    输出：DataFrame形式的结果
    '''
    result = []
    index_id = []
    print('get self report data...')
    for year in range(start_year, datetime.now().year):
        try:
            if Config.data_src == 'SQL':
                a = GetItemInfo.GetSingleItem(target_id,year)
            elif Config.data_src == 'CSV':
                a = GetItemInfo.GetSingleLocalItem(target_id,year)
            else:
                print('compare failure. bad parameter')
                return
            
            result.append(a)
            index_id.append(year)
        except:
            print('pass ', str(year))
            pass
    result = pd.DataFrame(result,index = index_id)
    return result

def Compare2Industry(company):
    '''
    辅助函数：获取配置文件中所指代公司的上一年年报数据，用于同行业对比（用户不必关心）
    输入：行业对比
    输出：DataFrame形式的结果（最后一行是输入的平均水平）
    '''
    result = []
    index_id = []
    print('get compare report data...')
    for individual in company:
        try:
            if Config.data_src == 'SQL':
                a = GetItemInfo.GetSingleItem(individual,datetime.now().year - 1)
            elif Config.data_src == 'CSV':
                a = GetItemInfo.GetSingleLocalItem(individual,datetime.now().year - 1)
            else:
                print('compare failure. bad parameter')
                return
            
            result.append(a)
            index_id.append(individual)
        except:
            print('drop ', individual,'\'s report')
            pass
    result = pd.DataFrame(result,index = index_id)
    result.loc['avarage'] = result.apply(lambda x: x.sum()/len(index_id))
#    result.to_csv('compare_industry.csv')
    return result

def GetGrowth(data, column):
    '''
    辅助函数：程式化获取年复合增长率和去年的增长率
    data:输入的dataframe
    column:第几列数据对比（查看GetItemInfo或者Parameter_list.txt
    返回值： 历史平均增速， 去年增速， 增速等级(-2,-1,0,1,2)衰退->增长
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
    辅助函数：程式化获取年平均水平并与去年做比较
    '''
    years = len(data)
    sum_data = 0
    for s in range(years):
        sum_data = sum_data + data.iloc[s][column]
    avg = sum_data / years
    return round(avg,3), data.iloc[-1][column]

def GetRate(df, target, base):
    '''
    辅助函数，程式化获取最近一年target参数占base参数的比率
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


## 同行业对比

def CompareItem(fh, comment, data, column, pole = 1):
    '''
    辅助函数：用于实现column字段的同行业对比，并直接输出到文档
    pole: 1 -> 高于对比值为良好）  -1 -> 低于对比值为良好
    '''
    score = 5 #初始单项分数为5分
    fh.write(comment)
    t = data.iloc[0][column]
    c = data.iloc[1][column]
    a = data.iloc[-1][column]
    if c == 0 or a == 0:
        print('column = ', column,'一栏除数为0，特殊处理',t,c,a)
        return score
    else:
        rate1 = round((t - c) / c,3)
        rate2 = round((t - a) / a,3)
        fh.write(str(rate1)+',\t'+str(rate2)+'\t')

    cnt = 0
    r1 = rate1 * pole
    r2 = rate2 * pole

    if r1 < -0.01:
        fh.write('劣于竞争对手，')
        cnt = cnt - 1
        score -= 2
    else:
        fh.write(' ')
        cnt = cnt + 1
    if r2 < -0.01:
        fh.write('劣于平均水平,')
        cnt = cnt - 1
        score -= 3
    else:
        fh.write(' ')
        cnt = cnt + 1

    if cnt < 0:
        fh.write('该指标异常，请格外注意！\n')
    else:
        fh.write('\n')


    return score



def data_normalize(data):
    '''
    辅助函数：同行业输出数据归一化（用户不用管）
    行业对比前必须把数据归一化处理，否则没法同行业比较
    '''
    head = data.columns #获取表头
    tag = head[0]
    #total_assets = data['总资产']
    total_assets = data[tag]

    tag = head[8]
    #total_sale = data['营业收入']
    total_sale = data[tag]
    result = pd.DataFrame(total_assets) #形成一个新的DataFrame，之后再添加列

    tag = head[1]#净资产
    opt = data[tag]
    result[tag] = opt

    tag = head[2]#资产负债比
    opt = data[tag]
    result[tag] = opt

    tag = head[3]#流动资产
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[4]#一年内到期的长期负债
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[5]#应收款
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[6]#预收款
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[7]#存货
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[8]#营业收入
    opt = data[tag]
    opt = round(opt / total_assets, 3)
    result[tag] = opt

    tag = head[9]#营业成本
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[10]#营业税金及附加
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[11]#财务费用
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[12]#营业外收入
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[13]#净利润
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[14]#除非净利润
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[15]#营业税金及附加
    result[tag] = opt

    tag = head[16]#经营净额
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[17]#投资净额
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[18]#筹资净额
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[19]#汇率影响
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[20]#现金净增加额
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[21]#期末现金净额
    opt = data[tag]
    opt = round(opt / total_sale, 3)
    result[tag] = opt

    tag = head[22]#流动比率
    opt = data[tag]
    result[tag] = opt

    tag = head[23]#资产周转率
    opt = data[tag]
    result[tag] = opt

    tag = head[24]#存货周转率
    opt = data[tag]
    result[tag] = opt

    tag = head[25]#溢价比
    opt = data[tag]
    result[tag] = opt

    tag = head[26]#市盈率
    opt = data[tag]
    result[tag] = opt

    tag = head[27]#市净率
    opt = data[tag]
    result[tag] = opt

    tag = head[28]#名义净资产收益率
    opt = data[tag]
    result[tag] = opt

    tag = head[29]#实际净资产收益率
    opt = data[tag]
    result[tag] = opt

    tag = head[30]#毛利率
    opt = data[tag]
    result[tag] = opt

    tag = head[31]#营收增长率
    opt = data[tag]
    result[tag] = opt

    tag = head[32]#除非净利润增长率
    opt = data[tag]
    result[tag] = opt

    tag = head[33]#股息率
    opt = data[tag]
    result[tag] = opt

    tag = head[34]#分红率
    opt = data[tag]
    result[tag] = opt
    return result
###############################################################################
if __name__ =='__main__':
    # 1. 初始化配置
    id_list = ['000651', '000333', '600690']
    Config.M1809_config(id_list,'CSV')
    
    # 2. 获取数据
    a = Compare2Themself(Config.company_id_list[0])    #自身对比
    a.to_csv('../output/compare_self.csv', encoding= 'gbk') 
    b1= Compare2Industry(Config.company_id_list)    #同行业对比
    b1.to_csv('../output/compare_industry.csv', encoding = 'gbk')
    b = data_normalize(b1)  #归一化的同行业对比
    b.to_csv('../output/normalize.csv', encoding = 'gbk') 
    
    # 3. 分析并保存图片
    Analyse(a,b)
    PlotAnalyse.PlotAnalyse(a)
