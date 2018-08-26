# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:35:34 2018

@author: 54206
"""
import requests
import datetime
from requests.exceptions import RequestException
import re
import urllib
import os
import shutil
def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

class FolderNotCleanException (Exception):
    pass

class PdfDownLoad:
    def __init__(self,year=2016,month=1,downloadAdrr = 'D:/downloadTest/'):
        self.headers = {'Accept':'*/*',
           'Accept-Encoding':'gzip, deflate',
           'Accept-Language':'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Cookie': 'yfx_c_g_u_id_10000042=_ck18030722220815231570139781377; VISITED_STOCK_CODE=%5B%22600066%22%5D; VISITED_MENU=%5B%229062%22%2C%229729%22%2C%228307%22%5D; UM_distinctid=1629a80cb0b7e3-0da2cab7416fbd-c343567-144000-1629a80cb0c185; websearch=%22900957%22%3A%22%u51CC%u4E91B%u80A1%22%2C%22603966%22%3A%22%u6CD5%u5170%u6CF0%u514B%22%2C%22603933%22%3A%22%u777F%u80FD%u79D1%u6280%22%2C%22603955%22%3A%22%u5927%u5343%u751F%u6001%22%2C%22600066%22%3A%22%u5B87%u901A%u5BA2%u8F66%22; VISITED_COMPANY_CODE=%5B%22600066%22%2C%22%5Bobject%20Object%5D%22%5D; seecookie=%5B900957%5D%3A%u51CC%u4E91B%u80A1%2C%5B603966%5D%3A%u6CD5%u5170%u6CF0%u514B%2C%5B603933%5D%3A%u777F%u80FD%u79D1%u6280%2C%5B603955%5D%3A%u5927%u5343%u751F%u6001%2C%5B600066%5D%3A%u5B87%u901A%u5BA2%u8F66%2C%u5B87%u901A%u5BA2%u8F66%u4EA7%u9500%u5FEB%u62A5; yfx_f_l_v_t_10000042=f_t_1520432528520__r_t_1522998662756__v_t_1523023134976__r_c_7',
           'Host':'query.sse.com.cn',
           'Referer':'http://www.sse.com.cn/home/search/?webswd=%E5%AE%87%E9%80%9A%E5%AE%A2%E8%BD%A6%E4%BA%A7%E9%94%80%E5%BF%AB%E6%8A%A5',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
        self.year = year
        self.month = month
        self.downloadAdrr=downloadAdrr
        self.pdfList=[]
        

    def get_one_page(self,url):
        try:
            response = requests.get(url,headers = self.headers)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            return None
        except RequestException as e:
            print (e)
            return None
    
    def getCurrentPage(self,url,beginDate):
        RList=[]
        html = self.get_one_page(url)
        Reguler =r"\\/disclosure\\/listedinfo\\/announcement\\/c\\/.*?pdf"
        pattern = re.compile(Reguler)
        ls = pattern.findall(html)
        #print (ls)
        for eachLink in ls:
            element = eachLink.split('\\/')
            YMD=element[-2].split("-")
            year = int(YMD[0])
            month = int(YMD[1])
            day = int(YMD[2])
            eachDate = datetime.date(year,month,day)
            if(eachDate.__ge__(beginDate)):
                RList.append(eachLink)
            else:
                break
        #print (RList)
        return RList



    def getAllPDFAdd(self):
        AllList = []
        beginDate = datetime.date(self.year,self.month+1,1)
        beginNum =1
        RLength = 10
        url1=r"http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&jsonCallBack=jQuery111205573825303579625_1523023138864&page="
        url2=r"&searchword=T_L+CTITLE+T_D+E_KEYWORDS+T_JT_E+likeT_L%E5%AE%87%E9%80%9A%E5%AE%A2%E8%BD%A6%E4%BA%A7%E9%94%80%E5%BF%AB%E6%8A%A5T_RT_R&orderby=-CRELEASETIME&perpage=10&_=1523023138865"
        while (RLength==10):
            url = url1+str(beginNum)+url2
            Rlist = self.getCurrentPage(url,beginDate)
            RLength = len(Rlist)
            AllList =AllList+Rlist
            beginNum=beginNum+1
        return AllList



    def getFile(self,url):
        pdf_name = url.split('/')[-1]
        file_name = self.downloadAdrr+pdf_name
        u = urllib.request.urlopen(url)
        f = open(file_name, 'wb')
    
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
    
            f.write(buffer)
        f.close()
        print ("Sucessful to download" + " " + pdf_name)
        return pdf_name


    

    def FolderClean(self):
            for i in os.listdir(self.downloadAdrr):
               path_file = os.path.join(self.downloadAdrr,i)  # 取文件路径
               if os.path.isfile(path_file):
                   os.remove(path_file)
               if os.path.isdir(path_file):
                   shutil.rmtree(path_file)
            if os.listdir(self.downloadAdrr):   #如果文件夹没有清理干净，抛出异常
                raise FolderNotCleanException
        
 
    def GetAllPdfFile(self):
        self.FolderClean()
        AllList = self.getAllPDFAdd()
        baseUrl = r"http://www.sse.com.cn"
        for EachList in AllList:
            url=baseUrl+EachList
            #url.replace('\','/')
            urlList = url.split('/')
            url = ""
            for Each in urlList:
                if (Each==urlList[0]):
                    url=Each
                elif(Each==urlList[-1]):
                    url=url+'/'+Each
                else:
                    url=url+'/'+Each[:-1]
            pdf_name=self.getFile(url)
            self.pdfList.append(pdf_name)
            
    def RPdfList(self):
        return self.pdfList

if __name__ == "__main__":
    i = PdfDownLoad()
    i.GetAllPdfFile()
    print (i.RPdfList())
