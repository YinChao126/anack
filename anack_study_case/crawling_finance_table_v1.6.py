'''
类名：crawling_finance_table_v1.4
作者：徐抒田
日期：2018-1-4
描述：一个帮助你获取股票财报数据的小伙伴,实现了爬取福耀玻璃（600660）的利润表、资产负债表、现金流量表所有数据，并输出为csv格式的三张报表

方法： get_one_page->爬取一页网页数据
      parse_one_page_zhengze-> 通过正则表达式整理数据（网页不规则使用）
      parse_one_page_2017_zichanfuzhai->解析17年的资产负债表数据
      parse_one_page_zichanfuzhai->解析资产负债表数据
      parse_one_page_2017_xianjinliuliang->解析17年的现金流量表数据
      parse_one_page_xianjinliuliang->解析现金流量表数据
      parse_one_page_2017_lirunbiao->解析17年的利润表数据
      parse_one_page_lirunbiao->解析利润表数据
      
版本号：V1.4
'''

'''
类名：crawling_finance_table_v1.5
作者：徐抒田
日期：2018-1-10
描述：
1.修改BEAUTIFULSOUP的解析表达式->soup.select('table#BalanceSheetNewTable0 tbody tr td')
2.删除部分的无用代码
3.添加部分注释


版本号：V1.5
'''

# =============================================================================
# import re
# import json
# import numpy as np
# =============================================================================
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


