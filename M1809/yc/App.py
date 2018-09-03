# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 19:35:20 2018

@author: yinchao
"""

import UserApi


id_list = ['000651', '000333', '600690']
if __name__ =='__main__':
    UserApi.Init(id_list,'CSV')
    UserApi.GetData('OFF')
    UserApi.Analyse()