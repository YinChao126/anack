# 作者：翦林鹏
# 更新日期：2018-3-25
# 版本号：V0.1
# 描述：实现了宇通客车产销数据的自动入库
#环境搭建：
#1、安装firefox浏览器
#2、安装selenium库（pip install selenium）
#3、安装selenium webdriver浏览器驱动
#   地址：https://github.com/mozilla/geckodriver/releases/   下载geckodriver-vo.20.0-win64.zip或geckodriver-vo.20.0-win32.zip
#   下载解压后，将geckodriver.exe发到Python的安装目录，例如 D:\python 。 然后再将Python的安装目录添加到系统环境变量的Path下面。
#4、安装autoit 地址：https://www.autoitscript.com/site/autoit/downloads/ 默认安装即可
# 使用说明：
# 1. 请将UpfileWithPara.exe（用于文件上传）文件下载到本地，并把其路径赋值给ExeAdr
# 2. 确保DownloadAdr下没有任何重要的文件，因为程序会将DownloadAdr文件夹下面的所有文件清空
# 3. 起始年月默认为2017.6，根据需要修改
# 4. 输入连接数据库的用户名、密码等，点击运行即可
# 版本缺点
# 1、依赖在线pdf转excel网站，转换出来的excel可能发生格式错位
# 2、模拟网页操作，速度相对较慢
#-------------------------------------------------------------------------------------------
# 作者：翦林鹏
# 更新日期：2018-5-15
# 版本号：V0.2
# 描述：优化pdf数据获取
#环境搭建：
#1、下载pdf2htmlex
#   下载地址：http://soft.rubypdf.com/software/pdf2htmlex-windows-version，下载后缀为win32-static的版本
#2、解压pdf2htmlex
# 使用说明：
# 1. 将pdf2htmlex解压地址赋值给ExeAdr
# 2. 确保DownloadAdr下没有任何重要的文件，因为程序会将DownloadAdr文件夹下面的所有文件清空
# 3. 起始年月默认为2017.6，根据需要修改
# 4. 输入连接数据库的用户名、密码等，点击运行即可

#--------------------------------------------------------------------


# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 17:22:21 2018

