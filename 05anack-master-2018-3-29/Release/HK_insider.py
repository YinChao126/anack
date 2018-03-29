#---------------------------------------------------------------------------
'''
������HK_insider�����������Ļ֪���ߣ�
���ߣ�����
���ڣ�2017-12-3
��������������һ��������۵�֪���ߣ��ܹ���������˳���A�ɵľ������
������HK_update->����ϸ�ĳֹ���ϸ��Ϊcsv�ļ�
      HK_plot->��ȡcsv�ļ�������ͼ��
      HK_stat->��ȡcsv�ļ��������������������������
�汾�ţ�V0.1
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
    һ��������۵�֪���ߣ��ܹ�������һ�и���Ȥ�Ķ���
    '''
    def __init__(self,work_path, stock_name, mode = 1):
        '''
        ��ʼ�����ṩ����Ŀ¼�͸���Ȥ�Ĺ�Ʊ����
        ���룺  work_path -> ���ݱ����·��
                stock_name-> ��Ʊ���ƣ����磺'��ҫ����'
                mode  -> ����0    ����1��Ĭ��ֵ��
        '''
        self.work_path = work_path
        self.stock_name = stock_name
        if mode == 0:
            self.url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'
        else:
            self.url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'
    def HK_debug(self): 
        '''
        ���Ժ�������ӡ��ʱ��Ϣ�����û�����
        '''
        print(self.work_path)
        #print(self.stock_name)
    def HK_update(self, elapse_day = 0): 
        '''
        ��������HK_update
        ��������������ȡ��Ϣ����Ϊcsv�ļ�������ļ��Ѵ��ڣ������
        ���룺elapse_day(��ѡ��   Ĭ�ϸ��µ����죬����elapse_day=5�������5������
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

        # �Զ����£��ж�start��end�������������������ֱ��ֹͣ
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
        if elapse_day == 0:  #��������øò�������ֱ�Ӹ��µ�����
            end = end_now
        else:  #������øò���������µ�start�ĺ�elapse_day��
            end = start + timedelta(elapse_day - 1)
        if end > end_now:    #��ֹ����ʱ��ȡ�õ�end̫�󣬳���������
            end = end_now
        #end = datetime(2017,3,20) #��������ʱʹ�� !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        if start > end:
            print(self.stock_name + '�Ѿ�����������')
            return
            #exit()
        yt_date_format = pd.date_range(start,end)
        #print(yt_date_format)

        # ѭ����ʼ����
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

            stock_raw_data = [] #�ǵó�ʼ��������append��һֱ����
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
            
        # д�ļ�������ԭʼ��¼                
        gupiao_output.to_csv(file_name,mode='a',header=False)        
    def HK_plot(self):
        '''
        ��������HK_plot
        ��;����ȡstock.csv�ļ�������ʱ��˳�򽫳ֹɱ�����ͼ
        ���룺��
        �����һ��ͼ��
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
            stock[5] = stock[5].astype(float) #DataFrame �������ݣ�str ת float
            D = stock.iloc[:,[2,5]]
            A = D.set_index([2])
            A.plot()
            plt.xlabel('day')  #�������ǩ
            plt.ylabel('rate') #�������ǩ
            plt.xticks(rotation=30)  #��������ת
            plt.title('�۹ɳ���' + self.stock_name + '�����䶯')  
            plt.show()      
        except:
            print('cannot open file correctly.')
    def HK_stat(self):
        '''
        ��������HK_stat
        ��;����ȡstock.csv�ļ������з������õ�����ָ���ԵĽ��ۣ���ʱû��ʵ�֣�
        '''
        print('��Ҫ������ݴ������\n')
        
#---------------------------------------------------------------------------
# �û�����ʾ����Ҫ��        
# 1. ʹ��ǰ��������pwdȷ�ϵ�ǰ����Ŀ¼�ڣ�F:/GitHubCenter/anack/Src��
#     ������ڵĹ���Ŀ¼���ԣ��������ʾ��������path������Լ�������޸�
# 2. �����������ַ�����ʵ����һ������ע��mode=1�����У���Ĭ��ֵ
#     test = HK_insider(path,'��ͨ�ͳ�')
#     test = HK_insider(path,'��ͨ�ͳ�',1)
#     test = HK_insider(path,'��������',0)
# 3. ����HK_update������ԭʼ����
#     test.HK_update()    ֱ�Ӹ��µ�����
#     test.HK_update(5)   �������������������5��
# 4. ����HK_plot�����Ƹ۹���¶��Ϣ�ĳֹ�����
#     test.HK_plot()      ����
#---------------------------------------------------------------------------

path = '../ExampleData/'
gldq = HK_insider(path,'��������',0)
gldq.HK_update(5)
gldq.HK_plot()
print ('hello')