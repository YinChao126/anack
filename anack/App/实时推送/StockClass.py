#from DistinguishData import DataType

class stock:
    '''
# 参数定义
# ID            代码             600660      由单独变量给出
# 0 TdyOpen       今开盘价                     由List变量给出
# 1 YdyClose      昨天收盘
# 2 CurPrice      现价
# 3 HighPrice     最高价
# 4 LowPrice      最低价
# 5 CurBuyPrice   竞买价
# 6 CurSellPrice  竞卖价
# 7 CurQuantity   成交量
# 8 CurMoney      成交额
# 9 Buy1_quant    买一数量
# 10Buy1_price    买一报价
# 11Buy2_quant    买一数量
# 12Buy2_price    以此类推。。。
# 13Buy3_quant
# 14Buy3_price
# 15Buy4_quant
# 16Buy4_price
# 17Buy5_quant
# 18Buy5_price
# 19Sell1_quant
# 20Sell1_price
# 21Sell2_quant
# 22Sell2_price
# 23Sell3_quant
# 24Sell3_price
# 25Sell4_quant
# 26Sell4_price
# 27Sell5_quant
# 28Sell5_price
    '''
    def SetData(self, ldata):
        '''
        一次性设置所有的信息
        :param id: 股票代码，{'gldq',000651}
        :param lista: 输入结构体 只能通过正则表达式获得
        :return:无
        '''
        if ldata == 0:
            return 0
        self.TdyOpen = float(ldata[0])
        self.YdyClose = float(ldata[1])
        self.CurPrice = float(ldata[2])
        self.HighPrice = float(ldata[3])
        self.LowPrice = float(ldata[4])
        self.CurBuyPrice = float(ldata[5])
        self.CurSellPrice = float(ldata[6])
        self.CurQuantity = int(ldata[7])/1000000
        self.CurMoney = float(ldata[8])/100000000
        self.Buy1_quant = int(int(ldata[9])/100)
        self.Buy1_price = float(ldata[10])
        self.Buy2_quant = int(int(ldata[11])/100)
        self.Buy2_price = float(ldata[12])
        self.Buy3_quant = int(int(ldata[13])/100)
        self.Buy3_price = float(ldata[14])
        self.Buy4_quant = int(int(ldata[15])/100)
        self.Buy4_price = float(ldata[16])
        self.Buy5_quant = int(int(ldata[17])/100)
        self.Buy5_price = float(ldata[18])
        self.Sell1_quant = int(int(ldata[19])/100)
        self.Sell1_price = float(ldata[20])
        self.Sell2_quant = int(int(ldata[21])/100)
        self.Sell2_price = float(ldata[22])
        self.Sell3_quant = int(int(ldata[23])/100)
        self.Sell3_price = float(ldata[24])
        self.Sell4_quant = int(int(ldata[25])/100)
        self.Sell4_price = float(ldata[26])
        self.Sell5_quant = int(int(ldata[27])/100)
        self.Sell5_price = float(ldata[28])
        self.date = ldata[29]
        self.time = ldata[30]
        self.id = ldata[31]

    def PrintAllData(self):
        '''
        一次性打印所有信息（仅用于调试）
        :return:
        '''
        print('ID:\t'+self.id)
        print('今开:\t'+str(self.TdyOpen))
        print('昨收:\t'+str(self.YdyClose))
        print('现价:\t'+str(self.CurPrice))
        print('最高价:\t'+str(self.HighPrice))
        print('最低价:\t'+str(self.LowPrice))
        print('竞买:\t'+str(self.CurBuyPrice))
        print('竞卖:\t'+str(self.CurSellPrice))
        print('成交量(万手):\t'+str(self.CurQuantity))
        print('成交额(亿元):\t'+str(self.CurMoney))
        print('买一/手:\t'+str(self.Buy1_quant))
        print('买一/价:\t'+str(self.Buy1_price))
        print('买二/手:\t'+str(self.Buy2_quant))
        print('买二/价:\t'+str(self.Buy2_price))
        print('买三/手:\t'+str(self.Buy3_quant))
        print('买三/价:\t'+str(self.Buy3_price))
        print('买四/手:\t'+str(self.Buy4_quant))
        print('买四/价:\t'+str(self.Buy4_price))
        print('买五/手:\t'+str(self.Buy5_quant))
        print('买五/价:\t'+str(self.Buy5_price))
        print('卖一/手:\t'+str(self.Sell1_quant))
        print('卖一/价:\t'+str(self.Sell1_price))
        print('卖二/手:\t'+str(self.Sell2_quant))
        print('卖二/价:\t'+str(self.Sell2_price))
        print('卖三/手:\t'+str(self.Sell3_quant))
        print('卖三/价:\t'+str(self.Sell3_price))
        print('卖四/手:\t'+str(self.Sell4_quant))
        print('卖四/价:\t'+str(self.Sell4_price))
        print('卖五/手:\t'+str(self.Sell5_quant))
        print('卖五/价:\t'+str(self.Sell5_price))
        print(self.date)
        print(self.time)

    def RiseRate(self):
        '''
        获取股票实时涨幅
        :return:
        '''
        rate = (self.CurPrice - self.YdyClose)/self.YdyClose * 100
        rate = round(rate,2)
        return rate



