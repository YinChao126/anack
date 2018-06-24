# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:47:45 2018

@author: 54206
"""

#import tushare as ts
#import numpy as np
#result=ts.get_today_all()
#print (result)
#
#re2=result[result['code']=='600660']
#print (re2)
#per = re2['per']

#re1=np.arange(4.0)
#print (re1)
#print (type(re1))
import re
import urllib.request

base = 'http://hq.sinajs.cn/list='
company_id = '600660'
flag = int(company_id)
if flag >= 600000:
    bios = 'sh' + company_id
else:
    bios = 'sz' + company_id
inputstr = base + bios
page = urllib.request.urlopen(inputstr).read()
if len(page) < 30:
    print('error, invalid id')
s = page[30:]
s = str(s)

pattern_data = '\d+\.*\d*(?=,)'
reobj = re.compile(pattern_data)
data = reobj.findall(s)
#data.pop()
#data.pop()
#
#pattern_data = '\d\d\d\d-\d\d-\d\d'
#reobj = re.compile(pattern_data)
#date = reobj.findall(s)
#data.append(date)
#
#pattern_data = '\d\d:\d\d:\d\d'
#reobj = re.compile(pattern_data)
#time = reobj.findall(s)
#data.append(time)
print(data)
cur_price = data[2]