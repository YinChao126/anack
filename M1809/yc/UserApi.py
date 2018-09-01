# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 19:22:58 2018

@author: yinchao
"""
import PlotAnalyse
import CoreAnalyse
import Config

def Init(company_id_list, data_src = 'CSV'):
    '''
    初始化配置函数
    company_id_list:待考察的id列表（1个到n个，eg: ['000651','00124','600660']
    data_src: 'SQL'数据来源是数据库， 'CSV'数据来源是读文件
    '''
    Config.M1809_config(company_id_list, data_src)

def GetData(file_switch = 'ON'):
    '''
    获取财务原始数据
    file_switch: 'ON'结果输出到文本（默认） 'OFF'原始结果不输出
    返回值： a->自身对比原始结果 b->同行业对比结果（归一化处理）
    备注：a,b两个返回值原封不动交给Analyse函数进行分析即可
    '''
    a = CoreAnalyse.Compare2Themself(Config.company_id_list[0])    #自身对比
    b1= CoreAnalyse.Compare2Industry(Config.company_id_list)    #同行业对比
    b = CoreAnalyse.data_normalize(b1)  #归一化的同行业对比
    if file_switch == 'ON':
        a.to_csv('../output/compare_self.csv', encoding= 'gbk') 
        b1.to_csv('../output/compare_industry.csv', encoding = 'gbk')
        b.to_csv('../output/normalize.csv', encoding = 'gbk') 
    return a, b

def Analyse(a,b):
    '''
    对比分析，并输出
    1. ../output/文件夹下会生成诊断报告
    2. 控制台输出对比图像（之后可以考虑保存图片）
    '''
    CoreAnalyse.Analyse(a,b)
    PlotAnalyse.PlotAnalyse(a)
    
    
if __name__ =='__main__':
    id_list = ['000651', '000333', '600690']
    para,company = Init(id_list,'CSV')
    a = CoreAnalyse.Compare2Themself(company)