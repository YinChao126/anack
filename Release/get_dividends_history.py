# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:29:43 2018

@author: 尹超
# 该模块用于获取指定个股的历史分红记录，以DataFrame形式给出
"""
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

 
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

def parse(html):
    raw_data = []
    try:
        year_raw = []
        year = []
        bonus_share = []
        bonus_convert = []
        profit_send = []
        ex_rights = []
        register_day = []
        
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#sharebonus_1')
        ls = l[0].tbody
        lls = ls.select('td')
        for l in lls:
            if (l.get_text().strip()) != '预案' and \
            (l.get_text().strip()) != '实施' and \
            (l.get_text().strip()) != '不分配' and \
            (l.get_text().strip()) != '查看':
                raw_data.append(l.get_text().strip())
        
        year_raw = raw_data[::7]
#        print(raw_data)        #出错的话请检查此处的输出
#        print(year_raw)        #出错的话请检查此处的输出
        for item in year_raw:
            a = pd.to_datetime(item).year - 1
            year.append(a)
        bonus_share = raw_data[1::7]
        bonus_convert = raw_data[2::7]
        profit_send = raw_data[3::7]
        ex_rights = raw_data[4::7]
        register_day = raw_data[5::7]
#        print(register_day)
        data = {'年度':year,
                '送股':bonus_share,
                '转股':bonus_convert,
                '派息':profit_send,
                '除权日':ex_rights,
                '登记日':register_day
                }
        frame = pd.DataFrame(data)
        return frame
    except:
        print('cannot parse this page')


# 提供给用户的函数，输入ID，解析出历史分红列表   
def get_bonus_table(id):
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/'
    url += str(id)
    url += '.phtml'
    html = get_one_page(url)
    return parse(html)     

###############################################################################  
###############################################################################      
# APP示例代码，用完了请关闭   
s = get_bonus_table('600066')
print(s)