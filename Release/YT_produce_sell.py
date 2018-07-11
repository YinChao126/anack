# 作者：尹超
# 更新日期：2018-1-6
# 版本号：V0.3
# 描述：本程序用于宇通客车产销快报数据的分析
# 内容：系统初始化、数据读入、数据处理、绘图、统计分析
# 备注：
# 1. 务必保持工程下有连续的xlsx文件，并确保文件名有效
# 2. 确保year/lastmonth和文件一致，否则会出现错误
# 3. 暂时只能靠手工将pdf文件转成xlsx文件，以后可以考虑做成全自动的

# 修改记录：2018-1-6.修复了产销比计算错误的bug
#--------------------------------------------------------------------
# initialize
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']  

#--------------------------------------------------------------------
# data import
data = [] #data初始化为一个list
data.append(0)
header = ['产品','当月','去年同期','同比变动','本年累计','去年累计','累计变动']
reindex = [0,1,2,3,4,5,6,7]

default_path = '../ExampleData/宇通客车产销数据/'
#--------------------------------------------------------------------

class YTKC_Buy_Seller:
    '''
    利用产销快报绘制相关图形并保存图表，便于日常经营分析
    ''' 
    def __init__(self,year, month, work_path = default_path): 
        self.year = year
        self.month = month
        self.path = work_path
        self.data = []
        self.data.append(0)

    def run(self):
        for month in range(1,self.month+1):
          try:
            filename = str(self.year) + '年' + str(month) + '月份产销快报.xlsx'
            xls_file = pd.ExcelFile(self.path + filename)
          except: 
            filename = str(self.year) + '年' + str(month) + '月产销快报.xlsx'
            xls_file = pd.ExcelFile(self.path + filename)  
          table = xls_file.parse('Table 1')
          self.data.append(table.loc[7:14].copy())
          self.data[month].columns = header
          self.data[month].index = reindex
          self.data[month] = self.data[month].set_index(['产品'])
         
              
        #--------------------------------------------------------------------
        # data handle
        CurSale = [] #今年销量明细
        CurTotalSale = [] #今年销量累计
        CurProduce = [] #今年产量
        CurTotalProduce = [] #今年产量累计

        LastSale = []
        LastTotalSale = []
        LastProduce = []
        LastTotalProduce = []

        CurBigSale = [] #大车销量
        CurMidSale = [] #中车销量
        CurSmallSale = [] #小车销量

        LastBigSale = [] #大车销量
        LastMidSale = [] #中车销量
        LastSmallSale = [] #小车销量

        sum_cur0 = 0
        sum_last0 = 0
        sum_cur1 = 0
        sum_last1 = 0
        idx = []
        for i in range(1,self.month+1):
          CurProduce.append(self.data[i].loc['生产量','当月'])
          LastProduce.append(self.data[i].loc['生产量','去年同期'])  
          sum_cur0 += self.data[i].loc['生产量','当月']
          sum_last0 += self.data[i].loc['生产量','去年同期']
          CurTotalProduce.append(sum_cur0)
          LastTotalProduce.append(sum_last0)
          
          CurSale.append(self.data[i].loc['销售量','当月'])
          LastSale.append(self.data[i].loc['销售量','去年同期'])  
          sum_cur1 += self.data[i].loc['销售量','当月']
          sum_last1 += self.data[i].loc['销售量','去年同期']
          CurTotalSale.append(sum_cur1)
          LastTotalSale.append(sum_last1)
            
          CurBigSale.append(self.data[i].iloc[1,0])
          CurMidSale.append(self.data[i].iloc[2,0])
          CurSmallSale.append(self.data[i].iloc[3,0])
          LastBigSale.append(self.data[i].iloc[1,1])
          LastMidSale.append(self.data[i].iloc[2,1])
          LastSmallSale.append(self.data[i].iloc[3,1])
          idx.append(str(i)+'月')

        #汇总数据，什么都有  
        Stat = DataFrame([CurProduce,LastProduce,CurTotalProduce,LastTotalProduce,CurSale,LastSale,CurTotalSale,LastTotalSale,CurBigSale,CurMidSale,CurSmallSale,LastBigSale,LastMidSale,LastSmallSale])
        Stat = Stat.T
        Stat.index = idx
        Stat.columns=['今年产量','去年产量','今年产量累计','去年产量累计', '今年销量','去年销量','今年销量累计','去年销量累计','今年大车产量','今年中车产量','今年小车产量','去年大车产量','去年中车产量','去年小车产量']

