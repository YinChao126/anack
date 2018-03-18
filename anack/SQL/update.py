'''
本模块用于更新数据库
'''

import finnance_to_sql as f
import k_data_to_sql as k
import macro_to_sql as m


from SQL.classify_to_sql import classify_info_to_sql
from SQL.macro_to_sql import macro_info_to_sql
from SQL.k_data_to_sql import create_k_table
from SQL.k_data_to_sql import k_data

  
def get_interest_list(filepath):
    '''
    解析"感兴趣的个股列表.txt",返回list类型的数据供其他模块使用
    '''
    list_id = []
    filename = filepath + '感兴趣的个股列表.txt'
    with open(filename,'r') as fh:
        s = fh.readline()   #获取更新时间
        s = fh.readline()   #获取目标长度  
        
        lines = fh.readlines()  #获取目标内容
    for s in lines:
        code = s[:6]
        list_id.append(code)    
    list_id.sort()
    return list_id  
    
def sql_update():
    classify_info_to_sql()    #update classify data
    
    macro_info_to_sql()       #update macro data
    
    lls = []                    #update k_data, both day and month
    lls = get_interest_list()
    create_k_table()
    for l in lls:
        k_data(l) 
        k_data(l,'M') 

    # update finnance data here...
    # 在代码执行路径自动生成输入路径

    column_interest = ['货币资金','应收账款','存货','流动资产合计','固定资产净额','无形资产','资产总计','短期借款','预收款项','流动负债合计','长期借款','一年内到期的非流动负债','负债合计','盈余公积','所有者权益(或股东权益)合计']
    for i in lls:
        try:
            cbfx = f.crawling_finance(path,i,column_interest)
            cbfx.crawling_update()
            f.Data_extract_balance()
        except:
            print(i)
#------------------------------------------------------------------------------
#sql_update()  #一条更新语句完成所有事情      
