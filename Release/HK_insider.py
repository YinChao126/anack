#---------------------------------------------------------------------------
'''
类名：HK_insider（香港来的内幕知情者）
作者：尹超
日期：2017-12-3
描述：你碰到了一个来自香港的知情者，能够告诉你港人持有A股的具体情况
方法：HK_update->将详细的持股明细存为csv文件
      HK_plot->读取csv文件，绘制图形
      HK_stat->读取csv文件，分析具体情况，并给出建议
版本号：V0.1
'''
#---------------------------------------------------------------------------
import requests
from requests.exceptions import RequestException
import re
import json
from bs4 import BeautifulSoup
import csv
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
import matplotlib.pyplot as plt
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']
#---------------------------------------------------------------------------
class HK_insider:
    '''
    一个来自香港的知情者，能够告诉你一切感兴趣的东西
    '''
    def __init__(self,work_path, stock_name, mode = 1):
        '''
        初始化，提供工作目录和感兴趣的股票名称
        输入：  work_path -> 数据保存的路径
                stock_name-> 股票名称，例如：'福耀玻璃'
                mode  -> 深市0    沪市1（默认值）
        '''
        self.work_path = work_path
        self.stock_name = stock_name
        if mode == 0:
            self.url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'
        else:
            self.url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'
    def HK_debug(self): 
        '''
        调试函数，打印临时信息，对用户无用
        '''
        print(self.work_path)
        #print(self.stock_name)
    def HK_update(self, elapse_day = 0): 
        '''
        方法名：HK_update
        描述：从网上爬取信息并存为csv文件，如果文件已存在，则更新
        输入：elapse_day(可选）   默认更新到昨天，设置elapse_day=5，则更新5天数据
        '''
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        stock_raw_data = []
        data = {
                    "__VIEWSTATE":"XsRiWTu1/KBf9sV6+jF/j7DirltRgxkPREuZmh4Bv2F6XqWFvE+oMPK5Gimcd0dte1ts5EcrWHjFjyf7OfSlnptnmeJx0Ew7a7b6ZENIMBnIhIIM5GEIRrfbSY0axU3X3gEUZLr2xzgXs0LkvxNxlk7/GdqQfmznseviSftJwPO/WeBnehJ8fL3QbPTUf+ghYjMxjg==",
                    "__VIEWSTATEGENERATOR":"EC4ACD6F",
                    "__EVENTVALIDATION":"WvLN3nFZG1uW4Zvb+fCbalO1qaJAWQHPYYwnvDKgAH1eQTG6T5I4v+304hfy1jopBkVIRxzeGYMK+FL6E3Hb5YStfmtPOTxxVabyPEktMZ2QLbB3WhP1hqkw6prQVBcWImuw/CPIvezFsrPGFevnp60BIL6pcQIBgdJGwat5uu4F2fIgDT7mXR83IgUyz70lh3p9568SDPVRegpQ2JkqB2QWCsN2jyQ2PN4Q3d2+k0q47xipsGtEJL4qEK7HiyFiCa14VFn0O7cT8kX2g0rxpstyvofcTgrRWqFpGHXB2FRj2UfMjOlAfMwXXweeUIxkzpf2uobPxVNo8kdiwtFOEQyspFB5lV5dFaKEnt0z2fXglv816Cr65CiHfCliv+WzUd306Bt/W+cSS2cNYYDK0CJ+F4HxrIloMwd/2YbUOwNRRbplPPqDsKvC4QcpEMAl2hcn7VwrvHWpRR1PPOvkyJ/n7YCTQbrfJh1/kawchorFftc/uJlTPOxZut4IIU7abr/OmCokz8qIn6z38B7W+eB8Z5eI8LExALfZTuUidqjCeTR14A5pfLalCmXSZc/nOEmsYlm9EQbkh5BkUC7DZjM/V75ptjtLQr2v/9dD5HPVmGOmM///TMid9SFrbetHTXUpDGs4cj7JjOFH/GaZDv6eYsBOAb51/IsJmVDNMEdYuONDUbcOJKPnPevs36c3S3APlwqROMwxkMYNh2QLVByrTfau5b7EoqOQaimJ1RH2+WH7jAnpYBItBD4m7p76tfyhQMkpkZsmtovFRoTVVyOQFVmww9l4MSPTcxXUGFhCFE9InC+CpL60eMa01Eg2XNNAiW5J0aAU5731n/9QX9nFh7iFcqfpJF3D2b9KvT4eRZaRUUvTGOUwAhVMz/4ybnrYVOBWTVkr69lm/Bv19/SAS4N9580nhm0maVQGRYyU4YhRinfvz2TnR66pbh0NhSg/FssSvPgzHuz1Oh+YmAOy232vPQonW9NLVLIFo+Mgq7HTCCVS2UU34N74Wm2UVEcfcUoxIrkc+cUNVlWjg9+WS2fuaKhejnKKlEen1FGEu8hQTihDEgv2r3xuTrAoLfO0QBx8RaV4VyuixWy7iIaUxx4/7ZRrnu+Ys7P8G6PojLDBW6V8Zqf0kqjGxYTwyWWyMCUXKLs+ZrNZL+36UaSAALU=",
                    "today":20171201,
                    "sortBy":"",
                    "alertMsg":"",
                    "ddlShareholdingDay":11,
                    "ddlShareholdingMonth":11,
                    "ddlShareholdingYear":2017,
                    "btnSearch.x":13,
                    "btnSearch.y":10
                }         
        yt_date = []
        yt_code = []
        yt_name = []
        yt_quantity = []
        yt_rate = []

        # 自动更新，判断start和end，如果不满足条件，则直接停止
        file_name = self.work_path + self.stock_name + '.csv'
        l = []
        try:
            f=open(file_name,'r')
            content=csv.reader(f)
            for i in content:
                l.append(i)
        except:
            f=open(file_name,'w')    
        f.close()

        if len(l) < 2:
            start = datetime.datetime(2017,3,17)
        else:
            start = parse(l[len(l) - 1][2]) + timedelta(1)
        
        end_now = datetime.datetime.now() - timedelta(1)    
        if elapse_day == 0:  #如果不设置该参数，则直接更新到昨天
            end = end_now
        else:  #如果设置该参数，则更新到start的后elapse_day天
            end = start + timedelta(elapse_day - 1)
        if end > end_now:    #防止测试时，取得的end太大，超过了昨天
            end = end_now
        #end = datetime(2017,3,20) #仅供测试时使用 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        if start > end:
            print(self.stock_name + '已经是最新数据')
            return
            #exit()
        yt_date_format = pd.date_range(start,end)
        #print(yt_date_format)

        # 循环开始爬虫
        for i in yt_date_format:
            print(i.strftime('%Y-%m-%d'))
            yt_date.append(i.strftime('%Y-%m-%d'))
            month = i.strftime('%m')
            day = i.strftime('%d')
            data['ddlShareholdingMonth'] = str(month)
            data['ddlShareholdingDay'] = str(day)
            r = requests.post(self.url, data=data,headers = headers)
            soup = BeautifulSoup(r.text,'html5lib')
            lls = soup.select('td.arial12black')

            stock_raw_data = [] #记得初始化，否则append会一直叠加
            for l in lls:
                stock_raw_data.append(l.get_text().strip())
            len(stock_raw_data)

            code = stock_raw_data[::4]
            name = stock_raw_data[1::4]
            quantity = stock_raw_data[2::4]
            rate = stock_raw_data[3::4]

            length = len(code)
            i = 0
            while i < length:
                if(name[i] == self.stock_name):
                    yt_code.append(code[i])
                    yt_name.append(name[i])
                    yt_quantity.append(quantity[i])
                    a = rate[i]
                    a = a[:-1]
                    a = float(a)            
                    yt_rate.append(a)
                i += 1
        gupiao_output = pd.DataFrame({
                       'date' : yt_date,
                       'code' : yt_code,
                       'name' : yt_name,
                       'quantity' : yt_quantity,
                       'rate' : yt_rate                            
                    })  
            
        # 写文件，保存原始记录                
        gupiao_output.to_csv(file_name,mode='a',header=False)        
    def HK_plot(self):
        '''
        方法名：HK_plot
        用途：读取stock.csv文件并按照时间顺序将持股比例绘图
        输入：无
        输出：一副图像
        '''
        file_name = self.work_path + self.stock_name + '.csv'
        print(file_name)
        try:
            f=open(file_name,'r')
            content=csv.reader(f)
            l = []

            for i in content:
                l.append(i) 
            f.close()

            stock = pd.DataFrame(l)
            stock[5] = stock[5].astype(float) #DataFrame 类型数据，str 转 float
            D = stock.iloc[:,[2,5]]
            A = D.set_index([2])
            A.plot()
            plt.xlabel('day')  #横坐标标签
            plt.ylabel('rate') #纵坐标标签
            plt.xticks(rotation=30)  #坐标标号旋转
            plt.title('港股持有' + self.stock_name + '比例变动')  
            plt.show()      
        except:
            print('cannot open file correctly.')
    def HK_stat(self):
        '''
        方法名：HK_stat
        用途：读取stock.csv文件并进行分析，得到具有指导性的结论（暂时没有实现）
        '''
        print('需要添加数据处理过程\n')
        
#---------------------------------------------------------------------------
# 用户代码示例及要点        
# 1. 使用前，请输入pwd确认当前工作目录在：F:/GitHubCenter/anack/Src下
#     如果当期的工作目录不对，则下面的示例代码中path请根据自己的情况修改
# 2. 利用以下三种方法来实例化一个对象，注意mode=1（沪市）是默认值
#     test = HK_insider(path,'宇通客车')
#     test = HK_insider(path,'宇通客车',1)
#     test = HK_insider(path,'格力电器',0)
# 3. 利用HK_update来更新原始数据
#     test.HK_update()    直接更新到昨天
#     test.HK_update(5)   接着已有数据往后更新5天
# 4. 利用HK_plot来绘制港股披露信息的持股曲线
#     test.HK_plot()      即可
#---------------------------------------------------------------------------

path = '../ExampleData/'
gldq = HK_insider(path,'格力电器',0)
gldq.HK_update(5)
gldq.HK_plot()