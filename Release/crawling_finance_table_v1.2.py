# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:58:15 2018

@author: 1707500
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 09:37:36 2017

@author: 1707500
"""

import requests
from requests.exceptions import RequestException
import re
import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = 'GB2312'
        if response.status_code == 200:
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
    
    
def parse_one_page_2017_zichanfuzhai(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#BalanceSheetNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        #print(stock_raw_data)
        stock_data = stock_raw_data[4:]
        dates = stock_raw_data[1:4]
        dates = list(reversed(dates))
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
def parse_one_page_zichanfuzhai(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#BalanceSheetNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        #print(stock_raw_data)
        stock_data = stock_raw_data[5:]
        
        dates = stock_raw_data[1:5]
        dates = list(reversed(dates))
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

def parse_one_page_2017_xianjinliuliang(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#ProfitStatementNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        #print(stock_raw_data)
        stock_data = stock_raw_data[4:]
        dates = stock_raw_data[1:4]
        dates = list(reversed(dates))
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
   


def parse_one_page_xianjinliuliang(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#ProfitStatementNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        #print(stock_raw_data)
        stock_data = stock_raw_data[5:]
        
        dates = stock_raw_data[1:5]
        dates = list(reversed(dates))
        features = stock_data[::5]
        senson_one = stock_data[1::5]
        senson_two = stock_data[2::5]
        senson_three = stock_data[3::5]
        senson_four = stock_data[4::5]
        
# =============================================================================
#         print(dates)
#         print(features)
#         print(senson_one)
#         print(senson_two)
#         print(senson_three)
#         print(senson_four)
#         
# =============================================================================
        
        data.append(senson_one)
        data.append(senson_two)
        data.append(senson_three)
        data.append(senson_four)

        df = pd.DataFrame(data, index=dates, columns= features)
        return df

    except:
        pass
    
    
    
    
    
    
    
    
def parse_one_page_2017_lirunbiao(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#ProfitStatementNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        dates = list(reversed(dates))
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
   


def parse_one_page_lirunbiao(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#ProfitStatementNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
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
        dates = list(reversed(dates))
        features = stock_data[::5]
        senson_one = stock_data[1::5]
        senson_two = stock_data[2::5]
        senson_three = stock_data[3::5]
        senson_four = stock_data[4::5]
        
# =============================================================================
#         print(dates)
#         print(features)
#         print(senson_one)
#         print(senson_two)
#         print(senson_three)
#         print(senson_four)
# =============================================================================
        
        
        data.append(senson_one)
        data.append(senson_two)
        data.append(senson_three)
        data.append(senson_four)

        df = pd.DataFrame(data, index=dates, columns= features)
        return df

    except:
        pass




    
    
    
    
    
    
# =============================================================================
# 
# def write_to_file(content):
#     with open('F:\document\crawling\shengpingjia1.txt','a',encoding = 'utf-8') as f:
#         f.write(content  +'\n')
#         f.close()
# 
# =============================================================================



def main():
    
    zichanfuzai = pd.DataFrame()    
    for i in range(2008,2018):
        url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600660/ctrl/'+str(i)+'/displaytype/4.phtml'
        html = get_one_page(url)
        if i == 2017:            
            df = parse_one_page_2017_zichanfuzhai(html)
            print(df)
        else:
            df = parse_one_page_zichanfuzhai(html)
            print(df)
        zichanfuzai = pd.concat([zichanfuzai,df])
    print(zichanfuzai)
    zichanfuzai.to_csv('F:\document\crawling\zichanfuzhai.csv')



    xianjinliuliang = pd.DataFrame()    
    for i in range(2008,2018):
        url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/600660/ctrl/'+str(i)+'/displaytype/4.phtml'
        html = get_one_page(url)
        if i == 2017:            
            df = parse_one_page_2017_xianjinliuliang(html)
            print(df)
        else:
            df = parse_one_page_xianjinliuliang(html)
            print(df)
        xianjinliuliang = pd.concat([xianjinliuliang,df])
    print(xianjinliuliang) 
    
    xianjinliuliang.to_csv('F:\document\crawling\liuliang.csv')


  


    lirunbiao = pd.DataFrame()    
    for i in range(2008,2018):
        url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/600660/ctrl/'+str(i)+'/displaytype/4.phtml'
        html = get_one_page(url)
        if i == 2017:            
            df = parse_one_page_2017_lirunbiao(html)
            print(df)
        else:      
            df = parse_one_page_lirunbiao(html)
            print(df)
        lirunbiao = pd.concat([lirunbiao,df])
    print(lirunbiao)    
    lirunbiao.to_csv('F:\document\crawling\lirunbiao.csv')

      
    
if __name__ == '__main__':
    main()
    