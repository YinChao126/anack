# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 01:47:40 2018

@author: yinchao
"""

import crawling_finance_table
import pymysql
def Connect_sql():
    conn = pymysql.connect(
            host = '',
            port = 3306,
#            user = '',
#            passwd = '',
            user = '',
            passwd = '',
            db = "test",
            charset = "utf8"
            )
    
    cur = conn.cursor()
    print("\nconnect to aliyun success!\n")
    return cur


parameter = []
id_list = []     
def M1809_config():
    '''
    以读文件的方式获取配置参数
    1. 读取待考察的参数
    2. 读取公司名称列表，并转换成id
    3. 更新该公司的财务报表，以备以后使用
    注意：文件名不可改
    '''
    del parameter[:]
    with open ('parameter_list.txt','r',encoding = 'utf-8') as fh:
        ct = fh.readlines()
    
    
    for s in ct:
        items = s.strip()
        if items != '': 
            if items[0] == '#': #剔除注释部分
                break
            parameter.append(items)
    
    del id_list[:]
    with open('company_list.txt','r', encoding = 'utf-8') as fh:
        ct = fh.readlines()
    company = []
    for s in ct:
        if s.strip() != '': 
            company.append(s.strip())
    
    cur = Connect_sql()
    for name in company:
        cmd = "select * from anack_classify where name = \'"+name+"\';"
        cur.execute(cmd)
        result = cur.fetchall()
        try:
            id = result[0][0] 
            id_list.append(id)
            
        except:
            print(name+' is not in list')
            pass    
    return parameter, id_list

def M1809_Update():
    '''
    更新数据库
    '''
    print('start to update finnance data,please wait...')
    for item in id_list:
            #此段增加判断逻辑，如果数据库已经是最新的，则不必更新了
            
            #
            print(id)
            cbfx = crawling_finance_table.crawling_finance('',id,'')
            cbfx.crawling_update()
    print('update finished!') 

#############################################################################
if __name__ =='__main__':
    para,list_id = M1809_config()
