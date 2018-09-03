# -*- coding: utf-8 -*-
"""
Created on Tue July 24 08:26:21 2018

@author: guqiuyang
"""

import numpy as np
import CoreAnalyse
from matplotlib import pyplot as plt


# 绘制分组柱状图的函数
def groupedbarplot(ax, x_data, x_data_name, y_data_list, y_data_names, colors, x_label, y_label, title):
    '''
    绘制输出报告个分析指标的柱状图
    '''
    # 设置每一组柱状图的宽度
    total_width = 0.8
    # 设置每一个柱状图的宽度
    ind_width = total_width / len(y_data_list)
    # 计算每一个柱状图的中心偏移
    alteration = np.arange(-total_width / 2 + ind_width / 2, total_width / 2 + ind_width / 2, ind_width)

    # 分别绘制每一个柱状图
    for i in range(0, len(y_data_list)):
        # 横向散开绘制
        ax.bar(x_data + alteration[i], y_data_list[i], color=colors[i], label=y_data_names[i], width=ind_width)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x_data)
    ax.set_xticklabels(x_data_name)
    ax.set_title(title)
    ax.legend(loc='upper right')


# 4. 绘图分析
def PlotAnalyse(data):
    '''
    个股纵向对比绘图逻辑
    '''
    # 设置图片尺寸 20" x 15"
    plt.rc('figure', figsize=(14, 14))
    # 设置字体 14
    plt.rc('font', size=14)
    # 不显示网格
    plt.rc('axes', grid=False)
    # 设置背景颜色是白色
    plt.rc('axes', facecolor='white')
    # 显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 正常显示正负号
    plt.rcParams['axes.unicode_minus'] = False

    # 资产水平分析
    avg, last, level = CoreAnalyse.GetGrowth(data, 0)  # 总资产_复合增长率
    avg_, last_, level_ = CoreAnalyse.GetGrowth(data, 1)  # 净资产_复合增长率
    rate = CoreAnalyse.GetRate(data, 3, 0)  # 流动资产_总资产占比
    debt_avg, debt_last = CoreAnalyse.GetAverage(data, 2)  # 资产负债比_平均水平

    x1 = data.iloc[:, [0]].index.tolist()
    x2 = np.arange(4)
    x2_data_name = ['总资产增长率', '净资产增长率', '流动资产占比', '资产负债比']
    y1 = data.iloc[:, [0, 1, 3]]
    y2 = [[avg, avg_, rate, debt_avg], [last, last_, 0, debt_last]]

    _, axs = plt.subplots(2, 1, figsize=(14, 14))
    axs[0].plot(x1, y1, 'o-')
    axs[0].set_title('体量')
    axs[0].set_ylabel('元')
    axs[0].set_xlabel('年份')
    axs[0].legend(loc='upper left')

    groupedbarplot(axs[1]
                   , x_data=x2
                   , x_data_name=x2_data_name
                   , y_data_list=y2
                   , y_data_names=['长期', '去年']
                   , colors=['#539caf', '#7663b0']
                   , x_label='数据指标'
                   , y_label='增幅比例'
                   , title='资产水平分析')

    # 经营质量分析
    avg1, last1, _ = CoreAnalyse.GetGrowth(data, 8)  # 营业收入_复合增长率
    avg2, last2 = CoreAnalyse.GetAverage(data, 30)  # 毛利率
    avg3, last3, _ = CoreAnalyse.GetGrowth(data, 14)  # 除非净利润
    avg4, last4, _ = CoreAnalyse.GetGrowth(data, 10)  # 营业税
    rate = CoreAnalyse.GetRate(data, 12, 8)  # 现金与净资产的占比关系
    avg5, last5 = CoreAnalyse.GetAverage(data, 33) #股息率
    avg6, last6 = CoreAnalyse.GetAverage(data, 34) #分红率

    x1 = np.arange(3)
    x1_data_name = ['现金/净资产', '股息率', '分红率']
    x2 = np.arange(4)
    x2_data_name = ['营收增长率', '毛利率', '除非净利润增长率', '营业税增长率']
    y1 = [[0, avg5, avg6], [rate, last5, last6]]
    y2 = [[avg1, avg2, avg3, avg4], [last1, last2, last3, last4]]

    _, axs = plt.subplots(2, 1, figsize=(14, 14))
    groupedbarplot(axs[0]
                   , x_data=x1
                   , x_data_name=x1_data_name
                   , y_data_list=y1
                   , y_data_names=['长期', '去年']
                   , colors=['#539caf', '#7663b0']
                   , x_label='数据指标'
                   , y_label='增幅比例'
                   , title='经营质量分析')

    groupedbarplot(axs[1]
                   , x_data=x2
                   , x_data_name=x2_data_name
                   , y_data_list=y2
                   , y_data_names=['长期', '去年']
                   , colors=['#539caf', '#7663b0']
                   , x_label='数据指标'
                   , y_label='增幅比例'
                   , title='经营质量分析')

    # 现金流分析
    avg1, last1, _ = CoreAnalyse.GetGrowth(data, 16)  # 营业现金
    avg2, last2, _ = CoreAnalyse.GetGrowth(data, 20)  # 增加的现金
    avg3, last3, _ = CoreAnalyse.GetGrowth(data, 21)  # 期末现金
    rate = CoreAnalyse.GetRate(data, 21, 1)  # 现金与净资产的占比关系

    x1 = np.arange(4)
    x1_data_name = ['营业现金增长率', '现金增长净额', '期末现金', '现金与净资产的占比']
    y1 = [[avg1, avg2, avg3, 0], [last1, last2, last3, rate]]

    _, axs = plt.subplots(1, 1, figsize=(10, 7))
    groupedbarplot(axs
                   , x_data=x1
                   , x_data_name=x1_data_name
                   , y_data_list=y1
                   , y_data_names=['长期', '去年']
                   , colors=['#539caf', '#7663b0']
                   , x_label='数据指标'
                   , y_label='增幅比例'
                   , title='现金流分析')

    # 4.营运质量分析
    avg1, last1 = CoreAnalyse.GetAverage(data, 22)  # 流动比率
    avg2, last2 = CoreAnalyse.GetAverage(data, 23)  # 资产周转率
    avg3, last3 = CoreAnalyse.GetAverage(data, 24)  # 存货周转率

    x1 = np.arange(3)
    x1_data_name = ['流动比率', '资产周转率', '存货周转率']
    y1 = [[avg1, avg2, avg3], [last1, last2, last3]]

    _, axs = plt.subplots(1, 1, figsize=(10, 7))
    groupedbarplot(axs
                   , x_data=x1
                   , x_data_name=x1_data_name
                   , y_data_list=y1
                   , y_data_names=['长期', '去年']
                   , colors=['#539caf', '#7663b0']
                   , x_label='数据指标'
                   , y_label='增幅比例'
                   , title='营运参数分析')
    plt.show()