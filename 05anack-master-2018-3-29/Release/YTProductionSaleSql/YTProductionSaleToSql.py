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
#--------------------------------------------------------------------

import pymysql
import xlrd
import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FolderNotCleanException (Exception):
    pass

class UnfoundExcelFileException (Exception):
    pass

class ProductionSaleToSql:
    def ParametersSet(self,user,password,database,stock_code,StockName,DownloadAdr,ExeAdr,YearBegin = 2017,MonthBegin = 6):
        self.user = user                      #用户名 
        self.password = password              #密码
        self.database = database              #数据库
        self.stock_code = stock_code          #股票代码
        self.StockName = StockName            #股票名称
        self.DownloadAdr = DownloadAdr        #下载路径
        self.ExeAdr = ExeAdr                  #可执行文件路径
        self.YearBegin = YearBegin            #起始日期
        self.MonthBegin = MonthBegin          #结束日期
        # 所有的字段列表   
        self.AllField ='''(`stock_code`,`stock_name`,`year`,`month`,`production`,`SPLY_production`,`moth_changeP`,`cumulativeP`,`SPLY_cumulativeP`,`cumulativeP_changeP`,`large_production`,`SPLY_production_large`,\
        `month_changeP_large`,`cumulativeP_large`,`SPLY_cumulativeP_large`,`cumulativeP_changeP_large`,`mid_production`,`SPLY_production_mid`,`month_changeP_mid`,`cumulativeP_mid`,\
        `SPLY_cumulativeP_mid`,`cumulativeP_changeP_mid`,`small_production`,`SPLY_production_small`,`month_changeP_small`,`cumulativeP_small`,`SPLY_cumulativeP_small`,\
        `cumulativeP_changeP_small`,`sale`,`SPLY_sale`,`moth_changeS`,`cumulativeS`,`SPLY_cumulativeS`,`cumulativeS_changeS`,`large_sale`,`SPLY_sale_large`,`month_changeS_large`,\
        `cumulativeS_large`,`SPLY_cumulativeS_large`,`cumulativeS_changeS_large`,`mid_sale`,`SPLY_sale_mid`,`month_changeS_mid`,`cumulativeS_mid`,`SPLY_cumulativeS_mid`,`cumulativeS_changeS_mid`,\
        `small_sale`,`SPLY_sale_small`,`month_changeS_small`,`cumulativeS_small`,`SPLY_cumulativeS_small`,`cumulativeS_changeS_small`)'''

    #清空文件夹
    def FolderClean(self):
        for i in os.listdir(self.DownloadAdr):
           path_file = os.path.join(self.DownloadAdr,i)  # 取文件路径
           if os.path.isfile(path_file):
               os.remove(path_file)
        #文件夹必须清理干净，否则会影响后面的流程
        if os.listdir(self.DownloadAdr):   #如果文件夹没有清理干净，抛出异常
            raise FolderNotCleanException
    
   #在目录下查询excel文档    
    def FindExcelFile(self):
        ExcelPath = ""
        for i in os.listdir(self.DownloadAdr):
           path_file = os.path.join(self.DownloadAdr,i)  # 取文件路径
           if (path_file.find('.xlsx')!=-1 or path_file.find('.xls')!=-1):  #查找后缀为.xlsx或.xls的文件
               ExcelPath = path_file
        if ExcelPath:
            return ExcelPath
        else:
            raise UnfoundExcelFileException
      
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
        db = pymysql.connect(user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        cursor.close()
        db.close()
    
    #数据库插入
    def InsertPSTable(self):
        sql = '''INSERT INTO `ProductionSale` (`stock_code`,`stock_name`,`year`,`month`)
                 VALUES (600360,'宇通客车',2018,3)'''
        db = pymysql.connect(user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        
    #数据库查询，返回查询结果  
    def QueryPSTable(self,years,months):
        
        sql = "SELECT * FROM `ProductionSale` WHERE `stock_code`="+self.stock_code+" AND `year`="+years+" AND `month`="+months
                 
        db = pymysql.connect(user=self.user,password=self.password,database=self.database,charset="utf8")
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
        

    
    #excel文件入库
    def ExcelToSql(self,ExcelAdr,Year,Month):
        data = xlrd.open_workbook(ExcelAdr)
        table =data.sheets()[0]
        nrows =table.nrows
        DataInsert = [self.stock_code,self.StockName,Year,Month]
        for i in range(nrows):
            if (table.row_values(i)[0]=='生产量'):
                #测试发现，“生产量”这一列后可能有一行空列
                if table.row_values(i)[1]:
                    ColumnAdd=0
                else:
                    ColumnAdd = 1 #如果存在空行，则列数加1
                break;
        for j in range(i,i+8):
                DataInsert.extend(table.row_values(j)[1+ColumnAdd:7+ColumnAdd])
        DataTuple=tuple(list(DataInsert))
        DataStr = str(tuple(DataTuple))
        sql = "INSERT INTO `ProductionSale`"+" "+self.AllField+" "+"VALUES"+" "+DataStr
        db = pymysql.connect(user=self.user,password=self.password,database=self.database,charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        
       
  
    
    
    
    #获取最后更新的日期
    def DateLastUpdate(self,driver):
        content = driver.find_element_by_xpath("//div[@id='sse_query_list']/dl/dd/a/span").text
        date = content.split('-')
        year = date[0]
        month = date[1]
        return (year,month)
    
    
    #下载某年某月的产销快报
    def DownloadPDF(self,driver,year,month):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self.DownloadAdr)
        fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        driverPDF = webdriver.Firefox(firefox_profile=fp)
        
        
        XpathTitle =self.StockName+year+"年"+month+"月份产销数据快报"
        title = "//a[@title=\'"+XpathTitle+"\']"
        href=driver.find_element_by_xpath(title).get_attribute('href')
        list=href.split('/')
        PDF_name=list[-1]
        
        driverPDF.get(href)
        driverPDF.implicitly_wait(10)
        driverPDF.find_element_by_id("download").click()
        driverPDF.quit()
        #driver.back()
        return PDF_name
    
    #PDF转excel
    def PdfToExcel(self,fileName,driver):
        #driver.find_element_by_xpath("//div[@class = 'settings']/div[2]/a[2]").click()  #此语句可以
        driver.find_element_by_id("filePicker").click()
        fileAdr = self.DownloadAdr+'\\'+fileName
        os.system(self.ExeAdr+" "+"firefox"+" "+fileAdr)
        time.sleep(4) 
        driver.find_element_by_xpath("//div[@class = 'btns']/a").click()
        #设置显示等待，等待时间不超过50s，每隔0.5检查一次
        locator = (By.CLASS_NAME, 'downloadBtn')
        WebDriverWait(driver, 50, 0.5).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//div[@class = 'btns']/a[3]").click()
        driver.refresh()
    
    
      
    

    def ProSaleUpdate(self):
        self.CreatePSTable()
        #配置产销快报页面参数，实现pdf自动下载  
        try:
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", self.DownloadAdr)
            fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
            fp.set_preference("pdfjs.disabled", True)
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            driver = webdriver.Firefox(firefox_profile=fp)
            #driver.maximize_window()
            #打开页面
            url = "http://www.sse.com.cn/home/search/?webswd="+self.StockName+"产销快报"
            driver.get(url)
        
            
            #配置pdf转excel页面参数，实现excel文件自动下载
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.dir', self.DownloadAdr)
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            #profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.ms-excel')
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet ')
            driverEx = webdriver.Firefox(firefox_profile=profile)
            #打开页面
            urlEx = "http://app.xunjiepdf.com/pdf2excel"
            driverEx.get(urlEx)
            #driverEx.implicitly_wait(4)
        
            #设置隐式等待，括号中的参数为最大等待时间，如果在最大等待时间内，页面加载完成，则等待立结束，否则抛出异常
            #整个driver的时间内，该设置只用设置一次
            driver.implicitly_wait(100)
            driverEx.implicitly_wait(50)
            
            #从产销快报页面获取最新一次更新的日期，月份-1作为获取数据的起始年、月参数
            (year,month)=self.DateLastUpdate(driver)
            if (month=="1"):
                YearInt = int(year)-1
                MonthInt= 12
            else:
                YearInt = int(year)
                MonthInt= int(month) -1       
        
            #清空下载文件夹，避免历史文件的干扰
            self.FolderClean()
            DateBegin =datetime.date(YearInt,MonthInt,1)
            DateEnd = datetime.date(self.YearBegin,self.MonthBegin,1)
            #count用于计数，因为一个页面只有10条数据，所以每隔10条需要翻页
            count = 0
            for i in range(0,(DateBegin-DateEnd).days+1,1):
                day = DateBegin -datetime.timedelta(days=i)
                if (day.day == 1):
                    count = count+1
                    YearExact = day.year
                    MonthExact = day.month
                    try:
                        if(count==11):
                            driver.find_element_by_id('Next').click()
                            count=0
                        TrueOrFalse = self.QueryPSTable(years=str(YearExact),months=str(MonthExact))
                        if (TrueOrFalse == -1):
                            PDF_Name = self.DownloadPDF(driver=driver,year=str(YearExact),month=str(MonthExact))
                            self.PdfToExcel(fileName=PDF_Name,driver = driverEx)
                            ExcelAdr = self.FindExcelFile()
                            self.ExcelToSql(ExcelAdr=ExcelAdr,Year=str(YearExact),Month=str(MonthExact))         
                            print (self.StockName+str(YearExact)+"年"+str(MonthExact)+"月入库成功")
                        else:
                            print (self.StockName+str(YearExact)+"年"+str(MonthExact)+"月数据库中已有记录")
                        self.FolderClean()
                    except (Exception) as e:
                        print (self.StockName+str(YearExact)+"年"+str(MonthExact)+"月入库失败，请检查")
                        print ("检查失败原因："+str(e))
                else:
                    pass
        finally:
            driver.quit()
            driverEx.quit()
            self.FolderClean()
            
     
if __name__ == "__main__":
    user = "root"
    password = ""
    database = ""
    stock_code = "600066"
    StockName = "宇通客车"
    DownloadAdr = "d:\\downloadTest"
    #ExeAdr=r"E:\JianLPeng\Project\Anack\anack\Release\YTProductionSaleSql\UpfileWithPara.exe" #绝对路径
    ExeAdr="UpfileWithPara.exe"   #如果UpfileWithPara.exe在同一个文件夹下可以使用相对路径
    Update = ProductionSaleToSql()
    Update.ParametersSet(user=user,password=password,database=database,stock_code=stock_code,StockName=StockName,DownloadAdr=DownloadAdr,ExeAdr=ExeAdr,YearBegin = 2017,MonthBegin = 6)
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
"""