class crawling_finance:
    '''
    一个帮助你获取股票财报数据的小伙伴
    '''
    
    
    def __init__(self,work_path, stock_code):
    
        self.work_path = work_path
        self.stock_code = stock_code

    def get_one_page(self,url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        try:
            response = requests.get(url,headers = headers)                  
            response.encoding = 'GB2312'                        #解决中文乱码
            if response.status_code == 200:                     #判断是否爬取网页成功
                return response.text
            return None
        except RequestException:
            return None
    
    
    # =============================================================================
    # def parse_one_page_zhengze(html):
    #     try:    
    #         pattern = re.compile('>(.*?)".*?>(.*?)</td><td',re.S)
    #         items = re.findall(pattern,html)
    #     except:
    #         pass
    #     print(items)
    # =============================================================================
        
        
    def parse_one_page_2017_zichanfuzhai(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#BalanceSheetNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '流动资产' and (l.get_text().strip()) != '非流动资产' and (l.get_text().strip()) != '流动负债' and (l.get_text().strip()) != '非流动负债' and (l.get_text().strip()) != '所有者权益':
                    #去除没有值得字段
                    stock_raw_data.append(l.get_text().strip())                  
            #print(stock_raw_data)
            stock_data = stock_raw_data[4:]            #原数据中去除日期   
            dates = stock_raw_data[1:4]                #原数据中选取日期
            features = stock_data[::4]                 #选取所有字段名
            senson_one = stock_data[1::4]              #选取第一季度所有数据
            senson_two = stock_data[2::4]              #选取第二季度所有数据
            senson_three = stock_data[3::4]            #选取第三季度所有数据
            
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
    
            df = pd.DataFrame(data, index=dates, columns= features)   #转为dataframe结构
            return df
    
        except:
            pass
    def parse_one_page_zichanfuzhai(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#BalanceSheetNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '流动资产' and (l.get_text().strip()) != '非流动资产' and (l.get_text().strip()) != '流动负债' and (l.get_text().strip()) != '非流动负债' and (l.get_text().strip()) != '所有者权益':
                    stock_raw_data.append(l.get_text().strip())
                    
            #print(stock_raw_data)                       #调试使用
            stock_data = stock_raw_data[5:]              #原数据中去除日期
            dates = stock_raw_data[1:5]                  #原数据中选取日期
            features = stock_data[::5]                   #选取所有字段名
            senson_one = stock_data[1::5]                #选取第一季度所有数据
            senson_two = stock_data[2::5]                #选取第二季度所有数据
            senson_three = stock_data[3::5]              #选取第三季度所有数据
            senson_four = stock_data[4::5]               #选取第四季度所有数据
            
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
            data.append(senson_four)
    
            df = pd.DataFrame(data, index=dates, columns= features)   #转为dataframe结构
            return df
        except:
            pass
    
    def parse_one_page_2017_xianjinliuliang(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#ProfitStatementNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '一、经营活动产生的现金流量' and (l.get_text().strip()) != '二、投资活动产生的现金流量' and (l.get_text().strip()) != '三、筹资活动产生的现金流量' and (l.get_text().strip()) != '附注':
                    stock_raw_data.append(l.get_text().strip())
                    
            #print(stock_raw_data)                     #调试使用       
            stock_data = stock_raw_data[4:]            #原数据中去除日期
            dates = stock_raw_data[1:4]                #原数据中选取日期
            features = stock_data[::4]                 #选取所有字段名
            senson_one = stock_data[1::4]              #选取第一季度所有数据
            senson_two = stock_data[2::4]              #选取第二季度所有数据
            senson_three = stock_data[3::4]            #选取第三季度所有数据        
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
    
            df = pd.DataFrame(data, index=dates, columns= features)
            return df
    
        except:
            pass       
       
    
    
    def parse_one_page_xianjinliuliang(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#ProfitStatementNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '一、经营活动产生的现金流量' and (l.get_text().strip()) != '二、投资活动产生的现金流量' and (l.get_text().strip()) != '三、筹资活动产生的现金流量' and (l.get_text().strip()) != '附注':
                    stock_raw_data.append(l.get_text().strip())
            #print(stock_raw_data)                     #调试使用 
            stock_data = stock_raw_data[5:]            #原数据中去除日期
            
            dates = stock_raw_data[1:5]                #原数据中选取日期
            features = stock_data[::5]                 #选取所有字段名
            senson_one = stock_data[1::5]              #选取第一季度所有数据
            senson_two = stock_data[2::5]              #选取第二季度所有数据
            senson_three = stock_data[3::5]            #选取第三季度所有数据
            senson_four = stock_data[4::5]             #选取第四季度所有数据
            
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
            data.append(senson_four)
    
            df = pd.DataFrame(data, index=dates, columns= features)
            return df
    
        except:
            pass
        
    
        
    def parse_one_page_2017_lirunbiao(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#ProfitStatementNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '六、每股收益':
                    stock_raw_data.append(l.get_text().strip())
            #print(stock_raw_data)
            stock_data = stock_raw_data[4:]
            dates = stock_raw_data[1:4]
            features = stock_data[::4]
            senson_one = stock_data[1::4]
            senson_two = stock_data[2::4]
            senson_three = stock_data[3::4]
            
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
    
            df = pd.DataFrame(data, index=dates, columns= features)
            return df
    
        except:
            pass       
       
    
    
    def parse_one_page_lirunbiao(self,html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls = soup.select('table#ProfitStatementNewTable0 tbody tr td')
            stock_raw_data = [] #记得初始化，否则append会一直叠加
            stock_data=[]
            data = []
            senson_one=[]
            senson_two=[]
            senson_three=[]
            senson_four=[]
            for l in lls:
                if (l.get_text().strip()) != '六、每股收益':
                    stock_raw_data.append(l.get_text().strip())
            #print(stock_raw_data)
            stock_data = stock_raw_data[5:]
            
            dates = stock_raw_data[1:5]
            features = stock_data[::5]
            senson_one = stock_data[1::5]
            senson_two = stock_data[2::5]
            senson_three = stock_data[3::5]
            senson_four = stock_data[4::5]
            
            data.append(senson_one)
            data.append(senson_two)
            data.append(senson_three)
            data.append(senson_four)
    
            df = pd.DataFrame(data, index=dates, columns= features)
            return df
    
        except:
            pass
    
    
    def crawling_update(self):
        date=[]
        html = self.get_one_page('http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/'+self.stock_code+'/ctrl/2017/displaytype/4.phtml')
        soup = BeautifulSoup(html,'html5lib')
        lls = soup.select('div#con02-1 table tbody tr td a')
        for l in lls:
            item = l.get_text().strip()
            try:
                item = int(item)
                date.append(item)
            except:
                pass       
        zichanfuzai = pd.DataFrame()    
        for i in range(date[len(date)-1],date[0]+1):
            url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/'+self.stock_code+'/ctrl/'+str(i)+'/displaytype/4.phtml'
            html = self.get_one_page(url)
            if i == 2017:            
                df = self.parse_one_page_2017_zichanfuzhai(html)
                print(df)
            else:
                df = self.parse_one_page_zichanfuzhai(html)
                print(df)
            zichanfuzai = pd.concat([zichanfuzai,df])            #两个dataframe做连接，类似数据库的union all
        print(zichanfuzai)
        zichanfuzai.to_csv(self.work_path + '/'+self.stock_code +'_'+'balance_sheet.csv')
        
        
        xianjinliuliang = pd.DataFrame()    
        for i in range(date[len(date)-1],date[0]+1):
            url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/'+self.stock_code+'/ctrl/'+str(i)+'/displaytype/4.phtml'
            html = self.get_one_page(url)
            if i == 2017:            
                df = self.parse_one_page_2017_xianjinliuliang(html)
                print(df)
            else:
                df = self.parse_one_page_xianjinliuliang(html)
                print(df)
            xianjinliuliang = pd.concat([xianjinliuliang,df])          #两个dataframe做连接，类似数据库的union all
        print(xianjinliuliang)        
        xianjinliuliang.to_csv(self.work_path + '/'+self.stock_code + '_'+'cash_flow.csv')
        
        
        lirunbiao = pd.DataFrame()    
        for i in range(date[len(date)-1],date[0]+1):
            url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/'+self.stock_code+'/ctrl/'+str(i)+'/displaytype/4.phtml'
            html = self.get_one_page(url)
            if i == 2017:
                df = self.parse_one_page_2017_lirunbiao(html)
                print(df)
            else:
                df = self.parse_one_page_lirunbiao(html)
                print(df)
            lirunbiao = pd.concat([lirunbiao,df])                       #两个dataframe做连接，类似数据库的union all
        print(lirunbiao)
        lirunbiao.to_csv(self.work_path+'/'+self.stock_code + '_'+'profit.csv')
    
    
    
path = 'D:/document/crawling/'
cbfx = crawling_finance(path,'600660')
cbfx.crawling_update()
    