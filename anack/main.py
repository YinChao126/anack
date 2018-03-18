# -*- coding:utf-8 -*- 
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import tushare as ts  

import App.IndustryEstimation
from SQL.sql import pymysql_connect

dbconn=pymysql_connect()


App.IndustryEstimation.CreateTable() #此处开启则清空此前所有内容
name = App.IndustryEstimation.GetIndustryName('000651')
App.IndustryEstimation.Estimation(dbconn,name,2017)
name = App.IndustryEstimation.GetIndustryName('601012')
App.IndustryEstimation.Estimation(dbconn,name,2017)