# 作者：尹超
# 更新日期：2018-5-13
# 版本号：V0.3
# 描述：本程序用于宇通客车产销快报数据的分析
# 内容：系统初始化、数据读入、数据处理、绘图、统计分析
# 备注：
# 1. 务必保持工程下有连续的xlsx文件，并确保文件名有效
# 2. 确保year/lastmonth和文件一致，否则会出现错误
# 3. 暂时只能靠手工将pdf文件转成xlsx文件，以后可以考虑做成全自动的

# 修改记录：2018-1-6.修复了产销比计算错误的bug
#修改记录：2018-5-13.更改数据来源，由离线数据变为数据库
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']  


import DataToSql
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
class DataAnalyze:
    def __init__(self,year,month):
        self.year=year
        self.month = month
        
    def run(self):

        dataBase=DataToSql.ProductionSaleToSql(YearBegin = 2018,MonthBegin = 7)
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
            CurProduceData=dataBase.QueryPSData(str(self.year),str(i),"production")
            CurProduce.append(CurProduceData)
            
            LastProducData=dataBase.QueryPSData(str(self.year),str(i),"SPLY_production")
            LastProduce.append(LastProducData)
            
            sum_cur0+=CurProduceData
            sum_last0+=LastProducData
            CurTotalProduce.append(sum_cur0)
            LastTotalProduce.append(sum_last0)
            
            CurSaleData=dataBase.QueryPSData(str(self.year),str(i),"sale")
            CurSale.append(CurSaleData)
            
            LastSaleData=dataBase.QueryPSData(str(self.year),str(i),"SPLY_sale")
            LastSale.append(LastSaleData)
            
            sum_cur1 += CurSaleData
            sum_last1 += LastSaleData
            CurTotalSale.append(sum_cur1)
            LastTotalSale.append(sum_last1)
            
            CurBigSaleData=dataBase.QueryPSData(str(self.year),str(i),"large_sale")
            CurBigSale.append(CurBigSaleData)
            
            CurMidSaleData=dataBase.QueryPSData(str(self.year),str(i),"mid_sale")
            CurMidSale.append(CurMidSaleData)
            
            CurSmallSaleData=dataBase.QueryPSData(str(self.year),str(i),"small_sale")
            CurSmallSale.append(CurSmallSaleData)
            
            LastBigSaleData=dataBase.QueryPSData(str(self.year),str(i),"SPLY_sale_large")
            LastBigSale.append(LastBigSaleData)
            
            LastMidSaleData=dataBase.QueryPSData(str(self.year),str(i),"SPLY_sale_mid")
            LastMidSale.append(LastMidSaleData)
            
            LastSmallSaleData=dataBase.QueryPSData(str(self.year),str(i),"SPLY_sale_small")
            LastSmallSale.append(LastSmallSaleData)
            
            idx.append(str(i)+'月')
        print (CurSale)
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
# 使用前确保数据库中有相应数据

if __name__ == "__main__":
    DA=DataAnalyze(2017,2)
    DA.run()
       