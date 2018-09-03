# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 01:47:40 2018

@author: yinchao
"""
import sys
sys.path.append('../..')

from datetime import datetime
import crawling_finance_table
import crawling_finance_table_v1_7
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
    print(account)
    print("\nconnect to aliyun success!\n")
    return cur




global parameter
parameter = [
 '总资产',
 '净资产',
 '资产负债比',
 '流动资产',
 '一年内到期的长期负债',
 '应收账款',
 '预收账款',
 '存货',
 '营业收入',
 '营业成本',
 '营业税金及附加',
 '财务费用',
 '营业外收入',
 '净利润',
 '除非净利润',
 '每股收益',
 '经营净额',
 '投资净额',
 '筹资净额',
 '汇率影响',
 '现金净增加额',
 '期末现金余额',
 '流动比率',
 '资产周转率',
 '存货周转率',
 '溢价比',
 '市盈率',
 '市净率',
 '名义净资产收益率',
 '真实净资产收益率',
 '毛利率',
 '营收增长率',
 '除非净利润增长率',
 '股息率',
 '分红率']

global company_id_list
company_id_list = ['000651', '000333', '600690'] #此处可以修改
global data_base_path
data_base_path = '../history_data/'

global data_src
global cur

def M1809_config(company_list, mode = 'CSV'):
    '''
    本地模式配置
    只需要提供感兴趣的对比公司即可，如果只有一个，说明只进行自主分析
    '''
    global data_base_path
    global data_src
    global cur
    global parameter
    global company_id_list
    data_src = mode
    print('please wait, check for updating...')
     
    try: #自动检查并创建文件夹
        os.mkdir('../history_data')
    except:
        pass 
    try: #自动检查并创建文件夹
        os.mkdir('../sys_config')
    except:
        pass 
    try: #自动检查并创建文件夹
        os.mkdir('../output')
    except:
        pass 
    
    if len(company_list) < 2:
        print('最少需要输入2个id作为对比')
        return
    
    if data_src == 'SQL' or data_src == 'sql':
        '''
        网络模式配置
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
        id_list = []
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
#        print(id_list)
#        return parameter, company_list
        M1809_Update(cur, company_list)
    
    elif data_src == 'CSV' or data_src == 'csv':  
        for item in company_list:
            try:
                file_name = data_base_path + item + '_profit.csv'
    #            print(file_name)
                with open(file_name, 'r') as fh:
                    from datetime import datetime
                    from dateutil.parser import parse
                    from dateutil.relativedelta import relativedelta
                    content = fh.readlines()
                    s = content[-1].split(',')
                    latest_record = parse(s[0]) #获取最新时间
                    
                    current_day = datetime.now() - relativedelta(months=+12) 
                    if latest_record > current_day:
                        pass
                    else:
                        cbfx = crawling_finance_table_v1_7.crawling_finance(data_base_path,item)
                        cbfx.crawling_update()                    
            except:
                cbfx = crawling_finance_table_v1_7.crawling_finance(data_base_path,item)
                cbfx.crawling_update() 
    else:
        print('模式设置错误，请二选一：CSV/SQL') 
        
    print('finished!')
    company_id_list = company_list
    
def M1809_Update(cur, id_list):
    '''
    更新数据库
    '''
    print('check for update,please wait...')
#    print(id_list)
    for item in id_list:
        try:
            
            cmd = "select * from zichanfuzhai where h79 = \'" + item + "\' and h80 = \'" + str(datetime.now().year - 1)+"-12-31\';"
            cur.execute(cmd)
            result1 = cur.fetchall()
        except:
            print('updating ', item)
            cbfx = crawling_finance_table.crawling_finance('',item,'')
            cbfx.crawling_update()
            continue
        
        try:
            cmd2 = "select * from cashFlow where h72 = \'" + item + "\' and h73 = \'" + str(datetime.now().year - 1)+"-12-31\';"
            cur.execute(cmd2)
            result2 = cur.fetchall()
        except:
            print('updating ', item)
            cbfx = crawling_finance_table.crawling_finance('',item,'')
            cbfx.crawling_update()
            continue
            
        try:
            cmd3 = "select * from Profit where h29 = \'" + item + "\' and h30 = \'" + str(datetime.now().year - 1)+"-12-31\';"
            cur.execute(cmd3)
            result3 = cur.fetchall()
            trash_data = result3[0] #获得资产负债表信息
        except:
            print('updating ', item)
            cbfx = crawling_finance_table.crawling_finance('',item,'')
            cbfx.crawling_update()
            continue
        
    print('update check finished!') 

#############################################################################
if __name__ =='__main__':
    id_list = ['000651', '000333', '600690']
    #网络测试
    M1809_config(id_list, 'SQL')     
    
    #本地测试
#    M1809_config(id_list, 'CSV')
        