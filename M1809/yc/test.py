# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:47:45 2018

@author: 54206
"""

import tushare as ts
import numpy as np
result=ts.get_today_all()
print (result)

re2=result[result['code']=='600660']
print (re2)
per = re2['per']

#re1=np.arange(4.0)
#print (re1)
#print (type(re1))