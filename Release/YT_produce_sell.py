# ���ߣ�����
# �������ڣ�2018-1-6
# �汾�ţ�V0.3
# ������������������ͨ�ͳ������챨���ݵķ���
# ���ݣ�ϵͳ��ʼ�������ݶ��롢���ݴ�����ͼ��ͳ�Ʒ���
# ��ע��
# 1. ��ر��ֹ�������������xlsx�ļ�����ȷ���ļ�����Ч
# 2. ȷ��year/lastmonth���ļ�һ�£��������ִ���
# 3. ��ʱֻ�ܿ��ֹ���pdf�ļ�ת��xlsx�ļ����Ժ���Կ�������ȫ�Զ���

# �޸ļ�¼��2018-1-6.�޸��˲����ȼ�������bug
#--------------------------------------------------------------------
# initialize
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']  

#--------------------------------------------------------------------
# data import
data = [] #data��ʼ��Ϊһ��list
data.append(0)
header = ['��Ʒ','����','ȥ��ͬ��','ͬ�ȱ䶯','�����ۼ�','ȥ���ۼ�','�ۼƱ䶯']
reindex = [0,1,2,3,4,5,6,7]

default_path = '../ExampleData/��ͨ�ͳ���������/'
#--------------------------------------------------------------------

class YTKC_Buy_Seller:
    '''
    ���ò����챨�������ͼ�β�����ͼ�������ճ���Ӫ����
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
            filename = str(self.year) + '��' + str(month) + '�·ݲ����챨.xlsx'
            xls_file = pd.ExcelFile(self.path + filename)
          except: 
            filename = str(self.year) + '��' + str(month) + '�²����챨.xlsx'
            xls_file = pd.ExcelFile(self.path + filename)  
          table = xls_file.parse('Table 1')
          self.data.append(table.loc[7:14].copy())
          self.data[month].columns = header
          self.data[month].index = reindex
          self.data[month] = self.data[month].set_index(['��Ʒ'])
         
              
        #--------------------------------------------------------------------
        # data handle
        CurSale = [] #����������ϸ
        CurTotalSale = [] #���������ۼ�
        CurProduce = [] #�������
        CurTotalProduce = [] #��������ۼ�

        LastSale = []
        LastTotalSale = []
        LastProduce = []
        LastTotalProduce = []

        CurBigSale = [] #������
        CurMidSale = [] #�г�����
        CurSmallSale = [] #С������

        LastBigSale = [] #������
        LastMidSale = [] #�г�����
        LastSmallSale = [] #С������

        sum_cur0 = 0
        sum_last0 = 0
        sum_cur1 = 0
        sum_last1 = 0
        idx = []
        for i in range(1,self.month+1):
          CurProduce.append(self.data[i].loc['������','����'])
          LastProduce.append(self.data[i].loc['������','ȥ��ͬ��'])  
          sum_cur0 += self.data[i].loc['������','����']
          sum_last0 += self.data[i].loc['������','ȥ��ͬ��']
          CurTotalProduce.append(sum_cur0)
          LastTotalProduce.append(sum_last0)
          
          CurSale.append(self.data[i].loc['������','����'])
          LastSale.append(self.data[i].loc['������','ȥ��ͬ��'])  
          sum_cur1 += self.data[i].loc['������','����']
          sum_last1 += self.data[i].loc['������','ȥ��ͬ��']
          CurTotalSale.append(sum_cur1)
          LastTotalSale.append(sum_last1)
            
          CurBigSale.append(self.data[i].iloc[1,0])
          CurMidSale.append(self.data[i].iloc[2,0])
          CurSmallSale.append(self.data[i].iloc[3,0])
          LastBigSale.append(self.data[i].iloc[1,1])
          LastMidSale.append(self.data[i].iloc[2,1])
          LastSmallSale.append(self.data[i].iloc[3,1])
          idx.append(str(i)+'��')

        #�������ݣ�ʲô����  
        Stat = DataFrame([CurProduce,LastProduce,CurTotalProduce,LastTotalProduce,CurSale,LastSale,CurTotalSale,LastTotalSale,CurBigSale,CurMidSale,CurSmallSale,LastBigSale,LastMidSale,LastSmallSale])
        Stat = Stat.T
        Stat.index = idx
        Stat.columns=['�������','ȥ�����','��������ۼ�','ȥ������ۼ�', '��������','ȥ������','���������ۼ�','ȥ�������ۼ�','����󳵲���','�����г�����','����С������','ȥ��󳵲���','ȥ���г�����','ȥ��С������']

#--------------------------------------------------------------------
# plot

        #��ͬ��ݵĶԱ� 
        DiffYearCmp = Stat.iloc[:,[0,1]]
        DiffYearCmp.plot(kind='bar')
        plt.xlabel('month')  #�������ǩ
        plt.ylabel('quantity') #�������ǩ
        #plt.xticks(rotation=45)  #��������ת
        plt.title('��ͨ�ͳ��²����Ա�')

        DiffYearTotal = Stat.iloc[:,[2,3]]
        DiffYearTotal.plot()
        plt.xlabel('month')  #�������ǩ
        plt.ylabel('quantity') #�������ǩ
        plt.title('��ͨ�ͳ��ܲ����Ա�')

        #��ͬ��ݵĶԱ�
        SameYearCmp = Stat.iloc[:,[0,4]]
        SameYearCmp.plot(kind='bar')
        plt.xlabel('month')  #�������ǩ
        plt.ylabel('quantity') #�������ǩ
        plt.title('��ͨ�ͳ��������Ա�')

        SameYearDiff = Stat.iloc[:,[8,9,10]]
        SameYearDiff.plot(kind='bar')
        plt.xlabel('month')  #�������ǩ
        plt.ylabel('quantity') #�������ǩ
        plt.title('��Ʒ�ṹ�Ա�')
        plt.show()
 
        #--------------------------------------------------------------------
        #analyse
        #1.�����������ȵ�����
        print('ͳ�ƻ��ܱ��棬��ֹ'+str(self.year)+'��'+str(self.month)+'�¡�����')
        print('-----------------------------------------------')
        print('1:����ͬ��')
        IncRate = DiffYearTotal.iloc[self.month-1,:].pct_change() * -100
        a = IncRate.round(2)  #������λС��
        print('����ͬ��������'+str(a[1])+'%') 
        IncRate = (Stat.iloc[self.month-1,6] - Stat.iloc[self.month-1,7])/Stat.iloc[self.month-1,7]*100
        a = ("%.2f" % IncRate)  #������λС��
        print('����ͬ��������'+ a +'%')  
        print('-----------------------------------------------')
        #2.�������Ƿ񽡿���
        print('2.�����ṹͳ��')
        total = SameYearCmp.sum()
        rate = total.pct_change() * 100
        a = rate.round(2)  #������λС��
        print('�������죺'+str(abs(a[1]))+'%')   
        if(abs(a[1]) <= 1):
          print('�����ṹ�ܽ���')
        print('-----------------------------------------------')
        #3.�²����Ƿ����춯
        print('3.�²����������')
        diff = DiffYearCmp.pct_change().round(2) * 100
        s1=diff.�������
        s2=diff.ȥ�����
        print('ÿ�²�������')
        for i in range(1,self.month):
          print(s1[i],end='\t')
        print('')
        print('-----------------------------------------------')
        #4.��Ʒ�ṹ�Ƿ������ش�仯��
        print('4.��Ʒ�ṹ�仯')
        s=SameYearDiff.T
        s_sum=s.sum()
        Rate = (s/s_sum).round(2)
        print(Rate)
        
       
#---------------------------------------------------------------------------
# �û�����ʾ��    
# ʹ��ǰ������pwd��鵱ǰ�Ĺ���Ŀ¼���Ƽ���./anack/Release�£�
# 1.ʵ����YTKC_Buy_Seller�����������µ������,��������д��������
#   yt = YTKC_Buy_Seller(2017,11)   //ȷ��path��./anack/Release��
#   yt = YTKC_Buy_Seller(2017,11��your_path)
# 2.ֱ��run����

year = 2017
lastmonth = 12
filepath = 'E:/Investment/DataCenter/��Ʊ/������ʷ��Ϣ/��ͨ�ͳ�/����δ����/�����챨/'   
#yt= YTKC_Buy_Seller(year,lastmonth)  #ʹ��Ĭ�ϵ�ַ
yt= YTKC_Buy_Seller(year,lastmonth,filepath)  #ʹ�ø�����ַ

yt.run()      