@author: JianLpeng
"""
import pymysql
import PdfDown
import subprocess
from lxml import etree
import os
import datetime
import sys

parent_path = os.path.dirname(sys.argv[0])
list = parent_path.split('/')
WindowsPath = ''
for part in  list:
    WindowsPath = WindowsPath+part+'\\'

class ProductionSaleToSql:
    def __init__(self,YearBegin = 2017,MonthBegin = 6):
        try:
            with open('./config/account.txt', 'r') as fh:
                account = fh.readlines()
        except:
            print('fail to initialize.')
            return
       
        self.host = account[0].strip()       
        self.user = account[1].strip()                      #用户名 
        self.password = account[2].strip()              #密码
        self.database = account[3].strip()              #数据库
        self.stock_code = "600066"          #股票代码
        self.StockName = "宇通客车"           #股票名称
        
        #初始化文件下载区
        self.DownloadAdr =  parent_path+r"/PdfDownload/"    #下载路径
        isExists=os.path.exists(self.DownloadAdr)
        if not isExists:
            os.makedirs(self.DownloadAdr)
    
            
        
        self.YearBegin = YearBegin            #起始日期
        self.MonthBegin = MonthBegin          #结束日期
        self.ExeAdr=WindowsPath+'\\ExeFile\\'+"pdf2htmlEX.exe"
    

        # 所有的字段列表   
        self.AllField ='''(`stock_code`,`stock_name`,`year`,`month`,`production`,`SPLY_production`,`moth_changeP`,`cumulativeP`,`SPLY_cumulativeP`,`cumulativeP_changeP`,`large_production`,`SPLY_production_large`,\
        `month_changeP_large`,`cumulativeP_large`,`SPLY_cumulativeP_large`,`cumulativeP_changeP_large`,`mid_production`,`SPLY_production_mid`,`month_changeP_mid`,`cumulativeP_mid`,\
        `SPLY_cumulativeP_mid`,`cumulativeP_changeP_mid`,`small_production`,`SPLY_production_small`,`month_changeP_small`,`cumulativeP_small`,`SPLY_cumulativeP_small`,\
        `cumulativeP_changeP_small`,`sale`,`SPLY_sale`,`moth_changeS`,`cumulativeS`,`SPLY_cumulativeS`,`cumulativeS_changeS`,`large_sale`,`SPLY_sale_large`,`month_changeS_large`,\
        `cumulativeS_large`,`SPLY_cumulativeS_large`,`cumulativeS_changeS_large`,`mid_sale`,`SPLY_sale_mid`,`month_changeS_mid`,`cumulativeS_mid`,`SPLY_cumulativeS_mid`,`cumulativeS_changeS_mid`,\
        `small_sale`,`SPLY_sale_small`,`month_changeS_small`,`cumulativeS_small`,`SPLY_cumulativeS_small`,`cumulativeS_changeS_small`)'''

      
    #建表
     #命名规则 P：生产量 S：销售量  SPLY：去年同期
    def CreatePSTable(self):
        cmd = '''CREATE TABLE IF NOT EXISTS `ProductionSale` (
    `stock_code` VARCHAR(100),                           #股票代码
    `stock_name` VARCHAR(100),                           #股票名称
    `year` VARCHAR(100),                                 #年
    `month` VARCHAR(100),                                #月
    `production` VARCHAR(100),                           #当月生产量
    `SPLY_production` VARCHAR(100),                      #去年同期（生产量）
    `moth_changeP` VARCHAR(100),                         #当月数量同比变动（生产量）
    `cumulativeP` VARCHAR(100),                          #本年累计（生产量）
    `SPLY_cumulativeP` VARCHAR(100),                     #去年同期累计（生产量）
    `cumulativeP_changeP` VARCHAR(100),                  #累计数量同比变动（生产量）
    `large_production` VARCHAR(100),                     #当月生产量（大型生产量）
    `SPLY_production_large` VARCHAR(100),                #去年同期（大型生产量）
    `month_changeP_large` VARCHAR(100),                  #单月数量同比变动（大型生产量）
    `cumulativeP_large` VARCHAR(100),                    #本年累计（大型生产量）
    `SPLY_cumulativeP_large` VARCHAR(100),               #去年同期累计（大型生产量）
    `cumulativeP_changeP_large`VARCHAR(100),             #累计数量同比变动（大型生产量）
    `mid_production` VARCHAR(100),                       #当月生产量（中型生产量）
    `SPLY_production_mid` VARCHAR(100),                  #去年同期（中型生产量）
    `month_changeP_mid` VARCHAR(100),                    #当月数量同比变动（中型生产量）
    `cumulativeP_mid` VARCHAR(100),                      #本年累计（中型生产量）
    `SPLY_cumulativeP_mid` VARCHAR(100),                 #去年同期累计（中型生产量）
    `cumulativeP_changeP_mid` VARCHAR(100),              #累计数量同比变动（中型生产量）
    `small_production` VARCHAR(100),                     #当月生产量（轻型生产量）
    `SPLY_production_small` VARCHAR(100),                #去年同期（轻型生产量）
    `month_changeP_small` VARCHAR(100),                  #当月数量同比变动（轻型生产量）
    `cumulativeP_small` VARCHAR(100),                    #本年累计（轻型生产量）
    `SPLY_cumulativeP_small` VARCHAR(100),               #去年同期累计（轻型生产量）
    `cumulativeP_changeP_small` VARCHAR(100),            #累计数量同比变动（轻型生产量）
    `sale` VARCHAR(100),                                 #当月销售量
    `SPLY_sale` VARCHAR(100),                            #去年同期（当月销售量）
    `moth_changeS` VARCHAR(100),                         #单月数量同比变动（当月销售量）
    `cumulativeS` VARCHAR(100),                          #本年累计（销售量）
    `SPLY_cumulativeS` VARCHAR(100),                     #去年同期累计（销售量）
    `cumulativeS_changeS` VARCHAR(100),                  #累计数量同比变动（销售量）
    `large_sale` VARCHAR(100),                           #当月销售量（大型销售量）
    `SPLY_sale_large` VARCHAR(100),                      #去年同期（大型销售量）
    `month_changeS_large` VARCHAR(100),                  #单月数量同比变动（大型销售量）
    `cumulativeS_large` VARCHAR(100),                    #本年累计（大型销售量）
    `SPLY_cumulativeS_large` VARCHAR(100),               #去年同期累计（大型销售量）
    `cumulativeS_changeS_large`VARCHAR(100),             #累计数量同比变动（大型销售量）
    `mid_sale` VARCHAR(100),                             #当月销售量（中型销售量）
    `SPLY_sale_mid` VARCHAR(100),                        #去年同期（大型销售量）
    `month_changeS_mid` VARCHAR(100),                    #当月数量同比变动（大型销售量）
    `cumulativeS_mid` VARCHAR(100),                      #本年累计（大型销售量）
    `SPLY_cumulativeS_mid` VARCHAR(100),                 #去年同期累计（大型销售量）
    `cumulativeS_changeS_mid` VARCHAR(100),              #累计数量同比变动（大型销售量）
    `small_sale` VARCHAR(100),                           #小型当月销售量（小型销售量）
    `SPLY_sale_small` VARCHAR(100),                      #去年同期（小型销售量）
    `month_changeS_small` VARCHAR(100),                  #单月数量同比变动（小型销售量）
    `cumulativeS_small`  VARCHAR(100),                   #本年累计（小型销售量）
    `SPLY_cumulativeS_small` VARCHAR(100),               #去年同期累计（小型销售量）
    `cumulativeS_changeS_small` VARCHAR(100),            #累计数量同比变动（小型销售量）
    primary key (`stock_code`,`year`,`month`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
        db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        cursor.close()
        db.close()
    
    #数据库插入
    def InsertPSTable(self):
        sql = '''INSERT INTO `ProductionSale` (`stock_code`,`stock_name`,`year`,`month`)
                 VALUES (600360,'宇通客车',2018,3)'''
        db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        
    #数据库查询，返回查询结果  
    def QueryPSTable(self,years,months):
        
        sql = "SELECT * FROM `ProductionSale` WHERE `stock_code`="+self.stock_code+" AND `year`="+years+" AND `month`="+months
                 
        db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        rs=cursor.fetchall()
        flag = -1
        if rs:
            flag = 0
        else:
            flag = -1
        cursor.close()
        db.close()
        return flag
    
    
    
    def QueryPSData(self,years,months,fieldName):
       
        sql = "SELECT "+fieldName+" FROM `ProductionSale` WHERE `stock_code`="+self.stock_code+" AND `year`="+years+" AND `month`="+months
                 
        db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        rs=cursor.fetchall()
        if rs:
            data=int(rs[0][0].replace(',',''))
        else:
            data=-1
            print ("error! There is no record in the database!")
        cursor.close()
        db.close()
        return data

    
    
 
    def CMDRun(self,cmd):
        #print('start executing cmd...')
        s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stderrinfo, stdoutinfo = s.communicate()
        #print('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo))
        #print('finish executing cmd....')
        return s.returncode
    
    def PDF2Html(self,PDFList):
        os.makedirs(self.DownloadAdr+'/HTML')
        print ("Transform PDF to Html...")
        HtmlAdd = WindowsPath + 'PdfDownload\HTML'
        PdfAdd = WindowsPath+'PdfDownload\\'
        cmd2 =r' --dest-dir '
        cmd2 = cmd2 + HtmlAdd+' '+PdfAdd
        HtmlList=[]
        for PDFFile in PDFList:
            DatePDF=PDFFile.split('_')[-2]
            year=(int)(DatePDF[0:4])
            month=(int)(DatePDF[4:6])
            datePDF =datetime.date(year,month,1)
            date=datePDF+datetime.timedelta(days = -1)
            #print (date)
            if (self.QueryPSTable(str(date.year),str(date.month))==-1):
                HtmlName= PDFFile.split('.')[0]+'.html'
                CMD=self.ExeAdr+cmd2+PDFFile+' '+HtmlName
                print ("transform "+PDFFile)
                self.CMDRun(CMD)
                HtmlList.append(HtmlName)
                print ('done')
            else:
                print(self.StockName+str(date.year)+'年'+str(date.month)+'月已有记录')       
        print ("Transform done!")
        #print (HtmlList)
        return HtmlList
        
          
    def HtmlScrap(self,HtmlList):
        for Htmlname in HtmlList:
            HtmlPath=self.DownloadAdr+'HTML/'+Htmlname
            print ('HtmlPath',HtmlPath)
            YMD=Htmlname.split('_')[-2]
        
            month=YMD[4:6]
            if (month[0]=='0'):
                month=month[1:]
            
            year=YMD[0:4]
            dateHtml=datetime.date(int(year),int(month),1)
            date=dateHtml+datetime.timedelta(days = -1)
            htmlf=open(HtmlPath,'r',encoding="utf-8")
            html=htmlf.read()
            selector=etree.HTML(html)
            #element='//*[@id="pf1"]/div[1]/div[21]/div'
            lls=[self.stock_code,self.StockName]

#            if ((selector.xpath('//*[@id="pf1"]/div[1]/div[3]/text()')[0])=='证券代码：'):
#                offset=20
#
#            else:
#                offset=18
          
            try:
                path1='//*[@id="pf1"]/div[1]/div['
                path2=']/div/text()' 
                for i in range(0,100):
                    LocPath=path1+str(i)+path2
                    LocElement=selector.xpath(LocPath)
                   
                    if (LocElement!=[] and LocElement[0]=='生产量' ):
                        offset=i
                        break
                print (offset)
             
                year =str(date.year)
                month = str(date.month)
                lls.append(str(date.year))
                lls.append(str(date.month))
                for i in range(0,8):
                    for j in range(1,7):
                        num=str(j+i*7+offset)
                        path=path1+num+path2
                        content=selector.xpath(path)
                        #print(content)
                        lls.append(content[0])
                #print (lls)
                DataTuple=tuple(lls)
                DataStr = str(tuple(DataTuple))
                sql = "INSERT INTO `ProductionSale`"+" "+self.AllField+" "+"VALUES"+" "+DataStr
                db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,charset="utf8")
                cursor = db.cursor()
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
                print(self.StockName+year+'年'+month+'月入库成功')
            except:
                 print(self.StockName+year+'年'+month+'月入库失败')
            finally:
                htmlf.close()
            

      
    def ProSaleUpdate(self):
        self.CreatePSTable()
        downLoad = PdfDown.PdfDownLoad(self.YearBegin,self.MonthBegin,self.DownloadAdr)
        downLoad.GetAllPdfFile()
        #print (downLoad.pdfList)
        HtmlList=self.PDF2Html(downLoad.pdfList)
        self.HtmlScrap(HtmlList)
#        TxtTrans = PDF_TXT.PDFToTXT(PDFList=downLoad.pdfList)
#        TxtTrans.TransAll()
#        for Txt in TxtTrans.TxtList:
#            txtAdd=self.DownloadAdr+'/'+Txt
#            self.TxtToSql(txtAdd)
#            print (Txt+'入库成功')
            
     
if __name__ == "__main__":

    Update = ProductionSaleToSql(YearBegin = 2016,MonthBegin = 5)
    Update.ProSaleUpdate()

    
"""
self.user = user                      #用户名 
self.password = password              #密码
self.database = database              #数据库
self.stock_code = stock_code          #股票代码
self.StockName = StockName            #股票名称
self.DownloadAdr = DownloadAdr        #下载路径
self.ExeAdr = ExeAdr                  #可执行文件路径
self.YearBegin = YearBegin            #起始日期
self.MonthBegin = MonthBegin          #结束日期
日期要大于2015年8月（因为这之前的格式会发生变化）
"""
