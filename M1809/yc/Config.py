# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 01:47:40 2018

@author: yinchao
"""
import sys
sys.path.append('../..')

from datetime import datetime
import crawling_finance_table
import pymysql
import os
def Connect_sql(account):
    conn = pymysql.connect(
            host = account[0].strip(),
            port = 3306,
            user = account[1].strip(),
            passwd = account[2].strip(),
            db = account[3].strip(),
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
    2. 读取公司名称列表，并转换成id（如果输入无法解析成id，会自动剔除）
    3. 更新该公司的财务报表，以备以后使用
    注意：文件名不可改
    '''
    del parameter[:]
    with open ('./config/parameter_list.txt','r',encoding = 'utf-8') as fh:
        ct = fh.readlines()
    
    
    for s in ct:
        items = s.strip()
        if items != '': 
            if items[0] == '#': #剔除注释部分
                break
            parameter.append(items)
    
    del id_list[:]
    with open('./config/company_list.txt','r', encoding = 'utf-8') as fh:
        ct = fh.readlines()
    company = []
    for s in ct:
        if s.strip() != '': 
            company.append(s.strip())
    try:
        with open('./config/account.txt', 'r') as fh:
            account = fh.readlines()
    except:
        print('fail to initialize.')
        return
    cur = Connect_sql(account)
    for name in company:
        cmd = "select * from anack_classify where name = \'"+name+"\';"
        cur.execute(cmd)
        result = cur.fetchall()
        try:
            id = result[0][0] 
            id_list.append(id)
            
        except: #错误的ID号不会被解析（刚上市的，不会出现在anack_classify里，需要更新）
            print(name+' is not in list')
            pass   
    try:
        os.mkdir('.//output')
    except:
        pass 
#    print(id_list)
    M1809_Update(cur, id_list)
    return cur, parameter, id_list


def M1809_Update(cur, id_list):
    '''
    更新数据库
    '''
    print('check for update,please wait...')
    for item in id_list:
            cmd = "select * from Profit where h29 = \'" + item + "\' and h30 = \'" + str(datetime.now().year - 1)+"-12-31\';"
            cur.execute(cmd)
            result = cur.fetchall()
            try:
                trash_data = result[0] #获得资产负债表信息
            except:
                print('updating ', item)
                cbfx = crawling_finance_table.crawling_finance('',item,'')
                cbfx.crawling_update()
    print('update check finished!') 

#############################################################################
if __name__ =='__main__':
    cur, para,list_id = M1809_config()     
    cmd = "select * from Profit where h29 = 600887;"            
    cur.execute(cmd)
    result = cur.fetchall()
    print(len(result))