#--------------------------------------------------------------------
# plot

        #不同年份的对比 
        DiffYearCmp = Stat.iloc[:,[0,1]]
        DiffYearCmp.plot(kind='bar')
        plt.xlabel('month')  #横坐标标签
        plt.ylabel('quantity') #纵坐标标签
        #plt.xticks(rotation=45)  #坐标标号旋转
        plt.title('宇通客车月产量对比')

        DiffYearTotal = Stat.iloc[:,[2,3]]
        DiffYearTotal.plot()
        plt.xlabel('month')  #横坐标标签
        plt.ylabel('quantity') #纵坐标标签
        plt.title('宇通客车总产量对比')

        #相同年份的对比
        SameYearCmp = Stat.iloc[:,[0,4]]
        SameYearCmp.plot(kind='bar')
        plt.xlabel('month')  #横坐标标签
        plt.ylabel('quantity') #纵坐标标签
        plt.title('宇通客车产销量对比')

        SameYearDiff = Stat.iloc[:,[8,9,10]]
        SameYearDiff.plot(kind='bar')
        plt.xlabel('month')  #横坐标标签
        plt.ylabel('quantity') #纵坐标标签
        plt.title('产品结构对比')
        plt.show()
 
        #--------------------------------------------------------------------
        #analyse
        #1.今年和往年相比的增量
        print('统计汇总报告，截止'+str(self.year)+'年'+str(self.month)+'月。。。')
        print('-----------------------------------------------')
        print('1:产销同比')
        IncRate = DiffYearTotal.iloc[self.month-1,:].pct_change() * -100
        a = IncRate.round(2)  #保留两位小数
        print('产量同比增长：'+str(a[1])+'%') 
        IncRate = (Stat.iloc[self.month-1,6] - Stat.iloc[self.month-1,7])/Stat.iloc[self.month-1,7]*100
        a = ("%.2f" % IncRate)  #保留两位小数
        print('销量同比增长：'+ a +'%')  
        print('-----------------------------------------------')
        #2.产销比是否健康？
        print('2.产销结构统计')
        total = SameYearCmp.sum()
        rate = total.pct_change() * 100
        a = rate.round(2)  #保留两位小数
        print('产销差异：'+str(abs(a[1]))+'%')   
        if(abs(a[1]) <= 1):
          print('产销结构很健康')
        print('-----------------------------------------------')
        #3.月产量是否有异动
        print('3.月产量波动情况')
        diff = DiffYearCmp.pct_change().round(2) * 100
        s1=diff.今年产量
        s2=diff.去年产量
        print('每月产量增幅')
        for i in range(1,self.month):
          print(s1[i],end='\t')
        print('')
        print('-----------------------------------------------')
        #4.产品结构是否发生了重大变化？
        print('4.产品结构变化')
        s=SameYearDiff.T
        s_sum=s.sum()
        Rate = (s/s_sum).round(2)
        print(Rate)
        
       
#---------------------------------------------------------------------------
# 用户代码示例    
# 使用前，请先pwd检查当前的工作目录（推荐在./anack/Release下）
# 1.实例化YTKC_Buy_Seller，参数是最新的年和月,以下两种写法都可以
#   yt = YTKC_Buy_Seller(2017,11)   //确保path在./anack/Release下
#   yt = YTKC_Buy_Seller(2017,11，your_path)
# 2.直接run即可

year = 2017
lastmonth = 12
filepath = 'E:/Investment/DataCenter/股票/个股历史信息/宇通客车/其他未分类/产销快报/'   
#yt= YTKC_Buy_Seller(year,lastmonth)  #使用默认地址
yt= YTKC_Buy_Seller(year,lastmonth,filepath)  #使用给定地址

yt.run()      



