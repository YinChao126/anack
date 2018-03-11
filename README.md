# welcome anack

## anack是什么？
anack是一款金融数据分析工具，用于实现股市投资中的基本面分析，提供投资建议，最终形成一种量化交易工具

## anack具备什么功能？
* 获取多种金融原始数据
* 实现个股基本面分析
* 实现个股价值估计并提供投资建议
* 实现宏观经济形势分析与A股趋势预判
* 实现量化交易功能

## 谁会对anack有兴趣
* 广大股民
* 人工智能、大数据工程师
* 量化交易开发者


## 已发布工具速查
* HK_insider。  实现港股持股披露信息分析
* YT_produce_sell。实现宇通客车的产销数据分析
 
 
## 数据接口速览（持续添加）：
* [实时数据_福耀玻璃](http://hq.sinajs.cn/list=sh600660)
* [实时数据_上证综指](http://hq.sinajs.cn/list=s_sh000001)
* [实时数据_深成指数](http://hq.sinajs.cn/list=s_sz399001)
* [日线图_福耀玻璃](http://image.sinajs.cn/newchart/daily/n/sh600660.gif)
* [月线图_福耀玻璃](http://image.sinajs.cn/newchart/monthly/n/sh600660.gif)
* [成交明细](http://market.finance.sina.com.cn/downxls.php?date=2011-07-08&symbol=sh600660)
* [当日分价表](http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol=sh600660)
* [多日分价表](http://market.finance.sina.com.cn/pricehis.php?symbol=sh600660&startdate=2011-08-17&enddate=2011-08-19)


>## 反馈交流
>在使用中有任何问题，欢迎反馈给我，可以用以下邮件跟我交流

>*yc86247931@126.com*

>*shutian318@163.com*

## SubProject1 基于PYTHON和树莓派的盈亏分析平台设计


#1.通过Python爬取网页获取实时金融指标数据
  http://hq.sinajs.cn/list=sz000651（每天更新）
  choice(需要付费)
  http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh （含历史数据）
  
  http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/000651/ctrl/2017/displaytype/4.phtml (爬取历史的报表数据)
  
#2.指标的实时监控，有预警信息后推送手机

#3.经过历史指标筛选出值得投资的长期股票及适合买入时机（具体算法再商议），历史数据的存储放在数据库或者树莓派上完成。
  同时建模获取短期投资股票时机，短信提示手机

#4.训练一个模拟操盘手，按每周/每月进行操作，最后按照盈亏指标来验证训练模型好坏


## 理念


把炒股的经验做成算法，利用软件来实现。同时利用软件来发掘新的机会（机器学习）。
其次可以发布推荐信息。设置自己的持仓后，一方面根据算法向用户发布买卖信号。另一方面算法
在内部自己计算操作盈亏（用户可以无视买卖信号），最终可以通过比对二者差异来确定算法的好坏

开发阶段可以设置多种算法同时运行，针对某一个具体指标。可以通过对比来确定使用哪种策略更有效
直接利用已经发生了的数据进行海量机器学习。

可以实时模拟投资，看最终的投资结果


## 架构设计


整体框架，需要实现的功能规划好
功能：
1. 能够实时监控数据变化
2. 能够根据指定的算法进行相关的输出
3. 能够根据算法进行模拟操盘并可以自己分析收益
4. 能够自主学习，用以验证经验的有效性
