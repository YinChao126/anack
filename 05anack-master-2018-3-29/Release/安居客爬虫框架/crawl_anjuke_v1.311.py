# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:30:50 2017
@author: 1707501
"""

"""
crawling anjuke house price 
GuiYang
20171212 add proxy and detailed the parse of house information
20171214 add spidertime and multiprocess
"""

import requests
from bs4 import BeautifulSoup
import pymysql
import random,time

def parse_detial(html):
    soup = BeautifulSoup(html.text,'html5lib')
    houseinfo = soup.select('div.houseInfoBox')
    houseinfotitle = houseinfo[0].h4
    an_xian = houseinfotitle.select('span.anxian')[0].get_text()
    if '假一赔百' in an_xian:
        an_xian = "Yes"
    else:
        an_xian = "No"
    houseencode= houseinfotitle.select('span.house-encode')[0].get_text()
    houseinfoV2 = houseinfo[0].select('div.houseInfoV2-desc')[0].get_text()
    housedetail1 = houseinfoV2.split()
    housedetail2 = ':'.join(housedetail1)
    housedetail = housedetail2.replace('\ue092','').replace('\u200b','').replace('\ue094','').replace('\ue093','').replace('\ue095','')
    housefirstv = soup.select('div.first-col.detail-col')[0].find_all('dl')
    house_estate = ''.join(housefirstv[0].get_text().split())[3:]
    house_add  = ''.join(housefirstv[1].get_text().split())[3:]
    house_build_time = ''.join(housefirstv[2].get_text().split())[3:]
    house_type = ''.join(housefirstv[3].get_text().split())[3:]
    housesecondv = soup.select('div.second-col.detail-col')[0].find_all('dl')
    house_model_detail = ''.join(housesecondv[0].get_text().split())[3:]
    house_size = ''.join(housesecondv[1].get_text().split())[3:]
    house_orientation = ''.join(housesecondv[2].get_text().split())[3:]
    house_floor = ''.join(housesecondv[3].get_text().split())[3:]
    housethirdv = soup.select('div.third-col.detail-col')[0].find_all('dl')
    house_decorate = ''.join(housethirdv[0].get_text().split())[5:]
    house_univalence = ''.join(housethirdv[1].get_text().split())[5:]
    down_payment = ''.join(housethirdv[2].get_text().split())[5:]
#   monthly_payment = ''.join(housethirdv[3].get_text().split())[5:] #javescript loading data
    salerinfo = soup.select('p.broker-mobile')
    salerphone = salerinfo[0].get_text().replace('\ue047','')
    housetitle = ''.join(soup.select('h3.long-title')[0].get_text().split())
    houseinfov1 = soup.select('div.basic-info.clearfix')[0].find_all('span')
    housetotleprice = houseinfov1[0].get_text()
#==============================================================================
#     housemodel = houseinfov1[1].get_text()
#     housesize = houseinfov1[2].get_text()
#==============================================================================
    line = []
    line.append(housetitle)
    line.append(an_xian)
    line.append(houseencode)
    line.append(housetotleprice)
    line.append(house_model_detail)
    line.append(house_size)
    line.append(house_estate)
    line.append(house_add)
    line.append(house_build_time)
    line.append(house_type)
    line.append(house_orientation)
    line.append(house_floor)
    line.append(house_decorate)
    line.append(house_univalence)
    line.append(down_payment)
    line.append(housedetail)
    line.append(salerphone)
    result = '\t'.join(line)
    print(result)
    return result

def parse_list(html):
    secondurl = []
    soup = BeautifulSoup(html.text,'html5lib')
    houselists = soup.select('a.houseListTitle')
    for houseid in houselists:
        houseurl = houseid['href']
        secondurl.append(houseurl)
    return secondurl

def downloadhtml(url,proxy_ip):
    response = requests.get(url,headers=header,proxies={"http":proxy_ip})
    if response.status_code == 200:
        return response
    else:
        print("download html error!")


def Create_table():
    query = """CREATE TABLE IF NOT EXISTS `anjuke_collecter_original_test` (
`No` int(10) unsigned NOT NULL AUTO_INCREMENT,
`housetitle`    varchar(255) DEFAULT NULL,
`an_xian`    varchar(255) DEFAULT NULL,
`houseencode`    varchar(255) DEFAULT NULL,
`housetotleprice`    varchar(255) DEFAULT NULL,
`house_model_detail`    varchar(255) DEFAULT NULL,
`house_size`    varchar(255) DEFAULT NULL,
`house_estate`    varchar(255) DEFAULT NULL,
`house_add`    varchar(255) DEFAULT NULL,
`house_build_time`    varchar(255) DEFAULT NULL,
`house_type`    varchar(255) DEFAULT NULL,
`house_orientation`    varchar(255) DEFAULT NULL,
`house_floor`    varchar(255) DEFAULT NULL,
`house_decorate`    varchar(255) DEFAULT NULL,
`house_univalence`    varchar(255) DEFAULT NULL,
`down_payment`    varchar(255) DEFAULT NULL,
`housedetail`    text DEFAULT NULL,
`salerphone`    varchar(255) DEFAULT NULL,
`Url`  varchar(255) DEFAULT NULL,
`SpiderTime`  varchar(255) DEFAULT NULL,
PRIMARY KEY (`No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()


def etl_mysql(result):
    db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    cursor = db.cursor()
    result = tuple(result)
    query = "insert into anjuke_collecter_original_test(housetitle,an_xian,houseencode,housetotleprice,house_model_detail,house_size,house_estate,house_add,house_build_time,house_type,house_orientation,house_floor,house_decorate,house_univalence,down_payment,housedetail,salerphone,Url,SpiderTime) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % result
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    

def get_next_page(html):
    soup = BeautifulSoup(html.text,'html5lib')
    nexturl = soup.select('a.aNxt')[0]['href']
    return nexturl

def get_proxy_ip():
    db = pymysql.connect(host = hosts,user = users, password = passwords, database = databases,charset='utf8')
    cursor = db.cursor()
    query = "select ip,port from ip_collecter_original_test limit 17000"
    cursor.execute(query)
    ip_result = cursor.fetchall()
    IPList = []
    for i in ip_result:
        Ip = i[0] + ":" + i[1]
        IPList.append(Ip)
    return IPList

def check_ip(IPList):
    url = "https://www.baidu.com/"
    proxy_ip = random.choice(IPList)
    res = requests.get(url,headers=header,proxies={"http":proxy_ip})
    if res.status_code == 200:
        print(proxy_ip)
        return proxy_ip
    else:
        return None    # 后期修改成迭代
    
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
          'Connection':'keep-alive'          }

# https://gy.anjuke.com/sale/p1/#filtersort
# https://shanghai.anjuke.com/sale/p1/#filtersort
# https://hangzhou.anjuke.com/sale/
url = "https://shanghai.anjuke.com/sale/p1/#filtersort"

hosts = 
users = 
passwords = 
databases = 

if __name__ == '__main__':
    List_ip = get_proxy_ip()
    next_url = url
    Create_table()
    while next_url != None:
        proxy_ip = check_ip(List_ip)
        res = downloadhtml(url,proxy_ip)
        if res != None:
            try:
                urllist = parse_list(res)
            except:
                print('house url list parsing error!')
            if urllist != None:
                for houseurl in urllist:
                    proxy_ip = check_ip(List_ip)
                    houseinfor = downloadhtml(houseurl,proxy_ip)
                    try:
                        results = parse_detial(houseinfor)
                    except:
                        results = None
                        with open(r'E:\documents\personal\python\crawler\anjuke\anjuke_error_shanghai.txt','a',encoding='utf-8') as f:
                            f.write(houseurl +"\n")
                        print("parse hosue detial infor error!")
                        continue
                    with open(r'E:\documents\personal\python\crawler\anjuke\anjuke_shanghai_v15.txt','a',encoding='utf-8') as f:
                        f.write(results + '\n')
                    try:
                        line = results.split('\t')
                        ts = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                        line.append(houseurl)
                        line.append(ts)
#                        print(line)
                        etl_mysql(line)
                    except:
                        print("data insert into mysql error!")
                        continue
            try:
                next_url = get_next_page(res)
            except:
                next_url = None
    print("crawling end!")